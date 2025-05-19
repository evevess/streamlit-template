from __future__ import annotations

import datetime
import uuid

import streamlit as st
from src.utils import save_to_onedrive

# Constants
CLOUD_INFRA_OPTIONS = [
    "Azure",
    "AWS",
    "Google Cloud Platform",
    "On-Premise",
]

UI_REQ_OPTIONS = [
    "Power BI Dashboards",
    "Web UI for planners",
    "Mobile App Interface",
    "Custom Visualization",
    "None of the above",
]

BRAND_PALETTES = {
    "Default": ["#004B87", "#F2A900"],
    "ClientA": ["#123456", "#abcdef"],
    "ClientB": ["#654321", "#fedcba"],
}

# Streamlit App UI
st.set_page_config(page_title="📋 Proposal Request Form")
st.title("📋 Proposal Request Form")

# Start form
with st.form("proposal_form"):
    client_name = st.text_input("Client Name")
    industry = st.text_input("Industry")
    goal = st.text_area("Goal of the Proposal")
    ui_visualization_reqs = st.multiselect(
        "UI / Visualization Requirements", options=UI_REQ_OPTIONS
    )

    team_size = st.number_input("Team Size", min_value=1, max_value=20, value=5)
    duration_weeks = st.number_input(
        "Duration in Weeks", min_value=1, max_value=52, value=12
    )
    client_logo = st.text_input("Client Logo URL or Path")

    brand_palette_key = st.selectbox(
        "Brand Color Palette", options=list(BRAND_PALETTES.keys())
    )
    brand_palette = BRAND_PALETTES[brand_palette_key]

    # Additional Section
    additional_info = st.text_area("Additional Information (Optional)")

    submitted = st.form_submit_button("Submit Request")

# Submission handling
if submitted:
    full_ui_reqs = [ui for ui in ui_visualization_reqs if ui != "None of the above"]
    proposal_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "client_name": client_name,
        "industry": industry,
        "goal": goal,
        "ui_visualization_reqs": full_ui_reqs,
        "team_size": team_size,
        "duration_weeks": duration_weeks,
        "client_logo": client_logo,
        "brand_palette": brand_palette,
        "additional_info": additional_info or "",
    }

    save_to_onedrive(proposal_data)
    st.success("✅ Proposal request submitted and saved to OneDrive.")
