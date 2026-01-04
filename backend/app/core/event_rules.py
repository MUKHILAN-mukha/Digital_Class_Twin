ROLE_EVENT_MAP = {
    "student": {
        "attendance_marked",
        "test_score_recorded",
        "activity_completed"
    },
    "teacher": {
        "teacher_attendance",
        "marks_uploaded",
        "behavior_observation"
    },
    "parent": {
        "parent_feedback",
        "acknowledged_alert"
    },
    "admin": {
        "system_configuration_change"
    }
}


def apply_event_rule(event_type: str, payload: dict, twin):
    """
    T2 — Event-driven twin update.
    NO risk calculation.
    NO aggregation.
    Deterministic metric mutation only.
    """

    payload = payload or {}

    # ───────────────── Attendance ─────────────────
    if event_type == "attendance_marked":
        present = payload.get("present")

        if present is True:
            twin.attendance_score += 1
        elif present is False:
            twin.attendance_score -= 1

    # ───────────────── Academic ─────────────────
    elif event_type == "test_score_recorded":
        score = payload.get("score")

        if isinstance(score, (int, float)):
            # Normalize roughly to 0–10 scale
            twin.academic_score += score / 10
            twin.academic_score = max(0.0, min(twin.academic_score, 10.0))

    # ───────────────── Behavior ─────────────────
    elif event_type == "behavior_observation":
        severity = payload.get("severity")

        if isinstance(severity, (int, float)):
            twin.behavior_score -= severity

    # ───────────────── Unknown Event ─────────────────
    else:
        twin.explanation = {
            "last_event": event_type,
            "note": "Unknown event type safely ignored"
        }
        return twin

    # ───────────────── Metadata only ─────────────────
    twin.explanation = {
        "last_event": event_type,
        "update": "metric mutation applied"
    }

    return twin
