from datetime import datetime

from sqlalchemy import DateTime, Text

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_query: Mapped[str] = mapped_column(Text)

    response: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime
    )