"""Montagem de prompts para perguntas matemáticas."""


class MathPromptBuilder:
    """Constrói prompts para resolver perguntas matemáticas."""

    def build_system_prompt(self) -> str:
        """Cria o prompt de sistema."""
        return (
            "Você é um assistente matemático. "
            "Responda apenas perguntas matemáticas. "
            "Explique de forma curta e objetiva. "
            "Quando possível, retorne o resultado numérico final."
        )

    def build_user_prompt(self, question: str) -> str:
        """Cria o prompt de usuário."""
        return f"Resolva a seguinte pergunta matemática de forma objetiva:\n\n{question}"
