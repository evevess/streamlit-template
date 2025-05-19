from __future__ import annotations

import datetime
import json
import uuid

from azure.storage.blob import BlobServiceClient

import streamlit as st

# Azure Blob Storage config
AZURE_STORAGE_CONNECTION_STRING = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
CONTAINER_NAME = "proposal-submissions"
FOLDER_NAME = "proposal-requests"

blob_service_client = BlobServiceClient.from_connection_string(
    AZURE_STORAGE_CONNECTION_STRING
)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

st.set_page_config(page_title="📋 Proposal Intake Form", layout="centered")
st.title("📋 Proposal Request Form")

with st.form("proposal_form"):
    client_name = st.text_input("Client Name")
    industry = st.text_input("Industry")
    goal = st.text_area("Project Goal")
    tools_tech_stack = st.multiselect(
        "Tools / Tech Stack",
        [
            "Python",
            "Azure",
            "Databricks",
            "SQL",
            "Spark",
            "Streamlit",
            "Power BI",
            "Tableau",
        ],
    )
    cloud_infra = st.selectbox(
        "Cloud Infrastructure", ["Azure", "AWS", "GCP", "Hybrid", "On-prem"]
    )
    storage_db = st.multiselect(
        "Storage / DB", ["Blob", "ADLS", "Postgres", "CosmosDB", "MySQL", "MongoDB"]
    )
    model_type = st.multiselect(
        "Model Type",
        ["LLM", "ML", "RAG", "MLOps", "Vision", "Tabular", "Classification"],
    )
    ui_visualization_reqs = st.selectbox(
        "UI / Visualization", ["Power BI", "Streamlit", "Dash", "None"]
    )
    team_size = st.number_input("Team Size", min_value=1, step=1, value=5)
    duration_weeks = st.number_input(
        "Project Duration (weeks)", min_value=1, step=1, value=12
    )
    client_logo = st.text_input("Client Logo (URL or Blob path)")
    brand_palette = st.selectbox(
        "Brand Palette",
        [
            '["#004B87", "#F2A900"]',
            '["#1B1F3B", "#E63946"]',
            '["#14213D", "#FCA311"]',
            '["#003049", "#D62828"]',
        ],
    )

    submitted = st.form_submit_button("Submit Proposal Request")

if submitted:
    data = {
        "client_name": client_name,
        "industry": industry,
        "goal": goal,
        "tools_tech_stack": tools_tech_stack,
        "cloud_infra": cloud_infra,
        "storage_db": storage_db,
        "model_type": model_type,
        "ui_visualization_reqs": ui_visualization_reqs,
        "team_size": team_size,
        "duration_weeks": duration_weeks,
        "client_logo": client_logo,
        "brand_palette": json.loads(brand_palette),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "id": str(uuid.uuid4()),
    }

    json_bytes = json.dumps(data, indent=2).encode("utf-8")

    # Blob name with folder path prefix (Azure treats this as virtual folder)
    blob_name = (
        f"{FOLDER_NAME}/{data['client_name'].replace(' ', '_')}_{data['id']}.json"
    )

    try:
        container_client.upload_blob(name=blob_name, data=json_bytes)
        st.success(f"Proposal submitted and stored as `{blob_name}` in blob storage.")
    except Exception as e:
        st.error(f"Upload failed: {e}")
