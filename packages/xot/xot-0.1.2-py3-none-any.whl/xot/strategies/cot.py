from .base_strategy import BaseThoughtStrategy
from ..models.model_interface import ModelInterface
from typing import List
from ..tools.base_tool import BaseTool


class ChainOfThought(BaseThoughtStrategy):
    """
    Chain of Thought (CoT) synthetic data type.
    """

    def __init__(self, model: ModelInterface, tools: List[BaseTool] = None):
        super().__init__(model, tools)

    def generate(self, question: str, solution: str, temperature: float = 0.7) -> str:
        prompt = f"""
        Question: {question}
        
        Please provide a step-by-step solution to this question, explaining your thought process along the way.
        
        Solution:
        """
        return self.model.generate(prompt, temperature)

    def validate(
        self, generated: str, solution: str, judge_model: ModelInterface = None
    ) -> bool:
        if judge_model:
            prompt = f"""
            Question: {generated}
            
            Generated Solution:
            {generated}
            
            Expected Solution:
            {solution}
            
            Is the generated solution correct and adequately explains the thought process? Answer with Yes or No.
            """
            response = judge_model.generate(prompt, temperature=0.2).strip().lower()
            return response == "yes"
        else:
            return generated.strip() == solution.strip()
