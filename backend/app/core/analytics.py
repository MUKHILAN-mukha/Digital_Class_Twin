from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.digital_twin import DigitalTwin
from app.models.alert import Alert

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/teacher")
def teacher_overview(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Teachers only")

    return {
        "total_students": db.query(DigitalTwin).count(),
        "high_risk_students": db.query(DigitalTwin)
            .filter(DigitalTwin.risk_level == "high")
            .count()
    }


@router.get("/admin")
def admin_overview(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return {
        "total_students": db.query(DigitalTwin).count(),
        "active_alerts": db.query(Alert)
            .filter(Alert.resolved == False)
            .count(),
        "risk_distribution": {
            "high": db.query(DigitalTwin)
                .filter(DigitalTwin.risk_level == "high").count(),
            "medium": db.query(DigitalTwin)
                .filter(DigitalTwin.risk_level == "medium").count(),
            "low": db.query(DigitalTwin)
                .filter(DigitalTwin.risk_level == "low").count(),
        }
    }
