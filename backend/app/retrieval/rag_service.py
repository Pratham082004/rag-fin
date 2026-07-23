from app.retrieval.prompt_builder import PromptBuilder


class RAGService:

    def __init__(
        self,
        retrieval_service,
        llm_service,
    ):
        self.retrieval_service = retrieval_service
        self.prompt_builder = PromptBuilder()
        self.llm_service = llm_service

    async def ask(
        self,
        question: str,
        ticker: str,
        limit: int = 5,
    ):

        retrieval = await self.retrieval_service.search(
            question=question,
            ticker=ticker,
            limit=limit,
        )

        prompt = self.prompt_builder.build(
            retrieval,
        )

        answer = await self.llm_service.generate(
            prompt,
        )

        return {
            "question": question,
            "ticker": ticker,
            "answer": answer,
            "sources": [
                {
                    "section": result.metadata.get("section"),
                    "score": result.score,
                }
                for result in retrieval.results
            ],
        }