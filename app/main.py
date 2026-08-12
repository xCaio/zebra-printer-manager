from fastapi import FastAPI
from routers import layouts
app = FastAPI()

app.include_router(layouts.layouts_router)