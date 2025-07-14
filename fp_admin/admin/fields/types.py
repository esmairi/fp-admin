"""
Field types for fp-admin.

This module defines the supported field types for admin forms.
"""

from typing import Literal

FieldType = Literal[
    "string",
    "number",
    "float",
    "time",
    "datetime",
    "boolean",
    "choice",
    "multichoice",
    "foreignkey",
    "many_to_many",
    "OneToOneField",
    "date",
    "file",
    "image",
    "json",
    "color",
    "primarykey",
]
