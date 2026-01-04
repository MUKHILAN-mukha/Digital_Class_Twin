from sqlalchemy.orm import Session
from datetime import datetime

from app.models.digital_twin import DigitalTwin
from app.models.twin_snapshot import TwinSnapshot


def _trend_from_delta(delta: float):
    if delta > 2:
        return "improving"
    if delta < -2:
        return "declining"
    return "stable"


def compute_twin_trends(db: Session, child_id: str):
    """
    Detect improvement / decline trends based on last snapshot
    """

    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.child_id == child_id)
        .first()
    )

    if not twin:
        return

    # Get previous snapshot (excluding latest)
    prev_snapshot = (
        db.query(TwinSnapshot)
        .filter(TwinSnapshot.child_id == child_id)
        .order_by(TwinSnapshot.snapshot_time.desc())
        .offset(1)
        .first()
    )

    if not prev_snapshot:
        _set_insufficient_trends(twin)
        db.commit()
        return

    trends = {}

    # Attendance trend
    trends["attendance"] = _trend_from_delta(
        twin.attendance_score - prev_snapshot.attendance_score
    )

    # Academic trend
    trends["academic"] = _trend_from_delta(
        twin.academic_score - prev_snapshot.academic_score
    )

    # Behavior trend (higher is better)
    trends["behavior"] = _trend_from_delta(
        twin.behavior_score - prev_snapshot.behavior_score
    )

    twin.derived_metrics = twin.derived_metrics or {}
    twin.derived_metrics["trends"] = trends
    twin.last_updated_at = datetime.utcnow()

    db.commit()


def _set_insufficient_trends(twin: DigitalTwin):
    twin.derived_metrics = twin.derived_metrics or {}
    twin.derived_metrics["trends"] = {
        "attendance": "insufficient_data",
        "academic": "insufficient_data",
        "behavior": "insufficient_data",
    }
