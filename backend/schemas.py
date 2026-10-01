from pydantic import BaseModel
from typing import List


class ScamRequest(BaseModel):
    message: str


class Indicator(BaseModel):
    type: str
    description: str


class ScamAnalysis(BaseModel):
    risk_level: str
    risk_score: int
    category: str
    summary: str
    indicators: List[Indicator]
    recommended_actions: List[str]