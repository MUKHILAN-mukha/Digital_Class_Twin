from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.event import Event
from app.models.digital_twin import DigitalTwin
from app.models.twin_snapshot import TwinSnapshot


def aggregate_twin_metrics(db: Session, child_id: str):
    """
    Aggregate daily and weekly metrics for a single child
    """

    now = datetime.utcnow()
    day_start = now - timedelta(days=1)
    week_start = now - timedelta(days=7)

    # ─────────────── FETCH EVENTS ───────────────
    daily_events = (
        db.query(Event)
        .filter(
            Event.child_id == child_id,
            Event.timestamp >= day_start
        )
        .all()
    )

    weekly_events = (
        db.query(Event)
        .filter(
            Event.child_id == child_id,
            Event.timestamp >= week_start
        )
        .all()
    )

    daily = _summarize_events(daily_events)
    weekly = _summarize_events(weekly_events)

    # ─────────────── UPDATE DIGITAL TWIN ───────────────
    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.child_id == child_id)
        .first()
    )

    if not twin:
        return

    twin.derived_metrics = {
        "daily": daily,
        "weekly": weekly
    }
    twin.last_updated_at = now

    # ─────────────── SNAPSHOT ───────────────
    snapshot = TwinSnapshot(
        child_id=child_id,
        snapshot_time=now,
        twin_state=twin.twin_state,
        derived_metrics=twin.derived_metrics
    )

    db.add(snapshot)
    db.commit()


def _summarize_events(events):
    """
    Reduce raw events into stable metrics
    """

    attendance = []
    academic = []
    behavior = []

    for e in events:
        payload = e.payload or {}

        if e.event_type == "attendance_marked":
            present = payload.get("present")
            if present is True:
                attendance.append(1)
            elif present is False:
                attendance.append(0)

        elif e.event_type == "test_score_recorded":
            score = payload.get("score")
            if isinstance(score, (int, float)):
                academic.append(score)

        elif e.event_type == "behavior_observation":
            severity = payload.get("severity")
            if isinstance(severity, (int, float)):
                behavior.append(severity)

    return {
        "attendance": round(sum(attendance) / len(attendance), 2) if attendance else None,
        "academic": round(sum(academic) / len(academic), 2) if academic else None,
        "behavior": sum(behavior) if behavior else 0
    }
