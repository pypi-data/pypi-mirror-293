from abc import ABC, abstractmethod


class ModelInterface(ABC):
    """
    Abstract base class for model interfaces.
    """

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate a response based on the given prompt.

        Args:
            prompt (str): Input prompt for the model.
            temperature (float): Sampling temperature. Defaults to 0.7.

        Returns:
            str: Generated response.
        """
        pass


class OpenAIModel(ModelInterface):
    """
    Interface for OpenAI models.
    """

    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        import openai

        openai.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        import openai

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content


# Add more model interfaces as needed (e.g., HuggingFaceModel, AnthropicModel)
