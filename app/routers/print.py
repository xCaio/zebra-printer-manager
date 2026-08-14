from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.printer import Printer
from app.models.layout import Layout
from app.schemas.print import PrintRequest, PrintResponse
from app.services.zpl import render_zpl
from app.services.printer import PrinterService

router = APIRouter(prefix="/print", tags=["print"])

@router.post('/', response_model=PrintResponse, status_code=status.HTTP_200_OK)
async def print_label(print_data: PrintRequest, db: Session = Depends(get_db)):
    printer = db.query(Printer).filter(Printer.id == print_data.printer_id).first()
    if not printer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Impressora nao encontrada")
    if not printer.active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Impressora está desativada")

    layout = db.query(Layout).filter(Layout.id == print_data.layout_id).first()
    if not layout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Layout nao encontrada")
    if not layout.active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Layout está desativado")

    try:
        zpl = render_zpl(
            layout.zpl_template,
            print_data.data
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error))

    try:
        PrinterService.print_zpl(
            ip=printer.ip,
            port=printer.port,
            zpl=zpl
        )
    except ConnectionError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error))

    return PrintResponse(
        success=True,
        message="Etiqueta enviada para impressao com sucesso.",
        printer=printer.name,
        layout=layout.name
    )