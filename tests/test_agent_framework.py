from agent_app.config import Settings
from agent_app.prompts import build_prompt
from agent_app.rag_tools import search_knowledge_base
from agent_app.tools import build_tools, calculator


def test_settings_defaults_are_available():
    settings = Settings()

    assert settings.deepseek_model == "deepseek-chat"
    assert settings.deepseek_temperature == 0
    assert settings.rag_top_k == 4


def test_prompt_contains_required_variables():
    prompt = build_prompt()

    assert {"input", "agent_scratchpad"} <= set(prompt.input_variables)


def test_tools_are_registered():
    tools = build_tools()

    assert {tool.name for tool in tools} == {
        "calculator",
        "current_time",
        "search_knowledge_base",
    }


def test_calculator_handles_basic_math():
    assert calculator.invoke({"expression": "2 + 3 * 4"}) == "14"


def test_search_tool_rejects_empty_query():
    assert search_knowledge_base.invoke({"query": " "}) == "Search query is required."
