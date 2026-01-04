from sqlalchemy.orm import Session
from datetime import datetime

from app.models.event import Event
from app.models.digital_twin import DigitalTwin
from app.models.twin_snapshot import TwinSnapshot

from app.core.event_normalizer import normalize_event
from app.core.feature_engine import update_student_features
from app.core.twin_engine import compute_twin_metrics
from app.core.risk_engine import compute_risk
from app.core.alert_engine import trigger_risk_alert
def process_events(db: Session, limit: int = 50):
    events = (
        db.query(Event)
        .filter(Event.processed == False)
        .order_by(Event.timestamp)
        .limit(limit)
        .all()
    )

    for event in events:
        try:
            process_single_event(db, event)
        except Exception as e:
            event.processed = True
            event.payload = {
                "error": str(e),
                "note": "Auto-skipped due to processing error"
            }

    db.commit()
def process_single_event(db: Session, event: Event):

    # SYSTEM / ADMIN EVENTS
    if not event.child_id:
        event.processed = True
        return

    # 1️⃣ Normalize event
    normalized = normalize_event(event)

    # 2️⃣ Update features (student_features table)
    update_student_features(
        db=db,
        child_id=event.child_id,
        event=normalized
    )

    # 3️⃣ Fetch or create twin
    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.child_id == event.child_id)
        .first()
    )

    if not twin:
        twin = DigitalTwin(
            child_id=event.child_id,
            academic_score=0.0,
            attendance_score=0.0,
            behavior_score=0.0,
            risk_level="unknown",
            twin_state="stable",
            explanation={},
            derived_metrics={},
            last_updated=datetime.utcnow(),
            last_updated_at=datetime.utcnow()
        )
        db.add(twin)
        db.flush()


    # 4️⃣ Compute twin metrics (aggregation)
    metrics = compute_twin_metrics(db, event.child_id)

    twin.academic_score = metrics.academic
    twin.attendance_score = metrics.attendance
    twin.behavior_score = metrics.behavior

    # 5️⃣ Risk engine
    risk = compute_risk(metrics)

    previous_state = twin.risk_level
    twin.risk_level = risk.level
    twin.explanation = risk.explanation
    twin.last_updated = datetime.utcnow()

    # 6️⃣ Snapshot on state change
    if previous_state != twin.risk_level:
        snapshot = TwinSnapshot(
            child_id=event.child_id,
            snapshot_time=datetime.utcnow(),
            twin_state=twin.risk_level,
            derived_metrics=metrics.dict()
        )
        db.add(snapshot)

        # 7️⃣ Alert trigger (state-aware)
        trigger_risk_alert(db, twin, previous_state)

    # 8️⃣ Mark processed
    event.processed = True
