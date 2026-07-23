import logging

from app.schemas.parsed_filing import (
    FilingChunk,
    ParsedFiling,
)

logger = logging.getLogger(__name__)


class FilingChunker:
    """
    Splits filing sections into overlapping chunks suitable
    for embedding and vector search.
    """

    def __init__(
        self,
        chunk_size: int = 1200,
        overlap: int = 200,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if overlap < 0:
            raise ValueError("overlap cannot be negative.")

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        filing: ParsedFiling,
    ) -> list[FilingChunk]:
        """
        Split every filing section into overlapping chunks.

        Parameters
        ----------
        filing : ParsedFiling

        Returns
        -------
        list[FilingChunk]
        """

        chunks: list[FilingChunk] = []

        chunk_id = 1

        logger.info(
            "Chunking filing %s (%s)",
            filing.company,
            filing.ticker,
        )

        for section in filing.sections:

            text = section.content.strip()

            if not text:
                continue

            start = 0

            while start < len(text):

                end = start + self.chunk_size

                chunk_text = text[start:end].strip()

                if not chunk_text:
                    break

                chunks.append(
                    FilingChunk(
                        chunk_id=chunk_id,
                        section=section.title,
                        text=chunk_text,
                        token_count=len(
                            chunk_text.split()
                        ),
                    )
                )

                chunk_id += 1

                start += (
                    self.chunk_size - self.overlap
                )

        logger.info(
            "Generated %d chunks.",
            len(chunks),
        )

        return chunks