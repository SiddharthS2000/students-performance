from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config import PLOTS_DIR

from backend.routes.health import router as health_router
from backend.routes.pages import router as pages_router
from backend.routes.predict import router as predict_router
from backend.routes.training import router as training_router

app = FastAPI(title="Students Performance Score Prediction")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
app.mount("/plots", StaticFiles(directory=str(PLOTS_DIR)), name="plots")

app.include_router(health_router)
app.include_router(pages_router)
app.include_router(predict_router)
app.include_router(training_router)
