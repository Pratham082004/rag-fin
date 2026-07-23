from datetime import datetime, timezone
from pathlib import Path
import json

import httpx

from app.config import settings
from app.ingestion.company_lookup import CompanyInfo
from app.ingestion.filing_lookup import FilingInfo

USER_AGENT = "FinRAG AI (your-email@example.com)"


class SECDownloader:
    """
    Downloads SEC filings and stores them locally.

    Storage Structure:

    storage/
    └── reports/
        └── AAPL/
            └── 2025/
                └── 10-K/
                    └── 000032019325000079/
                        ├── filing.html
                        └── metadata.json
    """

    BASE_ARCHIVE = "https://www.sec.gov/Archives/edgar/data"

    def __init__(self, client: httpx.Client | None = None):
        self.client = client or httpx.Client(
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html",
            },
            timeout=60,
            follow_redirects=True,
        )

    def __enter__(self):
        """Support: with SECDownloader() as downloader:"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the underlying HTTP client."""
        self.client.close()

    def download(
        self,
        company: CompanyInfo,
        filing: FilingInfo,
    ) -> Path:
        """
        Download a SEC filing and save it locally.

        Parameters
        ----------
        company : CompanyInfo
            Company metadata.

        filing : FilingInfo
            Filing metadata returned from SEC.

        Returns
        -------
        Path
            Local path to the downloaded HTML filing.
        """

        ticker = company.ticker
        company_name = company.name
        cik = company.cik

        cik_folder = str(int(cik))
        accession = filing.accession_number.replace("-", "")

        filing_url = (
            f"{self.BASE_ARCHIVE}/"
            f"{cik_folder}/"
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

        # Skip download if already present
        if html_path.exists():
            print(f"✓ Filing already exists: {html_path}")
            return html_path

        response = self.client.get(filing_url)
        response.raise_for_status()

        html_path.write_text(
            response.text,
            encoding="utf-8",
        )

        metadata = {
            "company": company_name,
            "ticker": ticker,
            "cik": cik,
            "form": filing.form,
            "filing_date": filing.filing_date,
            "accession_number": filing.accession_number,
            "primary_document": filing.primary_document,
            "download_url": filing_url,
            "downloaded_at": datetime.now(timezone.utc).isoformat(),
            "status": "DOWNLOADED",
        }

        metadata_path.write_text(
            json.dumps(metadata, indent=4),
            encoding="utf-8",
        )

        print(f"✓ Downloaded: {html_path}")

        return html_path