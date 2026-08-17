from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.models.layout import Layout
from app.models.printer import Printer
from app.models.print_job import PrintJob
from app.schemas.printer_job import (
    PrintJobCreate,
    PrintJobResponse
)
from app.services.printer import PrinterService
from app.services.zpl import render_zpl


router = APIRouter(
    prefix="/print",
    tags=["print"]
)


@router.post(
    "/",
    response_model=PrintJobResponse,
    status_code=status.HTTP_201_CREATED
)
async def print_layout(
    print_data: PrintJobCreate,
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

    if not printer.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impressora está inativa"
        )

    if not layout.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Layout está inativo"
        )

    try:
        zpl = render_zpl(
            layout.zpl_template,
            print_data.data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    print_job = PrintJob(
        printer_id=printer.id,
        layout_id=layout.id,
        status="printing",
        quantity=print_data.quantity
    )

    db.add(print_job)
    db.commit()
    db.refresh(print_job)

    try:
        for _ in range(print_data.quantity):
            PrinterService.print_zpl(
                ip=printer.ip,
                port=printer.port,
                zpl=zpl
            )

        print_job.status = "completed"

    except (ConnectionError, OSError) as error:
        print_job.status = "failed"
        print_job.error_message = str(error)

    db.commit()
    db.refresh(print_job)

    return print_job