from langchain.agents import create_agent

from agent_app.config import Settings, load_settings
from agent_app.llm import build_llm
from agent_app.prompts import SYSTEM_PROMPT
from agent_app.tools import build_tools


def _create_agent(settings: Settings):
    llm = build_llm(settings)
    tools = build_tools()

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )


_cached_agent = None


def build_agent(settings: Settings | None = None):
    global _cached_agent

    settings = settings or load_settings()
    if _cached_agent is None:
        _cached_agent = _create_agent(settings)

    return _cached_agent


def run_agent(message: str, settings: Settings | None = None) -> str:
    agent = build_agent(settings)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]}
    )
    messages = result.get("messages", [])
    if not messages:
        return "Agent returned no messages."

    content = messages[-1].content
    if isinstance(content, str):
        return content
    return str(content)
