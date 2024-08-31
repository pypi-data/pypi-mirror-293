from enum import Enum
from typing import Optional

from sqlmodel import Field

from .base_models import BaseSQLModel
from .shared_enums import TaskType


class StatusType(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    # ERROR = "ERROR"


class AssigneeType(str, Enum):
    CODER = "CODER"
    CTO = "CTO"
    CEO = "CEO"
    COO = "COO"


class NecessityType(str, Enum):
    """Must/Should/Could/Won't Have"""

    MUST = "MUST"
    SHOULD = "SHOULD"
    COULD = "COULD"
    WONT = "WONT"


class PriorityType(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class BaseProjectModel(BaseSQLModel):
    description: str
    status: StatusType
    name: str

    # Support these fields in the future
    # estimated_duration: Optional[str]
    # deadline: Optional[datetime]


class Project(BaseProjectModel, table=True):
    pass


class Objective(BaseProjectModel, table=True):
    project_id: int = Field(foreign_key="project.id")


class KeyResult(BaseProjectModel, table=True):
    objective_id: int = Field(foreign_key="objective.id")


class Requirement(BaseProjectModel, table=True):
    key_result_id: int = Field(foreign_key="keyresult.id")
    necessity: NecessityType


class ScopedTask(BaseProjectModel, table=True):
    requirement_id: int = Field(foreign_key="requirement.id")
    assignee: Optional[AssigneeType] = None
    priority: Optional[PriorityType] = None
    task_type: Optional[TaskType] = TaskType.UNDEFINED

    # Additional fields to provide more information
    # estimated_duration: Optional[str]
    # difficulty: Optional[str]

    # This can be used to link the task to Gitlab MR
    # merge_request_id: Optional[str] = None


class ScopedTaskStep(BaseSQLModel, table=True):
    task_id: int = Field(foreign_key="scopedtask.id")
    action: str
    status: StatusType
    expected_result: Optional[str] = None
    # consider adding execution_log here
