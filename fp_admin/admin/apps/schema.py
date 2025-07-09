from typing import List

from pydantic import BaseModel


class ModelInfo(BaseModel):
    name: str
    label: str
    url: str


class AppInfo(BaseModel):
    name: str
    label: str
    models: List[ModelInfo]
