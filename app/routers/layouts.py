from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.layout import Layout
from app.schemas.layout import LayoutCreate, LayoutResponse


router = APIRouter(
    prefix="/layouts",
    tags=["layouts"]
)

@router.post(
    "/",
    response_model=LayoutResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_layout(
    layout_data: LayoutCreate,
    db: Session = Depends(get_db)
):
    layout = Layout(
        name=layout_data.name,
        description=layout_data.description,
        zpl_template=layout_data.zpl_template
    )

    db.add(layout)
    db.commit()
    db.refresh(layout)

    return layout