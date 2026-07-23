import logging

from app.ingestion.models import IngestionResult

logger = logging.getLogger(__name__)


class IngestionPipeline:

    def __init__(
        self,
        company_lookup,
        filing_lookup,
        downloader,
        parser,
        chunker,
        embedding_service,
        vector_store,
    ):
        self.company_lookup = company_lookup
        self.filing_lookup = filing_lookup
        self.downloader = downloader
        self.parser = parser
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    async def ingest(
        self,
        ticker: str,
        filing_type: str = "10-K",
    ) -> IngestionResult:

        logger.info(
            "Starting ingestion for %s (%s)",
            ticker,
            filing_type,
        )

        # --------------------------------------------------
        # Company Lookup
        # --------------------------------------------------

        company = await self.company_lookup.search(
            ticker
        )

        if company is None:
            raise ValueError(
                f"Company '{ticker}' not found."
            )

        logger.info(
            "Found company %s (%s)",
            company.name,
            company.ticker,
        )

        # --------------------------------------------------
        # Filing Lookup
        # --------------------------------------------------

        filing = await self.filing_lookup.latest_filing(
            cik=company.cik,
            form_type=filing_type,
        )

        if filing is None:
            raise ValueError(
                f"No {filing_type} filing found for {ticker}."
            )

        logger.info(
            "Found filing %s",
            filing.accession_number,
        )

        # --------------------------------------------------
        # Download Filing
        # --------------------------------------------------

        html_path = await self.downloader.download(
            company,
            filing,
        )

        logger.info(
            "Downloaded filing to %s",
            html_path,
        )

        # --------------------------------------------------
        # Parse Filing
        # --------------------------------------------------

        parsed_filing = self.parser.parse(
            html_path
        )

        logger.info(
            "Extracted %d sections",
            len(parsed_filing.sections),
        )

        # --------------------------------------------------
        # Chunk Filing
        # --------------------------------------------------

        chunks = self.chunker.chunk(
            parsed_filing
        )

        logger.info(
            "Generated %d chunks",
            len(chunks),
        )

        # --------------------------------------------------
        # Generate Embeddings
        # --------------------------------------------------

        vectors = await self.embedding_service.embed_batch(
            [
                chunk.text
                for chunk in chunks
            ]
        )

        logger.info(
            "Generated %d embeddings",
            len(vectors),
        )

        # --------------------------------------------------
        # Build Payloads
        # --------------------------------------------------

        payloads = []

        for chunk in chunks:

            payloads.append(
                {
                    "ticker": company.ticker,
                    "company": company.name,
                    "cik": company.cik,
                    "filing_type": filing.form,
                    "filing_date": filing.filing_date,
                    "accession_number": filing.accession_number,
                    "section": chunk.section,
                    "chunk_id": chunk.chunk_id,
                    "token_count": chunk.token_count,
                    "text": chunk.text,
                }
            )

        # --------------------------------------------------
        # Store in ChromaDB
        # --------------------------------------------------

        await self.vector_store.upsert(
            vectors=vectors,
            payloads=payloads,
        )

        logger.info(
            "Stored %d vectors in ChromaDB",
            len(vectors),
        )

        # --------------------------------------------------
        # Return Result
        # --------------------------------------------------

        return IngestionResult(
            company=company.name,
            ticker=company.ticker,
            filing_type=filing.form,
            filing_date=filing.filing_date,
            sections=len(parsed_filing.sections),
            chunks=len(chunks),
            vectors=len(vectors),
            status="SUCCESS",
            message="Financial filing ingested successfully.",
        )