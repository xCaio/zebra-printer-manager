from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from math import ceil

from app.core.database import get_db
from app.models.layout import Layout
from app.models.printer import Printer
from app.models.print_job import PrintJob
from app.services.printer import PrinterService
from app.services.zpl import render_zpl
from app.schemas.printer_job import PrintJobCreate, PrintJobResponse
from app.schemas.print import PrintJobListResponse

router = APIRouter(
    prefix="/print",
    tags=["print"]
)


@router.post(
    "/",
    response_model=PrintJobResponse,
    status_code=status.HTTP_201_CREATED
)
async def print_layout(print_data: PrintJobCreate,db: Session = Depends(get_db)):
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

@router.get("/",response_model=PrintJobListResponse,status_code=status.HTTP_200_OK)
async def list_print_jobs(
    printer_id: int | None = None,
    layout_id: int | None = None,
    status: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(PrintJob)

    if printer_id is not None:
        query = query.filter(
            PrintJob.printer_id == printer_id
        )

    if layout_id is not None:
        query = query.filter(
            PrintJob.layout_id == layout_id
        )

    if status is not None:
        query = query.filter(
            PrintJob.status == status
        )

    total = query.count()

    offset = (page - 1) * limit

    print_jobs = (
        query
        .order_by(PrintJob.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    pages = ceil(total / limit) if total > 0 else 0

    return {
        "items": print_jobs,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }

@router.get("/{print_job_id}",response_model=PrintJobResponse,status_code=status.HTTP_200_OK)
async def get_print_job(print_job_id: int,db: Session = Depends(get_db)):
    print_job = (db.query(PrintJob).filter(PrintJob.id == print_job_id).first())

    if not print_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de impressão não encontrado"
        )
    return print_job