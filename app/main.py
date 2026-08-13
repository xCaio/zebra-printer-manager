from fastapi import FastAPI
from app.routers.printers import router as printer_router
from app.routers.layouts import router as layouts_router

app = FastAPI()

app.include_router(printer_router)
app.include_router(layouts_router)
