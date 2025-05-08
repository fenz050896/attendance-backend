from uuid import uuid4

from sqlalchemy import Uuid, LargeBinary, String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint

from database import BaseModel

class UserRegisteredFacesModel(BaseModel):
    __tablename__ = "user_registered_faces"

    Schema = None

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, index=True, default=uuid4)
    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(50), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    real_content: Mapped[bytes] = mapped_column(LargeBinary(2 ** 24), nullable=False)
    rgb_content: Mapped[bytes] = mapped_column(LargeBinary(2 ** 24), nullable=False)

    def url(self):
        return f'api/v1/user/register-faces/registered/{self.id}'
