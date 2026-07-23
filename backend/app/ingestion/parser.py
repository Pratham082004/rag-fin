from pathlib import Path
import json

from bs4 import BeautifulSoup

from app.ingestion.extractor import SectionExtractor
from app.schemas.parsed_filing import ParsedFiling


class FilingParser:
    """
    Converts a SEC filing HTML into a structured ParsedFiling object.
    """

    def __init__(self):
        self.section_extractor = SectionExtractor()

    def parse(self, html_path: Path) -> ParsedFiling:
        """
        Parse a downloaded SEC filing.

        Parameters
        ----------
        html_path : Path
            Path to filing.html

        Returns
        -------
        ParsedFiling
        """

        metadata_path = html_path.parent / "metadata.json"

        metadata = json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )

        html = html_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        # Remove unwanted tags
        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "svg",
                "img",
            ]
        ):
            tag.decompose()

        text = soup.get_text(separator="\n")

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:
                lines.append(line)

        clean_text = "\n".join(lines)

        sections = self.section_extractor.extract(
            clean_text
        )

        return ParsedFiling(
            company=metadata["company"],
            ticker=metadata["ticker"],
            filing_type=metadata["form"],
            filing_date=metadata["filing_date"],
            title=f'{metadata["company"]} {metadata["form"]}',
            raw_text=clean_text,
            sections=sections,
        )