from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from an LLM.
        """
        raise NotImplementedError