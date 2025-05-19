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
    target_folder = get_onedrive_path()
    target_folder.mkdir(parents=True, exist_ok=True)
    file_path = f"{target_folder}/{filename}"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return file_path


def load_proposal_data(json_path: Path, filename: str) -> dict:
    target_folder = get_onedrive_path()
    target_folder.mkdir(parents=True, exist_ok=True)

    matching_files = list(target_folder.glob(f"*{filename}*.json"))
    if not matching_files:
        raise FileNotFoundError(
            f"No matching files containing '{filename}' found in {target_folder}"
        )

    latest_file = max(matching_files, key=os.path.getmtime)
    with open(latest_file, encoding="utf-8") as f:
        return json.load(f)
