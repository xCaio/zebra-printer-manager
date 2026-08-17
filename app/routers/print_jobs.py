from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.print_job import PrintJob
from app.schemas.print import PrintJobListResponse
from app.schemas.printer_job import PrintJobResponse


router = APIRouter(prefix="/print", tags=["print"])


@router.get("/", response_model=PrintJobListResponse, status_code=status.HTTP_200_OK)
async def list_print_jobs(
    printer_id: int | None = None,
    layout_id: int | None = None,
    status: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(PrintJob)

    if printer_id is not None:
        query = query.filter(PrintJob.printer_id == printer_id)
    if layout_id is not None:
        query = query.filter(PrintJob.layout_id == layout_id)
    if status is not None:
        query = query.filter(PrintJob.status == status)

    total = query.count()
    print_jobs = (
        query.order_by(PrintJob.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": print_jobs,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": ceil(total / limit) if total > 0 else 0,
    }


@router.get("/{print_job_id}", response_model=PrintJobResponse, status_code=status.HTTP_200_OK)
async def get_print_job(print_job_id: int, db: Session = Depends(get_db)):
    print_job = db.query(PrintJob).filter(PrintJob.id == print_job_id).first()

    if not print_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de impressão não encontrado",
        )

    return print_job
