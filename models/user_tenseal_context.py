from sqlalchemy import Uuid, LargeBinary
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint

from database import BaseModel

class UserTensealContextModel(BaseModel):
    __tablename__ = "user_tenseal_context"
    __table_args__ = (UniqueConstraint("user_id"),)

    Schema = None

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))
    context: Mapped[bytes] = mapped_column(LargeBinary(2 ** 24), nullable=False)
