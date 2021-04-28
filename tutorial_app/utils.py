"""Utility classes & functions."""
# Credit to Meredith Murphy, BEW instructor, for this enum utility function
import enum


class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""

    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)
