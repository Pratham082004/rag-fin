from dataclasses import dataclass
import logging

import httpx

logger = logging.getLogger(__name__)

USER_AGENT = "FinRAG AI contact@example.com"


@dataclass(slots=True)
class FilingInfo:
    form: str
    filing_date: str
    accession_number: str
    primary_document: str


class SECFilingLookup:

    BASE_URL = "https://data.sec.gov/submissions"

    def __init__(self) -> None:

        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }

        self.timeout = 30

    async def latest_filing(
        self,
        cik: str,
        form_type: str = "10-K",
    ) -> FilingInfo | None:
        """
        Returns the latest filing of the requested form type.

        Example:
            await latest_filing("0000320193", "10-K")
        """

        url = f"{self.BASE_URL}/CIK{cik}.json"

        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=self.timeout,
        ) as client:

            response = await client.get(url)

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
            strict=False,
        ):

            if form != form_type:
                continue

            logger.info(
                "Found %s filing dated %s",
                form,
                date,
            )

            return FilingInfo(
                form=form,
                filing_date=date,
                accession_number=accession,
                primary_document=document,
            )

        logger.warning(
            "No %s filing found for CIK %s",
            form_type,
            cik,
        )

        return None