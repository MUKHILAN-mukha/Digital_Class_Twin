from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.db.session import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertOut
from app.core.dependencies import get_current_user
from app.core.ownership import is_parent_of_child, is_teacher_of_child

router = APIRouter(prefix="/alerts", tags=["Alerts"])


# ─────────────────────────────
# STUDENT — VIEW OWN ALERTS
# ─────────────────────────────
@router.get("/self", response_model=List[AlertOut])
def get_my_alerts(
    resolved: bool | None = None,
    severity: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user["role"] != "student":
        raise HTTPException(403, "Only students allowed")

    q = db.query(Alert).filter(Alert.child_id == user["user_id"])

    if resolved is not None:
        q = q.filter(Alert.resolved == resolved)
    if severity:
        q = q.filter(Alert.severity == severity)

    return q.order_by(Alert.created_at.desc()).all()


# ─────────────────────────────
# PARENT — VIEW CHILD ALERTS
# ─────────────────────────────
@router.get("/child/{child_id}", response_model=List[AlertOut])
def get_child_alerts(
    child_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user["role"] != "parent":
        raise HTTPException(403, "Only parents allowed")

    if not is_parent_of_child(db, user["user_id"], child_id):
        raise HTTPException(403, "Unauthorized access")

    return (
        db.query(Alert)
        .filter(Alert.child_id == child_id)
        .order_by(Alert.created_at.desc())
        .all()
    )


# ─────────────────────────────
# TEACHER — VIEW STUDENT ALERTS
# ─────────────────────────────
@router.get("/student/{child_id}", response_model=List[AlertOut])
def teacher_view_student_alerts(
    child_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user["role"] != "teacher":
        raise HTTPException(403)

    if not is_teacher_of_child(db, user["user_id"], child_id):
        raise HTTPException(403)

    return (
        db.query(Alert)
        .filter(Alert.child_id == child_id)
        .order_by(Alert.created_at.desc())
        .all()
    )


# ─────────────────────────────
# ADMIN — VIEW ALL ALERTS
# ─────────────────────────────
@router.get("/all", response_model=List[AlertOut])
def get_all_alerts(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(403, "Admin only")

    return db.query(Alert).order_by(Alert.created_at.desc()).all()


# ─────────────────────────────
# MARK ALERT AS READ (A5)
# ─────────────────────────────
@router.post("/{alert_id}/read")
def mark_alert_read(
    alert_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(404, "Alert not found")

    if alert.child_id != user["user_id"] and user["role"] != "admin":
        raise HTTPException(403)

    if not alert.is_read:
        alert.is_read = True
        alert.read_at = datetime.utcnow()
        db.commit()

    return {"status": "read"}


# ─────────────────────────────
# DISMISS / RESOLVE ALERT (A7)
# ─────────────────────────────
@router.post("/{alert_id}/dismiss")
def dismiss_alert(
    alert_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user["role"] not in ("student", "parent", "teacher", "admin"):
        raise HTTPException(403)

    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(404, "Alert not found")

    if alert.resolved:
        return {"status": "already_resolved"}

    alert.resolved = True
    alert.resolved_at = datetime.utcnow()
    db.commit()

    return {"status": "dismissed"}
