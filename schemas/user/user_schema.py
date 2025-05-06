from pydantic import ConfigDict, Field, UUID4
from .base_schema import BaseSchema
from .user_profile_schema import UserProfileSchema

class UserSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True, extra='allow')

    id: UUID4
    email: str = Field(str, max_length=100)
    full_name: str = Field(str, max_length=100)
    profile: UserProfileSchema | None
