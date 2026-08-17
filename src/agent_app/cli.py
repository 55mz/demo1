import argparse

from agent_app.agent import run_agent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the LangChain agent.")
    parser.add_argument("message", nargs="*", help="Message to send to the agent.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.message:
        print(run_agent(" ".join(args.message)))
        return

    print("LangChain Agent is ready. Type 'exit' or 'quit' to stop.")
    while True:
        message = input("> ").strip()
        if message.lower() in {"exit", "quit"}:
            break
        if not message:
            continue
        print(run_agent(message))


if __name__ == "__main__":
    main()
