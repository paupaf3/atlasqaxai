from commands import ingest, wipe


def run() -> None:
    print("Rebuilding index...")
    wipe.run()
    ingest.run()
    print("Index rebuilt.")
