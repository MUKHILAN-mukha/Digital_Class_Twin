from db import SessionLocal
from models import Event
from feature_extractor import extract_features
from risk_engine import compute_risk
from forecasting_engine import generate_forecast
import twin_updater
update_twin = twin_updater.update_twin
import twin_updater
print("USING FILE:", twin_updater.__file__)
print("ARGS:", twin_updater.update_twin.__code__.co_varnames)



def run():
    db = SessionLocal()

    # Fetch unprocessed events
    events = (
        db.query(Event)
        .filter(Event.processed == False)
        .all()
    )

    if not events:
        db.close()
        return

    # Group events by student
    grouped = {}
    for e in events:
        grouped.setdefault(e.child_id, []).append(e)

    # Process each student independently
    for child_id, evts in grouped.items():
        child_id = str(child_id)
        # ─────────────────────────────
        # STEP 3 — Feature Engineering
        # ─────────────────────────────
        features = extract_features(evts)

        # ─────────────────────────────
        # STEP 4 — Risk Engine (M1–M6)
        # ─────────────────────────────
        scores = compute_risk(features)

        # ─────────────────────────────
        # STEP 5 — Forecasting Engine (M7–M10)
        # ─────────────────────────────
        forecasts = generate_forecast(features)

        # ─────────────────────────────
        # Update Digital Twin + Predictions
        # ─────────────────────────────
        update_twin(
            db=db,
            child_id=child_id,
            scores=scores
        )


        # Mark events as processed
        for e in evts:
            e.processed = True

    db.commit()
    db.close()


if __name__ == "__main__":
    run()
