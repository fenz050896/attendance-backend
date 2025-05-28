from sqlalchemy import String, Text
from sqlalchemy.orm import mapped_column, Mapped

from app.database import BaseModel
from app.schemas.app_config_schema import AppConfigSchema

class AppConfigModel(BaseModel):
    __tablename__ = "application_configurations"

    Schema = AppConfigSchema

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    field: Mapped[str] = mapped_column(String(255), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), default='single')
    value: Mapped[str] = mapped_column(Text, nullable=False)
