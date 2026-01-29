from pydantic import BaseModel

class AnalysisResult(BaseModel):
    scam_score: int
    verdict: str