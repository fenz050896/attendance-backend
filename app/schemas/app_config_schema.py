from pydantic import ConfigDict, Field, UUID4
from .base_schema import BaseSchema

class AppConfigSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True, extra='allow')

    id: int
    field: str
    label: str
    type: str
    value: str
