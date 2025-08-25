from typing import TypedDict, Dict


class Manifest(TypedDict):
    files: Dict[str, str]  # {filename: sha256}
