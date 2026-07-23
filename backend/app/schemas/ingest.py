from pydantic import BaseModel


class IngestRequest(BaseModel):

    ticker: str
    filing_type: str = "10-K"


class IngestResponse(BaseModel):

    company: str
    ticker: str
    filing_type: str

    sections: int
    chunks: int
    vectors: int

    status: str