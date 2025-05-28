from datetime import date, time, datetime, UTC

from sqlalchemy import ForeignKey
from sqlalchemy import Uuid, Time, Date, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from app.database import BaseModel
from app.schemas.user_attendance_schema import UserAttendanceSchema


class UserAttendanceModel(BaseModel):
    __tablename__ = "user_attendances"

    Schema = UserAttendanceSchema

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))
    day_date: Mapped[date] = mapped_column(Date, default=date.today)
    clock_in: Mapped[time] = mapped_column(Time, default=lambda: datetime.now(UTC).time().replace(tzinfo=None))
    clock_out: Mapped[time] = mapped_column(Time, nullable=True)
    late_in: Mapped[bool] = mapped_column(Boolean, nullable=True)
    early_out: Mapped[bool] = mapped_column(Boolean, nullable=True)
