import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & INTAKE SETTINGS
# ==========================================
st.set_page_config(
    page_title="VM Production & Pipeline Tracker",
    page_icon="📊",
    layout="wide"
)

# Initialize data state tracking matrix for the pipeline rows
if "pipeline_data" not in st.session_state:
    st.session_state.pipeline_data = []

# Master list array containing your explicit language directory selections
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

# ==========================================
# 2. SIDEBAR NAVIGATION & INTAKE CONTROL ENGINE
# ==========================================
with st.sidebar:
    st.markdown("### 📥 PM / Sales Project Intake")
    st.write("Use this form to submit upcoming project requirements to the VM pipeline.")
    st.markdown("---")
    
    src_langs = st.multiselect("Source Language(s) *", options=LANGUAGES_POOL)
    tgt_langs = st.multiselect("Target Language(s) *", options=LANGUAGES_POOL)
    
    task_type = st.selectbox("Task Type *", [
        "AI Voice-Over", "Audio Content Check", "Audio Data Collection", 
        "Back Translation (Chars)", "Back Translation (Words)", "Closed Captioning", 
        "Data Annotation", "Data Collection", "Desktop Publishing", "Editing", 
        "Evaluation", "Interpretation", "Machine Translation and Full Post-Editing", 
        "Machine Translation and Light Post-Editing", "Post-Editing", "Proofreading", 
        "Review", "Revision", "Subtitle Integration", "Subtitling", 
        "TEP (Translation, Editing & Proofreading)", "Transcreation", 
        "Transcription", "Translation", "Voice-Over"
    ])
    
    cat_options = [
        "MateCat", "MateSub", "MemoQ", "Phrase", "SDL Trados 2019", 
        "SDL Trados 2021", "SDL Trados 2022", "Similis", "SmartCAT", 
        "Smartling", "Wordfast"
    ]
    selected_tools = st.multiselect("Client CAT Tool *", options=cat_options)
    
    volume = st.text_input("Volume (Words / Minutes) *", placeholder="e.g., 5000 words")
    
    st.markdown("<label style='font-size: 14px;'>Client Deadline Date *</label>", unsafe_allow_html=True)
    deadline_date = st.date_input("Deadline Date", datetime.today(), label_visibility="collapsed")
    
    st.markdown("<label style='font-size: 14px;'>Deadline Time (IST) *</label>", unsafe_allow_html=True)
    col_hr, col_min = st.columns(2)
    with col_hr:
        hours_options = [f"{i:02d}" for i in range(24)]
        selected_hour = st.selectbox("Hour", options=hours_options)
    with col_min:
        minutes_options = [f"{i:02d}" for i in range(60)]
        selected_min = st.selectbox("Minute", options=minutes_options)
        
    st.markdown("<label style='font-size: 14px;'>Client Budget *</label>", unsafe_allow_html=True)
    col_curr, col_amt = st.columns([0.8, 1.2])
    with col_curr:
        currency = st.selectbox("Currency", options=["USD ($)", "JPY (¥)", "INR (₹)"], label_visibility="collapsed")
    with col_amt:
        # Changed step value to 0.001 and removed strict string formatting limits to prevent decimal cutoff drops
        budget_val = st.number_input("Amount", min_value=0.000, step=0.001, format="%f", label_visibility="collapsed")
    
    st.markdown(" ")
    if st.button("Submit to VM Pipeline", use_container_width=True, type="primary"):
        if src_langs and tgt_langs and selected_tools and volume and budget_val > 0:
            src_str = ", ".join(src_langs)
            tgt_str = ", ".join(tgt_langs)
            tools_str = ", ".join(selected_tools)
            formatted_deadline = f"{deadline_date.strftime('%Y-%m-%d')} {selected_hour}:{selected_min} IST"
            
            symbol = currency.split(" ")[1].replace("(", "").replace(")", "")
            
            # Format output presentation to perfectly retain multi-decimal fraction logic string drops
            if "JPY" in currency:
                formatted_budget = f"{symbol}{int(budget_val):,}"
            else:
                # If the value has fractions beyond two decimals, print full precision, else default standard formatting
                formatted_budget = f"{symbol}{budget_val:.3f}".rstrip('0').rstrip('.') if budget_val % 0.01 != 0 else f"{symbol}{budget_val:,.2f}"
            
            new_task = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Source Language": src_str,
                "Target Language": tgt_str,
                "Task Type": task_type,
                "CAT Tool(s)": tools_str,
                "Volume": volume,
                "Deadline (IST)": formatted_deadline,
                "Budget": formatted_budget,
                "Status": "Pipeline Intake"
            }
            st.session_state.pipeline_data.append(new_task)
            st.success("🎯 Task successfully routed to main production queue.")
        else:
            st.error("❌ Form Incomplete. Please specify languages, tools, volume, and budget metrics.")

# ==========================================
# 3. MAIN DASHBOARD FRAME DISPLAY LAYER
# ==========================================
col_icon, col_title = st.columns([0.6, 5.4], vertical_alignment="center")
with col_icon:
    st.markdown(
        "<div style='background-color:#FFFFFF; padding:12px; border-radius:8px; display:flex; justify-content:center; align-items:center; width:70px; height:70px;'>"
        "<span style='font-size:38px; color:#1E3A8A;'>🪢</span>"
        "</div>", 
        unsafe_allow_html=True
    )
with col_title:
    st.markdown("<h1 style='margin: 0; padding: 0; font-size: 2.5rem;'>VM Production & Pipeline Tracker</h1>", unsafe_allow_html=True)

st.write("Track active localization workflows, monitor client budgets against vendor rates, and manage execution states seamlessly.")
st.markdown("---")

if len(st.session_state.pipeline_data) == 0:
    st.info("💡 No active pipeline requirements registered yet. Use the sidebar form to populate tasks into the tracker matrix.")
else:
    df_pipeline = pd.DataFrame(st.session_state.pipeline_data)
    st.dataframe(df_pipeline.iloc[::-1], use_container_width=True, hide_index=True)
