from langchain_openai import ChatOpenAI

from agent_app.config import Settings


def build_llm(settings: Settings) -> ChatOpenAI:
    if not settings.deepseek_api_key:
        raise ValueError("DEEPSEEK_API_KEY is required. Copy .env.example to .env and fill it in.")

    return ChatOpenAI(
        api_key=settings.deepseek_api_key,
        base_url="https://api.deepseek.com",
        model=settings.deepseek_model,
        temperature=settings.deepseek_temperature,
    )
