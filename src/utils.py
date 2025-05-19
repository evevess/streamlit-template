from __future__ import annotations

import json
import os
from pathlib import Path


def get_onedrive_path() -> Path:
    """Automatically detects the user's OneDrive folder from environment variables."""
    onedrive_path = os.environ.get("OneDrive")

    if not onedrive_path:
        raise OSError("OneDrive path not found in environment variables.")

    return Path(onedrive_path)


def save_to_onedrive(data: dict, filename: str) -> Path:
    """Saves a dictionary as a JSON file into the user's OneDrive folder."""
    file_path = get_onedrive_path()
    file_path.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return file_path
