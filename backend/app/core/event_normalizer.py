from app.models.event import Event


def normalize_event(event: Event) -> dict:
    """
    Convert raw payload into normalized numeric values
    """

    event_type = event.event_type
    payload = event.payload or {}

    if event_type == "attendance":
        return {
            "type": "attendance",
            "present": bool(payload.get("present", False))
        }

    if event_type == "test":
        return {
            "type": "test",
            "score": float(payload.get("score", 0))
        }

    if event_type == "behavior":
        return {
            "type": "behavior",
            "note": payload.get("note", "")
        }

    # Default fallback
    return {
        "type": event_type,
        "raw": payload
    }
