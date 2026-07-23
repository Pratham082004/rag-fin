from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.company import Company

class CompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, company_id: int) -> Optional[Company]:
        return self.db.get(Company, company_id)

    def get_by_ticker(self, ticker: str) -> Optional[Company]:
        stmt = select(Company).where(Company.ticker == ticker)
        return self.db.scalar(stmt)

    def get_by_name(self, name: str) -> Optional[Company]:
        stmt = select(Company).where(Company.name == name)
        return self.db.scalar(stmt)

    def create(
        self,
        *,
        ticker: str,
        name: str,
        exchange: str | None = None,
        sector: str | None = None,
        industry: str | None = None,
    ) -> Company:

        company = Company(
            ticker=ticker,
            name=name,
            exchange=exchange,
            sector=sector,
            industry=industry,
        )

        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)

        return company

    def list_all(self) -> list[Company]:
        stmt = select(Company).order_by(Company.name)
        return list(self.db.scalars(stmt).all())

    def delete(self, company: Company) -> None:
        self.db.delete(company)
        self.db.commit()