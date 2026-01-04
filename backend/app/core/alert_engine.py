from datetime import datetime
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.digital_twin import DigitalTwin
from app.models.risk_score import RiskScore


def trigger_risk_alert(db: Session, twin: DigitalTwin):
    """
    A1–A6: Rule + analytics driven alert engine
    """

    risk = (
        db.query(RiskScore)
        .filter(RiskScore.child_id == twin.child_id)
        .first()
    )

    if not risk:
        return

    # ─────────────────────────────
    # A2 — Severity assignment
    # ─────────────────────────────
    if risk.total_risk >= 75 or twin.twin_state == "critical":
        severity = "high"
    elif risk.total_risk >= 50 or twin.twin_state == "warning":
        severity = "medium"
    else:
        severity = "low"

    # ─────────────────────────────
    # A5 — Auto-resolve when low
    # ─────────────────────────────
    if severity == "low":
        db.query(Alert).filter(
            Alert.child_id == twin.child_id,
            Alert.resolved == False
        ).update(
            {
                "resolved": True,
                "resolved_at": datetime.utcnow()
            }
        )
        db.commit()
        return

    # ─────────────────────────────
    # A6 — Category inference
    # ─────────────────────────────
    category = "academic"
    if risk.attendance_risk > risk.academic_risk:
        category = "attendance"
    if risk.behavior_risk and risk.behavior_risk > 0:
        category = "behavior"

    # ─────────────────────────────
    # A4 — Avoid duplicates
    # ─────────────────────────────
    exists = (
        db.query(Alert)
        .filter(
            Alert.child_id == twin.child_id,
            Alert.alert_type == f"{category}_risk",
            Alert.resolved == False
        )
        .first()
    )

    if exists:
        return

    # ─────────────────────────────
    # A1 + A3 — Create alert
    # ─────────────────────────────
    alert = Alert(
        child_id=twin.child_id,
        alert_type=f"{category}_risk",
        severity=severity,
        message=f"{category.capitalize()} risk is {severity}",
        context={
            "total_risk": float(risk.total_risk),
            "attendance_risk": float(risk.attendance_risk or 0),
            "academic_risk": float(risk.academic_risk or 0),
            "behavior_risk": float(risk.behavior_risk or 0),
            "twin_state": twin.twin_state
        },
        resolved=False
    )

    db.add(alert)
    db.commit()
