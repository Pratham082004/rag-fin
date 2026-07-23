class IngestionError(Exception):
    """Base ingestion exception."""


class CompanyNotFoundError(IngestionError):
    """Company could not be found."""


class FilingNotFoundError(IngestionError):
    """Requested SEC filing could not be found."""


class DownloadError(IngestionError):
    """Failed to download filing."""


class EmbeddingError(IngestionError):
    """Failed to generate embeddings."""