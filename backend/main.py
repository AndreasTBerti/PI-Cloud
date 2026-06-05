from fastapi import FastAPI

from backend.Database.database import save_data
from backend.Models.model import ClimateData

app = FastAPI(
    title="DataViewer API",
    description="API para análise de dados climáticos",
    version="1.0"
)

@app.get("/")
def root() -> dict:
    return {"status": "API online"}


@app.post("/sensor")
def upload_climate_data(file: ClimateData):
    # data validation
    save_data(data=file)
    return {"responde": "200"}