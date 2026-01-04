from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.core.dependencies import get_current_user

from app.models.parent_child_map import ParentChildMap
from app.models.teacher_class_map import TeacherClassMap
from app.models.digital_twin import DigitalTwin
from app.models.risk_score import RiskScore
from app.models.student_features import StudentFeatures
from app.models.alert import Alert
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ─────────────────────────────
# ROLE GUARD
# ─────────────────────────────
def require_roles(roles: list):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker


# ─────────────────────────────
# BASIC SELF CHECK
# ─────────────────────────────
@router.get("/me")
def my_dashboard(user=Depends(get_current_user)):
    return {
        "user_id": user["user_id"],
        "role": user["role"]
    }


# ─────────────────────────────
# STUDENT DASHBOARD
# ─────────────────────────────
@router.get("/student")
def student_dashboard(
    user=Depends(require_roles(["student"])),
    db: Session = Depends(get_db)
):
    child_id = user["user_id"]

    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.child_id == child_id)
        .first()
    )

    risk = (
        db.query(RiskScore)
        .filter(RiskScore.child_id == child_id)
        .first()
    )

    features = (
        db.query(StudentFeatures)
        .filter(StudentFeatures.child_id == child_id)
        .first()
    )

    alerts = (
        db.query(Alert)
        .filter(
            Alert.child_id == child_id,
            Alert.resolved == False
        )
        .order_by(Alert.created_at.desc())
        .all()
    )

    return {
        "student_id": child_id,

        "twin": {
            "academic_score": twin.academic_score if twin else None,
            "attendance_score": twin.attendance_score if twin else None,
            "behavior_score": twin.behavior_score if twin else None,
            "state": twin.twin_state if twin else None,
        },

        "forecast": {
            "predicted_gpa": twin.predicted_gpa if twin else None,
            "failure_probability": twin.failure_probability if twin else None,
            "confidence": twin.forecast_confidence if twin else None,
        },

        "risk": {
            "attendance_risk": float(risk.attendance_risk) if risk else None,
            "academic_risk": float(risk.academic_risk) if risk else None,
            "behavior_risk": float(risk.behavior_risk) if risk else None,
            "volatility_risk": float(risk.volatility_risk) if risk else None,
            "total_risk": float(risk.total_risk) if risk else None,
        },

        "features": {
            "attendance_7d": features.attendance_7d if features else None,
            "attendance_30d": features.attendance_30d if features else None,
            "attendance_delta": features.attendance_delta if features else None,
            "test_score_7d": features.test_score_7d if features else None,
            "test_score_30d": features.test_score_30d if features else None,
            "test_score_delta": features.test_score_delta if features else None,
        },

        "alerts": [
            {
                "id": a.id,
                "severity": a.severity,
                "type": a.alert_type,
                "message": a.message,
                "created_at": a.created_at
            }
            for a in alerts
        ]
    }


# ─────────────────────────────
# PARENT DASHBOARD
# ─────────────────────────────
@router.get("/parent")
def parent_dashboard(
    user=Depends(require_roles(["parent"])),
    db: Session = Depends(get_db)
):
    parent_id = user["user_id"]

    children = (
        db.query(ParentChildMap.child_id)
        .filter(ParentChildMap.parent_id == parent_id)
        .all()
    )

    dashboard = []

    for (child_id,) in children:
        twin = (
            db.query(DigitalTwin)
            .filter(DigitalTwin.child_id == child_id)
            .first()
        )

        risk = (
            db.query(RiskScore)
            .filter(RiskScore.child_id == child_id)
            .first()
        )

        active_alerts = (
            db.query(Alert)
            .filter(
                Alert.child_id == child_id,
                Alert.resolved == False
            )
            .count()
        )

        dashboard.append({
            "child_id": child_id,
            "twin_state": twin.twin_state if twin else None,
            "academic_score": twin.academic_score if twin else None,
            "attendance_score": twin.attendance_score if twin else None,
            "behavior_score": twin.behavior_score if twin else None,
            "risk_score": float(risk.total_risk) if risk else None,
            "active_alerts": active_alerts
        })

    return {
        "parent_id": parent_id,
        "children": dashboard
    }


# ─────────────────────────────
# TEACHER DASHBOARD (CORRECTED)
# ─────────────────────────────
@router.get("/teacher")
def teacher_dashboard(
    user=Depends(require_roles(["teacher"])),
    db: Session = Depends(get_db)
):
    teacher_id = user["user_id"]

    students = (
        db.query(User)
        .join(
            TeacherClassMap,
            TeacherClassMap.student_id == User.id
        )
        .filter(
            TeacherClassMap.teacher_id == teacher_id,
            User.role == "student"
        )
        .all()
    )

    students_data = []

    for s in students:
        twin = (
            db.query(DigitalTwin)
            .filter(DigitalTwin.child_id == s.id)
            .first()
        )

        risk = (
            db.query(RiskScore)
            .filter(RiskScore.child_id == s.id)
            .first()
        )

        active_alerts = (
            db.query(Alert)
            .filter(
                Alert.child_id == s.id,
                Alert.resolved == False
            )
            .count()
        )

        students_data.append({
            "child_id": s.id,
            "full_name": s.full_name,
            "twin_state": twin.twin_state if twin else None,
            "academic_score": twin.academic_score if twin else None,
            "attendance_score": twin.attendance_score if twin else None,
            "behavior_score": twin.behavior_score if twin else None,
            "risk_score": float(risk.total_risk) if risk else None,
            "active_alerts": active_alerts
        })

    return {
        "teacher_id": teacher_id,
        "students_count": len(students_data),
        "high_risk_students": sum(
            1 for s in students_data
            if s["risk_score"] is not None and s["risk_score"] >= 75
        ),
        "students": students_data
    }


# ─────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────
@router.get("/admin")
def admin_dashboard(
    user=Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "system_status": "healthy" if db_ok else "degraded",

        "users": {
            "total": db.query(User).count(),
            "students": db.query(User).filter(User.role == "student").count(),
            "parents": db.query(User).filter(User.role == "parent").count(),
            "teachers": db.query(User).filter(User.role == "teacher").count(),
            "admins": db.query(User).filter(User.role == "admin").count(),
        },

        "alerts": {
            "active": db.query(Alert).filter(Alert.resolved == False).count()
        },

        "risk": {
            "high_risk_students": db.query(RiskScore)
            .filter(RiskScore.total_risk >= 75)
            .count()
        }
    }
