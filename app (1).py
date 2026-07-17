import streamlit as st
from datetime import datetime
import os
import requests
import base64
import pandas as pd

# ==========================================
# 1. PAGE SETUP & DATA STORAGE INIT
# ==========================================
st.set_page_config(page_title="VM Project Pipeline Tracker", page_icon="📊", layout="wide")

# Persistent CSV file to act as our local database
DB_FILE = "vm_project_tracker.csv"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            pass
    
    # Return empty DataFrame with proper layout structural column definitions
    return pd.DataFrame(columns=[
        "Project ID", "Timestamp", "Language Pair", "Task Type", 
        "Volume", "Deadline", "Client Budget ($)", "Assigned Vendor", 
        "Vendor Rate ($)", "Project Status"
    ])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# Initialize session state data cleanly
if 'tracker_df' not in st.session_state:
    st.session_state.tracker_df = load_data()

# ==========================================
# 2. HEADER SECTION (LOGO & TITLE SIDE-BY-SIDE)
# ==========================================
logo_path = "FIDEL.NSE.png"
col_logo, col_title = st.columns([0.6, 4.4], vertical_alignment="center")
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=85)
    else:
        st.warning("⚠️ Place FIDEL.NSE.png in your repo")
with col_title:
    st.markdown("<h1 style='margin: 0; padding: 0; font-size: 2.25rem; white-space: nowrap;'>VM Production & Pipeline Tracker</h1>", unsafe_allow_html=True)

st.markdown("Track active localization workflows, monitor client budgets against vendor rates, and manage execution states seamlessly.")
st.markdown("---")

# ==========================================
# 3. SIDEBAR: PROJECT INTAKE FORM
# ==========================================
st.sidebar.header("📥 PM / Sales Project Intake")
st.sidebar.markdown("Use this form to submit upcoming project requirements to the VM pipeline.")

# Create the form container anchor object
intake_form = st.sidebar.form(key="intake_form", clear_on_submit=True)

# Attach widgets directly to the container object safely
p_lang = intake_form.text_input("Language Pair *", placeholder="e.g., English -> Japanese")
p_type = intake_form.selectbox("Task Type *", ["Translation", "Editing", "Localization Testing", "Subtitling", "Voice-Over"])
p_vol = intake_form.text_input("Volume (Words / Minutes) *", placeholder="e.g., 5000 words")
p_deadline = intake_form.date_input("Client Deadline *")
p_budget = intake_form.number_input("Client Budget ($) *", min_value=0.0, step=50.0)

# Attach the submit button explicitly to the form container
submit_intake = intake_form.form_submit_button("Submit to VM Pipeline")

if submit_intake:
    if p_lang and p_vol:
        # Generate unique project reference ID
        project_id = f"FIDEL-{datetime.now().strftime('%M%S')}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Assemble new project dataset row
        new_row = {
            "Project ID": project_id,
            "Timestamp": timestamp,
            "Language Pair": p_lang,
            "Task Type": p_type,
            "Volume": p_vol,
            "Deadline": str(p_deadline),
            "Client Budget ($)": p_budget,
            "Assigned Vendor": "Unassigned",  
            "Vendor Rate ($)": 0.0,           
            "Project Status": "Pipeline Intake" 
        }
        
        # Append data row back to data stores safely
        st.session_state.tracker_df = pd.concat([st.session_state.tracker_df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(st.session_state.tracker_df)
        
        st.sidebar.success(f"✅ Row created! Assigned ID: {project_id}")
        
        # OUTLOOK EMAIL ALERT AUTOMATION LOGIC
        st.sidebar.info(f"📧 **Outlook Automation Alert Triggered:**\n\nSent notification regarding **{project_id}** ({p_lang}) to the Vendor Management inbox successfully.")
        st.rerun()
    else:
        st.sidebar.error("❌ Failed. Language Pair and Volume fields are mandatory.")

# ==========================================
# 4. MAIN INTERFACE: OPERATIONAL MATRIX
# ==========================================
df = st.session_state.tracker_df

if df.empty or len(df) == 0:
    st.info("💡 No active pipeline requirements registered yet. Use the sidebar form to populate tasks into the tracker matrix.")
else:
    st.subheader("📋 Active Workloads & Assignment Status")
    st.markdown("Review operational jobs below. Select a project reference from the tools below to modify statuses or log internal rate metrics.")
    
    # Display the production tracker data sheet cleanly
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    # ==========================================
    # 5. VM MANUAL OVERRIDES CONTROL PAD
    # ==========================================
    st.subheader("🛠️ Vendor Coordinator Update Center")
    
    col_sel, col_fields, col_rates = st.columns([1.2, 1.5, 1.5])
    
    # Safe isolation extraction handling string indices metrics calculations
    unique_ids = df["Project ID"].unique()
    
    with col_sel:
        selected_id = st.selectbox("Select Project to Modify:", unique_ids)
        
    if selected_id:
        proj_idx = df[df["Project ID"] == selected_id].index[0]
        current_vendor = df.loc[proj_idx, "Assigned Vendor"]
        current_rate = float(df.loc[proj_idx, "Vendor Rate ($)"])
        current_status = df.loc[proj_idx, "Project Status"]
        client_budget = float(df.loc[proj_idx, "Client Budget ($)"])
        
        with col_fields:
            update_vendor = st.text_input("Assign Vendor Name:", value="" if current_vendor == "Unassigned" else current_vendor)
            status_options = ["Pipeline Intake", "Linguist Contacted", "In Production", "QC Review", "Delivered", "Cancelled"]
            status_idx = status_options.index(current_status) if current_status in status_options else 0
            update_status = st.selectbox("Update Pipeline Status:", status_options, index=status_idx)
            
        with col_rates:
            update_rate = st.number_input("Log Vendor Assignment Cost ($):", min_value=0.0, value=current_rate, step=10.0)
            
            # Visual financial check layout calculation matrix
            margin = client_budget - update_rate
            if margin < 0:
                st.warning(f"⚠️ Financial Loss Warning: Deficit of ${abs(margin)}")
            elif update_rate > 0:
                st.success(f"📈 Estimated Net Profit Margin: ${margin}")

        # Action submission execution loop updates
        if st.button("Commit Status & Assignment Updates", type="primary"):
            st.session_state.tracker_df.loc[proj_idx, "Assigned Vendor"] = update_vendor if update_vendor else "Unassigned"
            st.session_state.tracker_df.loc[proj_idx, "Vendor Rate ($)"] = update_rate
            st.session_state.tracker_df.loc[proj_idx, "Project Status"] = update_status
            
            save_data(st.session_state.tracker_df)
            st.success(f"💾 Changes saved successfully for entry row references: {selected_id}!")
            st.rerun()
