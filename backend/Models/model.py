from pydantic import BaseModel

class ClimateData(BaseModel):
    sensor_id: str
    temperatura: float
    umidade: float