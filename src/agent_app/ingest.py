import argparse
from pathlib import Path

from agent_app.rag import DEFAULT_INPUT_DIR, ingest_documents


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the local document vector index.")
    parser.add_argument(
        "--input-dir",
        default=str(DEFAULT_INPUT_DIR),
        help="Directory containing .txt, .md, or .markdown files.",
    )
    args = parser.parse_args()

    count = ingest_documents(Path(args.input_dir))
    print(f"Indexed {count} document chunks.")


if __name__ == "__main__":
    main()
