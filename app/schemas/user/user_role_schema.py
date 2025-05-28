from pydantic import ConfigDict

from app.schemas.base_schema import BaseSchema

class UserRoleSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True, extra='allow')

    id: int
    role_id: int
    role_name: str
