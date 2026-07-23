from dataclasses import dataclass

import httpx


SEC_COMPANY_TICKERS_URL = (
    "https://www.sec.gov/files/company_tickers.json"
)

USER_AGENT = (
    "FinRAG AI contact@example.com"
)


@dataclass
class CompanyInfo:
    cik: str
    ticker: str
    name: str


class SECCompanyLookup:

    def __init__(self):
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }

    def search(self, company_name: str) -> CompanyInfo | None:

        response = httpx.get(
            SEC_COMPANY_TICKERS_URL,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        companies = response.json()

        company_name = company_name.lower()

        for company in companies.values():

            if company_name in company["title"].lower():

                return CompanyInfo(
                    cik=str(company["cik_str"]).zfill(10),
                    ticker=company["ticker"],
                    name=company["title"],
                )

        return None