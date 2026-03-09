from pydantic import BaseModel

class RainStats(BaseModel):
    total_precipitacao: float
    media_precipitacao: float
    desvio_padrao_precipitacao: float
    dias_secos: int


class AnalysisResponse(BaseModel):
    sucesso: bool
    estatisticas: RainStats