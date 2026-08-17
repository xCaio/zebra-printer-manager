from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.printer import Printer
from app.schemas.printer import PrinterCreate, PrinterResponse, PrinterUpdate, PrinterStatusUpdate, PrinterTestResponse
from app.schemas.printer_status import PrinterStatusResponse
from app.services.printer import PrinterService

router = APIRouter(prefix='/printers', tags=["Printers"])

@router.post('/', response_model=PrinterResponse, status_code=status.HTTP_201_CREATED)
async def create_printers(printer: PrinterCreate, db: Session = Depends(get_db)):
    new_printer = Printer(name = printer.name, ip = printer.ip, port=printer.port)
    db.add(new_printer)
    db.commit()
    db.refresh(new_printer)
    return new_printer


@router.get('/', response_model=list[PrinterResponse], status_code=status.HTTP_200_OK)
async def get_printers(db: Session = Depends(get_db)):
    printers = db.query(Printer).all()
    return printers

@router.get('/{printer_id}', response_model=PrinterResponse, status_code=status.HTTP_200_OK)
async def get_printer(printer_id: int, db: Session = Depends(get_db)):
    printer = db.query(Printer).filter(Printer.id == printer_id).first()
    if not printer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Impressora não encontrada")
    return printer

@router.patch('/{printer_id}', response_model=PrinterResponse, status_code=status.HTTP_200_OK)
async def update_printer(printer_id:int, printer_data: PrinterUpdate, db: Session = Depends(get_db)):
    printer = db.query(Printer).filter(Printer.id == printer_id).first()
    if not printer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Impressora não encontrada")

    data = printer_data.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(printer, field, value)

    db.commit()
    db.refresh(printer)
    return printer

@router.delete('/{printer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_printer(printer_id: int, db: Session = Depends(get_db)):
    printer = db.query(Printer).filter(Printer.id == printer_id).first()
    if not printer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Impressora não encontrada")
    db.delete(printer)
    db.commit()
    return {
        "message": "impressora excluída com sucesso",
    }

@router.patch('/{printer_id}/status', response_model=PrinterResponse, status_code=status.HTTP_200_OK)
async def change_printer_status(printer_id: int, printer_data: PrinterStatusUpdate, db: Session = Depends(get_db)):
    printer = db.query(Printer).filter(Printer.id == printer_id).first()
    if not printer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Impressora não encontrada")
    printer.active = printer_data.active
    db.commit()
    db.refresh(printer)

    return printer

@router.post('/{printer_id}/test', response_model=PrinterTestResponse, status_code=status.HTTP_200_OK)
async def test_printer(printer_id: int, db: Session = Depends(get_db)):
    printer = db.query(Printer).filter(Printer.id == printer_id).first()
    if not printer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Impressora não encontrada")
    if not printer.active:
        raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="Impressora está desativada")
    try:
        PrinterService.test_printer(
            ip=printer.ip,
            port=printer.port
        )
    except ConnectionError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error))

    return PrinterTestResponse(
        success=True,
        message="Teste de impressão enviado com sucesso.",
        printer=printer.name
    )

@router.get(
    "/{printer_id}/status",
    response_model=PrinterStatusResponse,
    status_code=status.HTTP_200_OK
)
async def get_printer_status(
    printer_id: int,
    db: Session = Depends(get_db)
):
    printer = (
        db.query(Printer)
        .filter(Printer.id == printer_id)
        .first()
    )

    if not printer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Impressora não encontrada"
        )

    online = PrinterService.check_status(
        ip=printer.ip,
        port=printer.port
    )

    return {
        "printer_id": printer.id,
        "name": printer.name,
        "ip": printer.ip,
        "port": printer.port,
        "online": online
    }