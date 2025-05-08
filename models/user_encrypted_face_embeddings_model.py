from uuid import uuid4

from sqlalchemy import Uuid, LargeBinary, String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint

from database import BaseModel

class UserEncryptedFaceEmbeddingModel(BaseModel):
    __tablename__ = "user_encrypted_face_embeddings"
    __table_args__ = (UniqueConstraint("source_file_id"),)

    Schema = None

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, index=True, default=uuid4)
    user_id: Mapped[str] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))
    source_file_id: Mapped[str] = mapped_column(Uuid, ForeignKey("user_registered_faces.id", ondelete="CASCADE"))
    embedding: Mapped[bytes] = mapped_column(LargeBinary(2 ** 20), nullable=False)
    detection_score: Mapped[float]
