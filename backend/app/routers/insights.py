from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.digital_twin import DigitalTwin
from app.models.insight_review import InsightReview
from app.schemas.insights import RiskInsightOut
from app.core.dependencies import get_current_user
from app.core.ownership import is_parent_of_child, is_teacher_of_class

router = APIRouter(prefix="/insights", tags=["Risk Insights"])


@router.get("/self", response_model=RiskInsightOut)
def get_my_risk(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Students only")

    twin = db.query(DigitalTwin).filter_by(
        child_id=current_user["user_id"]
    ).first()

    if not twin:
        raise HTTPException(status_code=404, detail="Twin not found")

    return {
        "child_id": twin.child_id,
        "risk_level": twin.risk_level,
        "scores": {
            "academic": twin.academic_score or 0,
            "attendance": twin.attendance_score or 0,
            "behavior": twin.behavior_score or 0,
        },
        "explanation": twin.explanation,
        "last_updated": twin.last_updated,
    }


@router.get("/child/{child_id}", response_model=RiskInsightOut)
def get_child_risk(
    child_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "parent":
        raise HTTPException(status_code=403)

    if not is_parent_of_child(db, current_user["user_id"], child_id):
        raise HTTPException(status_code=403)

    twin = db.query(DigitalTwin).filter_by(child_id=child_id).first()
    if not twin:
        raise HTTPException(status_code=404)

    return {
        "child_id": twin.child_id,
        "risk_level": twin.risk_level,
        "scores": {
            "academic": twin.academic_score or 0,
            "attendance": twin.attendance_score or 0,
            "behavior": twin.behavior_score or 0,
        },
        "explanation": twin.explanation,
        "last_updated": twin.last_updated,
    }


@router.get("/class/{class_name}/{section}", response_model=List[RiskInsightOut])
def get_class_risks(
    class_name: str,
    section: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403)

    if not is_teacher_of_class(
        db, current_user["user_id"], class_name, section
    ):
        raise HTTPException(status_code=403)

    twins = (
        db.query(DigitalTwin)
        .filter(
            DigitalTwin.class_name == class_name,
            DigitalTwin.section == section
        )
        .all()
    )

    return [
        {
            "child_id": t.child_id,
            "risk_level": t.risk_level,
            "scores": {
                "academic": t.academic_score or 0,
                "attendance": t.attendance_score or 0,
                "behavior": t.behavior_score or 0,
            },
            "explanation": t.explanation,
            "last_updated": t.last_updated,
        }
        for t in twins
    ]


@router.post("/review/{child_id}")
def review_insight(
    child_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    role = current_user["role"]
    user_id = current_user["user_id"]

    if role == "student" and user_id != child_id:
        raise HTTPException(status_code=403)

    if role == "parent" and not is_parent_of_child(db, user_id, child_id):
        raise HTTPException(status_code=403)

    # 🛑 Prevent duplicate acknowledgements
    existing = (
        db.query(InsightReview)
        .filter_by(
            child_id=child_id,
            reviewer_id=user_id,
            reviewer_role=role
        )
        .first()
    )
    if existing:
        return {"status": "already_acknowledged"}

    review = InsightReview(
        child_id=child_id,
        reviewer_id=user_id,
        reviewer_role=role
    )

    db.add(review)
    db.commit()

    return {
        "status": "acknowledged",
        "child_id": child_id,
        "reviewer": role
    }
