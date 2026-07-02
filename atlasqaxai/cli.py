import argparse
from streamlit.web import cli

from .commands import ingest, ask, wipe, rebuild, inspect, summary


def run_app(_) -> None:
    print("Access Web App through http://localhost:8501")
    cli.main_run(["atlasqaxai/ui/streamlit_app.py", "--server.port", "8501"])


def run_inspect(_) -> None:
    inspect.run()


def run_summary(_) -> None:
    summary.run()


def run_ingest(_) -> None:
    ingest.run()


def run_rebuild(_) -> None:
    rebuild.run()


def run_wipe(_) -> None:
    wipe.run()


def run_ask(args) -> None:
    if args.question:
        ask.run(" ".join(args.question), mode=args.mode)
        return

    print("Entering interactive mode (type 'exit' to quit)")
    while True:
        question = input("\n> ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if question:
            ask.run(question, mode=args.mode)


def build_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        prog="atlasqaxai",
        description="AtlasQAX.ai — Intelligent Question Answering with RAG-Anything",
    )

    sub = argument_parser.add_subparsers(dest="cmd")

    parser_app = sub.add_parser("app", help="Launch the Streamlit web UI")
    parser_app.set_defaults(func=run_app)

    parser_ingest = sub.add_parser("ingest", help="Ingest and index documents")
    parser_ingest.set_defaults(func=run_ingest)

    parser_rebuild = sub.add_parser(
        "rebuild", help="Wipe and re-ingest all documents"
    )
    parser_rebuild.set_defaults(func=run_rebuild)

    parser_wipe = sub.add_parser("wipe", help="Delete the entire index")
    parser_wipe.set_defaults(func=run_wipe)

    parser_inspect = sub.add_parser("inspect", help="Show index contents")
    parser_inspect.set_defaults(func=run_inspect)

    parser_summary = sub.add_parser("summary", help="Show index summary")
    parser_summary.set_defaults(func=run_summary)

    parser_ask = sub.add_parser("ask", help="Ask a question against the index")
    parser_ask.add_argument(
        "question", nargs="*", help="Question text (omit for interactive mode)"
    )
    parser_ask.add_argument(
        "--mode",
        choices=["hybrid", "local", "global", "naive", "mix"],
        default="hybrid",
        help="Retrieval mode (default: hybrid)",
    )
    parser_ask.set_defaults(func=run_ask)

    return argument_parser


def run():
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        args = parser.parse_args(["ask"])

    args.func(args)
