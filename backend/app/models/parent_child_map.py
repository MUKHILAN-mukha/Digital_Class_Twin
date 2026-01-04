from sqlalchemy import Column, String, ForeignKey
from app.db.base import Base


class ParentChildMap(Base):
    __tablename__ = "parent_child_map"

    parent_id = Column(
        String,
        ForeignKey("users.id"),
        primary_key=True
    )

    child_id = Column(
        String,
        ForeignKey("users.id"),
        primary_key=True
    )
