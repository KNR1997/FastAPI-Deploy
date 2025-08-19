from tortoise import fields

from app.models.admin import User
from app.models.subject import Subject

from .base import AuditModel
from .enums import GradeType, CourseType

class Course(AuditModel):
    course_type = fields.CharEnumField(CourseType, description="Course_type", null=True, index=True)
    name = fields.CharField(max_length=150, unique=True, description="Course Name", index=True)
    code = fields.CharField(max_length=150, unique=True, description="Course Code", index=True)
    subject: fields.ForeignKeyRelation[Subject] = fields.ForeignKeyField(
        "models.Subject", related_name="courses"
    )
    teacher: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="courses"
    )
    grade = fields.CharEnumField(GradeType, description="Grade", index=True)
    batch = fields.IntField(default=1, description="Course Batch", index=True)
    is_active = fields.BooleanField(default=True, description="Is Course active or not")
    fee =  fields.FloatField(null=True)

    class Meta:
        table = "course"
