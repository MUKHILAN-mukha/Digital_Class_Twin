def extract_features(events):
    features = {
        "attendance": [],
        "scores": [],
        "behavior": []
    }

    for e in events:
        if e.event_type == "attendance_marked":
            features["attendance"].append(
                1 if e.payload.get("present") else 0
            )

        elif e.event_type == "marks_uploaded":
            score = e.payload.get("score")
            max_score = e.payload.get("max_score", 100)
            if score is not None:
                features["scores"].append(score / max_score)

        elif e.event_type == "behavior_observation":
            level = e.payload.get("level", "normal")
            features["behavior"].append(
                1 if level == "good" else 0
            )

    return features
