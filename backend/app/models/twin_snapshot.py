from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from sqlalchemy.sql import func
from app.db.base import Base

class TwinSnapshot(Base):
    __tablename__ = "twin_snapshots"

    snapshot_id = Column(Integer, primary_key=True, index=True)
    child_id = Column(String, nullable=False)

    snapshot_time = Column(DateTime, default=datetime.utcnow)
    twin_state = Column(String, nullable=False)

    derived_metrics = Column(JSON, nullable=True)
