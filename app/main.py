import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database import init_db
from app.scheduler import scheduler
from app.api.routes import router as api_router
from app.easters import get_subhechha_now, get_random_proverb, get_header_subhechha, get_header_proverb

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize database schema
    init_db()
    # 2. Start background scheduler (24-hour periodic crawl + startup bootstrap)
    scheduler.start()
    yield
    # 3. Clean up on shutdown
    scheduler.stop()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="REST API and autonomous web crawler for cataloging popular and unpopular Durga Puja pandals in Kolkata and West Bengal. শারদীয়া শুভেচ্ছা! Try ?search=dhaak 🥁",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Sharodiya easter headers on every response — Bengali soul in the API.
# NOTE: headers must stay ASCII/latin-1; full Bengali script lives in JSON bodies.
@app.middleware("http")
async def sharodiya_headers_middleware(request, call_next):
    resp = await call_next(request)
    try:
        resp.headers["X-Sharodiya-Subhechha"] = get_header_subhechha()
        resp.headers["X-Pujo-Proverb"] = get_header_proverb()
    except Exception:
        pass
    return resp

# Enable CORS for browser integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include primary endpoints (/pandals, /stats, /crawl, etc.)
app.include_router(api_router)

# Mount static folder for interactive visual explorer
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def serve_dashboard():
    """Serves the interactive Pandal Explorer web dashboard."""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": f"{settings.PROJECT_NAME} is running. Visit /docs for API documentation."}

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for container and uptime monitoring."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "scheduler_running": scheduler.is_running,
        "subhechha": get_subhechha_now(),
        "proverb": get_random_proverb(),
        "easter_hint": "Try /pandals?search=dhaak 🥁 — or kashful, shiuli, bijoya, dhunuchi, bhog",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
