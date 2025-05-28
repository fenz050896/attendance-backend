from pydantic import ConfigDict, UUID4
from .base_schema import BaseSchema

from datetime import date, time

class UserAttendanceSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True, extra='allow')

    id: int
    user_id: UUID4 | str
    day_date: str | date
    clock_in: str | time
    clock_out: str | time | None
    late_in: bool | int | None
    early_out: bool | int | None
