from sqlalchemy import Column, String, ForeignKey
from app.db.base import Base


class TeacherClassMap(Base):
    __tablename__ = "teacher_class_map"

    teacher_id = Column(
        String,
        ForeignKey("users.id"),
        primary_key=True
    )

    student_id = Column(
        String,
        ForeignKey("users.id"),
        primary_key=True
    )

    class_name = Column(String, nullable=False)
    section = Column(String, nullable=False)
