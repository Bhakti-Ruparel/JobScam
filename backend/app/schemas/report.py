from pydantic import BaseModel

class Report(BaseModel):
    linkedin_url: str
    website_url: str
    scam_score: int
    verdict: str