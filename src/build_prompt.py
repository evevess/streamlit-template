from __future__ import annotations

import json
from pathlib import Path


def load_proposal_data(json_path: str | Path) -> dict:
    """Load proposal data from JSON file."""
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def build_prompt(data: dict) -> str:
    """Build a structured prompt from proposal data."""
    prompt = f"""
    You are a senior consultant and proposal writer at a top-tier consulting firm.

    Write a professional and visually clear client proposal deck for the following engagement:

    Client: {data.get("client_name")}
    Goal: {data.get("goal")}
    Industry: {data.get("industry")}
    Tech Stack: {', '.join(data.get("tools_tech_stack", []))}
    Cloud Infrastructure: {data.get("cloud_infra", "N/A")}
    Storage & DB: {', '.join(data.get("storage_db", []))}
    Recommended ML Models: {', '.join(data.get("model_type", []))}
    UI/Visualization Requirements: {', '.join(data.get("ui_visualization_reqs", []))}
    Team: {data.get("team_size")} people over {data.get("duration_weeks")} weeks

    Brand Palette: {', '.join(data.get("brand_palette", []))}
    Logo Path: {data.get("client_logo")}

    Additional Information:
    {data.get("additional_info", "N/A")}

    Include the following sections:
    - Title Slide
    - Executive Summary
    - Objectives
    - Our Understanding
    - Proposed Architecture
    - Solution Approach
    - Tools & Tech Stack
    - Timeline
    - Team Composition
    - Benefits
    - Next Steps

    Use professional language and tailor the visuals to consulting presentation standards.
    """
    return prompt.strip()


def main():
    json_file = Path("data/proposal_example.json")  # Adjust path as needed
    proposal_data = load_proposal_data(json_file)
    prompt = build_prompt(proposal_data)

    print("\n📄 Generated Prompt:\n")
    print(prompt)


if __name__ == "__main__":
    main()
