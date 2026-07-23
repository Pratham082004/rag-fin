from functools import lru_cache

from app.ingestion.company_lookup import SECCompanyLookup
from app.ingestion.downloader import SECDownloader
from app.ingestion.filing_lookup import SECFilingLookup
from app.ingestion.parser import FilingParser
from app.ingestion.chunker import FilingChunker
from app.ingestion.pipeline import IngestionPipeline

from app.retrieval.search import RetrievalService
from app.retrieval.rag_service import RAGService

from app.services.embeddings.gemini import GeminiEmbeddingProvider
from app.services.llm.gemini import GeminiLLMProvider
from app.services.vector_store.chroma import ChromaService
from app.services.company_resolver import CompanyResolver
from app.services.company_cache import CompanyCache


@lru_cache
def get_embedding_service():
    return GeminiEmbeddingProvider()


@lru_cache
def get_llm_service():
    return GeminiLLMProvider()


@lru_cache
def get_vector_store():
    return ChromaService()


@lru_cache
def get_retrieval_service():
    return RetrievalService(
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )


@lru_cache
def get_rag_service():
    return RAGService(
        retrieval_service=get_retrieval_service(),
        llm_service=get_llm_service(),
        company_resolver=get_company_resolver()
    )


@lru_cache
def get_pipeline():
    return IngestionPipeline(
        company_lookup=SECCompanyLookup(),
        filing_lookup=SECFilingLookup(),
        downloader=SECDownloader(),
        parser=FilingParser(),
        chunker=FilingChunker(),
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )

@lru_cache
def get_company_cache():

    return CompanyCache()


@lru_cache
def get_company_resolver():

    return CompanyResolver(
        cache=get_company_cache()
    )