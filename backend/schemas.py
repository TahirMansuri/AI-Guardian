from pydantic import BaseModel
from typing import List, Optional


class ScamRequest(BaseModel):
    message: str
    provider: Optional[str] = "local"
    lang: Optional[str] = "en"


class Indicator(BaseModel):
    type: str
    description: str
    source: Optional[str] = None


class ScamAnalysis(BaseModel):
    risk_level: str
    risk_score: int
    category: str
    summary: str
    indicators: List[Indicator]
    recommended_actions: List[str]