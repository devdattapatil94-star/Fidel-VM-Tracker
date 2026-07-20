import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- SETUP & HELPERS ---
st.set_page_config(layout="wide")

# CSS to make the interface look professional and modern
st.markdown("""
    <style>
    .project-card {
        padding: 20px;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        background: #FFFFFF;
        margin-bottom: 12px;
        transition: transform 0.1s;
    }
    .project-card:hover { border-color: #3B82F6; }
    .status-pill {
        font-size: 12px;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# Load data (stub)
def get_data():
    return pd.DataFrame({
        "ID": ["FID-001", "FID-002"],
        "Client": ["Client A", "Client B"],
        "Status": ["In progress", "Not started"],
        "Margin": [45.0, 38.0]
    })

data = get_data()

# --- LAYOUT ---
st.title("Production Control Deck")
st.markdown("---")

col_main, col_dock = st.columns([2, 1])

with col_main:
    st.subheader("Active Projects")
    for idx, row in data.iterrows():
        # Displaying project as a clean card
        st.markdown(f"""
            <div class="project-card">
                <div style="display:flex; justify-content:space-between;">
                    <strong>{row['ID']} - {row['Client']}</strong>
                    <span class="status-pill" style="background:#EFF6FF; color:#1E40AF;">{row['Status']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Manage", key=f"btn_{idx}"):
            st.session_state.active_project = row['ID']

with col_dock:
    st.subheader("Operational Dock")
    if 'active_project' in st.session_state:
        st.write(f"Editing: {st.session_state.active_project}")
        # Dedicated, isolated space for updates
        st.selectbox("Status", ["Not started", "In progress", "Completed"], key="new_status")
        st.number_input("Vendor Cost", min_value=0.0)
        st.button("Update Project", type="primary")
    else:
        st.info("Select a project from the left to view operational details.")
