from datetime import datetime, timezone
from sqlalchemy import Text, Integer, DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Layout(Base):

    __tablename__ = "layouts"
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        index=True
    )
    name: Mapped[str] = mapped_column(
      String(100),
      nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(200),
        nullable=True
    )
    zpl_template: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )