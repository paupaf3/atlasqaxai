import asyncio
from pathlib import Path

from ..rag import session
from ..utils import paths


def _read_lines(file_path: Path) -> list[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except Exception as e:
        print(f"[ingest] Error reading {file_path.name}: {e}")
        return []


async def _ingest_all(rag, output_dir: str):
    rag.verify_parser_installation_once()

    files_processed = 0

    if paths.DATA_DIR.exists() and paths.DATA_DIR.is_dir():
        print(f"[ingest] Processing folder: {paths.DATA_DIR}")
        await rag.process_folder_complete(
            folder_path=str(paths.DATA_DIR),
            output_dir=output_dir,
            recursive=True,
        )
        files_processed += 1

    if paths.DATA_DOCS_PATHS.exists():
        file_paths = _read_lines(paths.DATA_DOCS_PATHS)
        for fp in file_paths:
            fp = fp.strip()
            if not fp:
                continue
            p = Path(fp)
            if p.exists():
                print(f"[ingest] Processing file: {fp}")
                await rag.process_document_complete(
                    file_path=str(p),
                    output_dir=output_dir,
                )
                files_processed += 1
            else:
                print(f"[ingest] File not found: {fp}")

    if paths.DATA_WEBS_PATHS.exists():
        urls = _read_lines(paths.DATA_WEBS_PATHS)
        for url in urls:
            url = url.strip()
            if not url:
                continue
            print(f"[ingest] Will process URL: {url}")
            try:
                import requests
                from bs4 import BeautifulSoup

                resp = requests.get(
                    url,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36"
                        )
                    },
                    timeout=30,
                )
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
                text = soup.get_text(separator="\n", strip=True)

                tmp_dir = Path(output_dir) / "_web_sources"
                tmp_dir.mkdir(parents=True, exist_ok=True)

                safe_name = (
                    url.replace("https://", "")
                    .replace("http://", "")
                    .replace("/", "_")
                    .replace("?", "_")[:100]
                )
                tmp_path = tmp_dir / f"{safe_name}.md"
                tmp_path.write_text(text, encoding="utf-8")
                print(f"[ingest] Downloaded web page -> {tmp_path}")

                await rag.process_document_complete(
                    file_path=str(tmp_path),
                    output_dir=output_dir,
                )
                files_processed += 1
            except Exception as e:
                print(f"[ingest] Failed to process URL {url}: {e}")

    if files_processed == 0:
        print("[ingest] No documents to process.")
    else:
        print(f"[ingest] Done. Processed {files_processed} sources.")


def run() -> None:
    print("Ingesting documents into RAG-Anything...")
    rag = session.get_session().get_rag()

    working_dir = rag.config.working_dir if rag.config else "./rag_storage"
    output_dir = getattr(rag.config, "parser_output_dir", "./output")

    asyncio.run(_ingest_all(rag, output_dir))

    session.get_session().force_reload()
    print("Ingest complete.")
