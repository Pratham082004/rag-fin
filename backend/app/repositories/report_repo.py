from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.report import Report

class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, report_id: int):
        return self.db.get(Report, report_id)

    def get_latest_report(self, company_id: int):
        stmt = (
            select(Report)
            .where(Report.company_id == company_id)
            .order_by(
                Report.fiscal_year.desc(),
                Report.report_date.desc(),
            )
        )

        return self.db.scalar(stmt)

    def create(self, report: Report):
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def list_company_reports(self, company_id: int):
        stmt = (
            select(Report)
            .where(Report.company_id == company_id)
            .order_by(Report.report_date.desc())
        )

        return list(self.db.scalars(stmt).all())