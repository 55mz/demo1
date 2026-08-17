from langchain_core.tools import tool

from agent_app.config import load_settings
from agent_app.rag import search_documents


@tool
def search_knowledge_base(query: str) -> str:
    """Search the local document knowledge base for relevant information."""
    query = query.strip()
    if not query:
        return "Search query is required."

    try:
        documents = search_documents(query, load_settings())
    except Exception as exc:
        return f"Knowledge base search failed: {exc}"

    if not documents:
        return "No relevant documents found. The knowledge base may be empty."

    results = []
    for index, document in enumerate(documents, start=1):
        results.append(
            f"[Result {index}]\n"
            f"source: {document.metadata.get('source', 'unknown')}\n"
            f"start_index: {document.metadata.get('start_index', 'unknown')}\n"
            f"content: {document.page_content}"
        )

    return "\n\n".join(results)
