import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict


# ─────────────────────────────
# M7 — GPA Prediction
# ─────────────────────────────
def predict_gpa(features: Dict) -> float:
    academic_avg = features.get("academic_avg", 0)
    attendance_pct = features.get("attendance_pct", 0)

    gpa = (academic_avg * 0.7) + (attendance_pct * 0.3)
    return round(min(max(gpa, 0), 10), 2)


# ─────────────────────────────
# M8 — Subject Trend Forecast
# ─────────────────────────────
def subject_forecast(features: Dict) -> Dict[str, str]:
    trends = {}
    subject_deltas = features.get("subject_trends", {})

    for subject, delta in subject_deltas.items():
        if delta > 5:
            trends[subject] = "Improving"
        elif delta < -5:
            trends[subject] = "Declining"
        else:
            trends[subject] = "Stable"

    return trends


# ─────────────────────────────
# M9 — Failure Probability
# ─────────────────────────────
def failure_probability(features: Dict) -> float:
    risk = 0.0

    if features.get("attendance_pct", 100) < 60:
        risk += 0.4
    if features.get("academic_avg", 10) < 4:
        risk += 0.4
    if features.get("behavior_score", 1) < 0.5:
        risk += 0.2

    return round(min(risk, 1.0), 2)


# ─────────────────────────────
# M10 — Confidence Score
# ─────────────────────────────
def forecast_confidence(features: Dict) -> float:
    data_points = features.get("event_count", 0)
    volatility = features.get("volatility", 0)

    confidence = min(data_points / 50, 1.0) * (1 - min(volatility, 1))
    return round(max(confidence, 0.1), 2)


# ─────────────────────────────
# FINAL FORECAST PAYLOAD
# ─────────────────────────────
def generate_forecast(features: Dict) -> Dict:
    return {
        "predicted_gpa": predict_gpa(features),
        "failure_probability": failure_probability(features),
        "confidence": forecast_confidence(features),
        "subjects": subject_forecast(features)
    }
