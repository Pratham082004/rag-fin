from app.retrieval.prompt_builder import PromptBuilder


class RAGService:

    def __init__(
        self,
        retrieval_service,
        llm_service,
        company_resolver,
    ):
        self.retrieval_service = retrieval_service
        self.prompt_builder = PromptBuilder()
        self.llm_service = llm_service
        self.company_resolver = company_resolver

    async def ask(
        self,
        question: str,
        limit: int = 5,
    ):
        # Resolve the company mentioned in the user's question
        company = await self.company_resolver.resolve(question)

        print("=" * 60)
        print("Detected company:", company)
        print("=" * 60)

        if company is None:
            raise ValueError(
                "Could not identify a company from the question."
            )

        ticker = company["ticker"]

        # Retrieve relevant chunks
        retrieval = await self.retrieval_service.search(
            question=question,
            ticker=ticker,
            limit=limit,
        )

        # Build the RAG prompt
        prompt = self.prompt_builder.build(retrieval)

        # Generate answer
        answer = await self.llm_service.generate(prompt)

        # Return response
        return {
            "company": company["company"],
            "ticker": ticker,
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "section": result.metadata.get("section"),
                    "score": result.score,
                }
                for result in retrieval.results
            ],
        }