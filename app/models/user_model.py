from uuid import uuid4
from typing import Optional

from sqlalchemy import Uuid, String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped
from pydantic import ValidationError, BaseModel as PydanticBaseModel

from app.database import BaseModel
from app.schemas.user import LoginSchema, RegisterSchema, UserSchema

class UserModel(BaseModel):
    __tablename__ = "users"
    Schema = UserSchema

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, index=True, default=uuid4)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user_roles.id"), nullable=True)
    profile: Mapped["UserProfileModel"] = relationship(back_populates="user", cascade="all, delete-orphan")
    role: Mapped[Optional["UserRoleModel"]] = relationship()

    @classmethod
    def validate(cls, data: dict, schema: str) -> PydanticBaseModel | tuple[list|str, int]:
        try:
            if schema == "register":
                return RegisterSchema(**data)
            elif schema == "login":
                return LoginSchema(**data)
            else:
                return (f"Schema not exists: {str(e)}", 400)
        except ValidationError as e:
            errors = []
            for error in e.errors():
                field_names = ', '.join(error["loc"])
                message = error["msg"]
                errors.append(f"{field_names}: {message}")

            return (errors, 422)
