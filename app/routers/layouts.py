from fastapi import APIRouter

router = APIRouter(prefix='/layouts', tags=['layouts'])

@router.get('/')
async def first_layout():
    return {'message': 'first route test'}