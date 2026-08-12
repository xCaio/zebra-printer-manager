from fastapi import APIRouter

layouts_router = APIRouter(prefix='/layouts', tags=['layouts'])

@layouts_router.get('/')
async def first_layout():
    return {'message': 'first route test'}