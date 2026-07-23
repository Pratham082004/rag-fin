from app.schemas.parsed_filing import (
    FilingChunk,
    ParsedFiling,
)


class FilingChunker:

    def __init__(
        self,
        chunk_size: int = 1200,
        overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        filing: ParsedFiling,
    ) -> list[FilingChunk]:

        chunks = []

        chunk_id = 1

        for section in filing.sections:

            text = section.content

            start = 0

            while start < len(text):

                end = start + self.chunk_size

                chunk_text = text[start:end]

                chunks.append(
                    FilingChunk(
                        chunk_id=chunk_id,
                        section=section.title,
                        text=chunk_text,
                        token_count=len(chunk_text.split()),
                    )
                )

                chunk_id += 1

                start += (
                    self.chunk_size - self.overlap
                )

        return chunks