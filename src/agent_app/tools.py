from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.tools import tool

from agent_app.rag_tools import search_knowledge_base


@tool
def calculator(expression: str) -> str:
    """Evaluate a simple arithmetic expression, such as '2 + 2 * 5'."""
    allowed_chars = set("0123456789+-*/(). %")
    if not expression or any(char not in allowed_chars for char in expression):
        return "Only arithmetic characters are allowed."

    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Could not calculate expression: {exc}"


@tool
def current_time(timezone: str = "Asia/Shanghai") -> str:
    """Return the current time for an IANA timezone, such as 'Asia/Shanghai'."""
    try:
        tz = ZoneInfo(timezone)
    except Exception:
        return f"Unknown timezone: {timezone}"

    return datetime.now(tz).isoformat(timespec="seconds")


def build_tools():
    return [calculator, current_time, search_knowledge_base]
