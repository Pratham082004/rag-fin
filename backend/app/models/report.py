from datetime import date, datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id")
    )

    report_type: Mapped[str] = mapped_column(String(20))

    fiscal_year: Mapped[int]

    fiscal_quarter: Mapped[int | None]

    filing_date: Mapped[date]

    report_date: Mapped[date]

    accession_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
    )

    filing_url: Mapped[str]

    local_path: Mapped[str | None]

    status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    company = relationship(
        "Company",
        back_populates="reports",
    )

    chunks = relationship(
        "Chunk",
        back_populates="report",
        cascade="all, delete-orphan",
    )