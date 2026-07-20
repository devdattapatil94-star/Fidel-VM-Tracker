import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# ==========================================
# 1. PAGE CONFIGURATION & DATABASE SETUP
# ==========================================
st.set_page_config(
    page_title="VM Production & Pipeline Tracker",
    page_icon="📊",
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
    "Afar", "Afrikaans (South Africa)", "Ahrani", "Akan", "Akha", "Albanian", "Amharic", 
    "Ancient Greek", "Arabic", "Arabic (Egypt)", "Arabic (Oman)", "Arabic (Algeria)", 
    "Arabic (Bahrain)", "Arabic (Chad)", "Arabic (Iraq)", "Arabic (Jordan)", "Arabic (Kuwait)", 
    "Arabic (Lebanon)", "Arabic (Libya)", "Arabic (Mauritania)", "Arabic (Morocco)", 
    "Arabic (Palestinian Territory)", "Arabic (Qatar)", "Arabic (Saudi Arabia)", "Arabic (Sudan)", 
    "Arabic (Syria)", "Arabic (Tunisia)", "Arabic (United Arab Emirates)", "Arabic (Western Sahara)", 
    "Arabic (Yemen)", "Armenian", "Assamese", "Asturian (Spain)", "Ateso", "Avar", "Awadhi", 
    "Aymara", "Azerbaijani", "Azeri (Cyrillic)", "Azeri Latin", "Bagheli", "Bambara", "Bashkir", 
    "Basque", "Bassa (BSQ)", "Bemba", "Bengali", "Bengali (Bangladesh)", "Berber (Tamazight)", 
    "Bhili (India)", "Bhojpuri", "Bhutani", "Bihari", "Bikol", "Bislama", "Bodo", "Bosnian (Cyrillic)", 
    "Bosnian (Latin)", "Breton", "Bulgarian", "Buli", "Bundeli", "Burmese", "Burushaski", 
    "Burushaski (Pakistan)", "Byelorussian", "Cantonese", "Carolinian", "Catalan", "Catalan (Spain)", 
    "Cebuano (Philippines)", "Cham", "Chamorro", "Chhattisgarhi (India)", "Chichewa", "Chin (Falam)", 
    "Chinese (Mandarin)", "Chinese (Simplified)", "Chinese (Singapore)", "Chinese (Traditional)", 
    "Chinese, Hong Kong", "Chittagonian (CTG)", "Chuukese", "Corsican", "Croatian", "Czech", 
    "Dandami Maria (India)", "Danish", "Dari", "Dhivehi-Maldivian (Maldives)", "Dholuo", "Dhundari", 
    "Dinka", "Dioula", "Divehi", "Dogon", "Dogri", "Dothraki", "Dutch", "Dutch (Belgium)", 
    "Dzongkha (DZ)", "Eastern Armenian", "Eastern Tamang", "Edo(Bini)", "Efik (Africa)", 
    "English (Australia)", "English (Canada)", "English (Hong Kong)", "English (India)", 
    "English (Nigeria)", "English (Philippines)", "English (Singapore)", "English (South Africa)", 
    "English (Switzerland)", "English (UK)", "English (USA)", "English (United Arab Emirates)", 
    "English(Malaysia)", "English (Asia)", "English (Austria)", "English (Cyprus)", "English (Germany)", 
    "English (Holland)", "English (Ireland)", "English (Neutral)", "English (New Zealand)", 
    "Esperanto", "Estonian", "Ewe (Ghana)", "Fante (Fanti) (FAT)", "Faroese (Faroe Islands)", 
    "Farsi", "Fijian", "Filipino", "Finnish", "Flemish", "French", "French (Belgium)", 
    "French (Cameroon) (FR CM)", "French (Canada)", "French (France)", "French (Haiti) (FR-Haiti)", 
    "French (Luxembourg)", "French (Morocco)", "French (Switzerland)", "Frisian", "Fula", 
    "Galician (Spain)", "Garhwali", "Garo", "Georgian", "German (Austria)", "German (Belgium)", 
    "German (Germany)", "German (Holland)", "German (Luxembourg)", "German (Switzerland)", 
    "Gondi", "Greek", "Greenlandic", "Guarani", "Gujarati (India)", "Haitian Creole", "Hakha Chin", 
    "Haryanvi (BGC)", "Hausa", "Hawaiian", "Hebrew", "Herero (Namibia)", "Hijazi Arabic", 
    "Hiligaynon", "Hindi", "Hindi Latin", "Hmong", "Hmong (USA)", "Hokkien (Fukienese)", 
    "Hungarian", "Icelandic", "Igbo", "Ilocano", "India", "Indonesian", "Interlingua", 
    "Interlingue", "Inuktitut", "Inupiak", "Irish (Ireland)", "Italian", "Italian (Switzerland)", 
    "Iu Mien", "Jamaican English Creole", "Japanese", "Javanese", "Juba Arabic", "Kabiye", 
    "Kachin", "Kam Mueang (Lanna) (NOD)", "Kangri", "Kannada (India)", "Kanuri", "Kaonde", 
    "Karen", "Karenni (Kayah)(eastern)", "Karenni (Kayah)(western)", "Kasem", "Kashmiri", 
    "Kazakh", "Khashi", "Khasi", "Khmer", "Khmu (KJG)", "Khowar", "Kikongo (Congo)", "Kikuyu", 
    "Kinyarwanda", "Kirghiz", "Kiribati", "Kirundi (Rundi) (RN)", "Kiswahili (Africa)", 
    "Klingon", "Konkani (India)", "Korean", "Kosraean", "Kru", "Kuanyama", "Kurdish (Turkey)", 
    "Kurdish (Iraq)", "Kurdish (Kurmanji)", "Kurdish (Sorani)", "Lambadi", "Lao", "Laothian", 
    "Latin", "Latvian", "Lingala", "Lithuanian", "Lozi", "Luganda", "Lunda", "Luxembourgish", 
    "Maasai (MAS)", "Maay", "Macedonian", "Macedonian (MK)", "Maithili", "Malagasy (Madagascar)", 
    "Malay (Malysia)", "Malay Chinese", "Malayalam (India)", "Malinke", "Maltese", "Manipuri", 
    "Maori", "Marathi", "Maria-Dandami", "Marshallese", "Marwari", "Masalit", "Meru (Kimeru) (MER)", 
    "Mewari", "Mien (Iu Mien) (IUM)", "Mirpuri", "Mizo", "Moldavian", "Mongolian", "Montenegrin", 
    "Morisyen (Mauritian Créole)", "Nagamese", "Nankam", "Nauru", "Navajo", "Ndebele", "Nepali", 
    "Niuean", "Nkore", "Nobiin", "Northern Sotho (South Africa)", "Norwegian", "Norwegian (Bokmål)", 
    "Norwegian Bokmaal (Norway)", "Norwegian Nynorsk (Norway)", "Nuer", "Nyanja", "Nyoro", 
    "Occitan", "Oriya", "Oromo", "Ossetian", "Ottoman Turkish", "Pahari", "Pak Thai (Dambro) (SOU)", 
    "Palauan", "Pampanga (Kapampangan)", "Pangasinan", "Papiamento", "Pashto", "Persian", 
    "Pohnpeian", "Polish", "Portuguese", "Portuguese (Brazil)", "Portuguese (Portugal)", 
    "Portuguese (Angola)", "Portuguese (Mozambique)", "Punjabi", "Punjabi (India)", 
    "Punjabi (Pakistan)", "Quechua", "Quenya", "Ratotongan", "Rhaeto-Romance", "Rohingya", 
    "Romanian", "Rundi", "Russian", "Saint Lucian Creole French", "Samoan", 
    "Sango (Central African Republic)", "Sangro", "Sanskrit", "Santali", "Saraiki", "Sardinian", 
    "Scottish Gaelic (Scotland)", "Sepedi", "Serbian", "Serbian (Cyrillic)", "Serbian (Latin)", 
    "Serbian Montenegro (Cyrillic)", "Serbian Montenegro (Latin)", "Serbo-Croatian (SH)", 
    "Seselwa Creole French", "Sesotho", "Setswana (Africa)", "Shan", "Sherpa (Nepal)", "Shona", 
    "Sindarin", "Sindhi", "Singhalese", "Siswati", "Slovak", "Slovene", "Slovenian (SL)", 
    "Somali", "Sorbian (Lower)", "Sorbian (Upper)", "Sotho", "Spanish (Argentina)", "Spanish (Bolivia)", 
    "Spanish (Chile)", "Spanish (Colombia)", "Spanish (Costa Rica)", "Spanish (Cuba)", 
    "Spanish (Dominican Republic)", "Spanish (Ecuador)", "Spanish (El Salvador)", "Spanish (Guatemala)", 
    "Spanish (Honduras)", "Spanish (Latin America)", "Spanish (Mexico)", "Spanish (Nicaragua)", 
    "Spanish (Panama)", "Spanish (Paraguay)", "Spanish (Spain)", "Spanish (USA)", "Sundanese (SU)", 
    "Swahili (Burundi)", "Swahili (Kenya)", "Swahili (Rwanda)", "Swahili (Tanzania)", "Swahili (Uganda)", 
    "Swedish", "Sylheti (SYL)", "Syriac", "Tagalog (TL)", "Tai Dam (Vietnam)", "Tajik (TG)", 
    "Tamil", "Tamil Sri-Lankan", "Telugu", "Tetum", "Thai (TH)", "Tibetan (BO)", "Tigrinya (TI)", 
    "Tok Pisin", "Tonga (Polynesian)", "Tongan", "Tulu", "Turkish", "Turkmen (TK)", "Twi (TW)", 
    "Ukrainian", "Upper Guinea Creole", "Urdu", "Urdu (India)", "Uyghur", "Uzbek (UZ)", 
    "Venda (VE)", "Vietnamese (VI)", "Waray-Waray (WW)", "Xhosa (XH)", "Xârâcùù (New Caledonia)", 
    "Yagwoia", "Yiddish (Israel)", "Yiddish (USA)", "Yoruba", "Zomi/Zou", "Zulu (South Africa)"
]

def load_database():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            if "Client Currency" not in df.columns: df["Client Currency"] = "USD ($)"
            if "Budget Value" not in df.columns: df["Budget Value"] = 0.0
            if "Vendor Cost" not in df.columns: df["Vendor Cost"] = 0.0
            if "Gross Profit %" not in df.columns: df["Gross Profit %"] = 0.0
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

# ==========================================
# 2. SIDEBAR - PM / SALES INTAKE FORM (LEFT)
# ==========================================
with st.sidebar:
    st.markdown("### 📥 PM / Sales Project Intake")
    st.write("Use this form to submit upcoming project requirements to the VM pipeline.")
    st.markdown("---")
    
    src_langs = st.multiselect("Source Language(s) *", options=LANGUAGES_POOL, key="pm_src_langs")
    tgt_langs = st.multiselect("Target Language(s) *", options=LANGUAGES_POOL, key="pm_tgt_langs")
    
    task_type = st.selectbox("Task Type *", TASK_TYPE_OPTIONS, key="pm_task_type")
    
    cat_options = ["MateCat", "MateSub", "MemoQ", "Phrase", "SDL Trados 2019", "SDL Trados 2021", "SDL Trados 2022", "Similis", "SmartCAT", "Smartling", "Wordfast"]
    selected_tools = st.multiselect("Client CAT Tool *", options=cat_options)
    
    volume = st.text_input("Volume (Words / Minutes) *", placeholder="e.g., 5000 words")
    ref_file = st.file_uploader("Reference or sample file (if any)", type=['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'zip'])
    
    st.markdown("<label style='font-size: 14px;'>Client Deadline Date *</label>", unsafe_allow_html=True)
    deadline_date = st.date_input("Deadline Date", datetime.today(), label_visibility="collapsed")
    
    st.markdown("<label style='font-size: 14px;'>Deadline Time (IST) *</label>", unsafe_allow_html=True)
    col_hr, col_min = st.columns(2)
    with col_hr:
        hours_options = [f"{i:02d}" for i in range(24)]
        selected_hour = st.selectbox("Hour", options=hours_options, key="pm_hour")
    with col_min:
        minutes_options = [f"{i:02d}" for i in range(60)]
        selected_min = st.selectbox("Minute", options=minutes_options, key="pm_min")
        
    st.markdown("<label style='font-size: 14px;'>Client Budget *</label>", unsafe_allow_html=True)
    col_curr, col_amt = st.columns([0.8, 1.2])
    with col_curr:
        currency = st.selectbox("Currency", options=["USD ($)", "JPY (¥)", "INR (₹)"], label_visibility="collapsed")
    with col_amt:
        budget_val = st.number_input("Amount", min_value=0.000, step=0.001, format="%f", label_visibility="collapsed")
    
    st.markdown(" ")
    if st.button("Submit to VM Pipeline", use_container_width=True, type="primary"):
        if src_langs and tgt_langs and selected_tools and volume and budget_val > 0:
            src_str = ", ".join(src_langs)
            tgt_str = ", ".join(tgt_langs)
            tools_str = ", ".join(selected_tools)
            formatted_deadline = f"{deadline_date.strftime('%Y-%m-%d')} {selected_hour}:{selected_min} IST"
            
            symbol = currency.split(" ")[1].replace("(", "").replace(")", "")
            if "JPY" in currency:
                formatted_budget = f"{symbol}{int(budget_val):,}"
            else:
                formatted_budget = f"{symbol}{budget_val:.3f}".rstrip('0').rstrip('.') if budget_val % 0.01 != 0 else f"{symbol}{budget_val:,.2f}"
            
            file_name_record = ref_file.name if ref_file is not None else "None"
            proj_id = f"FID-{datetime.now().strftime('%m%d%H%M%S')}"
            
            new_task = pd.DataFrame([{
                "Project ID": proj_id,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Source Language": src_str,
                "Target Language": tgt_str,
                "Task Type": task_type,
                "CAT Tool(s)": tools_str,
                "Volume": volume,
                "Reference File": file_name_record,
                "Deadline (IST)": formatted_deadline,
                "Client Currency": currency,
                "Budget Value": float(budget_val),
                "Budget Display": formatted_budget,
                "Vendor Cost": 0.0,
                "Gross Profit %": 100.0,
                "Status": "Not started"
            }])
            
            df_updated = pd.concat([df_db, new_task], ignore_index=True)
            save_database(df_updated)
            st.success("🎯 Task successfully routed to main production queue.")
            st.rerun()
        else:
            st.error("❌ Form Incomplete. Please check mandatory fields.")

# ==========================================
# 3. MAIN WORKSPACE - VM PIPELINE ENGINE (RIGHT)
# ==========================================
col_icon, col_title = st.columns([0.6, 5.4], vertical_alignment="center")
with col_icon:
    st.markdown("<div style='background-color:#1E3A8A; padding:12px; border-radius:8px; display:flex; justify-content:center; align-items:center; width:70px; height:70px;'><span style='font-size:38px; color:white;'>📊</span></div>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 style='margin:0; padding:0; font-size:2.5rem;'>VM Production & Pipeline Tracker</h1>", unsafe_allow_html=True)

st.write("Monitor client pipelines, balance localization project margins, and assign workflow progress tags.")
st.markdown("---")

if len(df_db) > 0:
    # Live KPI Analytics Cards
    active_count = len(df_db[df_db["Status"].isin(["Not started", "In progress", "Pending", "Delayed"])])
    urgent_count = 0
    now = datetime.now()
    for dl in df_db["Deadline (IST)"]:
        try:
            dl_date = datetime.strptime(dl.split(" IST")[0], "%Y-%m-%d %H:%M")
            if now <= dl_date <= (now + timedelta(hours=24)):
                urgent_count += 1
        except: pass

    usd_tot = df_db[df_db["Client Currency"] == "USD ($)"]["Budget Value"].sum()
    jpy_tot = df_db[df_db["Client Currency"] == "JPY (¥)"]["Budget Value"].sum()
    inr_tot = df_db[df_db["Client Currency"] == "INR (₹)"]["Budget Value"].sum()

    kp1, kp2, kp3 = st.columns(3)
    kp1.metric("Active Queue Pipeline", f"{active_count} Projects")
    kp2.metric("Urgent Deliveries (24 Hours) 🚨", f"{urgent_count} Tasks")
    kp3.metric("Total Volume Value", f"${usd_tot:,.2f} | ¥{int(jpy_tot):,} | ₹{inr_tot:,.2f}")
    
    st.markdown("---")

    # ------------------------------------------
    # 🔍 HIGH-VISIBILITY COLLAPSIBLE FILTER PANEL
    # ------------------------------------------
    with st.expander("🛠️ Advanced Search & Filter Dashboard Controls", expanded=True):
        st.write("Use these options to filter down the main workspace table:")
        
        # Row 1: Language Multi-selects (Full width for clear, uncut tag visibility)
        search_src = st.multiselect("Filter Source Language", options=LANGUAGES_POOL, key="filter_src")
        search_tgt = st.multiselect("Filter Target Language", options=LANGUAGES_POOL, key="filter_tgt")
        
        # Row 2: Selectboxes arranged in a balanced layout grid to provide plenty of text space
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            filter_task = st.selectbox("Filter by Task Type", options=["All"] + TASK_TYPE_OPTIONS, key="filter_task_select")
        with filter_col2:
            filter_stat = st.selectbox("Filter by Workspace Status", options=["All"] + STATUS_OPTIONS, key="filter_status_select")

    # Apply logical filtering criteria arrays
    df_filtered = df_db.copy()
    
    if search_src:
        df_filtered = df_filtered[df_filtered["Source Language"].apply(lambda x: any(lang.strip() in [s.strip() for s in str(x).split(",")] for lang in search_src))]
    if search_tgt:
        df_filtered = df_filtered[df_filtered["Target Language"].apply(lambda x: any(lang.strip() in [t.strip() for t in str(x).split(",")] for lang in search_tgt))]
    if filter_task != "All":
        df_filtered = df_filtered[df_filtered["Task Type"] == filter_task]
    if filter_stat != "All":
        df_filtered = df_filtered[df_filtered["Status"] == filter_stat]

    # Tabbed Views
    tab_active, tab_archive = st.tabs(["📋 Active Pipeline Workspace", "🗄️ Completed & Performance Archives"])
    
    with tab_active:
        df_active_view = df_filtered[~df_filtered["Status"].isin(["Completed", "Cancelled"])].iloc[::-1].copy()
        if len(df_active_view) == 0:
            st.info("No active production allocations match current search criteria.")
        else:
            st.caption("💡 **VM Action Console:** Adjust **Vendor Cost** or change **Status** cell mapping tracks. PM fields stay locked down automatically.")
            
            edited_active = st.data_editor(
                df_active_view,
                use_container_width=True,
                hide_index=True,
                disabled=["Project ID", "Timestamp", "Source Language", "Target Language", "Task Type", "CAT Tool(s)", "Volume", "Reference File", "Deadline (IST)", "Budget Display", "Client Currency", "Budget Value", "Gross Profit %"],
                column_config={
                    "Status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTIONS, width="large", required=True),
                    "Vendor Cost": st.column_config.NumberColumn("Vendor Cost", help="Enter localized vendor delivery cost parameters", min_value=0.0, step=0.001, format="%f"),
                    "Budget Display": "Client Budget",
                    "Gross Profit %": st.column_config.NumberColumn("Gross Profit %", format="%.1f%%")
                },
                key="active_editor"
            )
            
            if not edited_active.equals(df_active_view):
                for idx, row in edited_active.iterrows():
                    p_id = row["Project ID"]
                    b_val = float(row["Budget Value"])
                    v_cost = float(row["Vendor Cost"])
                    
                    margin = ((b_val - v_cost) / b_val * 100.0) if b_val > 0 else 0.0
                    edited_active.at[idx, "Gross Profit %"] = margin
                    
                    if margin < 40.0 and v_cost > 0:
                        st.warning(f"⚠️ Margin Alert: Project {p_id} drops below target 40% threshold ({margin:.1f}%)")

                # Re-align indexes and save
                df_db.set_index("Project ID", inplace=True)
                edited_active.set_index("Project ID", inplace=True)
                df_db.update(edited_active)
                df_db.reset_index(inplace=True)
                save_database(df_db)
                st.rerun()

    with tab_archive:
        df_archive_view = df_filtered[df_filtered["Status"].isin(["Completed", "Cancelled"])].iloc[::-1].copy()
        if len(df_archive_view) == 0:
            st.info("Archive history queue is currently clear.")
        else:
            st.dataframe(df_archive_view, use_container_width=True, hide_index=True)

    # Report Exporter
    st.markdown("---")
    csv_report = df_db.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Master Production Report (CSV)",
        data=csv_report,
        file_name=f"FIDEL_VM_Report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        type="secondary"
    )
else:
    st.info("💡 No active pipeline requirements registered yet. Use the sidebar form to populate tasks into the tracker matrix.")
