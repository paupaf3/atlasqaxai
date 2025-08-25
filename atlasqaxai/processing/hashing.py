import hashlib
import json
from pathlib import Path

# (tiny local type to avoid pydantic)
# Why “avoid Pydantic”?
# For a simple JSON like {"files": {"doc.pdf": "abc123..."}}, that’s overkill.
from ..entities.manifest import Manifest


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(path: Path) -> Manifest:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"files": {}}


def save_manifest(path: Path, manifest: Manifest) -> None:
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
