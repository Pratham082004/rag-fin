from dataclasses import dataclass, field


@dataclass
class FilingSection:
    title: str
    content: str


@dataclass
class FilingChunk:
    chunk_id: int
    section: str
    text: str
    token_count: int


@dataclass
class ParsedFiling:
    company: str
    ticker: str
    filing_type: str
    filing_date: str
    title: str
    raw_text: str

    sections: list[FilingSection] = field(default_factory=list)