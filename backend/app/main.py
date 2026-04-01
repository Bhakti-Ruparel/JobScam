from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .routes import analyze, reports

app = FastAPI(
    title="Internship Scam Detection API",
    description="Detect fake internships using URLs, LinkedIn profiles & screenshots",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# API routes
app.include_router(analyze.router, prefix="/analyze", tags=["Analysis"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

# Serve frontend static files
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

    @app.get("/")
    def serve_home():
        return FileResponse(str(frontend_path / "home.html"))

    @app.get("/{page}.html")
    def serve_page(page: str):
        file = frontend_path / f"{page}.html"
        if file.exists():
            return FileResponse(str(file))
        return FileResponse(str(frontend_path / "home.html"))
