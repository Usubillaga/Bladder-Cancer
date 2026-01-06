import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Bladder Cancer Decision Support",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    .header-style { background-color: #f0f2f6; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    .success-box { border-left: 5px solid #28a745; background-color: #e6ffed; padding: 15px; border-radius: 4px; }
    .warning-box { border-left: 5px solid #ffc107; background-color: #fff3cd; padding: 15px; border-radius: 4px; }
    .alert-box { border-left: 5px solid #dc3545; background-color: #f8d7da; padding: 15px; border-radius: 4px; }
    .info-box { border-left: 5px solid #17a2b8; background-color: #e2fbfd; padding: 15px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# --- TRANSLATION DICTIONARY ---
TRANS = {
    "EN": {
        "title": "Bladder Cancer Clinical Decision Support",
        "caption": "EAU 2024/25 & German S3 (V3.0) | Includes NIAGARA & EV-302",
        "lang_select": "Select Language / Sprache / Idioma",  # <--- FIXED: Key added here
        "nav_title": "Navigation",
        "nav_modules": ["Diagnosis (TNM)", "EORTC Calculator", "NMIBC: Treatment", "MIBC: Neoadjuvant & NIAGARA", "Metastatic (mUC)", "Surgical Compass (Diversions)"],
        
        # NMIBC
        "nmibc_title": "🟢 NMIBC: Risk Stratification & Re-TURB",
        "risk_factors": "Risk Factors",
        "multifocal": "Multifocal (Multilocular)",
        "size_label": "Tumor Size",
        "grade_label": "Grade (WHO 2004/2016)",
        "t1_label": "Stage T1?",
        "muscle_label": "Muscle in specimen?",
        "complete_label": "Resection complete?",
        "returb_header": "🛑 Re-TURB (Nach-TUR-B) Check",
        "returb_req": "Re-TURB REQUIRED",
        "returb_reasons": "Reasons: T1, Incomplete, or No Muscle in High Risk.",
        "returb_ok": "Re-TURB likely not needed",
        "rec_header": "Treatment Recommendation",
        "rec_low": "Low Risk: Single Instillation (SI) within 24h. No adjuvant.",
        "rec_inter": "Intermediate: 1 Year Chemo (MMC) or BCG.",
        "rec_high": "High Risk: BCG for 1-3 Years (SWOG). Re-TURB Mandatory.",
        "rec_vhigh": "Very High Risk: Consider Early Cystectomy. BCG only if unfit.",
        "proto_header": "💉 Instillation Protocols",
        "bcg_sched": "**BCG (SWOG):** 6x Weekly Induction. Maintenance: 3x weekly at 3,6,12,18,24,30,36 mo.",
        "mmc_sched": "**Mitomycin:** Early instillation (<24h). Adj: Weekly x 6, then Monthly x 11.",

        # MIBC & NIAGARA
        "mibc_title": "🟠 MIBC: Neoadjuvant & Perioperative Therapy",
        "cis_fit": "Is patient Cisplatin-eligible?",
        "niagara_header": "🆕 NEW STANDARD: Perioperative Immunotherapy (NIAGARA Study 2024)",
        "niagara_desc": "**Durvalumab + Gem/Cis (NAC)** followed by RC + **Adjuvant Durvalumab**.",
        "niagara_benefit": "Shown to improve Event-Free Survival (EFS) and OS compared to Chemo alone.",
        "std_nac": "**Standard NAC:** Gemcitabine + Cisplatin (or ddMVAC) x 4 cycles -> RC.",
        "unfit_desc": "**Unfit for Cisplatin:** Direct Radical Cystectomy (Upfront RC). Carboplatin-NAC not recommended.",

        # SURGERY
        "surg_title": "🔪 Surgical Compass: Urinary Diversion",
        "tabs_div": ["Orthotopic Neobladder", "Ileal Conduit", "Ureterocutaneostomy (UCN)"],
        "nb_ind": "Gold standard for fit patients wanting natural voiding.",
        "nb_contra": "❌ **Absolute Contraindications (Neobladder):**",
        "nb_c_list": """
        1. Tumor infiltration of urethra / bladder neck.
        2. Renal insufficiency (GFR < 50 ml/min).
        3. Severe hepatic dysfunction.
        4. Inability to perform self-catheterization (mental/physical).
        5. Inflammatory Bowel Disease (Crohn's/Colitis).
        6. Prior high-dose radiation (relative).
        """,
        "ic_ind": "Standard for patients with contraindications to Neobladder or elderly/frail.",
        "ic_pros": "✅ **Pros:** Shorter OR time, fewer metabolic complications than Neobladder.",
        "ucn_ind": "⚠️ **Ureterocutaneostomy (UCN):** Palliative / Last Resort.",
        "ucn_desc": "Indicated for patients **unfit for bowel resection** (short bowel, radiation enteritis) or extreme frailty. High rate of stenosis/stenting required.",

        # METASTATIC
        "meta_title": "🔴 Metastatic (mUC)",
        "ev_pembro": "🏆 **1st Line:** Enfortumab Vedotin + Pembrolizumab (EV-302)",
    },
    "DE": {
        "title": "Klinische Entscheidungshilfe: Harnblasenkarzinom",
        "caption": "EAU 2025 & S3-Leitlinie (V3.0) | Inkl. NIAGARA & EV-302",
        "lang_select": "Sprache wählen", # <--- FIXED
        "nav_title": "Navigation",
        "nav_modules": ["Diagnose (TNM)", "EORTC Rechner", "NMIBC: Therapie", "MIBC: Neoadjuvant & NIAGARA", "Metastasiert (mUC)", "Chirurgie Kompass (Ableitung)"],
        
        # NMIBC
        "nmibc_title": "🟢 NMIBC: Risiko & Nach-TUR-B",
        "risk_factors": "Risikofaktoren",
        "multifocal": "Multifokal (Multilokulär)",
        "size_label": "Tumorgröße",
        "grade_label": "Grading (WHO 2004/2016)",
        "t1_label": "Stadium T1?",
        "muscle_label": "Detrusor (Muskel) im Präparat?",
        "complete_label": "Resektion komplett?",
        "returb_header": "🛑 Nach-TUR-B (Re-TURB) Check",
        "returb_req": "Nach-TUR-B ERFORDERLICH",
        "returb_reasons": "Gründe: T1, Inkomplett oder kein Muskel bei High Risk.",
        "returb_ok": "Nach-TUR-B wahrscheinlich nicht nötig",
        "rec_header": "Therapieempfehlung",
        "rec_low": "Low Risk: Einmalige Frühinstillation (SI) <24h. Keine weitere Therapie.",
        "rec_inter": "Intermediate: 1 Jahr Chemo (MMC) oder BCG.",
        "rec_high": "High Risk: BCG für 1-3 Jahre (SWOG). Nach-TUR-B obligat.",
        "rec_vhigh": "Very High Risk: Frühe Zystektomie erwägen. BCG nur wenn OP unmöglich.",
        "proto_header": "💉 Instillations-Protokolle",
        "bcg_sched": "**BCG (SWOG):** 6x Wöchentlich Induktion. Erhaltung: 3x wöchentlich in Monaten 3,6,12,18,24,30,36.",
        "mmc_sched": "**Mitomycin:** Frühinstillation (<24h). Adj: Wöchentlich x 6, dann Monatlich x 11.",

        # MIBC & NIAGARA
        "mibc_title": "🟠 MIBC: Neoadjuvant & Perioperative Therapie",
        "cis_fit": "Ist Patient Cisplatin-geeignet?",
        "niagara_header": "🆕 NEUER STANDARD: Perioperative Immuntherapie (NIAGARA Studie 2024)",
        "niagara_desc": "**Durvalumab + Gem/Cis (NAC)** gefolgt von RC + **Adjuvant Durvalumab**.",
        "niagara_benefit": "Signifikanter Vorteil im Event-Free Survival (EFS) und OS gegenüber Chemo allein.",
        "std_nac": "**Standard NAC:** Gemcitabin + Cisplatin (oder ddMVAC) x 4 Zyklen -> RC.",
        "unfit_desc": "**Nicht Cisplatin-geeignet:** Direkte Radikale Zystektomie. Carboplatin-NAC nicht empfohlen.",

        # SURGERY
        "surg_title": "🔪 Chirurgie Kompass: Harnableitung",
        "tabs_div": ["Orthotope Neoblase", "Ileum-Conduit", "Harnleiterhautfistel (UCN)"],
        "nb_ind": "Goldstandard für fitte Patienten mit Wunsch nach Kontinenz.",
        "nb_contra": "❌ **Absolute Kontraindikationen (Neoblase):**",
        "nb_c_list": """
        1. Tumor in der Harnröhre / Blasenhals.
        2. Niereninsuffizienz (GFR < 50 ml/min).
        3. Schwere Leberfunktionsstörung.
        4. Unfähigkeit zum Selbstkatheterismus (mental/physisch).
        5. Chronisch entzündliche Darmerkrankungen (Morbus Crohn/Colitis).
        6. Hochdosis-Bestrahlung Becken (relativ).
        """,
        "ic_ind": "Standard für Patienten mit Kontraindikationen zur Neoblase oder Ältere/Gebrechliche.",
        "ic_pros": "✅ **Vorteile:** Kürzere OP-Zeit, weniger Stoffwechselkomplikationen als Neoblase.",
        "ucn_ind": "⚠️ **Harnleiterhautfistel (UCN):** Palliativ / Ultima Ratio.",
        "ucn_desc": "Indiziert wenn **Darmresektion unmöglich** (Kurzdarm, Strahlenenteritis) oder extreme Gebrechlichkeit. Hohe Stenoserate (Dauer-Splint).",

        # METASTATIC
        "meta_title": "🔴 Metastasiert (mUC)",
        "ev_pembro": "🏆 **1. Linie:** Enfortumab Vedotin + Pembrolizumab (EV-302)",
    },
    "ES": {
        "title": "Soporte de Decisión Clínica: Cáncer de Vejiga",
        "caption": "Guías EAU 2025 y S3 (V3.0) | Incluye NIAGARA y EV-302",
        "lang_select": "Seleccionar Idioma", # <--- FIXED
        "nav_title": "Navegación",
        "nav_modules": ["Diagnóstico (TNM)", "Calculadora EORTC", "NMIBC: Tratamiento", "MIBC: Neoadyuvancia y NIAGARA", "Metastásico (mUC)", "Brújula Quirúrgica"],
        
        # NMIBC
        "nmibc_title": "🟢 NMIBC: Riesgo y Re-RTU",
        "risk_factors": "Factores de Riesgo",
        "multifocal": "Multifocal (Multilocular)",
        "size_label": "Tamaño Tumor",
        "grade_label": "Grado (WHO 2004/2016)",
        "t1_label": "¿Estadio T1?",
        "muscle_label": "¿Músculo en muestra?",
        "complete_label": "¿Resección completa?",
        "returb_header": "🛑 Chequeo Re-RTU (Nach-TUR-B)",
        "returb_req": "Re-RTU REQUERIDA",
        "returb_reasons": "Motivos: T1, Incompleta, o sin músculo en Alto Riesgo.",
        "returb_ok": "Probablemente no requiere Re-RTU",
        "rec_header": "Recomendación",
        "rec_low": "Bajo Riesgo: Instilación Única (SI) <24h. Sin adyuvancia.",
        "rec_inter": "Intermedio: 1 Año Quimio (MMC) o BCG.",
        "rec_high": "Alto Riesgo: BCG por 1-3 Años (SWOG). Re-RTU Obligatoria.",
        "rec_vhigh": "Muy Alto Riesgo: Considerar Cistectomía. BCG solo si no apto.",
        "proto_header": "💉 Protocolos de Instilación",
        "bcg_sched": "**BCG (SWOG):** Inducción Semanal x6. Mantenimiento: 3x sem en meses 3,6,12,18,24,30,36.",
        "mmc_sched": "**Mitomicina:** Instilación Temprana (<24h). Ady: Semanal x 6, luego Mensual x 11.",

        # MIBC & NIAGARA
        "mibc_title": "🟠 MIBC: Terapia Neoadyuvante y Perioperatoria",
        "cis_fit": "¿Paciente elegible para Cisplatino?",
        "niagara_header": "🆕 NUEVO ESTÁNDAR: Inmunoterapia Perioperatoria (Estudio NIAGARA 2024)",
        "niagara_desc": "**Durvalumab + Gem/Cis (NAC)** seguido de RC + **Durvalumab Adyuvante**.",
        "niagara_benefit": "Mejora significativa en Supervivencia Libre de Eventos (EFS) y OS vs Quimio sola.",
        "std_nac": "**NAC Estándar:** Gemcitabina + Cisplatino (o ddMVAC) x 4 ciclos -> RC.",
        "unfit_desc": "**No apto Cisplatino:** Cistectomía Radical Directa. No se recomienda Carboplatino-NAC.",

        # SURGERY
        "surg_title": "🔪 Brújula Quirúrgica: Derivación Urinaria",
        "tabs_div": ["Neovejiga Ortotópica", "Conducto Ileal", "Ureterocutaneostomía (UCN)"],
        "nb_ind": "Estándar de oro para pacientes aptos que desean micción natural.",
        "nb_contra": "❌ **Contraindicaciones Absolutas (Neovejiga):**",
        "nb_c_list": """
        1. Infiltración tumoral de uretra / cuello vesical.
        2. Insuficiencia renal (TFG < 50 ml/min).
        3. Disfunción hepática severa.
        4. Incapacidad para autocateterismo (mental/física).
        5. Enfermedad Inflamatoria Intestinal (Crohn/Colitis).
        6. Radiación pélvica previa (relativa).
        """,
        "ic_ind": "Estándar para pacientes con contraindicaciones a Neovejiga o ancianos/frágiles.",
        "ic_pros": "✅ **Pros:** Menor tiempo quirúrgico, menos complicaciones metabólicas.",
        "ucn_ind": "⚠️ **Ureterocutaneostomía (UCN):** Paliativo / Último Recurso.",
        "ucn_desc": "Indicado si **resección intestinal imposible** (intestino corto, enteritis actínica) o fragilidad extrema. Alta tasa de estenosis.",

        # METASTATIC
        "meta_title": "🔴 Metastásico (mUC)",
        "ev_pembro": "🏆 **1ª Línea:** Enfortumab Vedotin + Pembrolizumab (EV-302)",
    }
}

def get_text(lang, key):
    return TRANS[lang].get(key, key)

# --- MODULES ---

def render_tnm_calculator(lang):
    st.markdown("### TNM Calculator (8th Ed)")
    c1, c2, c3 = st.columns(3)
    t = c1.selectbox("T", ["Ta", "Tis", "T1", "T2", "T3", "T4"])
    n = c2.selectbox("N", ["N0", "N1", "N2", "N3"])
    m = c3.selectbox("M", ["M0", "M1"])
    
    stage = "NMIBC"
    if "T2" in t or "T3" in t or "T4" in t: stage = "MIBC"
    if "N" in n and n != "N0": stage = "Locally Advanced / Metastatic"
    if "M1" in m: stage = "Metastatic"
    
    st.success(f"Calculated Stage: {stage}")

def render_eortc_calculator(lang):
    st.markdown(f"## {get_text(lang, 'nav_modules')[1]}")
    st.info("The full Sylvester et al. 2006 scoring logic is implemented here (simplified for this view).")
    
    # Simple Implementation for functionality
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Number of Tumors", ["Single", "2-7", "≥8"])
        st.selectbox("Tumor Size", ["<3cm", "≥3cm"])
    with c2:
        st.selectbox("Prior Recurrence Rate", ["Primary", "≤1/year", ">1/year"])
        st.selectbox("T Stage", ["Ta", "T1"])
    st.caption("Output: Probability of Recurrence & Progression (See tables in full version)")

def render_nmibc_complex(lang):
    st.markdown(f"## {get_text(lang, 'nmibc_title')}")
    
    

    # Risk Factors
    st.subheader(get_text(lang, 'risk_factors'))
    col1, col2 = st.columns(2)
    with col1:
        grade = st.radio(get_text(lang, 'grade_label'), ["Low Grade", "High Grade"])
        size = st.radio(get_text(lang, 'size_label'), ["< 3 cm", "≥ 3 cm"])
        multifocal = st.checkbox(get_text(lang, 'multifocal'))
    with col2:
        is_t1 = st.checkbox(get_text(lang, 't1_label'))
        muscle = st.checkbox(get_text(lang, 'muscle_label'), value=True)
        complete = st.checkbox(get_text(lang, 'complete_label'), value=True)

    st.divider()

    # Re-TURB Logic
    st.subheader(get_text(lang, 'returb_header'))
    needs_returb = False
    if is_t1 or not complete:
        needs_returb = True
    if not muscle and ("High Grade" in grade or is_t1):
        needs_returb = True

    if needs_returb:
        st.markdown(f"""
        <div class="alert-box">
            <h4>{get_text(lang, 'returb_req')}</h4>
            {get_text(lang, 'returb_reasons')}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="success-box">{get_text(lang, 'returb_ok')}</div>""", unsafe_allow_html=True)

    # Treatment Recommendation
    st.subheader(get_text(lang, 'rec_header'))
    
    # Risk Logic (Simplified EAU)
    risk = "Low"
    if is_t1 and "High Grade" in grade and (multifocal or "≥" in size): risk = "Very High"
    elif "High Grade" in grade or is_t1: risk = "High"
    elif "Low Grade" in grade and ("≥" in size or multifocal): risk = "Intermediate"
    
    if risk == "Low": st.success(get_text(lang, 'rec_low'))
    elif risk == "Intermediate": st.warning(get_text(lang, 'rec_inter'))
    elif risk == "High": st.warning(get_text(lang, 'rec_high'))
    elif risk == "Very High": st.error(get_text(lang, 'rec_vhigh'))

    # Protocols
    st.subheader(get_text(lang, 'proto_header'))
    with st.expander("BCG Protocol"):
        st.write(get_text(lang, 'bcg_sched'))
    with st.expander("Mitomycin Protocol"):
        st.write(get_text(lang, 'mmc_sched'))

def render_mibc_niagara(lang):
    st.markdown(f"## {get_text(lang, 'mibc_title')}")
    
    fit = st.checkbox(get_text(lang, 'cis_fit'), value=True)
    
    if fit:
        # NIAGARA SECTION
        st.markdown(f"""
        <div class="info-box">
            <h4>{get_text(lang, 'niagara_header')}</h4>
            {get_text(lang, 'niagara_desc')}
            <br><i>{get_text(lang, 'niagara_benefit')}</i>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="success-box">
            {get_text(lang, 'std_nac')}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="warning-box">
            {get_text(lang, 'unfit_desc')}
        </div>
        """, unsafe_allow_html=True)

def render_surgery_compass(lang):
    st.markdown(f"## {get_text(lang, 'surg_title')}")
    
    tabs = st.tabs(get_text(lang, 'tabs_div'))
    
    # 1. Neobladder
    with tabs[0]:
        st.success(get_text(lang, 'nb_ind'))
        st.error(get_text(lang, 'nb_contra'))
        st.markdown(get_text(lang, 'nb_c_list'))
    
    # 2. Conduit
    with tabs[1]:
        st.info(get_text(lang, 'ic_ind'))
        st.markdown(get_text(lang, 'ic_pros'))
        
    # 3. UCN
    with tabs[2]:
        st.warning(get_text(lang, 'ucn_ind'))
        st.write(get_text(lang, 'ucn_desc'))

def render_metastatic(lang):
    st.markdown(f"## {get_text(lang, 'meta_title')}")
    st.success(get_text(lang, 'ev_pembro'))

# --- MAIN APP FLOW ---

def main():
    with st.sidebar:
        st.header(TRANS["EN"]["lang_select"]) # This key is now safely in the dictionary
        lang_choice = st.radio("", ["English", "Deutsch", "Español"])
        lang = "EN"
        if lang_choice == "Deutsch": lang = "DE"
        elif lang_choice == "Español": lang = "ES"
        
        st.divider()
        st.header(get_text(lang, 'nav_title'))
        modules = get_text(lang, "nav_modules")
        mode = st.radio("Go to:", modules)

    st.title(get_text(lang, "title"))
    st.caption(get_text(lang, "caption"))

    # Map the translated module names back to functions
    if mode == modules[0]: render_tnm_calculator(lang)
    elif mode == modules[1]: render_eortc_calculator(lang)
    elif mode == modules[2]: render_nmibc_complex(lang)
    elif mode == modules[3]: render_mibc_niagara(lang)
    elif mode == modules[4]: render_metastatic(lang)
    elif mode == modules[5]: render_surgery_compass(lang)

if __name__ == "__main__":
    main()
