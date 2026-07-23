from app.repositories.company_repo import CompanyRepository


class CompanyService:

    def __init__(self, company_repo: CompanyRepository):
        self.company_repo = company_repo

    def get_company(self, ticker: str):
        return self.company_repo.get_by_ticker(ticker)

    def create_company(
        self,
        ticker: str,
        name: str,
        exchange: str | None = None,
        sector: str | None = None,
        industry: str | None = None,
    ):
        return self.company_repo.create(
            ticker=ticker,
            name=name,
            exchange=exchange,
            sector=sector,
            industry=industry,
        )

    def get_or_create_company(
        self,
        ticker: str,
        name: str,
        exchange: str | None = None,
        sector: str | None = None,
        industry: str | None = None,
    ):

        company = self.company_repo.get_by_ticker(ticker)

        if company:
            return company

        return self.company_repo.create(
            ticker=ticker,
            name=name,
            exchange=exchange,
            sector=sector,
            industry=industry,
        )