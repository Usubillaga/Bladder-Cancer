import streamlit as st

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Bladder Cancer Decision Support",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .big-font { font-size:18px !important; }
    .header-style { background-color: #f0f2f6; padding: 10px; border-radius: 5px; }
    .success-box { border-left: 5px solid #28a745; background-color: #e6ffed; padding: 10px; }
    .warning-box { border-left: 5px solid #ffc107; background-color: #fff3cd; padding: 10px; }
    .alert-box { border-left: 5px solid #dc3545; background-color: #f8d7da; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- TRANSLATION DATABASE ---
TRANS = {
    "EN": {
        "title": "Bladder Cancer Clinical Decision Support",
        "caption": "Based on EAU Guidelines 2025 & German S3-Leitlinie (V3.0)",
        "nav_title": "Navigation",
        "nav_modules": ["Diagnosis & Staging", "NMIBC Pathway", "MIBC Pathway", "Metastatic Pathway", "Surgical Compass"],
        "lang_select": "Select Language / Sprache / Idioma",
        "calc_title": "🧮 TNM Calculator & Staging",
        "calc_info": "Based on TNM 8th Edition (UICC/AJCC)",
        "risk_low": "Low Risk",
        "risk_inter": "Intermediate Risk",
        "risk_high": "High Risk",
        "risk_vhigh": "Very High Risk",
        "rec_low": "**Standard:** Single post-operative instillation (e.g., Mitomycin C) within 24h.",
        "rec_inter": "**Standard:** 1 year of BCG (Induction + Maintenance) OR Intravesical Chemotherapy.",
        "rec_high": "**Standard:** Full-dose BCG for 1-3 years (Induction + Maintenance). Re-TURBT mandatory.",
        "rec_vhigh": "🚨 **CLINICAL ALERT:** Consider Early Radical Cystectomy. BCG only if unfit/refused.",
        "nac_fit": "**Gold Standard:** Neoadjuvant Cisplatin-based Chemotherapy (NAC) + Radical Cystectomy.",
        "nac_unfit": "**Recommendation:** Direct Radical Cystectomy (Upfront RC). Evidence for Carboplatin-NAC is weak.",
        "mibc_title": "🟠 Muscle Invasive (MIBC)",
        "meta_title": "🔴 Metastatic / Unresectable (mUC)",
        "ev_pembro": "🏆 **Preferred (New Standard):** Enfortumab Vedotin + Pembrolizumab",
        "surg_title": "🔪 Surgical Compass: Radical Cystectomy",
        "neobladder": "Orthotopic Neobladder",
        "conduit": "Ileal Conduit",
        "contraindications": "**Absolute Contraindications:**",
        "ideal_cand": "**Ideal Candidate:**"
    },
    "DE": {
        "title": "Klinische Entscheidungshilfe: Harnblasenkarzinom",
        "caption": "Basierend auf EAU 2025 & Deutscher S3-Leitlinie (V3.0)",
        "nav_title": "Navigation",
        "nav_modules": ["Diagnose & Staging", "NMIBC Pfad", "MIBC Pfad", "Metastasierter Pfad", "Chirurgie Kompass"],
        "lang_select": "Sprache wählen",
        "calc_title": "🧮 TNM Rechner & Staging",
        "calc_info": "Basiert auf TNM 8. Auflage (UICC/AJCC)",
        "risk_low": "Niedriges Risiko",
        "risk_inter": "Mittleres Risiko",
        "risk_high": "Hohes Risiko",
        "risk_vhigh": "Sehr hohes Risiko",
        "rec_low": "**Standard:** Einmalige postoperative Frühinstillation (z.B. Mitomycin C) innerhalb 24h.",
        "rec_inter": "**Standard:** 1 Jahr BCG (Induktion + Erhaltung) ODER Intravesikale Chemotherapie.",
        "rec_high": "**Standard:** Volldosis BCG für 1-3 Jahre. Nachresektion (Re-TURB) obligatorisch.",
        "rec_vhigh": "🚨 **KLINISCHER ALARM:** Frühe radikale Zystektomie erwägen. BCG nur wenn OP nicht möglich/abgelehnt.",
        "nac_fit": "**Goldstandard:** Neoadjuvante Cisplatin-basierte Chemotherapie (NAC) + Radikale Zystektomie.",
        "nac_unfit": "**Empfehlung:** Direkte Radikale Zystektomie. Evidenz für Carboplatin-NAC ist schwach.",
        "mibc_title": "🟠 Muskelinvasiv (MIBC)",
        "meta_title": "🔴 Metastasiert / Nicht resezierbar (mUC)",
        "ev_pembro": "🏆 **Bevorzugt (Neuer Standard):** Enfortumab Vedotin + Pembrolizumab",
        "surg_title": "🔪 Chirurgie Kompass: Radikale Zystektomie",
        "neobladder": "Orthotope Neoblase",
        "conduit": "Ileum-Conduit",
        "contraindications": "**Absolute Kontraindikationen:**",
        "ideal_cand": "**Idealer Kandidat:**"
    },
    "ES": {
        "title": "Soporte de Decisión Clínica: Cáncer de Vejiga",
        "caption": "Basado en Guías EAU 2025 y S3 Alemana (V3.0)",
        "nav_title": "Navegación",
        "nav_modules": ["Diagnóstico y Estadiaje", "Vía NMIBC", "Vía MIBC", "Vía Metastásica", "Brújula Quirúrgica"],
        "lang_select": "Seleccionar Idioma",
        "calc_title": "🧮 Calculadora TNM y Estadiaje",
        "calc_info": "Basado en TNM 8ª Edición (UICC/AJCC)",
        "risk_low": "Bajo Riesgo",
        "risk_inter": "Riesgo Intermedio",
        "risk_high": "Alto Riesgo",
        "risk_vhigh": "Muy Alto Riesgo",
        "rec_low": "**Estándar:** Instilación postoperatoria única (ej. Mitomicina C) en 24h.",
        "rec_inter": "**Estándar:** 1 año de BCG (Inducción + Mantenimiento) O Quimioterapia Intravesical.",
        "rec_high": "**Estándar:** Dosis completa de BCG por 1-3 años. Re-RTU obligatoria.",
        "rec_vhigh": "🚨 **ALERTA CLÍNICA:** Considerar Cistectomía Radical Temprana. BCG solo si no apto/rehúsa.",
        "nac_fit": "**Estándar de Oro:** Quimioterapia Neoadyuvante basada en Cisplatino (NAC) + Cistectomía.",
        "nac_unfit": "**Recomendación:** Cistectomía Radical Directa. Evidencia para Carboplatino-NAC es débil.",
        "mibc_title": "🟠 Músculo-Invasivo (MIBC)",
        "meta_title": "🔴 Metastásico / Irresecable (mUC)",
        "ev_pembro": "🏆 **Preferido (Nuevo Estándar):** Enfortumab Vedotin + Pembrolizumab",
        "surg_title": "🔪 Brújula Quirúrgica: Cistectomía",
        "neobladder": "Neovejiga Ortotópica",
        "conduit": "Conducto Ileal",
        "contraindications": "**Contraindicaciones Absolutas:**",
        "ideal_cand": "**Candidato Ideal:**"
    }
}

# Helper function to get text
def get_text(lang, key):
    return TRANS[lang].get(key, key)

# --- MODULES ---

def render_tnm_calculator(lang):
    t_key = get_text(lang, "calc_title")
    st.markdown(f"### {t_key}")
    st.info(get_text(lang, "calc_info"))
    
    # Translation maps for dropdowns
    t_map = {"Ta": "Ta", "Tis": "Tis (CIS)", "T1": "T1", "T2": "T2 (Muscle)", "T3": "T3", "T4": "T4"}
    
    col1, col2, col3 = st.columns(3)
    with col1:
        t_stage = st.selectbox("T", list(t_map.keys()))
    with col2:
        n_stage = st.selectbox("N", ["N0", "N1", "N2", "N3"])
    with col3:
        m_stage = st.selectbox("M", ["M0", "M1a", "M1b"])
        
    # Logic remains universal
    stage_group = "Stage 0/I (NMIBC)"
    if "M1" in m_stage: stage_group = "Stage IV (Metastatic)"
    elif "T4b" in t_stage: stage_group = "Stage IVB"
    elif "N" in n_stage and n_stage != "N0": stage_group = "Stage III (Locally Advanced)"
    elif "T2" in t_stage or "T3" in t_stage or "T4" in t_stage: stage_group = "Stage II/III (MIBC)"
    
    st.markdown(f"""
    <div class="header-style">
        <h3 style="margin:0; color:#0e1117;">Result: <span style="color:#d9534f;">{stage_group}</span></h3>
    </div>
    """, unsafe_allow_html=True)

def render_nmibc_module(lang):
    st.markdown(f"## {get_text(lang, 'nav_modules')[1]}") # NMIBC Title
    
    # Inputs (Simplified for brevity, but labels can be translated similarly)
    labels = {
        "EN": ["Low Grade", "High Grade", "< 3cm", ">= 3cm"],
        "DE": ["Low Grade", "High Grade", "< 3cm", ">= 3cm"],
        "ES": ["Bajo Grado", "Alto Grado", "< 3cm", ">= 3cm"]
    }
    l = labels[lang]
    
    col1, col2 = st.columns(2)
    with col1:
        grade = st.radio("Grade (WHO)", [l[0], l[1]])
    with col2:
        size = st.radio("Size/Größe/Tamaño", [l[2], l[3]])
        
    # Logic Mockup
    if grade == l[0] and size == l[2]:
        risk_label = "risk_low"
        rec_label = "rec_low"
        color = "success-box"
    elif grade == l[1]:
        risk_label = "risk_high"
        rec_label = "rec_high"
        color = "warning-box"
    else:
        risk_label = "risk_inter"
        rec_label = "rec_inter"
        color = "warning-box"

    # Display
    st.markdown(f"### {get_text(lang, risk_label)}")
    st.markdown(f"""
    <div class="{color}">
        {get_text(lang, rec_label)}
    </div>
    """, unsafe_allow_html=True)
    
    if risk_label == "risk_high":
        st.error(get_text(lang, "rec_vhigh"))

def render_mibc_module(lang):
    st.markdown(f"## {get_text(lang, 'mibc_title')}")
    
    fit_label = {"EN": "Cisplatin Eligible?", "DE": "Cisplatin-geeignet?", "ES": "¿Elegible para Cisplatino?"}
    cisplatin_fit = st.checkbox(fit_label[lang], value=True)
    
    if cisplatin_fit:
        st.markdown(f"""
        <div class="success-box">
            {get_text(lang, 'nac_fit')}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="warning-box">
            {get_text(lang, 'nac_unfit')}
        </div>
        """, unsafe_allow_html=True)

def render_metastatic_module(lang):
    st.markdown(f"## {get_text(lang, 'meta_title')}")
    
    st.markdown(f"""
    <div class="success-box">
        {get_text(lang, 'ev_pembro')}
    </div>
    """, unsafe_allow_html=True)
    
    # Table logic
    data = {
        "Scenario": ["Post-EV+Pembro", "FGFR3+"],
        "Therapy": ["Platinum Chemo", "Erdafitinib"]
    }
    st.table(data)

def render_surgery_compass(lang):
    st.markdown(f"## {get_text(lang, 'surg_title')}")
    
    tab1, tab2 = st.tabs([get_text(lang, "neobladder"), get_text(lang, "conduit")])
    
    with tab1:
        st.markdown(f"### {get_text(lang, 'neobladder')}")
        col1, col2 = st.columns(2)
        with col1:
            st.error(get_text(lang, "contraindications"))
            if lang == "DE":
                st.write("- Tumor in der Harnröhre")
                st.write("- Schlechte Nierenfunktion (GFR < 50)")
                st.write("- Unfähigkeit zum Selbstkatheterismus")
            elif lang == "ES":
                st.write("- Tumor en la uretra")
                st.write("- Mala función renal (TFG < 50)")
                st.write("- Incapacidad para autocateterismo")
            else:
                st.write("- Tumor in urethra")
                st.write("- Poor renal function (GFR < 50)")
                st.write("- Inability to self-catheterize")
                
        with col2:
            st.success(get_text(lang, "ideal_cand"))
            if lang == "DE":
                st.write("- Motivierter Patient")
                st.write("- Guter Sphinkter-Tonus")
            elif lang == "ES":
                st.write("- Paciente motivado")
                st.write("- Buen tono del esfínter")
            else:
                st.write("- Motivated patient")
                st.write("- Good sphincter tone")

# --- MAIN APP FLOW ---

def main():
    # Language Selector in Sidebar
    st.sidebar.header("Language / Sprache / Idioma")
    lang_choice = st.sidebar.radio("", ["English", "Deutsch", "Español"])
    
    if lang_choice == "Deutsch":
        lang = "DE"
    elif lang_choice == "Español":
        lang = "ES"
    else:
        lang = "EN"

    st.sidebar.divider()
    
    st.title(get_text(lang, "title"))
    st.caption(get_text(lang, "caption"))
    
    # Navigation
    st.sidebar.header(get_text(lang, "nav_title"))
    modules = get_text(lang, "nav_modules")
    mode = st.sidebar.radio("Go to:", modules)

    if mode == modules[0]: # Diagnosis
        render_tnm_calculator(lang)
    elif mode == modules[1]: # NMIBC
        render_nmibc_module(lang)
    elif mode == modules[2]: # MIBC
        render_mibc_module(lang)
    elif mode == modules[3]: # Metastatic
        render_metastatic_module(lang)
    elif mode == modules[4]: # Surgery
        render_surgery_compass(lang)

if __name__ == "__main__":
    main()
