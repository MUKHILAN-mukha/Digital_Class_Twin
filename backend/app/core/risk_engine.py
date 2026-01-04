class RiskResult:
    def __init__(self, level: str, explanation: dict):
        self.level = level
        self.explanation = explanation


def compute_risk(metrics) -> RiskResult:
    score = (
        metrics.academic * 0.5 +
        metrics.attendance * 0.3 +
        metrics.behavior * 0.2
    )

    if score >= 75:
        level = "low"
    elif score >= 50:
        level = "moderate"
    else:
        level = "high"

    return RiskResult(
        level=level,
        explanation={
            "academic": metrics.academic,
            "attendance": metrics.attendance,
            "behavior": metrics.behavior,
            "composite": score
        }
    )
