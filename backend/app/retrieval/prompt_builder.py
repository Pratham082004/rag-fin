from app.retrieval.models import RetrievalResult


class PromptBuilder:
    """
    Builds the prompt sent to the LLM.
    """

    SYSTEM_PROMPT = """
You are an expert financial analyst.

Answer ONLY using the supplied context.

Rules:
- If the answer is not contained in the context, say:
  "I couldn't find that information in the provided filing."
- Do not make up facts.
- Be concise and factual.
- Quote important numbers exactly when present.
"""

    def build(
        self,
        retrieval: RetrievalResult,
    ) -> str:

        context_parts = []

        for index, result in enumerate(
            retrieval.results,
            start=1,
        ):
            section = result.metadata.get(
                "section",
                "Unknown",
            )

            context_parts.append(
                f"""[Document {index}]
Section: {section}

{result.text}
"""
            )

        context = "\n\n".join(context_parts)

        prompt = f"""{self.SYSTEM_PROMPT}

Context
========
{context}

Question
========
{retrieval.question}

Answer
======
"""

        return prompt