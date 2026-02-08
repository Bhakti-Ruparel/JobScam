from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analyze, reports

app = FastAPI(
    title="Internship Scam Detection API",
    description="Detect fake internships using URLs, LinkedIn profiles & screenshots",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # allow all origins for dev
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # explicitly include OPTIONS
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router, prefix="/analyze", tags=["Analysis"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
