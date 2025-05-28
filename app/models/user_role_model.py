from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.database import BaseModel

class UserRoleModel(BaseModel):
    __tablename__ = "user_roles"

    Schema = None

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    role_id: Mapped[int] = mapped_column(nullable=False)
    role_name: Mapped[str] = mapped_column(String(100), index=True)
