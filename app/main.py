from fastapi import FastAPI
from app.routers.layouts import layouts_router

app = FastAPI()

app.include_router(layouts_router)
