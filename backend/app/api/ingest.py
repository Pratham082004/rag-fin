from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_pipeline
from app.ingestion.pipeline import IngestionPipeline
from app.schemas.ingest import (
    IngestRequest,
    IngestResponse,
)

router = APIRouter()


@router.post(
    "/",
    response_model=IngestResponse,
)
async def ingest_filing(
    request: IngestRequest,
    pipeline: IngestionPipeline = Depends(get_pipeline),
):

    try:

        result = await pipeline.ingest(
            ticker=request.ticker,
            filing_type=request.filing_type,
        )

        return IngestResponse(
            company=result.company,
            ticker=result.ticker,
            filing_type=result.filing_type,
            sections=result.sections,
            chunks=result.chunks,
            vectors=result.vectors,
            status=result.status,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )