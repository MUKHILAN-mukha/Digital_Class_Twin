from config import (
    ATTENDANCE_LOW_THRESHOLD,
    ACADEMIC_LOW_THRESHOLD,
    DEFAULT_BEHAVIOR_SCORE
)

def compute_risk(features):
    attendance = features["attendance"]
    scores = features["scores"]
    behavior = features["behavior"]

    attendance_avg = sum(attendance) / len(attendance) if attendance else None
    academic_avg = sum(scores) / len(scores) if scores else None
    behavior_avg = sum(behavior) / len(behavior) if behavior else DEFAULT_BEHAVIOR_SCORE

    risk = "Low"
    if attendance_avg is not None and attendance_avg < ATTENDANCE_LOW_THRESHOLD:
        risk = "High"
    elif academic_avg is not None and academic_avg < ACADEMIC_LOW_THRESHOLD:
        risk = "Medium"

    return {
        "attendance_score": attendance_avg,
        "academic_score": academic_avg,
        "behavior_score": behavior_avg,
        "risk_level": risk
    }
