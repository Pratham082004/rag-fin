from dataclasses import dataclass


@dataclass
class IngestionResult:
    company: str
    ticker: str
    filing_type: str
    filing_date: str

    sections: int
    chunks: int
    vectors: int

    status: str
    message: str