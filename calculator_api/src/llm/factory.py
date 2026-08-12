"""Factory da camada LLM."""

from dotenv import load_dotenv

from calculator_api.src.llm.clients import create_default_math_llm_client
from calculator_api.src.llm.service import MathQuestionService

load_dotenv()


def create_math_question_service() -> MathQuestionService:
    """Cria o serviço padrão de perguntas matemáticas."""
    llm_client = create_default_math_llm_client()

    return MathQuestionService(llm_client=llm_client)
