from enum import Enum, StrEnum


class EnumBase(Enum):
    @classmethod
    def get_member_values(cls):
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls):
        return [name for name in cls._member_names_]


class MenuType(StrEnum):
    CATALOG = "catalog"
    MENU = "menu"


class MethodType(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class GradeType(StrEnum):
    GRADE_5 = "GRADE_5"
    GRADE_6 = "GRADE_6"
    GRADE_7 = "GRADE_7"
    GRADE_8 = "GRADE_8"
    GRADE_9 = "GRADE_9"
    GRADE_10 = "GRADE_10"
    GRADE_11 = "GRADE_11"


class CourseType(StrEnum):
    ONLINE = "ONLINE"
    PHYSICAL = "PHYSICAL"
