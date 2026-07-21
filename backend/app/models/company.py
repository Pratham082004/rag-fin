from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    ticker: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    exchange: Mapped[str | None] = mapped_column(String(50))

    sector: Mapped[str | None] = mapped_column(String(100))

    industry: Mapped[str | None] = mapped_column(String(150))

    reports = relationship(
        "Report",
        back_populates="company",
        cascade="all, delete-orphan",
    )