from enum import Enum


class OdinEnum(Enum):
    """Enumeration Class for OdinEnum

    This enumeration class instructs all enumeration objects inheriting from it
    to show their value when they are requested to be printed to the standard
    output.
    """
    def __str__(self):
        return self.value
