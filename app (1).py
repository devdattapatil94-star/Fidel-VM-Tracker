import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# ==========================================
# 1. PAGE CONFIGURATION & DATABASE SETUP
# ==========================================
st.set_page_config(page_title="VM Production & Pipeline Tracker", page_icon="📊", layout="wide")

DB_FILE = "pipeline_database.csv"

# Updated Status/Task options remain the same...
STATUS_OPTIONS = ["Not started", "In progress", "Completed", "Cancelled", "Delayed", "In Discussion stage with the PM", "In Discussion stage with the client", "No Response received later from the linguist", "Pending"]
TASK_TYPE_OPTIONS = ["AI Voice-Over", "Audio Content Check", "Audio Data Collection", "Back Translation (Chars)", "Back Translation (Words)", "Closed Captioning", "Data Annotation", "Data Collection", "Desktop Publishing", "Editing", "Evaluation", "Interpretation", "Machine Translation and Full Post-Editing", "Machine Translation and Light Post-Editing", "Post-Editing", "Proofreading", "Review", "Revision", "Subtitle Integration", "Subtitling", "TEP (Translation, Editing & Proofreading)", "Transcreation", "Transcription", "Translation", "Voice-Over"]
LANGUAGES_POOL = ["Afar", "Afrikaans (South Africa)", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese", "Azerbaijani", "Basque", "Bengali", "Bosnian (Latin)", "Bulgarian", "Burmese", "Cantonese", "Catalan", "Cebuano (Philippines)", "Chinese (Mandarin)", "Chinese (Simplified)", "Chinese (Traditional)", "Croatian", "Czech", "Danish", "Dari", "Dutch", "English (UK)", "English (USA)", "Estonian", "Farsi", "Filipino", "Finnish", "French", "French (Canada)", "Galician (Spain)", "Georgian", "German", "Greek", "Gujarati (India)", "Haitian Creole", "Hausa", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish (Ireland)", "Italian", "Japanese", "Javanese", "Kannada (India)", "Kazakh", "Khmer", "Korean", "Lao", "Latvian", "Lithuanian", "Macedonian", "Malayalam (India)", "Maltese", "Marathi", "Mongolian", "Nepali", "Norwegian", "Oriya", "Pashto", "Persian", "Polish", "Portuguese (Brazil)", "Portuguese (Portugal)", "Punjabi", "Romanian", "Russian", "Sanskrit", "Serbian (Latin)", "Sindhi", "Singhalese", "Slovak", "Slovene", "Somali", "Spanish (Latin America)", "Spanish (Spain)", "Swahili (Tanzania)", "Swedish", "Tagalog (TL)", "Tajik (TG)", "Tamil", "Telugu", "Thai (TH)", "Tibetan (BO)", "Turkish", "Ukrainian", "Urdu", "Uzbek (UZ)", "Vietnamese (VI)", "Xhosa (XH)", "Zulu"]

def load_database():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            # Add new columns if they don't exist in existing CSV
            for col in ["Requester Name", "Resources Introduced", "Weekly Status"]:
                if col not in df.columns: df[col] = "N/A"
            return df
        except: pass
    return pd.DataFrame(columns=[
        "Project ID", "Timestamp", "Requester Name", "Resources Introduced", "Weekly Status",
        "Source Language", "Target Language", "Task Type", "CAT Tool(s)", "Volume", 
        "Deadline (IST)", "Client Currency", "Budget Value", "Budget Display", "Vendor Cost", "Gross Profit %", "Status"
    ])

def save_database(df):
    df.to_csv(DB_FILE, index=False)

df_db = load_database()

# ==========================================
# 2. SIDEBAR - PM / SALES INTAKE
# ==========================================
with st.sidebar:
    st.markdown("### 📥 PM / Sales Project Intake")
    requester = st.text_input("Requester Name *")
    resources = st.text_input("Resources Introduced")
    weekly_status = st.selectbox("Weekly Lifecycle Status", ["Open this week", "Closing next week", "Pending closure"])
    st.markdown("---")
    
    src_langs = st.multiselect("Source Language(s) *", options=LANGUAGES_POOL)
    tgt_langs = st.multiselect("Target Language(s) *", options=LANGUAGES_POOL)
    task_type = st.selectbox("Task Type *", TASK_TYPE_OPTIONS)
    volume = st.text_input("Volume *")
    budget_val = st.number_input("Budget Amount *", min_value=0.0)
    
    if st.button("Submit to VM Pipeline", type="primary"):
        if requester and src_langs and tgt_langs:
            proj_id = f"FID-{datetime.now().strftime('%m%d%H%M%S')}"
            new_task = pd.DataFrame([{
                "Project ID": proj_id,
                "Requester Name": requester,
                "Resources Introduced": resources,
                "Weekly Status": weekly_status,
                "Source Language": ", ".join(src_langs),
                "Target Language": ", ".join(tgt_langs),
                "Task Type": task_type,
                "Volume": volume,
                "Budget Value": float(budget_val),
                "Status": "Not started"
            }])
            save_database(pd.concat([df_db, new_task], ignore_index=True))
            st.rerun()

# ==========================================
# 3. MAIN WORKSPACE
# ==========================================
st.title("VM Production & Pipeline Tracker")

# Filter logic stays same...
tab_active, tab_archive = st.tabs(["📋 Active Pipeline Workspace", "🗄️ Archives"])

with tab_active:
    # Only display columns including the new ones
    display_df = df_db[~df_db["Status"].isin(["Completed", "Cancelled"])]
    
    edited_active = st.data_editor(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(options=STATUS_OPTIONS),
            "Weekly Status": st.column_config.SelectboxColumn(options=["Open this week", "Closing next week", "Pending closure"])
        }
    )
    
    if not edited_active.equals(display_df):
        save_database(edited_active)
        st.rerun()
