from datetime import datetime
from pydantic import Field, ConfigDict, UUID4
from .base_schema import BaseSchema, BaseModel

class UserProfileSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True, extra='allow')

    user_id: UUID4
    address: str | None = Field(str, max_length=255)
    phone_number: str | None = Field(str, max_length=255)
    birthdate: datetime | None

class UserProfileUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='allow')

    address: str | None = Field(str, max_length=255)
    phone_number: str | None = Field(str, max_length=255)
    birthdate: datetime | None
    user_id: UUID4 | None
    full_name: str | None = Field(str, max_length=100)
