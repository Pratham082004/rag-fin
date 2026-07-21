from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)

    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id")
    )

    page_number: Mapped[int]

    chunk_index: Mapped[int]

    section: Mapped[str | None]

    text: Mapped[str] = mapped_column(Text)

    report = relationship(
        "Report",
        back_populates="chunks",
    )