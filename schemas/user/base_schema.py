from datetime import datetime
from pydantic import BaseModel, field_serializer

class BaseSchema(BaseModel):
    created_at: datetime | None
    updated_at: datetime | None

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
