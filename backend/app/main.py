from fastapi import FastAPI
from app.routes import analyze, reports

app = FastAPI(
    title="Internship Scam Detection API",
    description="Detect fake internships using URLs, LinkedIn profiles & screenshots",
    version="1.0.0"
)

app.include_router(analyze.router, prefix="/analyze", tags=["Analysis"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])