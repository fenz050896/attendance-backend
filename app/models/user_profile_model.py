from datetime import date
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String, Uuid
from sqlalchemy.orm import mapped_column, relationship, Mapped
from pydantic import ValidationError, BaseModel as PydanticBaseModel

from app.database import BaseModel
from app.schemas.user import UserProfileUpdateSchema, UserProfileSchema


class UserProfileModel(BaseModel):
    __tablename__ = "user_profiles"
    __table_args__ = (UniqueConstraint("user_id"),)

    Schema = UserProfileSchema

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)
    birthdate: Mapped[date] = mapped_column(nullable=True)
    user: Mapped["UserModel"] = relationship(back_populates="profile", single_parent=True)

    @classmethod
    def validate(cls, data: dict, schema: str) -> PydanticBaseModel | tuple[list|str, int]:
        try:
            if schema == "update":
                return UserProfileUpdateSchema(**data)
            else:
                return (f"Schema not exists: {str(e)}", 400)
        except ValidationError as e:
            errors = []
            for error in e.errors():
                field_names = ', '.join(error["loc"])
                message = error["msg"]
                errors.append(f"{field_names}: {message}")

            return (errors, 422)
