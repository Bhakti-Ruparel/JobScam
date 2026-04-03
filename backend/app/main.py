import logging
import os
import subprocess
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# Fix 4 — MODEL_DIR from env variable with pathlib fallback
_default_model_dir = Path(__file__).parent.parent / "models"  # backend/models/
MODEL_DIR = Path(os.environ["MODEL_DIR"]) if os.environ.get("MODEL_DIR") else _default_model_dir
EMBEDDER_PATH = MODEL_DIR / "text_embedder.pkl"
CLASSIFIER_PATH = MODEL_DIR / "job_scam_classifier.pkl"


def download_embedder_with_retry():
    """
    Fix 1 — Download embedder with 3 retries, 10s wait, 120s timeout.
    Fails loudly if all attempts fail.
    """
    if EMBEDDER_PATH.exists():
        log.info("✅ text_embedder.pkl already exists, skipping download")
        return

    os.environ["HF_HUB_TIMEOUT"] = "120"

    last_error = None
    for attempt in range(1, 4):
        log.info(f"⬇️  Download attempt {attempt}/3 — all-MiniLM-L6-v2 from HuggingFace...")
        try:
            import joblib
            from sentence_transformers import SentenceTransformer

            MODEL_DIR.mkdir(parents=True, exist_ok=True)
            embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            joblib.dump(embedder, EMBEDDER_PATH)
            log.info("✅ Embedder downloaded and saved successfully")
            return
        except Exception as e:
            last_error = e
            log.error(f"❌ Attempt {attempt}/3 failed: {e}")
            if attempt < 3:
                log.info("⏳ Waiting 10 seconds before retry...")
                time.sleep(10)

    # All attempts failed — fail loudly so Railway restarts container
    raise RuntimeError(
        f"❌ All 3 download attempts failed. Last error: {last_error}\n"
        "Railway will restart the container. Check HuggingFace connectivity."
    )


def check_tesseract() -> str:
    try:
        result = subprocess.run(
            ["tesseract", "--version"],
            capture_output=True, text=True, timeout=5
        )
        version = result.stdout.splitlines()[0] if result.stdout else result.stderr.splitlines()[0]
        return version.strip()
    except Exception:
        return "not found"


@asynccontextmanager
async def lifespan(app: FastAPI):
    port = os.environ.get("PORT", "8000")
    log.info(f"🚀 Starting SafeOffer on port {port}")
    log.info(f"📁 Model directory: {MODEL_DIR.absolute()}")
    log.info(f"   classifier : {'✅ exists' if CLASSIFIER_PATH.exists() else '❌ missing'}")
    log.info(f"   embedder   : {'✅ exists' if EMBEDDER_PATH.exists() else '⬇️  will download'}")

    # Fix 2 — Lazy loading: classifier first, then embedder
    # Step 1: Load classifier
    if CLASSIFIER_PATH.exists():
        import joblib
        log.info("📦 Loading classifier...")
        joblib.load(CLASSIFIER_PATH)
        log.info("✅ Classifier loaded")
    else:
        raise RuntimeError(f"❌ Classifier not found at {CLASSIFIER_PATH}")

    # Step 2: Sleep to let container stabilize before heavy download
    log.info("⏳ Stabilizing container before embedder load (2s)...")
    time.sleep(2)

    # Step 3: Download embedder if needed, then load
    download_embedder_with_retry()

    log.info(f"🔍 Tesseract: {check_tesseract()}")
    log.info("📡 Routes: /analyze, /reports, /health, / (frontend)")

    yield

    log.info("🛑 Shutting down")


app = FastAPI(
    title="SafeOffer API",
    description="SafeOffer - Detect fake internships using ML, NLP, OCR and web analysis",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

from .routes import analyze, reports

app.include_router(analyze.router, prefix="/analyze", tags=["Analysis"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])


@app.get("/health", tags=["Health"])
def health_check():
    import joblib

    classifier_loaded = False
    embedder_loaded = False

    try:
        if CLASSIFIER_PATH.exists():
            joblib.load(CLASSIFIER_PATH)
            classifier_loaded = True
    except Exception:
        pass

    embedder_loaded = EMBEDDER_PATH.exists()
    tess_version = check_tesseract()

    return JSONResponse({
        "status": "ok",
        "tesseract_version": tess_version,
        "classifier_loaded": classifier_loaded,
        "embedder_loaded": embedder_loaded,
        "model_download_required": not embedder_loaded
    })


# Serve frontend
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    @app.get("/")
    def serve_home():
        return FileResponse(str(frontend_path / "home.html"))

    @app.get("/{page}.html")
    def serve_page(page: str):
        file = frontend_path / f"{page}.html"
        if file.exists():
            return FileResponse(str(file))
        return FileResponse(str(frontend_path / "home.html"))

    @app.get("/styles.css")
    def serve_css():
        return FileResponse(str(frontend_path / "styles.css"), media_type="text/css")

    # Mount static files last so API routes take priority
    app.mount("/", StaticFiles(directory=str(frontend_path)), name="static")
