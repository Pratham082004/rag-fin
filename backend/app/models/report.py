from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id")
    )

    report_type: Mapped[str] = mapped_column(
        String(20)
    )

    fiscal_year: Mapped[int]

    fiscal_quarter: Mapped[int | None]

    report_date: Mapped[date]

    pdf_path: Mapped[str]

    company = relationship(
        "Company",
        back_populates="reports",
    )

    chunks = relationship(
        "Chunk",
        back_populates="report",
        cascade="all, delete-orphan",
    )