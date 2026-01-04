from sqlalchemy.orm import Session

from app.models.teacher_class_map import TeacherClassMap
from app.models.parent_child_map import ParentChildMap


def is_parent_of_child(
    db: Session,
    parent_id: str,
    child_id: str
) -> bool:
    return (
        db.query(ParentChildMap)
        .filter(
            ParentChildMap.parent_id == parent_id,
            ParentChildMap.child_id == child_id
        )
        .first()
        is not None
    )


def is_teacher_of_class(
    db: Session,
    teacher_id: str,
    class_name: str,
    section: str
) -> bool:
    """
    Checks if teacher handles a given class & section.
    """
    return (
        db.query(TeacherClassMap)
        .filter(
            TeacherClassMap.teacher_id == teacher_id,
            TeacherClassMap.class_name == class_name,
            TeacherClassMap.section == section
        )
        .first()
        is not None
    )


def is_teacher_of_child(
    db: Session,
    teacher_id: str,
    child_id: str
) -> bool:
    """
    Checks if teacher is explicitly mapped to the student.
    THIS IS THE ONLY VALID CHECK.
    """
    return (
        db.query(TeacherClassMap)
        .filter(
            TeacherClassMap.teacher_id == teacher_id,
            TeacherClassMap.student_id == child_id
        )
        .first()
        is not None
    )
