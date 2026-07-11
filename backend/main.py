from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.routes.health import router as health_router
from backend.routes.pages import router as pages_router
from backend.routes.predict import router as predict_router

app = FastAPI(title="Students Performance Score Prediction")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

app.include_router(health_router)
app.include_router(pages_router)
app.include_router(predict_router)
