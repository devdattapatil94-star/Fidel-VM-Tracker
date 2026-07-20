import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# ==========================================
# 1. PAGE CONFIGURATION & DATABASE SETUP
# ==========================================
st.set_page_config(
    page_title="VM Production Control Deck",
    page_icon="💎",
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
            if "Budget Display" not in df.columns:
                if "Budget" in df.columns:
                    df["Budget Display"] = df["Budget"]
                else:
                    df["Budget Display"] = df["Budget Value"].astype(str)
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
    st.markdown("### 📥 Project Intake Panel")
    st.write("Route new project specs directly into the primary production deck.")
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
        selected_hour = st.selectbox("Hour", options=[f"{i:02d}" for i in range(24)], key="pm_hour")
    with col_min:
        selected_min = st.selectbox("Minute", options=[f"{i:02d}" for i in range(60)], key="pm_min")
        
    st.markdown("<label style='font-size: 14px;'>Client Budget *</label>", unsafe_allow_html=True)
    col_curr, col_amt = st.columns([0.8, 1.2])
    with col_curr:
        currency = st.selectbox("Currency", options=["USD ($)", "JPY (¥)", "INR (₹)"], label_visibility="collapsed")
    with col_amt:
        budget_val = st.number_input("Amount", min_value=0.000, step=0.001, format="%f", label_visibility="collapsed")
    
    st.markdown(" ")
    if st.button("Log to Production Deck", use_container_width=True, type="primary"):
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
            st.success(f"🚀 Project {proj_id} registered successfully!")
            st.rerun()
        else:
            st.error("❌ Form Incomplete. Please check mandatory fields.")

# ==========================================
# 3. MAIN WORKSPACE - PRODUCTION CONTROL DECK
# ==========================================
st.markdown(
    "<div style='display: flex; align-items: center; gap: 12px; margin-bottom: 5px;'>"
    "<div style='background-color: #0F172A; color: white; padding: 10px; border-radius: 6px; font-weight: bold; font-size: 22px;'>💎</div>"
    "<div><h2 style='margin: 0; padding: 0; color: #0F172A;'>VM Production Control Deck</h2>"
    "<span style='color: #475569; font-size: 14px;'>Minimalist Streamlined Workflow Center</span></div>"
    "</div>", 
    unsafe_allow_html=True
)
st.markdown("---")

if len(df_db) > 0:
    # Top Metrics Bar
    active_count = len(df_db[df_db["Status"].isin(["Not started", "In progress", "Pending", "Delayed"])])
    usd_tot = df_db[df_db["Client Currency"] == "USD ($)"]["Budget Value"].sum()
    jpy_tot = df_db[df_db["Client Currency"] == "JPY (¥)"]["Budget Value"].sum()
    inr_tot = df_db[df_db["Client Currency"] == "INR (₹)"]["Budget Value"].sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Active Run Track", f"{active_count} Production Projects")
    m2.metric("Total Operational Value", f"${usd_tot:,.2f} USD | ¥{int(jpy_tot):,} JPY")
    m3.metric("Total INR Value", f"₹{inr_tot:,.2f} INR")
    
    st.markdown("---")

    # High-Visibility Filter Bar
    with st.expander("🔍 Filter & Isolate Projects", expanded=True):
        f_src = st.multiselect("Filter Source Language", options=LANGUAGES_POOL)
        f_tgt = st.multiselect("Filter Target Language", options=LANGUAGES_POOL)
        c1, c2 = st.columns(2)
        with c1:
            f_task = st.selectbox("Filter by Task Type", options=["All Tasks"] + TASK_TYPE_OPTIONS)
        with c2:
            f_status = st.selectbox("Filter by Workspace Status", options=["All Statuses"] + STATUS_OPTIONS)

    # Filter Database
    df_filtered = df_db.copy()
    if f_src:
        df_filtered = df_filtered[df_filtered["Source Language"].apply(lambda x: any(l.strip() in [s.strip() for s in str(x).split(",")] for l in f_src))]
    if f_tgt:
        df_filtered = df_filtered[df_filtered["Target Language"].apply(lambda x: any(l.strip() in [t.strip() for t in str(x).split(",")] for l in f_tgt))]
    if f_task != "All Tasks":
        df_filtered = df_filtered[df_filtered["Task Type"] == f_task]
    if f_status != "All Statuses":
        df_filtered = df_filtered[df_filtered["Status"] == f_status]

    st.markdown(f"##### 📑 Active Batches ({len(df_filtered)} items matched)")

    # Render Expanded List Rows
    if df_filtered.empty:
        st.info("No projects match the selected active filter array configuration parameters.")
    else:
        for _, row in df_filtered.iloc[::-1].iterrows():
            pid = row["Project ID"]
            status_text = row["Status"]
            
            # Smart Color Badge Assignment Logic maps
            status_bg = "#E2E8F0"
            status_fg = "#334155"
            if status_text in ["In progress"]: status_bg, status_fg = "#FEF3C7", "#D97706"
            elif status_text in ["Completed"]: status_bg, status_fg = "#D1E7DD", "#0F5132"
            elif status_text in ["Delayed", "Pending"]: status_bg, status_fg = "#F8D7DA", "#842029"
            elif status_text.startswith("In Discussion"): status_bg, status_fg = "#E8DEF8", "#21005D"

            # Check for high-urgency timeline parameters
            is_urgent = False
            try:
                dl_date = datetime.strptime(row["Deadline (IST)"].split(" IST")[0], "%Y-%m-%d %H:%M")
                if datetime.now() <= dl_date <= (datetime.now() + timedelta(hours=24)):
                    is_urgent = True
            except: pass
            
            border_style = "border-left: 6px solid #EF4444; background-color: #FFF5F5;" if is_urgent else "border-left: 6px solid #475569; background-color: #FFFFFF;"
            urgent_tag = "<span style='background-color: #EF4444; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-left: 10px;'>🚨 URGENT</span>" if is_urgent else ""

            # Master Row Blueprint
            st.markdown(
                f"<div style='padding: 18px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 12px; {border_style} border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0;'>"
                f"  <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #E2E8F0; padding-bottom: 8px; margin-bottom: 10px;'>"
                f"      <div><span style='font-size: 16px; font-weight: bold; color: #0F172A;'>📌 ID: {pid}</span>{urgent_tag}</div>"
                f"      <div style='background-color: {status_bg}; color: {status_fg}; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;'>{status_text}</div>"
                f"  </div>"
                f"  <div style='display: flex; flex-wrap: wrap; gap: 24px; color: #334155; font-size: 13.5px;'>"
                f"      <div style='flex: 1; min-width: 250px;'><b>🌐 Lang Pair:</b> {row['Source Language']} ➡️ {row['Target Language']}</div>"
                f"      <div style='flex: 1; min-width: 18px;'><b>⚡ Task:</b> {row['Task Type']}</div>"
                f"      <div style='flex: 1; min-width: 120px;'><b>📊 Volume:</b> {row['Volume']}</div>"
                f"  </div>"
                f"  <div style='display: flex; flex-wrap: wrap; gap: 24px; color: #334155; font-size: 13.5px; margin-top: 8px;'>"
                f"      <div style='flex: 1; min-width: 250px;'><b>📅 Deadline (IST):</b> {row['Deadline (IST)']}</div>"
                f"      <div style='flex: 1; min-width: 18px;'><b>💰 Client Budget:</b> {row['Budget Display']}</div>"
                f"      <div style='flex: 1; min-width: 120px;'><b>📂 Ref File:</b> <span style='color: #475569; font-family: monospace;'>{row['Reference File']}</span></div>"
                f"  </div>"
                f"  <div style='display: flex; flex-wrap: wrap; gap: 24px; color: #334155; font-size: 13.5px; margin-top: 8px; background-color: #F8FAFC; padding: 6px 12px; border-radius: 4px; border: 1px solid #F1F5F9;'>"
                f"      <div><b>💵 Assigned Vendor Cost:</b> {row['Client Currency'].split(' ')[1].replace('(','').replace(')','')}{row['Vendor Cost']:.3f}</div>"
                f"      <div><b>📈 Est. Gross Margin:</b> <span style='font-weight: bold; color: " + ("#16A34A" if float(row['Gross Profit %']) >= 40.0 else "#DC2626") + f";'>{row['Gross Profit %']:.1f}%</span></div>"
                f"  </div>"
                f"</div>",
                unsafe_allow_html=True
            )
            
            # Popover controller stacked natively under row footers perfectly
            with st.popover(f"⚙️ Update Operations: {pid}", use_container_width=True):
                st.markdown(f"**Execution Panel for {pid}**")
                new_status = st.selectbox("Update Progress Track", options=STATUS_OPTIONS, index=STATUS_OPTIONS.index(status_text), key=f"stat_deck_{pid}")
                new_cost = st.number_input("Log Vendor Payout Cost", min_value=0.0, step=0.001, value=float(row["Vendor Cost"]), format="%f", key=f"cost_deck_{pid}")
                
                if st.button("Commit Operational Updates", key=f"btn_deck_{pid}", type="primary"):
                    df_db.set_index("Project ID", inplace=True)
                    df_db.at[pid, "Status"] = new_status
                    df_db.at[pid, "Vendor Cost"] = new_cost
                    
                    b_val = float(row["Budget Value"])
                    df_db.at[pid, "Gross Profit %"] = ((b_val - new_cost) / b_val * 100.0) if b_val > 0 else 0.0
                    
                    df_db.reset_index(inplace=True)
                    save_database(df_db)
                    st.toast(f"💾 Changes committed successfully to {pid}!", icon="✅")
                    st.rerun()

    # Master Report Exporter
    st.markdown("---")
    csv_report = df_db.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📤 Export Live Master Production Log (CSV)",
        data=csv_report,
        file_name=f"FIDEL_Production_Report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        type="secondary"
    )
else:
    st.info("💡 Production database is currently empty. Use the input matrix engine panel on the left to initialize logs.")
