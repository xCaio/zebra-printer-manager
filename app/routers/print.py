from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.printer import Printer
from app.models.layout import Layout
from app.models.print_job import PrintJob
from app.schemas.print import PrintRequest, PrintResponse
from app.services.zpl import render_zpl, set_quantity
from app.services.printer import PrinterService


router = APIRouter(
    prefix="/print",
    tags=["print"]
)


@router.post(
    "/",
    response_model=PrintResponse,
    status_code=status.HTTP_200_OK
)
async def print_label(
    print_data: PrintRequest,
    db: Session = Depends(get_db)
):
    printer = (
        db.query(Printer)
        .filter(Printer.id == print_data.printer_id)
        .first()
    )

    if not printer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Impressora não encontrada"
        )

    if not printer.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impressora está desativada"
        )

    layout = (
        db.query(Layout)
        .filter(Layout.id == print_data.layout_id)
        .first()
    )

    if not layout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layout não encontrado"
        )

    if not layout.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Layout está desativado"
        )

    print_job = PrintJob(
        printer_id=printer.id,
        layout_id=layout.id,
        status="failed",
        quantity=print_data.quantity
    )

    db.add(print_job)
    db.commit()
    db.refresh(print_job)

    # Renderiza o ZPL
    try:
        zpl = render_zpl(
            layout.zpl_template,
            print_data.data
        )

        # Define a quantidade no comando ^PQ
        zpl = set_quantity(
            zpl,
            print_data.quantity
        )

    except ValueError as error:

        print_job.status = "failed"
        print_job.error_message = str(error)

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error)
        )

    # Envia o ZPL para a impressora
    try:

        PrinterService.print_zpl(
            ip=printer.ip,
            port=printer.port,
            zpl=zpl
        )

    except ConnectionError as error:

        print_job.status = "failed"
        print_job.error_message = str(error)

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error)
        )

    # Impressão enviada com sucesso
    print_job.status = "success"

    db.commit()
    db.refresh(print_job)

    return PrintResponse(
        success=True,
        message="Etiqueta enviada para impressão com sucesso.",
        printer=printer.name,
        layout=layout.name
    )