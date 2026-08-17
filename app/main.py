from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.printers import router as printer_router
from app.routers.layouts import router as layouts_router
from app.routers.print import router as print_router
from app.routers.print_jobs import router as print_jobs_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(printer_router)
app.include_router(layouts_router)
app.include_router(print_router)
app.include_router(print_jobs_router)

