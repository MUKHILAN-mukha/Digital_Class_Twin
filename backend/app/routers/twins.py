from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.digital_twin import DigitalTwin
from app.schemas.twin import DigitalTwinOut
from app.core.dependencies import get_current_user
from app.core.ownership import is_parent_of_child, is_teacher_of_class

router = APIRouter(prefix="/twins", tags=["Digital Twins"])


# ─────────────────────────────
# STUDENT: own twin
# ─────────────────────────────
@router.get("/self", response_model=DigitalTwinOut)
def get_my_twin(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")

    twin = db.query(DigitalTwin).filter_by(
        child_id=current_user["user_id"]
    ).first()

    if not twin:
        raise HTTPException(status_code=404, detail="Twin not found")

    return twin


# ─────────────────────────────
# PARENT: child twin
# ─────────────────────────────
@router.get("/child/{child_id}", response_model=DigitalTwinOut)
def get_child_twin(
    child_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "parent":
        raise HTTPException(status_code=403, detail="Only parents allowed")

    if not is_parent_of_child(db, current_user["user_id"], child_id):
        raise HTTPException(status_code=403, detail="Unauthorized child access")

    twin = db.query(DigitalTwin).filter_by(child_id=child_id).first()
    if not twin:
        raise HTTPException(status_code=404, detail="Twin not found")

    return twin


# ─────────────────────────────
# TEACHER: class twins
# ─────────────────────────────
@router.get("/class/{class_name}/{section}", response_model=List[DigitalTwinOut])
def get_class_twins(
    class_name: str,
    section: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers allowed")

    if not is_teacher_of_class(
        db, current_user["user_id"], class_name, section
    ):
        raise HTTPException(status_code=403, detail="Teacher not assigned")

    # ✅ Fetch twins by students of this class
    twins = (
        db.query(DigitalTwin)
        .filter(
            DigitalTwin.class_name == class_name,
            DigitalTwin.section == section
        )
        .all()
    )

    return twins



# ─────────────────────────────
# ADMIN: all twins
# ─────────────────────────────
@router.get("/all", response_model=List[DigitalTwinOut])
def get_all_twins(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    return db.query(DigitalTwin).all()
