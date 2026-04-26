#!/usr/bin/env bash
#
# mobius-story-ui — Cloud Run deploy script
#
# Usage:
#   scripts/deploy.sh dev               # build + deploy
#   scripts/deploy.sh dev --dry-run     # print commands only
#   scripts/deploy.sh dev --skip-build  # redeploy last image
#
set -euo pipefail

# ── Args ─────────────────────────────────────────────────────────────
ENV_LABEL="${1:-}"
if [[ -z "${ENV_LABEL}" ]]; then
    echo "usage: $0 <env> [--dry-run] [--skip-build]" >&2
    exit 64
fi

DRY_RUN=0
SKIP_BUILD=0
shift || true
for arg in "$@"; do
    case "$arg" in
        --dry-run)     DRY_RUN=1 ;;
        --skip-build)  SKIP_BUILD=1 ;;
        *) echo "unknown flag: $arg" >&2; exit 64 ;;
    esac
done

# ── Config ───────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UI_DIR="$(dirname "${SCRIPT_DIR}")"
ENV_FILE="${UI_DIR}/deploy/${ENV_LABEL}.env"

if [[ ! -f "${ENV_FILE}" ]]; then
    echo "error: no env file at ${ENV_FILE}" >&2
    exit 65
fi

# shellcheck disable=SC1090
source "${ENV_FILE}"

# ── Helpers ──────────────────────────────────────────────────────────
run() {
    if [[ "${DRY_RUN}" == "1" ]]; then
        echo "[dry-run] $*"
    else
        "$@"
    fi
}

# ── Image tag ─────────────────────────────────────────────────────────
GIT_SHA="$(git -C "${UI_DIR}" rev-parse --short=10 HEAD 2>/dev/null || echo nogit)"
BUILD_TS="$(date -u +%Y%m%d-%H%M%S)"
IMAGE_TAG="${IMAGE_BASE}:${BUILD_TS}-${GIT_SHA}"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Service : ${SERVICE_NAME}"
echo "  Project : ${GCP_PROJECT}"
echo "  Region  : ${GCP_REGION}"
echo "  Image   : ${IMAGE_TAG}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Ensure AR repo exists ─────────────────────────────────────────────
run gcloud artifacts repositories describe "${AR_REPO}" \
    --project="${GCP_PROJECT}" --location="${GCP_REGION}" \
    --format="value(name)" >/dev/null 2>&1 || \
run gcloud artifacts repositories create "${AR_REPO}" \
    --repository-format=docker \
    --location="${GCP_REGION}" \
    --project="${GCP_PROJECT}" \
    --description="mobius-story-ui container images"

# ── Build ─────────────────────────────────────────────────────────────
if [[ "${SKIP_BUILD}" == "0" ]]; then
    echo "── Building ${IMAGE_TAG} ──"
    # Build context is the UI directory itself (Dockerfile at root)
    run gcloud builds submit "${UI_DIR}" \
        --project="${GCP_PROJECT}" \
        --region="${GCP_REGION}" \
        --config="${UI_DIR}/deploy/cloudbuild.yaml" \
        --substitutions="_IMAGE=${IMAGE_TAG}" \
        --timeout=15m
else
    # Resolve latest image
    IMAGE_TAG="$(gcloud artifacts docker images list \
        "${IMAGE_BASE}" --project="${GCP_PROJECT}" \
        --sort-by="~CREATE_TIME" --limit=1 \
        --format="value(VERSION)" 2>/dev/null || echo "${IMAGE_BASE}:latest")"
    echo "── Reusing image: ${IMAGE_TAG} ──"
fi

# ── Deploy ────────────────────────────────────────────────────────────
echo "── Deploying to Cloud Run ──"
run gcloud run deploy "${SERVICE_NAME}" \
    --image="${IMAGE_TAG}" \
    --project="${GCP_PROJECT}" \
    --region="${GCP_REGION}" \
    --service-account="${SERVICE_ACCOUNT}" \
    --memory="${RUN_MEMORY}" \
    --cpu="${RUN_CPU}" \
    --concurrency="${RUN_CONCURRENCY}" \
    --timeout="${RUN_TIMEOUT}" \
    --min-instances="${RUN_MIN_INSTANCES}" \
    --max-instances="${RUN_MAX_INSTANCES}" \
    --allow-unauthenticated \
    --set-env-vars="CHAT_API_URL=${CHAT_API_URL},SKILLS_API_URL=${SKILLS_API_URL},UI_PORT=${UI_PORT}" \
    --port=8080

# ── Print URL ────────────────────────────────────────────────────────
SERVICE_URL="$(gcloud run services describe "${SERVICE_NAME}" \
    --project="${GCP_PROJECT}" --region="${GCP_REGION}" \
    --format="value(status.url)")"

echo ""
echo "✓ Deployed: ${SERVICE_URL}"
echo "  Story:    ${SERVICE_URL}/story.html?org=Aspire+Health&s=0"
echo ""
echo "Next: add ${SERVICE_URL} to CHAT_CORS_ORIGINS in mobius-chat deploy/dev.env"
echo "      then: cd ../mobius-chat && scripts/deploy.sh dev --skip-build"
