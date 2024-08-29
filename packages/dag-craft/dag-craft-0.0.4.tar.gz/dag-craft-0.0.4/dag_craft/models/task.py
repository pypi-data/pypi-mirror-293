from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from airflow.models.baseoperator import BaseOperator, BaseOperatorMeta


class TaskType(str, Enum):
    script = "script"
    python = "python"
    dummy = "dummy"


class TaskModel(BaseModel):
    task_id: str
    task_group: Optional[str] = None
    dependencies: List[str] = []
    operator: BaseOperator | BaseOperatorMeta
    operator_args: dict = {}

    class Config:
        arbitrary_types_allowed = True
