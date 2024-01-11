from pydantic import BaseModel
from datetime import datetime


class AIModel(BaseModel):
    id: int
    name: str
    description: str
    model_file_path: str
    model_type: str
    model_version: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True