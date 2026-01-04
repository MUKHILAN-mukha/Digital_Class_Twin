from datetime import datetime
from sqlalchemy.orm import Session
from app.models.student_features import StudentFeatures
from app.models.digital_twin import DigitalTwin
from app.models.risk_score import RiskScore
from app.models.twin_snapshot import TwinSnapshot

def update_twin_state(db: Session, child_id: str):
    risk = (
        db.query(RiskScore)
        .filter(RiskScore.child_id == child_id)
        .first()
    )

    if not risk:
        return

    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.child_id == child_id)
        .first()
    )

    if not twin:
        return

    # ─────────────────────────────
    # CAPTURE PREVIOUS STATE
    # ─────────────────────────────
    previous_state = twin.twin_state
    previous_risk = twin.risk_level

    # ─────────────────────────────
    # ASSIGN NEW STATE
    # ─────────────────────────────
    if risk.total_risk >= 75:
        twin.twin_state = "stable"
    elif risk.total_risk >= 50:
        twin.twin_state = "warning"
    else:
        twin.twin_state = "critical"

    twin.last_updated_at = datetime.utcnow()

    # ─────────────────────────────
    # SNAPSHOT ONLY IF CHANGED
    # ─────────────────────────────
    if twin.twin_state != previous_state or twin.risk_level != previous_risk:
        snapshot = TwinSnapshot(
            child_id=twin.child_id,
            snapshot_time=datetime.utcnow(),
            twin_state=twin.twin_state,
            derived_metrics=twin.derived_metrics
        )
        db.add(snapshot)

    db.commit()


def create_twin_if_not_exists(db: Session, child_id: str) -> DigitalTwin:
    """
    Create a digital twin for a student if it does not already exist
    """

    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.child_id == child_id)
        .first()
    )

    if twin:
        return twin

    twin = DigitalTwin(
        child_id=child_id,
        academic_score=0.0,
        attendance_score=0.0,
        behavior_score=0.0,
        risk_level="unknown",
        twin_state="stable",
        derived_metrics={},
        explanation={},
        last_updated=datetime.utcnow(),
        last_updated_at=datetime.utcnow()
    )

    db.add(twin)
    db.commit()
    db.refresh(twin)

    return twin

def compute_twin_metrics(db: Session, child_id: str):
    """
    Compute Digital Twin metrics from engineered features
    """

    features = (
        db.query(StudentFeatures)
        .filter(StudentFeatures.child_id == child_id)
        .first()
    )

    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.child_id == child_id)
        .first()
    )

    if not twin or not features:
        return

    # ─────────────────────────────
    # METRIC CALCULATION (0–1 scale)
    # ─────────────────────────────
    twin.attendance_score = features.attendance_norm or 0.0
    twin.academic_score = features.test_score_norm or 0.0
    twin.behavior_score = features.homework_norm or 0.0

    # Derived metrics (for UI + explanations)
    twin.derived_metrics = {
        "attendance_7d": features.attendance_7d,
        "attendance_30d": features.attendance_30d,
        "test_score_7d": features.test_score_7d,
        "test_score_30d": features.test_score_30d,
        "attendance_delta": features.attendance_delta,
        "test_score_delta": features.test_score_delta
    }

    twin.last_updated_at = datetime.utcnow()

    db.commit()

    # After metrics → update state & snapshot
    update_twin_state(db, child_id)
