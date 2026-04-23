"""mobius-story-ui — standalone static file server.

Serves the FL Medicaid BH market intelligence UI on a dedicated port (default 8020).
All API calls from the UI go to SKILLS_API_URL (default http://localhost:8011).

Usage:
    python -m server.main
    UI_PORT=8020 SKILLS_API_URL=http://localhost:8011 python -m server.main
"""

import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ui] %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
UI_PORT = int(os.environ.get("UI_PORT", "8020"))
SKILLS_API_URL = os.environ.get("SKILLS_API_URL", "http://localhost:8011")

app = FastAPI(title="mobius-story-ui", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "mobius-story-ui", "skills_api": SKILLS_API_URL}


@app.get("/")
def root():
    return RedirectResponse(url="/story.html")


# Serve everything under public/ at root
app.mount("/", StaticFiles(directory=str(PUBLIC_DIR), html=True), name="public")


if __name__ == "__main__":
    logger.info("mobius-story-ui starting on port %d (skills API: %s)", UI_PORT, SKILLS_API_URL)
    uvicorn.run("server.main:app", host="0.0.0.0", port=UI_PORT, reload=False)
