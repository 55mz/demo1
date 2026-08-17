import hashlib
from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from agent_app.config import Settings, load_settings


SUPPORTED_EXTENSIONS = {".txt", ".md", ".markdown"}
DEFAULT_INPUT_DIR = Path("workspace/input")


@lru_cache(maxsize=4)
def build_embeddings(model_name: str):
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True},
    )


@lru_cache(maxsize=4)
def build_vector_store(
    persist_directory: str,
    collection_name: str,
    embedding_model: str,
) -> Chroma:
    return Chroma(
        collection_name=collection_name,
        embedding_function=build_embeddings(embedding_model),
        persist_directory=persist_directory,
    )


def load_documents(input_dir: Path = DEFAULT_INPUT_DIR) -> list[Document]:
    if not input_dir.exists():
        return []

    documents = []
    for path in sorted(input_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        text = path.read_text(encoding="utf-8")
        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": path.as_posix()},
                )
            )

    return documents


def split_documents(documents: list[Document], settings: Settings) -> list[Document]:
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.rag_chunk_size,
        chunk_overlap=settings.rag_chunk_overlap,
        add_start_index=True,
    )
    return splitter.split_documents(documents)


def document_id(document: Document, index: int) -> str:
    source = document.metadata.get("source", "unknown")
    digest = hashlib.sha256(document.page_content.encode("utf-8")).hexdigest()[:16]
    return f"{source}:{index}:{digest}"


def ingest_documents(
    input_dir: Path = DEFAULT_INPUT_DIR,
    settings: Settings | None = None,
) -> int:
    settings = settings or load_settings()
    chunks = split_documents(load_documents(input_dir), settings)
    if not chunks:
        return 0

    persist_directory = Path(settings.rag_persist_directory)
    persist_directory.mkdir(parents=True, exist_ok=True)
    vector_store = build_vector_store(
        str(persist_directory.resolve()),
        settings.rag_collection_name,
        settings.rag_embedding_model,
    )
    ids = [document_id(document, index) for index, document in enumerate(chunks)]
    vector_store.add_documents(chunks, ids=ids)
    return len(chunks)


def search_documents(
    query: str,
    settings: Settings | None = None,
    k: int | None = None,
) -> list[Document]:
    settings = settings or load_settings()
    vector_store = build_vector_store(
        str(Path(settings.rag_persist_directory).resolve()),
        settings.rag_collection_name,
        settings.rag_embedding_model,
    )
    return vector_store.similarity_search(query, k=k or settings.rag_top_k)
