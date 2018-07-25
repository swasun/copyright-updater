from enum import Enum

class CommentType(Enum):
    UNKNOWN = 0
    SUROUND_BY_STARS = 1
    SUROUND_BY_SYMBOL_NUMBERS = 2
    SLASH = 3
    SYMBOL_NUMBER = 4