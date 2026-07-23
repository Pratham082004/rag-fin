from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import httpx

from app.config import settings
from app.ingestion.company_lookup import CompanyInfo
from app.ingestion.filing_lookup import FilingInfo

logger = logging.getLogger(__name__)

USER_AGENT = "FinRAG AI (contact@example.com)"


class SECDownloader:
    """
    Downloads SEC filings and stores them locally.
    """

    BASE_ARCHIVE = "https://www.sec.gov/Archives/edgar/data"

    def __init__(self) -> None:

        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html",
        }

        self.timeout = 60

    async def download(
        self,
        company: CompanyInfo,
        filing: FilingInfo,
    ) -> Path:

        ticker = company.ticker
        cik = company.cik
        accession = filing.accession_number.replace("-", "")

        filing_url = (
            f"{self.BASE_ARCHIVE}/"
            f"{int(cik)}/"
            f"{accession}/"
            f"{filing.primary_document}"
        )

        save_dir = (
            Path(settings.REPORT_STORAGE)
            / ticker
            / filing.filing_date[:4]
            / filing.form
            / accession
        )

        save_dir.mkdir(parents=True, exist_ok=True)

        html_path = save_dir / "filing.html"
        metadata_path = save_dir / "metadata.json"

        if html_path.exists():

            logger.info(
                "Filing already downloaded: %s",
                html_path,
            )

            return html_path

        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=self.timeout,
            follow_redirects=True,
        ) as client:

            response = await client.get(filing_url)

        response.raise_for_status()

        html_path.write_text(
            response.text,
            encoding="utf-8",
        )

        metadata = {
            "company": company.name,
            "ticker": ticker,
            "cik": cik,
            "form": filing.form,
            "filing_date": filing.filing_date,
            "accession_number": filing.accession_number,
            "primary_document": filing.primary_document,
            "download_url": filing_url,
            "downloaded_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "status": "DOWNLOADED",
        }

        metadata_path.write_text(
            json.dumps(metadata, indent=4),
            encoding="utf-8",
        )

        logger.info(
            "Downloaded filing to %s",
            html_path,
        )

        return html_path