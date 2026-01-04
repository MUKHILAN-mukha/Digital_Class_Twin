from sqlalchemy.orm import Session
from datetime import datetime

from app.models.digital_twin import DigitalTwin


def compute_twin_metrics(db: Session, child_id: str):
    """
    Convert aggregated metrics into normalized twin scores (0–100)
    """

    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.child_id == child_id)
        .first()
    )

    if not twin or not twin.derived_metrics:
        return

    weekly = twin.derived_metrics.get("weekly", {})
    daily = twin.derived_metrics.get("daily", {})

    # ─────────────── ATTENDANCE SCORE ───────────────
    attendance_ratio = (
        weekly.get("attendance")
        if weekly.get("attendance") is not None
        else daily.get("attendance")
    )

    if attendance_ratio is not None:
        twin.attendance_score = round(attendance_ratio * 100, 2)

    # ─────────────── ACADEMIC SCORE ───────────────
    academic_avg = (
        weekly.get("academic")
        if weekly.get("academic") is not None
        else daily.get("academic")
    )

    if academic_avg is not None:
        twin.academic_score = round(float(academic_avg), 2)

    # ─────────────── BEHAVIOR SCORE ───────────────
    behavior_value = (
        weekly.get("behavior")
        if weekly.get("behavior") is not None
        else daily.get("behavior", 0)
    )

    if behavior_value is not None:
        penalty = abs(behavior_value) * 10
        twin.behavior_score = max(0, 100 - penalty)

    twin.last_updated_at = datetime.utcnow()

    db.commit()
