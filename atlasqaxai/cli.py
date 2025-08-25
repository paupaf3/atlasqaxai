import argparse

from .commands import ingest, ask, wipe, rebuild, inspect


def run_inspect(_) -> None:
    inspect.run()


def run_ingest(_) -> None:
    ingest.run()


def run_rebuild(_) -> None:
    rebuild.run()


def run_wipe(_) -> None:
    wipe.run()


def run_ask(args) -> None:
    # If a question is provided, answer once; otherwise enter an interactive loop
    if args.question:
        ask.run(" ".join(args.question))
        return

    print("Entering interactive mode (type 'exit' to quit)")

    while True:
        question = input("\n> ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if question:
            ask.run(question)


def build_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        prog="atlasqaxai", description="AtlasQAX.ai is an intelligent Question Answering system that delivers accurate answers from multiple data sources.")

    sub = argument_parser.add_subparsers(dest="cmd")

    parser_ingest = sub.add_parser(
        "ingest", help="Index new/changed documents")
    parser_ingest.set_defaults(func=run_ingest)

    parser_rebuild = sub.add_parser(
        "rebuild", help="Rebuild the entire index from scratch")
    parser_rebuild.set_defaults(func=run_rebuild)

    parser_wipe = sub.add_parser("wipe", help="Delete index")
    parser_wipe.set_defaults(func=run_wipe)

    parser_inspect = sub.add_parser("inspect", help="Inspect the index")
    parser_inspect.set_defaults(func=run_inspect)

    parser_ask = sub.add_parser("ask", help="Ask a question")
    parser_ask.add_argument("question", nargs="*",
                            help="Your question text (omit for interactive mode)")
    parser_ask.set_defaults(func=run_ask)

    return argument_parser


def run():
    parser = build_parser()
    args = parser.parse_args()

    # Default to interactive 'ask' if no subcommand provided
    if not hasattr(args, "func"):
        args = parser.parse_args(["ask"])

    args.func(args)
