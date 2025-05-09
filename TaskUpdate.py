from pydantic import BaseModel
from typing import Optional

from sqlmodel import SQLModel, Field
from typing import Optional

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None
