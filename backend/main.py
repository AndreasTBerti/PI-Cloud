from fastapi import FastAPI
from Pipeline.pipeline import run_pipeline

from Models.model import ClimateData

app = FastAPI(
    title="DataViewer API",
    description="API para análise de dados climáticos",
    version="1.0"
)

@app.get("/")
def root() -> dict:
    return {"status": "API online"}


@app.post("/upload")
def upload_climate_data(file: ClimateData):
    # data validation
    run_pipeline(file=file)