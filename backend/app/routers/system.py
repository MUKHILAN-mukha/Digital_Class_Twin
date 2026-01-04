from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import time
import os
import requests

from app.db.session import get_db
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/system", tags=["System"])

ML_ENGINE_URL = os.getenv("ML_ENGINE_URL", "http://localhost:9000")


# ─────────────────────────────
# B6 — Basic Health Check
# ─────────────────────────────
@router.get("/health")
def system_health():
    return {
        "status": "ok",
        "timestamp": time.time()
    }


# ─────────────────────────────
# B7 — Backend + DB Status (PROTECTED)
# ─────────────────────────────
@router.get("/status")
def backend_status(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "down"

    return {
        "api": "ok",
        "database": db_status
    }


# ─────────────────────────────
# B8 — ML Engine Status
# ─────────────────────────────
@router.get("/ml-status")
def ml_status():
    try:
        response = requests.get(
            f"{ML_ENGINE_URL}/health",
            timeout=2
        )
        if response.status_code == 200:
            return {"ml_engine": "ok"}
    except Exception:
        pass

    return {"ml_engine": "down"}


# ─────────────────────────────
# B9 — Aggregated System Summary (UI READY)
# ─────────────────────────────
@router.get("/summary")
def system_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Database check
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    # ML engine check
    try:
        ml_ok = (
            requests.get(f"{ML_ENGINE_URL}/health", timeout=2).status_code == 200
        )
    except Exception:
        ml_ok = False

    return {
        "api": True,
        "database": db_ok,
        "ml_engine": ml_ok,
        "overall_status": "online" if all([db_ok, ml_ok]) else "degraded"
    }
