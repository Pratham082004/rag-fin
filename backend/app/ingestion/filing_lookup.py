from dataclasses import dataclass

import httpx

USER_AGENT = "FinRAG AI contact@example.com"


@dataclass
class FilingInfo:
    form: str
    filing_date: str
    accession_number: str
    primary_document: str


class SECFilingLookup:

    BASE_URL = "https://data.sec.gov/submissions"

    def __init__(self):
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }

    def latest_filing(
        self,
        cik: str,
        form_type: str = "10-K",
    ) -> FilingInfo | None:

        url = f"{self.BASE_URL}/CIK{cik}.json"

        response = httpx.get(
            url,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        recent = data["filings"]["recent"]

        forms = recent["form"]
        dates = recent["filingDate"]
        accessions = recent["accessionNumber"]
        documents = recent["primaryDocument"]

        for form, date, accession, document in zip(
            forms,
            dates,
            accessions,
            documents,
        ):
            if form == form_type:
                return FilingInfo(
                    form=form,
                    filing_date=date,
                    accession_number=accession,
                    primary_document=document,
                )

        return None