from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.layout import Layout
from app.schemas.layout import LayoutCreate, LayoutResponse,LayoutPreviewResponse, LayoutPreviewRequest, LayoutDetailResponse
from app.services.zpl import extract_fields, render_zpl


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

@router.post("/{layout_id}/preview", response_model=LayoutPreviewResponse, status_code=status.HTTP_200_OK)
async def preview_layout(layout_id: int, preview_data: LayoutPreviewRequest, db: Session = Depends(get_db)):
    layout = db.query(Layout).filter(Layout.id == layout_id).first()
    if not layout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Layout não encontrado")
    try:
        zpl = render_zpl(layout.zpl_template, preview_data.data)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return {
        "zpl": zpl
    }

@router.get('/layouts/{layout_id}', response_model=LayoutDetailResponse, status_code=status.HTTP_200_OK)
async def get_layout(layout_id: int, db: Session = Depends(get_db)):
    layout = db.query(Layout).filter(Layout.id == layout_id).first()
    if not layout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Layout não encontrado")
    fields = extract_fields(layout.zpl_template)
    return{
        "id": layout.id,
        "name": layout.name,
        "description": layout.description,
        "fields": fields,
        "active": layout.active,
        "created_at": layout.created_at
    }
