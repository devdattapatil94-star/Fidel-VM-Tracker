import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & ARCHITECTURE
# ==========================================
st.set_page_config(
    page_title="Production Control Deck",
    page_icon="⚡",
    layout="wide"
)

DB_FILE = "pipeline_database.csv"

STATUS_OPTIONS = [
    "Not started", "In progress", "Completed", "Cancelled", "Delayed", 
    "In Discussion stage with the PM", "In Discussion stage with the client", 
    "No Response received later from the linguist", "Pending"
]

TASK_TYPE_OPTIONS = [
    "AI Voice-Over", "Audio Content Check", "Audio Data Collection", 
    "Back Translation (Chars)", "Back Translation (Words)", "Closed Captioning", 
    "Data Annotation", "Data Collection", "Desktop Publishing", "Editing", 
    "Evaluation", "Interpretation", "Machine Translation and Full Post-Editing", 
    "Machine Translation and Light Post-Editing", "Post-Editing", "Proofreading", 
    "Review", "Revision", "Subtitle Integration", "Subtitling", 
    "TEP (Translation, Editing & Proofreading)", "Transcreation", 
    "Transcription", "Translation", "Voice-Over"
]

LANGUAGES_POOL = [
    "Afar", "Afrikaans (South Africa)", "Albanian", "Amharic", "Arabic", "Armenian", 
    "Assamese", "Azerbaijani", "Basque", "Bengali", "Bosnian (Latin)", "Bulgarian", 
    "Burmese", "Cantonese", "Catalan", "Cebuano (Philippines)", "Chinese (Mandarin)", 
    "Chinese (Simplified)", "Chinese (Traditional)", "Croatian", "Czech", "Danish", 
    "Dari", "Dutch", "English (UK)", "English (USA)", "Estonian", "Farsi", "Filipino", 
    "Finnish", "French", "French (Canada)", "Galician (Spain)", "Georgian", "German", 
    "Greek", "Gujarati (India)", "Haitian Creole", "Hausa", "Hebrew", "Hindi", "Hmong", 
    "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish (Ireland)", "Italian", 
    "Japanese", "Javanese", "Kannada (India)", "Kazakh", "Khmer", "Korean", "Lao", 
    "Latvian", "Lithuanian", "Macedonian", "Malayalam (India)", "Maltese", "Marathi", 
    "Mongolian", "Nepali", "Norwegian", "Oriya", "Pashto", "Persian", "Polish", 
    "Portuguese (Brazil)", "Portuguese (Portugal)", "Punjabi", "Romanian", "Russian", 
    "Sanskrit", "Serbian (Latin)", "Sindhi", "Singhalese", "Slovak", "Slovene", "Somali", 
    "Spanish (Latin America)", "Spanish (Spain)", "Swahili (Tanzania)", "Swedish", 
    "Tagalog (TL)", "Tajik (TG)", "Tamil", "Telugu", "Thai (TH)", "Tibetan (BO)", 
    "Turkish", "Ukrainian", "Urdu", "Uzbek (UZ)", "Vietnamese (VI)", "Xhosa (XH)", "Zulu"
]

def load_database():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            # Ensure dynamic margin columns exist
            for col in ["Client Currency", "Budget Value", "Vendor Cost", "Gross Profit %"]:
                if col not in df.columns: df[col] = 0.0 if "Currency" not in col else "USD ($)"
            if "Budget Display" not in df.columns:
                df["Budget Display"] = df["Budget"] if "Budget" in df.columns else df["Budget Value"].astype(str)
            return df
        except:
            pass
    return pd.DataFrame(columns=[
        "Project ID", "Timestamp", "Source Language", "Target Language", 
        "Task Type", "CAT Tool(s)", "Volume", "Reference File", 
        "Deadline (IST)", "Client Currency", "Budget Value", "Budget Display", "Vendor Cost", "Gross Profit %", "Status"
    ])

def save_database(df):
    df.to_csv(DB_FILE, index=False)

df_db = load_database()

# Initialize selected project focus state tracking
if "focused_project_id" not in st.session_state:
    st.session_state.focused_project_id = None

# ==========================================
# 2. SIDEBAR INTAKE WORKFLOW (LEFT)
# ==========================================
with st.sidebar:
    st.markdown("### 📥 Project Intake")
    st.caption("PM Team entry submission layer")
    st.markdown("---")
    
    src_langs = st.multiselect("Source Language(s) *", options=LANGUAGES_POOL)
    tgt_langs = st.multiselect("Target Language(s) *", options=LANGUAGES_POOL)
    task_type = st.selectbox("Task Type *", TASK_TYPE_OPTIONS)
    
    cat_options = ["MateCat", "MateSub", "MemoQ", "Phrase", "SDL Trados", "SmartCAT", "Smartling", "Wordfast"]
    selected_tools = st.multiselect("Client CAT Tool *", options=cat_options)
    
    volume = st.text_input("Volume *", placeholder="e.g., 5000 words")
    ref_file = st.file_uploader("Reference or sample file", type=['txt', 'pdf', 'docx', 'xlsx', 'zip'])
    
    st.markdown("<label style='font-size: 14px;'>Deadline *</label>", unsafe_allow_html=True)
    d_date = st.date_input("Date", datetime.today(), label_visibility="collapsed")
    col_h, col_m = st.columns(2)
    with col_h: h_sel = st.selectbox("Hour", [f"{i:02d}" for i in range(24)])
    with col_m: m_sel = st.selectbox("Min", [f"{i:02d}" for i in range(60)])
        
    st.markdown("<label style='font-size: 14px;'>Client Budget *</label>", unsafe_allow_html=True)
    col_c, col_a = st.columns([0.8, 1.2])
    with col_c: curr_sel = st.selectbox("Currency", ["USD ($)", "JPY (¥)", "INR (₹)"], label_visibility="collapsed")
    with col_a: amt_sel = st.number_input("Amount", min_value=0.000, step=0.001, format="%f", label_visibility="collapsed")
    
    if st.button("Log to Master Pipeline", use_container_width=True, type="primary"):
        if src_langs and tgt_langs and selected_tools and volume and amt_sel > 0:
            symbol = curr_sel.split(" ")[1].replace("(","").replace(")","")
            f_budget = f"{symbol}{int(amt_sel):,}" if "JPY" in curr_sel else f"{symbol}{amt_sel:.3f}".rstrip('0').rstrip('.')
            proj_id = f"FID-{datetime.now().strftime('%m%d%H%M%S')}"
            
            new_row = pd.DataFrame([{
                "Project ID": proj_id, "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Source Language": ", ".join(src_langs), "Target Language": ", ".join(tgt_langs),
                "Task Type": task_type, "CAT Tool(s)": ", ".join(selected_tools), "Volume": volume,
                "Reference File": ref_file.name if ref_file else "None", "Deadline (IST)": f"{d_date.strftime('%Y-%m-%d')} {h_sel}:{m_sel} IST",
                "Client Currency": curr_sel, "Budget Value": float(amt_sel), "Budget Display": f_budget,
                "Vendor Cost": 0.0, "Gross Profit %": 100.0, "Status": "Not started"
            }])
            save_database(pd.concat([df_db, new_row], ignore_index=True))
            st.success(f"Log added: {proj_id}")
            st.rerun()

# ==========================================
# 3. HIGH-VISIBILITY CONTROL BOARD DESIGN (RIGHT)
# ==========================================
st.markdown("<h2 style='margin:0; padding:0; color:#0F172A; font-weight:800;'>VM Production Control Deck</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748B; font-size:14px; margin-top:2px;'>Clean, open matrix display optimizing word count allocations and global localization updates.</p>", unsafe_allow_html=True)
st.markdown("---")

if df_db.empty:
    st.info("Production pipeline database is currently clear.")
else:
    # High-level summary metrics block
    not_started_cnt = len(df_db[df_db["Status"] == "Not started"])
    in_progress_cnt = len(df_db[df_db["Status"] == "In progress"])
    discussion_cnt = len(df_db[df_db["Status"].str.contains("Discussion", na=False)])
    delayed_cnt = len(df_db[df_db["Status"].isin(["Delayed", "Pending"])])
    
    met1, met2, met3, met4 = st.columns(4)
    met1.markdown(f"<div style='background-color:#F8FAFC; border:1px solid #E2E8F0; padding:12px; border-radius:6px; text-align:center;'><span style='color:#64748B; font-size:12px; font-weight:600;'>🎯 BACKLOG</span><h3 style='margin:5px 0 0 0; color:#0F172A;'>{not_started_cnt}</h3></div>", unsafe_allow_html=True)
    met2.markdown(f"<div style='background-color:#FFFBEB; border:1px solid #FDE68A; padding:12px; border-radius:6px; text-align:center;'><span style='color:#B45309; font-size:12px; font-weight:600;'>⏳ IN PROGRESS</span><h3 style='margin:5px 0 0 0; color:#B45309;'>{in_progress_cnt}</h3></div>", unsafe_allow_html=True)
    met3.markdown(f"<div style='background-color:#F5F3FF; border:1px solid #DDD6FE; padding:12px; border-radius:6px; text-align:center;'><span style='color:#6D28D9; font-size:12px; font-weight:600;'>💬 DISCUSSION</span><h3 style='margin:5px 0 0 0; color:#6D28D9;'>{discussion_cnt}</h3></div>", unsafe_allow_html=True)
    met4.markdown(f"<div style='background-color:#FEF2F2; border:1px solid #FEE2E2; padding:12px; border-radius:6px; text-align:center;'><span style='color:#DC2626; font-size:12px; font-weight:600;'>🚨 BLOCKED / DELAYED</span><h3 style='margin:5px 0 0 0; color:#DC2626;'>{delayed_cnt}</h3></div>", unsafe_allow_html=True)
    
    st.markdown(" ")

    # Master split view configuration logic
    main_board_column, detail_action_column = st.columns([2.2, 0.8])
    
    with main_board_column:
        st.markdown("<h5 style='color:#0F172A; font-weight:700; margin-bottom:10px;'>📋 Current Delivery Queue</h5>", unsafe_allow_html=True)
        
        # Unified table layout array drop logic
        for idx, row in df_db.iloc[::-1].iterrows():
            pid = row["Project ID"]
            status = row["Status"]
            
            # Clean color flags mapped safely
            color_indicator = "#94A3B8"  # Muted slate default
            if status == "In progress": color_indicator = "#F59E0B"     # Amber yellow
            elif status == "Completed": color_indicator = "#10B981"     # Emerald green
            elif status in ["Delayed", "Pending"]: color_indicator = "#EF4444"  # Crimson red
            elif "Discussion" in status: color_indicator = "#8B5CF6"    # Purple track
            
            # Form clean horizontal block display elements
            st.markdown(
                f"<div style='background-color:#FFFFFF; border:1px solid #E2E8F0; border-left:5px solid {color_indicator}; padding:14px; border-radius:6px; margin-bottom:10px; color:#172B4D;'>"
                f"  <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>"
                f"      <span style='font-size:15px; font-weight:800; color:#0F172A;'>⚡ ID: {pid} &nbsp;|&nbsp; <span style='font-weight:500; color:#475569;'>{row['Task Type']}</span></span>"
                f"      <span style='background-color:#F1F5F9; color:#334155; border:1px solid #E2E8F0; padding:2px 10px; border-radius:4px; font-size:11px; font-weight:700;'>{status}</span>"
                f"  </div>"
                f"  <div style='font-size:13px; color:#334155; line-height:1.4;'>"
                f"      <b>Languages:</b> {row['Source Language']} ➡️ {row['Target Language']}<br>"
                f"      <b>Metrics:</b> Volume: {row['Volume']} &nbsp;|&nbsp; Budget: {row['Budget Display']} &nbsp;|&nbsp; Due: {row['Deadline (IST)']}"
                f"  </div>"
                f"</div>", 
                unsafe_allow_html=True
            )
            
            # Quick toggle link selector button to focus on a particular project card item
            if st.button(f"🔎 Select Project {pid}", key=f"select_{pid}", use_container_width=True):
                st.session_state.focused_project_id = pid
                st.rerun()

    with detail_action_column:
        st.markdown("<h5 style='color:#0F172A; font-weight:700; margin-bottom:10px;'>⚙️ Operations Desk</h5>", unsafe_allow_html=True)
        
        if st.session_state.focused_project_id is None:
            st.markdown(
                "<div style='border:2px dashed #E2E8F0; border-radius:6px; padding:30px; text-align:center; color:#94A3B8; font-size:13px;'>"
                "Select a project from the queue to edit status track mappings, view profit margins, or update costs."
                "</div>", 
                unsafe_allow_html=True
            )
        else:
            focus_id = st.session_state.focused_project_id
            target_data = df_db[df_db["Project ID"] == focus_id]
            
            if target_data.empty:
                st.session_state.focused_project_id = None
                st.rerun()
            else:
                proj_record = target_data.iloc[0]
                
                # Active operational control workspace card container
                st.markdown(
                    f"<div style='background-color:#F8FAFC; border:1px solid #E2E8F0; padding:16px; border-radius:6px; color:#172B4D; margin-bottom:15px;'>"
                    f"  <h5 style='margin:0 0 10px 0; color:#0F172A; font-weight:700;'>Selected: {focus_id}</h5>"
                    f"  <p style='margin:0; font-size:12.5px; color:#475569;'><b>Task:</b> {proj_record['Task Type']}</p>"
                    f"  <p style='margin:4px 0 0 0; font-size:12.5px; color:#475569;'><b>Budget Metric:</b> {proj_record['Budget Display']}</p>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
                # Direct adjustment tracking widgets inputs
                up_status = st.selectbox("Update Pipeline Status", options=STATUS_OPTIONS, index=STATUS_OPTIONS.index(proj_record["Status"]), key="op_status")
                up_cost = st.number_input("Log Vendor Payout Cost", min_value=0.0, step=0.001, value=float(proj_record["Vendor Cost"]), format="%f", key="op_cost")
                
                # Dynamic calculated gross profit display
                b_val = float(proj_record["Budget Value"])
                margin_val = ((b_val - up_cost) / b_val * 100.0) if b_val > 0 else 0.0
                margin_color = "#16A34A" if margin_val >= 40.0 else "#DC2626"
                
                st.markdown(
                    f"<div style='margin:12px 0; padding:10px; background-color:#FFFFFF; border:1px solid #E2E8F0; border-radius:4px; text-align:center; font-size:13px;'>"
                    f"  Estimated Margin: <b style='color:{margin_color}; font-size:14px;'>{margin_val:.1f}%</b>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
                col_save, col_clear = st.columns(2)
                with col_save:
                    if st.button("Save Changes", type="primary", use_container_width=True):
                        df_db.set_index("Project ID", inplace=True)
                        df_db.at[focus_id, "Status"] = up_status
                        df_db.at[focus_id, "Vendor Cost"] = up_cost
                        df_db.at[focus_id, "Gross Profit %"] = margin_val
                        df_db.reset_index(inplace=True)
                        save_database(df_db)
                        st.toast(f"Saved update for {focus_id}", icon="✅")
                        st.rerun()
                with col_clear:
                    if st.button("Close Panel", use_container_width=True):
                        st.session_state.focused_project_id = None
                        st.rerun()

    # Master Report data extraction export button utilities
    st.markdown("---")
    csv_report = df_db.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Master Production Log (CSV)",
        data=csv_report,
        file_name=f"FIDEL_Production_Report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        type="secondary",
        use_container_width=True
    )
