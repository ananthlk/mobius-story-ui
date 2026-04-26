"""mobius-story-ui — static file server + chat proxy.

Serves the FL Medicaid BH market intelligence UI.
Routes /proxy/chat/* to the mobius-chat Cloud Run service to avoid CORS.

Usage:
    python -m server.main
    UI_PORT=8020 CHAT_API_URL=https://... python -m server.main
"""

import logging
import os
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ui] %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
UI_PORT = int(os.environ.get("UI_PORT", "8020"))
SKILLS_API_URL = os.environ.get("SKILLS_API_URL", "http://localhost:8011")
CHAT_API_URL = os.environ.get("CHAT_API_URL", "https://mobius-chat-ortabkknqa-uc.a.run.app")

app = FastAPI(title="mobius-story-ui", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ───────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "mobius-story-ui", "chat_api": CHAT_API_URL}


# ── Root redirect ─────────────────────────────────────────────────────

@app.get("/")
def root():
    return RedirectResponse(url="/story.html")


# ── Chat proxy — transparent forward to mobius-chat ──────────────────
# MUST be registered before the catch-all StaticFiles mount.

_proxy = APIRouter()


@_proxy.api_route("/proxy/chat/{path:path}", methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"])
async def chat_proxy(path: str, request: Request):
    """Forward /proxy/chat/{path} → CHAT_API_URL/{path}.

    Avoids CORS: the browser talks to the same origin (this server),
    and this server forwards to Cloud Run server-to-server.
    """
    url = f"{CHAT_API_URL}/{path}"
    body = await request.body()
    # Strip hop-by-hop headers; preserve everything else (auth, content-type, etc.)
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length", "transfer-encoding")
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.request(
            method=request.method,
            url=url,
            content=body,
            headers=headers,
            params=dict(request.query_params),
        )
    return Response(
        content=r.content,
        status_code=r.status_code,
        headers=dict(r.headers),
        media_type=r.headers.get("content-type"),
    )


app.include_router(_proxy)

# ── Static files — catch-all (must be last) ───────────────────────────
app.mount("/", StaticFiles(directory=str(PUBLIC_DIR), html=True), name="public")


if __name__ == "__main__":
    logger.info(
        "mobius-story-ui on :%d  chat→%s  skills→%s",
        UI_PORT, CHAT_API_URL, SKILLS_API_URL,
    )
    uvicorn.run("server.main:app", host="0.0.0.0", port=UI_PORT, reload=False)
