from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.parent_child_map import ParentChildMap
from app.models.user import User

router = APIRouter(prefix="/profile", tags=["Linked Accounts"])
@router.post("/link-child")
def link_child(
    payload: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "parent":
        raise HTTPException(status_code=403, detail="Parents only")

    child_id = payload.get("child_id")
    if not child_id:
        raise HTTPException(status_code=400, detail="child_id required")

    # Validate child exists
    child = db.query(User).filter(User.id == child_id).first()
    if not child or child.role != "student":
        raise HTTPException(status_code=404, detail="Student not found")

    # Prevent duplicates
    exists = (
        db.query(ParentChildMap)
        .filter(
            ParentChildMap.parent_id == current_user["user_id"],
            ParentChildMap.child_id == child_id
        )
        .first()
    )
    if exists:
        return {"status": "already_linked"}

    mapping = ParentChildMap(
        parent_id=current_user["user_id"],
        child_id=child_id
    )
    db.add(mapping)
    db.commit()

    return {
        "status": "linked",
        "parent_id": current_user["user_id"],
        "child_id": child_id
    }
@router.delete("/unlink-child/{child_id}")
def unlink_child(
    child_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "parent":
        raise HTTPException(status_code=403, detail="Parents only")

    mapping = (
        db.query(ParentChildMap)
        .filter(
            ParentChildMap.parent_id == current_user["user_id"],
            ParentChildMap.child_id == child_id
        )
        .first()
    )

    if not mapping:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(mapping)
    db.commit()

    return {
        "status": "unlinked",
        "child_id": child_id
    }
@router.get("/children")
def get_my_children(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "parent":
        raise HTTPException(status_code=403, detail="Parents only")

    rows = (
        db.query(User.id, User.email)
        .join(ParentChildMap, ParentChildMap.child_id == User.id)
        .filter(ParentChildMap.parent_id == current_user["user_id"])
        .all()
    )

    return [
        {
            "child_id": r.id,
            "email": r.email
        }
        for r in rows
    ]
@router.get("/parents/{child_id}")
def get_child_parents(
    child_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    parents = (
        db.query(User.id, User.email)
        .join(ParentChildMap, ParentChildMap.parent_id == User.id)
        .filter(ParentChildMap.child_id == child_id)
        .all()
    )

    return [
        {
            "parent_id": p.id,
            "email": p.email
        }
        for p in parents
    ]
