from pathlib import Path

from ..rag import session
from ..utils import config


def _count_json_files(directory: Path) -> int:
    if not directory.exists():
        return 0
    return len(list(directory.glob("*.json")))


def run() -> None:
    print("Inspecting the RAG-Anything index...")
    rag = session.get_session().get_rag()

    lr = getattr(rag, "lightrag", None)
    working_dir = Path(config.WORKING_DIR)
    output_dir = Path(config.OUTPUT_DIR)

    if not working_dir.exists():
        print("No storage directory found. The index is empty.")
        return

    print(f"\nWorking directory: {working_dir}")
    print(f"Output directory: {output_dir}")

    ns_counts = {}
    for ns_dir in working_dir.iterdir():
        if ns_dir.is_dir():
            count = _count_json_files(ns_dir)
            if count > 0:
                ns_counts[ns_dir.name] = count

    if ns_counts:
        print("\nStorage namespaces:")
        for name, count in sorted(ns_counts.items()):
            print(f"  {name}: {count} entries")
    else:
        print("\nNo storage namespaces found.")

    if output_dir.exists():
        md_files = list(output_dir.rglob("*.md"))
        if md_files:
            print(f"\nParsed documents: {len(md_files)}")
            for f in md_files[:10]:
                print(f"  {f.relative_to(output_dir)}")
            if len(md_files) > 10:
                print(f"  ... and {len(md_files) - 10} more")

    print(f"\nTotal storage size: {_dir_size(working_dir):.1f} MB")


def _dir_size(path: Path) -> float:
    total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return total / (1024 * 1024)
