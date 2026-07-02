from pathlib import Path

from ..rag import session
from ..utils import config


def get_summary() -> str:
    try:
        rag = session.get_session().get_rag()
        working_dir = Path(config.WORKING_DIR)
        output_dir = Path(config.OUTPUT_DIR)

        if not working_dir.exists():
            return (
                "No index found. Please ingest documents first.\n"
                "Run: python -m atlasqaxai ingest"
            )

        ns_counts = {}
        for ns_dir in working_dir.iterdir():
            if ns_dir.is_dir():
                count = len(list(ns_dir.glob("*.json")))
                if count > 0:
                    ns_counts[ns_dir.name] = count

        total_chunks = ns_counts.get("text_chunks", 0)
        total_docs = ns_counts.get("full_docs", 0)
        total_entities = ns_counts.get("full_entities", 0)
        total_relations = ns_counts.get("full_relations", 0)

        output_count = 0
        if output_dir.exists():
            output_count = len(list(output_dir.rglob("*.md")))

        lines = [
            f"**Index Summary** — {total_docs} documents, {total_chunks} chunks",
            "",
        ]
        if total_entities > 0:
            lines.append(f"• Entities: {total_entities}")
        if total_relations > 0:
            lines.append(f"• Relations: {total_relations}")
        if output_count > 0:
            lines.append(f"• Parsed files: {output_count}")
        lines.extend(
            [
                "",
                "Ask me anything about these documents!",
            ]
        )
        return "\n".join(lines)

    except Exception as e:
        return (
            f"Could not load index summary: {e}\n\n"
            "Please make sure documents are ingested and Ollama is running."
        )


def run() -> None:
    print(get_summary())
