import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. PAGE CONFIG & DATA LAYER
# ==========================================
st.set_page_config(page_title="Fidel Production Deck", page_icon="💎", layout="wide")

DB_FILE = "production_deck.csv"

# [Add the same LANGUAGES_POOL, TASK_TYPE_OPTIONS, STATUS_OPTIONS from your previous version here for logic consistency]

def load_data():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["ID", "Client", "Task", "Status", "Deadline", "Budget", "Margin"])

df = load_data()

# ==========================================
# 2. SIDEBAR INTAKE (MINIMALIST)
# ==========================================
with st.sidebar:
    st.markdown("### 📥 Project Intake")
    # [Add your clean form fields here]
    if st.button("Initialize Project", use_container_width=True, type="primary"):
        st.toast("Project added to deck", icon="✅")

# ==========================================
# 3. EXECUTIVE DASHBOARD (THE CLEAN VIEW)
# ==========================================
# Header & Global KPIs
st.markdown("<h1 style='font-size: 1.8rem; color: #0F172A;'>Production Control Deck</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pipeline", len(df))
col2.metric("Active Projects", len(df[df["Status"] == "In progress"]))
col3.metric("Urgent (24h)", "3")
col4.metric("Avg Margin", "42%")

st.markdown("---")

# Layout: List Column (Left) | Operational Detail Column (Right)
left_col, right_col = st.columns([2, 1])

with left_col:
    # A clean search input
    search = st.text_input("🔍 Search Projects", placeholder="Type project ID or client name...")
    
    # Modern card-based row iteration
    for _, row in df.iloc[::-1].iterrows():
        # Each row as a 'Card'
        st.markdown(
            f"""
            <div style="padding: 16px; border: 1px solid #E2E8F0; border-radius: 8px; margin-bottom: 8px; background: white; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #1E293B;">{row['ID']}</strong> - {row['Task']}<br>
                    <small style="color: #64748B;">Due: {row['Deadline']} | Status: {row['Status']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

with right_col:
    st.markdown("### ⚙️ Operational Dock")
    st.info("Select a project row to modify margins, status, or vendor costs.")
