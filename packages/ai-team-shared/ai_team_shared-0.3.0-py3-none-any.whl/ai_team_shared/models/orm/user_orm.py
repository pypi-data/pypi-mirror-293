from sqlalchemy.orm import Mapped, mapped_column

from .base_orm import BaseOrmModel
from ..enums import UserRole


class UserOrm(BaseOrmModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(index=True)
    role: Mapped[UserRole]
