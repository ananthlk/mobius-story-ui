"""mobius-story-ui — static file server + streaming chat proxy.

Serves the FL Medicaid BH market intelligence UI.
Routes /proxy/chat/* to the mobius-chat Cloud Run service to avoid CORS.
SSE endpoints (/chat/stream/*) are proxied with true streaming — chunks
forwarded as they arrive so the browser sees tokens in real time.

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
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ui] %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
UI_PORT = int(os.environ.get("UI_PORT", "8020"))
SKILLS_API_URL = os.environ.get("SKILLS_API_URL", "http://localhost:8011")
CHAT_API_URL = os.environ.get("CHAT_API_URL", "https://mobius-chat-ortabkknqa-uc.a.run.app")

# Shared httpx client — keep-alive, no per-request connection overhead.
# read timeout=None for SSE streams (they stay open until done).
_http = httpx.AsyncClient(
    timeout=httpx.Timeout(connect=10, read=None, write=30, pool=10),
    follow_redirects=True,
)

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

_HOP_BY_HOP = {"host", "content-length", "transfer-encoding", "connection",
                "keep-alive", "proxy-authenticate", "proxy-authorization",
                "te", "trailers", "upgrade"}

_proxy = APIRouter()


def _proxy_headers(request: Request) -> dict:
    return {k: v for k, v in request.headers.items() if k.lower() not in _HOP_BY_HOP}


@_proxy.api_route("/proxy/chat/{path:path}", methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"])
async def chat_proxy(path: str, request: Request):
    """Forward /proxy/chat/{path} → CHAT_API_URL/{path}.

    SSE streams (/chat/stream/*) are forwarded with true streaming so the
    browser receives tokens as they emit rather than waiting for completion.
    All other paths (POST /chat, GET /chat/response/*) use buffered mode.
    """
    url = f"{CHAT_API_URL}/{path}"
    body = await request.body()
    headers = _proxy_headers(request)
    is_stream = "stream" in path  # /chat/stream/{correlation_id}

    if is_stream:
        # True streaming — forward SSE chunks as they arrive
        async def _iter_sse():
            async with _http.stream(
                method=request.method,
                url=url,
                content=body,
                headers=headers,
                params=dict(request.query_params),
            ) as upstream:
                async for chunk in upstream.aiter_bytes(chunk_size=512):
                    yield chunk

        return StreamingResponse(
            _iter_sse(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",   # tell nginx/GCF not to buffer
            },
        )
    else:
        # Buffered — normal JSON request/response
        r = await _http.request(
            method=request.method,
            url=url,
            content=body,
            headers=headers,
            params=dict(request.query_params),
        )
        return Response(
            content=r.content,
            status_code=r.status_code,
            headers={k: v for k, v in r.headers.items() if k.lower() not in _HOP_BY_HOP},
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
