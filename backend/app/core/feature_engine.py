from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.event import Event
from app.models.student_features import StudentFeatures
def extract_attendance_features(db: Session, child_id: str):
    now = datetime.utcnow()
    last_30d = now - timedelta(days=30)
    last_7d = now - timedelta(days=7)
    prev_7d = now - timedelta(days=14)

    present_30d = db.query(func.count()).filter(
        Event.child_id == child_id,
        Event.event_type == "attendance",
        Event.payload["present"].as_boolean() == True,
        Event.timestamp >= last_30d
    ).scalar()

    total_30d = db.query(func.count()).filter(
        Event.child_id == child_id,
        Event.event_type == "attendance",
        Event.timestamp >= last_30d
    ).scalar()

    present_7d = db.query(func.count()).filter(
        Event.child_id == child_id,
        Event.event_type == "attendance",
        Event.payload["present"].as_boolean() == True,
        Event.timestamp >= last_7d
    ).scalar()

    present_prev_7d = db.query(func.count()).filter(
        Event.child_id == child_id,
        Event.event_type == "attendance",
        Event.payload["present"].as_boolean() == True,
        Event.timestamp.between(prev_7d, last_7d)
    ).scalar()

    attendance_rate_30d = (present_30d / total_30d) if total_30d else 1.0
    attendance_delta = present_7d - present_prev_7d

    return attendance_rate_30d, attendance_delta
def extract_academic_features(db: Session, child_id: str):
    now = datetime.utcnow()
    last_30d = now - timedelta(days=30)
    last_7d = now - timedelta(days=7)
    prev_7d = now - timedelta(days=14)

    avg_30d = db.query(
        func.avg((Event.payload["score"].as_float()))
    ).filter(
        Event.child_id == child_id,
        Event.event_type == "test",
        Event.timestamp >= last_30d
    ).scalar() or 0.0

    avg_7d = db.query(
        func.avg((Event.payload["score"].as_float()))
    ).filter(
        Event.child_id == child_id,
        Event.event_type == "test",
        Event.timestamp >= last_7d
    ).scalar() or 0.0

    avg_prev_7d = db.query(
        func.avg((Event.payload["score"].as_float()))
    ).filter(
        Event.child_id == child_id,
        Event.event_type == "test",
        Event.timestamp.between(prev_7d, last_7d)
    ).scalar() or 0.0

    delta = avg_7d - avg_prev_7d

    return avg_30d, delta
def extract_behavior_features(db: Session, child_id: str):
    now = datetime.utcnow()
    last_30d = now - timedelta(days=30)
    last_7d = now - timedelta(days=7)
    prev_7d = now - timedelta(days=14)

    neg_30d = db.query(func.count()).filter(
        Event.child_id == child_id,
        Event.event_type == "behavior",
        Event.payload["severity"].as_integer() > 0,
        Event.timestamp >= last_30d
    ).scalar()

    neg_7d = db.query(func.count()).filter(
        Event.child_id == child_id,
        Event.event_type == "behavior",
        Event.payload["severity"].as_integer() > 0,
        Event.timestamp >= last_7d
    ).scalar()

    neg_prev_7d = db.query(func.count()).filter(
        Event.child_id == child_id,
        Event.event_type == "behavior",
        Event.payload["severity"].as_integer() > 0,
        Event.timestamp.between(prev_7d, last_7d)
    ).scalar()

    delta = neg_7d - neg_prev_7d

    return neg_30d, delta
def update_student_features(db: Session, child_id: str):
    attendance_rate, attendance_delta = extract_attendance_features(db, child_id)
    avg_score, test_delta = extract_academic_features(db, child_id)
    neg_behavior, behavior_delta = extract_behavior_features(db, child_id)

    volatility = abs(test_delta)

    features = db.query(StudentFeatures).filter(
        StudentFeatures.child_id == child_id
    ).first()

    if not features:
        features = StudentFeatures(child_id=child_id)
        db.add(features)

    features.attendance_rate_30d = attendance_rate
    features.attendance_delta = attendance_delta
    features.avg_test_score_30d = avg_score
    features.test_score_delta = test_delta
    features.behavior_count_30d = neg_behavior
    features.behavior_delta = behavior_delta
    features.volatility_score = volatility
    features.updated_at = datetime.utcnow()

    db.commit()
