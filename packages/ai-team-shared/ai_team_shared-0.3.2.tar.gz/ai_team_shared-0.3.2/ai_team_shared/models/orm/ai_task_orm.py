from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_orm import BaseOrm
from ..enums import ModelNameLLM, AiTaskStatus


class AiTaskOrm(BaseOrm):
    __tablename__ = "ai_tasks"

    llm_model_name: Mapped[ModelNameLLM]
    prompt_text: Mapped[str]
    status: Mapped[AiTaskStatus]
    user_prompt_id: Mapped[int] = mapped_column(ForeignKey("user_prompts.id"))
    scoped_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("scoped_tasks.id"))
    # context: Mapped[Optional["TaskContext"]] = relationship(back_populates="ai_task")
    # messages: Mapped[list["TaskMessage"]] = relationship(back_populates="ai_task")


# AiCompletion is not persisted until the use case is clear and AiTask table isn't enough
