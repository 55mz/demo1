from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


SYSTEM_PROMPT = """You are a practical AI agent.

Follow the user's request carefully. Use tools when they make the answer more accurate.
If a tool returns insufficient information, explain what is missing and provide the best next step.
Keep answers concise unless the user asks for detail.

For questions about local documents, use search_knowledge_base before answering.
Base document-related claims on retrieved content and mention the source when possible.
"""


def build_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
