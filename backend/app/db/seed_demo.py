# app/db/seed_demo.py

from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.models.parent_child_map import ParentChildMap
from app.models.teacher_class_map import TeacherClassMap
from app.models.event import Event
from app.core.security import hash_password


def get_or_create_user(
    db: Session,
    email: str,
    role: str,
    password: str,
    full_name: str = None
):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user

    user = User(
        id=str(uuid.uuid4()),
        email=email,
        hashed_password=hash_password(password),
        role=role,
        full_name=full_name,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    return user


def seed():
    db = SessionLocal()

    print("🌱 Seeding demo data...")

    # ─────────────────────────────
    # USERS
    # ─────────────────────────────
    student = get_or_create_user(
        db,
        email="student@test.com",
        password="password",
        role="student",
        full_name="Demo Student"
    )

    parent = get_or_create_user(
        db,
        email="parent@test.com",
        password="password",
        role="parent",
        full_name="Demo Parent"
    )

    teacher = get_or_create_user(
        db,
        email="teacher@test.com",
        password="password",
        role="teacher",
        full_name="Demo Teacher"
    )

    admin = get_or_create_user(
        db,
        email="admin@test.com",
        password="password",
        role="admin",
        full_name="System Admin"
    )

    # ─────────────────────────────
    # PARENT ↔ CHILD
    # ─────────────────────────────
 # Parent ↔ Child
    if not db.query(ParentChildMap).filter_by(
        parent_id=parent.id,
        child_id=student.id
    ).first():
        db.add(
            ParentChildMap(
                parent_id=parent.id,
                child_id=student.id
            )
        )


    # Teacher ↔ Student
    if not db.query(TeacherClassMap).filter_by(
        teacher_id=teacher.id,
        student_id=student.id
    ).first():
        db.add(
            TeacherClassMap(
                teacher_id=teacher.id,
                student_id=student.id,
                class_name="10",
                section="A"
            )
        )


    # ─────────────────────────────
    # EVENTS (only if none exist)
    # ─────────────────────────────
    if not db.query(Event).filter(Event.child_id == student.id).first():
        now = datetime.utcnow()
        events = [
            Event(
                child_id=student.id,
                event_type="attendance",
                payload={"present": True},
                created_at=now - timedelta(days=i),
                processed=False
            )
            for i in range(5)
        ] + [
            Event(
                child_id=student.id,
                event_type="academic",
                payload={"score": 60 + i * 5},
                created_at=now - timedelta(days=i),
                processed=False
            )
            for i in range(5)
        ]

        db.add_all(events)

    db.commit()
    db.close()

    print("✅ DEMO DATA SEEDED (safe to re-run)")


if __name__ == "__main__":
    seed()
