from app.db.session import engine
from app.db.base import Base

# 🔴 FORCE ALL MODELS TO LOAD
# If a model is not imported here, its table WILL NOT be created

import app.models.user
import app.models.parent_child_map
import app.models.teacher_class_map

import app.models.event
import app.models.digital_twin
import app.models.twin_snapshot

import app.models.student_features
import app.models.risk_score

import app.models.alert
import app.models.user_session
import app.models.insight_review


def init_db():
    print("🧱 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")
if __name__ == "__main__":
    init_db()
