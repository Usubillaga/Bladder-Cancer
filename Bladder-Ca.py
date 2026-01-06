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
    .success-box { border-left: 5px solid #28a745; background-color: #e6ffed; padding: 15px; border-radius: 4px; margin-bottom: 10px; }
    .warning-box { border-left: 5px solid #ffc107; background-color: #fff3cd; padding: 15px; border-radius: 4px; margin-bottom: 10px; }
    .alert-box { border-left: 5px solid #dc3545; background-color: #f8d7da; padding: 15px; border-radius: 4px; margin-bottom: 10px; }
    .info-box { border-left: 5px solid #17a2b8; background-color: #e2fbfd; padding: 15px; border-radius: 4px; margin-bottom: 10px; }
    .schema-box { border: 1px solid #ddd; background-color: #ffffff; padding: 15px; border-radius: 5px; margin-top: 5px; margin-bottom: 10px; }
    .dose-header { font-weight: bold; color: #333; font-size: 1.1em; }
    .dose-detail { font-family: monospace; color: #555; background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# --- TRANSLATION DICTIONARY ---
TRANS = {
    "EN": {
        "title": "Bladder Cancer Clinical Decision Support",
        "caption": "EAU 2024/25 & German S3 (V3.0) | NIAGARA, EV-302, Full Dosing Schemas",
        "lang_select": "Select Language / Sprache / Idioma",
        "nav_title": "Navigation",
        "nav_modules": [
            "Diagnosis (TNM)", 
            "EORTC Calculator", 
            "NMIBC: Treatment & Contraindications", 
            "MIBC: Neoadjuvant (Dosing & NIAGARA)", 
            "Metastatic (EV+Pembro Schema)", 
            "Surgical Compass (Diversions)"
        ],
        
        # NMIBC (Preserved)
        "nmibc_title": "🟢 NMIBC: Risk, Re-TURB & Instillations",
        "returb_header": "🛑 Re-TURB Check",
        "returb_req": "Re-TURB REQUIRED",
        "returb_reasons": "T1, Incomplete, or No Muscle in High Risk.",
        "returb_ok": "Re-TURB likely not needed",
        "proto_header": "💉 Instillation Protocols & Contraindications",
        "bcg_tab": "BCG Immunotherapy",
        "mmc_tab": "Mitomycin C",
        "bcg_sched": "**Induction:** Weekly x 6.\n**Maintenance (SWOG):** 3 weekly instillations at months 3, 6, 12, 18, 24, 30, 36.",
        "bcg_contra_title": "❌ BCG Contraindications:",
        "bcg_contra_list": "* Traumatic Cath / Hematuria (>7-14 days)\n* Active TB\n* Immunosuppression\n* Febrile Illness/UTI",
        "mmc_sched": "**Early:** <24h post-TURBT (40mg).\n**Adjuvant:** Weekly x 6, then Monthly x 11.",
        "mmc_contra_title": "❌ Mitomycin Contraindications:",
        "mmc_contra_list": "* Perforation (Extravasation Risk)\n* Uncontrolled UTI\n* Hypersensitivity",

        # MIBC Dosing & Contraindications
        "mibc_title": "🟠 MIBC: Neoadjuvant Therapy (NAC)",
        "cis_fit_q": "Is patient Cisplatin-eligible?",
        "nac_schemas_title": "💊 Neoadjuvant Dosing Schemas (Standard & NIAGARA)",
        
        # 1. Gem-Cis
        "gc_title": "Standard: Gemcitabine + Cisplatin (GC)",
        "gc_details": """
        * **Gemcitabine:** 1000 mg/m² IV (Days 1 & 8)
        * **Cisplatin:** 70 mg/m² IV (Day 1)
        * **Cycle:** Every 21 days (q3w)
        * **Duration:** 4 Cycles
        """,
        
        # 2. ddMVAC
        "ddmvac_title": "Alternative: Dose-Dense MVAC (ddMVAC)",
        "ddmvac_details": """
        * **Methotrexate:** 30 mg/m² IV (Day 1)
        * **Vinblastine:** 3 mg/m² IV (Day 2)
        * **Doxorubicin:** 30 mg/m² IV (Day 2)
        * **Cisplatin:** 70 mg/m² IV (Day 2)
        * **Support:** G-CSF (Pegfilgrastim) Day 3 or Days 3-9
        * **Cycle:** Every 14 days (q2w)
        * **Duration:** 4 Cycles
        """,
        
        # 3. NIAGARA
        "niagara_title": "🆕 NIAGARA: Durvalumab + Gem/Cis",
        "niagara_details": """
        **Pre-Operative (4 Cycles, q3w):**
        * **Durvalumab:** 1500 mg IV (Day 1)
        * **Gemcitabine:** 1000 mg/m² IV (Days 1 & 8)
        * **Cisplatin:** 70 mg/m² IV (Day 1)
        
        **-- SURGERY (RC) --**
        
        **Post-Operative (Adjuvant):**
        * **Durvalumab:** 1500 mg IV every 4 weeks
        * **Duration:** 8 Cycles (Total treatment span included)
        """,

        "nac_contra_title": "🚫 Contraindications for Cisplatin (Galsky Criteria):",
        "nac_contra_list": """
        1.  **ECOG PS ≥ 2**
        2.  **GFR < 60 ml/min** (Split dose 45-59 possible, but Carboplatin usually inferior for NAC).
        3.  **Hearing Loss:** Grade ≥ 2 (Audiometric).
        4.  **Neuropathy:** Grade ≥ 2.
        5.  **Heart Failure:** NYHA Class III/IV.
        """,

        # Metastatic
        "meta_title": "🔴 Metastatic (mUC): EV + Pembro",
        "ev_pembro_header": "🏆 Standard: Enfortumab Vedotin + Pembrolizumab (EV-302)",
        "ev_dose": "**Enfortumab Vedotin:** 1.25 mg/kg (Max 125 mg) IV Days 1 & 8",
        "pembro_dose": "**Pembrolizumab:** 200 mg IV Day 1 (q3w) OR 400 mg q6w",
        "meta_contra_title": "⚠️ EV+Pembro Contraindications:",
        "meta_contra_list": "* Uncontrolled Diabetes (Hyperglycemia)\n* Severe Cutaneous Reactions (SJS/TEN)\n* Severe Hepatic Impairment (Child-Pugh C)\n* Pre-existing PN > Gr2",

        # Surgery
        "surg_title": "🔪 Surgical Compass",
        "nb_ind": "Neobladder",
        "ic_ind": "Ileal Conduit",
        "ucn_ind": "UCN (Palliative)",
        "nb_contra_title": "❌ Absolute Neobladder Contraindications:",
        "nb_contra_list": "1. Tumor in Urethra\n2. GFR < 50\n3. Liver Failure\n4. Inability to Self-Cath\n5. IBD\n6. High-dose Radiation"
    },
    
    "DE": {
        "title": "Klinische Entscheidungshilfe: Harnblasenkarzinom",
        "caption": "EAU 2025 & S3 (V3.0) | NIAGARA, EV-302, Dosis-Schemata",
        "lang_select": "Sprache wählen",
        "nav_title": "Navigation",
        "nav_modules": [
            "Diagnose (TNM)", 
            "EORTC Rechner", 
            "NMIBC: Therapie & Kontraindikation", 
            "MIBC: Neoadjuvant (Dosis & NIAGARA)", 
            "Metastasiert (EV+Pembro Schema)", 
            "Chirurgie Kompass (Ableitung)"
        ],
        
        # NMIBC
        "nmibc_title": "🟢 NMIBC: Risiko, Nach-TUR-B & Instillationen",
        "returb_header": "🛑 Nach-TUR-B Check",
        "returb_req": "Nach-TUR-B ERFORDERLICH",
        "returb_reasons": "T1, Inkomplett, oder kein Muskel bei High Risk.",
        "returb_ok": "Nach-TUR-B wahrscheinlich nicht nötig",
        "proto_header": "💉 Protokolle & Kontraindikationen",
        "bcg_tab": "BCG Immuntherapie",
        "mmc_tab": "Mitomycin C",
        "bcg_sched": "**Induktion:** Wöchentlich x 6.\n**Erhaltung (SWOG):** 3 Wochen in den Monaten 3, 6, 12, 18, 24, 30, 36.",
        "bcg_contra_title": "❌ BCG Kontraindikationen:",
        "bcg_contra_list": "* Traumat. Katheter / Hämaturie (>7-14 Tage)\n* Aktive Tbc\n* Immunsuppression\n* Fieber/HWI",
        "mmc_sched": "**Früh:** <24h nach TUR-B (40mg).\n**Adjuvant:** Wöchentlich x 6, dann Monatlich x 11.",
        "mmc_contra_title": "❌ Mitomycin Kontraindikationen:",
        "mmc_contra_list": "* Perforation (Extravasation!)\n* Unkontrollierter HWI\n* Überempfindlichkeit",

        # MIBC Dosing
        "mibc_title": "🟠 MIBC: Neoadjuvante Therapie (NAC)",
        "cis_fit_q": "Ist Patient Cisplatin-geeignet?",
        "nac_schemas_title": "💊 Neoadjuvante Dosis-Schemata",
        
        # 1. Gem-Cis
        "gc_title": "Standard: Gemcitabin + Cisplatin (GC)",
        "gc_details": """
        * **Gemcitabin:** 1000 mg/m² i.v. (Tag 1 & 8)
        * **Cisplatin:** 70 mg/m² i.v. (Tag 1)
        * **Zyklus:** Alle 21 Tage (q3w)
        * **Dauer:** 4 Zyklen
        """,
        
        # 2. ddMVAC
        "ddmvac_title": "Alternativ: Dosis-intensiviertes MVAC (ddMVAC)",
        "ddmvac_details": """
        * **Methotrexat:** 30 mg/m² i.v. (Tag 1)
        * **Vinblastin:** 3 mg/m² i.v. (Tag 2)
        * **Doxorubicin:** 30 mg/m² i.v. (Tag 2)
        * **Cisplatin:** 70 mg/m² i.v. (Tag 2)
        * **Support:** G-CSF (Pegfilgrastim) Tag 3 od. 3-9
        * **Zyklus:** Alle 14 Tage (q2w)
        * **Dauer:** 4 Zyklen
        """,
        
        # 3. NIAGARA
        "niagara_title": "🆕 NIAGARA: Durvalumab + Gem/Cis",
        "niagara_details": """
        **Prä-Operativ (4 Zyklen, q3w):**
        * **Durvalumab:** 1500 mg i.v. (Tag 1)
        * **Gemcitabin:** 1000 mg/m² i.v. (Tag 1 & 8)
        * **Cisplatin:** 70 mg/m² i.v. (Tag 1)
        
        **-- OPERATION (RC) --**
        
        **Post-Operativ (Adjuvant):**
        * **Durvalumab:** 1500 mg i.v. alle 4 Wochen
        * **Dauer:** 8 Zyklen (Gesamttherapiedauer beachten)
        """,

        "nac_contra_title": "🚫 Cisplatin-Kontraindikationen (Galsky):",
        "nac_contra_list": """
        1.  **ECOG PS ≥ 2**
        2.  **GFR < 60 ml/min** (Split-Dose 45-59 möglich).
        3.  **Hörverlust:** Grad ≥ 2.
        4.  **Neuropathie:** Grad ≥ 2.
        5.  **Herzinsuffizienz:** NYHA III/IV.
        """,

        # Metastatic
        "meta_title": "🔴 Metastasiert (mUC): EV + Pembro",
        "ev_pembro_header": "🏆 Standard: Enfortumab Vedotin + Pembrolizumab (EV-302)",
        "ev_dose": "**Enfortumab Vedotin:** 1,25 mg/kg (Max 125 mg) i.v. Tage 1 & 8",
        "pembro_dose": "**Pembrolizumab:** 200 mg i.v. Tag 1 (q3w) ODER 400 mg q6w",
        "meta_contra_title": "⚠️ EV+Pembro Kontraindikationen:",
        "meta_contra_list": "* Unkontrollierter Diabetes (Hyperglykämie)\n* Schwere Hautreaktionen (SJS/TEN)\n* Leberinsuffizienz (Child-Pugh C)\n* Vorbestehende PNP > Gr2",

        # Surgery
        "surg_title": "🔪 Chirurgie Kompass",
        "nb_ind": "Neoblase",
        "ic_ind": "Conduit",
        "ucn_ind": "Harnleiterhautfistel",
        "nb_contra_title": "❌ Absolute Neoblasen-Kontraindikationen:",
        "nb_contra_list": "1. Tumor in Harnröhre\n2. GFR < 50\n3. Leberversagen\n4. Unfähigkeit Selbstkatheterismus\n5. CED (Crohn)\n6. Hochdosis-Bestrahlung"
    },

    "ES": {
        "title": "Soporte de Decisión Clínica: Cáncer de Vejiga",
        "caption": "Guías EAU 2025 & S3 (V3.0) | NIAGARA, EV-302, Esquemas Completos",
        "lang_select": "Seleccionar Idioma",
        "nav_title": "Navegación",
        "nav_modules": [
            "Diagnóstico (TNM)", 
            "Calculadora EORTC", 
            "NMIBC: Tratamiento y Contraindicaciones", 
            "MIBC: Neoadyuvancia (Dosis y NIAGARA)", 
            "Metastásico (Esquema EV+Pembro)", 
            "Brújula Quirúrgica"
        ],
        
        # NMIBC
        "nmibc_title": "🟢 NMIBC: Riesgo y Re-RTU",
        "returb_header": "🛑 Chequeo Re-RTU",
        "returb_req": "Re-RTU REQUERIDA",
        "returb_reasons": "T1, Incompleta, o sin músculo en Alto Riesgo.",
        "returb_ok": "No requiere Re-RTU",
        "proto_header": "💉 Protocolos y Contraindicaciones",
        "bcg_tab": "Inmunoterapia BCG",
        "mmc_tab": "Mitomicina C",
        "bcg_sched": "**Inducción:** Semanal x 6.\n**Mantenimiento (SWOG):** 3 dosis sem en meses 3, 6, 12, 18, 24, 30, 36.",
        "bcg_contra_title": "❌ Contraindicaciones BCG:",
        "bcg_contra_list": "* Catéter Traumático / Hematuria (>7-14 días)\n* Tuberculosis Activa\n* Inmunosupresión\n* Fiebre/ITU",
        "mmc_sched": "**Temprana:** <24h post-RTU (40mg).\n**Adyuvante:** Semanal x 6, luego Mensual x 11.",
        "mmc_contra_title": "❌ Contraindicaciones Mitomicina:",
        "mmc_contra_list": "* Perforación (Extravasación)\n* ITU no controlada\n* Hipersensibilidad",

        # MIBC Dosing
        "mibc_title": "🟠 MIBC: Neoadyuvancia (NAC)",
        "cis_fit_q": "¿Elegible para Cisplatino?",
        "nac_schemas_title": "💊 Esquemas de Dosis Neoadyuvantes",
        
        # 1. Gem-Cis
        "gc_title": "Estándar: Gemcitabina + Cisplatino (GC)",
        "gc_details": """
        * **Gemcitabina:** 1000 mg/m² IV (Días 1 y 8)
        * **Cisplatino:** 70 mg/m² IV (Día 1)
        * **Ciclo:** Cada 21 días (q3w)
        * **Duración:** 4 Ciclos
        """,
        
        # 2. ddMVAC
        "ddmvac_title": "Alternativo: MVAC Dosis-Densa (ddMVAC)",
        "ddmvac_details": """
        * **Metotrexato:** 30 mg/m² IV (Día 1)
        * **Vinblastina:** 3 mg/m² IV (Día 2)
        * **Doxorrubicina:** 30 mg/m² IV (Día 2)
        * **Cisplatino:** 70 mg/m² IV (Día 2)
        * **Soporte:** G-CSF (Pegfilgrastim) Día 3 o 3-9
        * **Ciclo:** Cada 14 días (q2w)
        * **Duración:** 4 Ciclos
        """,
        
        # 3. NIAGARA
        "niagara_title": "🆕 NIAGARA: Durvalumab + Gem/Cis",
        "niagara_details": """
        **Pre-Operatorio (4 Ciclos, q3w):**
        * **Durvalumab:** 1500 mg IV (Día 1)
        * **Gemcitabina:** 1000 mg/m² IV (Días 1 y 8)
        * **Cisplatino:** 70 mg/m² IV (Día 1)
        
        **-- CIRUGÍA (RC) --**
        
        **Post-Operatorio (Adyuvante):**
        * **Durvalumab:** 1500 mg IV cada 4 semanas
        * **Duración:** 8 Ciclos
        """,

        "nac_contra_title": "🚫 Contraindicaciones Cisplatino (Galsky):",
        "nac_contra_list": """
        1.  **ECOG PS ≥ 2**
        2.  **TFG < 60 ml/min** (Dosis dividida 45-59 posible).
        3.  **Pérdida Auditiva:** Grado ≥ 2.
        4.  **Neuropatía:** Grado ≥ 2.
        5.  **Insuficiencia Cardíaca:** NYHA III/IV.
        """,

        # Metastatic
        "meta_title": "🔴 Metastásico (mUC): EV + Pembro",
        "ev_pembro_header": "🏆 Estándar: Enfortumab Vedotin + Pembrolizumab (EV-302)",
        "ev_dose": "**Enfortumab Vedotin:** 1.25 mg/kg (Máx 125 mg) IV Días 1 y 8",
        "pembro_dose": "**Pembrolizumab:** 200 mg IV Día 1 (q3w) O 400 mg q6w",
        "meta_contra_title": "⚠️ Contraindicaciones EV+Pembro:",
        "meta_contra_list": "* Diabetes Descontrolada (Hiperglucemia)\n* Reacciones Cutáneas Severas (SJS/TEN)\n* Insuficiencia Hepática (Child-Pugh C)\n* Neuropatía Previa > Gr2",

        # Surgery
        "surg_title": "🔪 Brújula Quirúrgica",
        "nb_ind": "Neovejiga",
        "ic_ind": "Conducto Ileal",
        "ucn_ind": "UCN (Paliativo)",
        "nb_contra_title": "❌ Contraindicaciones Neovejiga:",
        "nb_contra_list": "1. Tumor en Uretra\n2. TFG < 50\n3. Falla Hepática\n4. Incapaz de Autocatet.\n5. EII (Crohn)\n6. Radiación Previa"
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
    st.success(f"Selected: {t} {n} {m}")

def render_eortc_calculator(lang):
    st.markdown(f"## {get_text(lang, 'nav_modules')[1]}")
    st.info("EORTC Risk Calculator (Sylvester et al. 2006)")
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Number of Tumors", ["Single", "2-7", "≥8"])
        st.selectbox("Tumor Size", ["<3cm", "≥3cm"])
    with c2:
        st.selectbox("Prior Recurrence Rate", ["Primary", "≤1/year", ">1/year"])
        st.selectbox("T Stage", ["Ta", "T1"])

def render_nmibc_complex(lang):
    st.markdown(f"## {get_text(lang, 'nmibc_title')}")
    

[Image of bladder cancer staging diagram]


    # Re-TURB
    st.subheader(get_text(lang, 'returb_header'))
    c1, c2 = st.columns(2)
    with c1:
        is_t1 = st.checkbox("T1 Stage?", value=False)
        muscle = st.checkbox("Muscle in specimen?", value=True)
    with c2:
        complete = st.checkbox("Resection complete?", value=True)
        high_grade = st.checkbox("High Grade?", value=False)
        
    needs_returb = False
    if is_t1 or not complete: needs_returb = True
    if not muscle and (high_grade or is_t1): needs_returb = True
    
    if needs_returb:
        st.markdown(f"""<div class="alert-box"><h4>{get_text(lang, 'returb_req')}</h4>{get_text(lang, 'returb_reasons')}</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="success-box">{get_text(lang, 'returb_ok')}</div>""", unsafe_allow_html=True)

    # Protocols
    st.divider()
    st.subheader(get_text(lang, 'proto_header'))
    
    tab_bcg, tab_mmc = st.tabs([get_text(lang, 'bcg_tab'), get_text(lang, 'mmc_tab')])
    
    with tab_bcg:
        st.markdown(get_text(lang, 'bcg_sched'))
        st.markdown(f"""<div class="alert-box"><strong>{get_text(lang, 'bcg_contra_title')}</strong><br>{get_text(lang, 'bcg_contra_list')}</div>""", unsafe_allow_html=True)
        
    with tab_mmc:
        st.markdown(get_text(lang, 'mmc_sched'))
        st.markdown(f"""<div class="alert-box"><strong>{get_text(lang, 'mmc_contra_title')}</strong><br>{get_text(lang, 'mmc_contra_list')}</div>""", unsafe_allow_html=True)

def render_mibc_niagara_dosings(lang):
    st.markdown(f"## {get_text(lang, 'mibc_title')}")
    
    fit = st.checkbox(get_text(lang, 'cis_fit_q'), value=True)
    
    if fit:
        # DOSING SCHEMAS
        st.markdown(f"### {get_text(lang, 'nac_schemas_title')}")
        
        c1, c2, c3 = st.columns(3)
        
        # 1. Gem-Cis
        with c1:
            st.markdown(f"""
            <div class="schema-box">
                <div class="dose-header">{get_text(lang, 'gc_title')}</div>
                <hr>
                {get_text(lang, 'gc_details')}
            </div>
            """, unsafe_allow_html=True)
            
        # 2. ddMVAC
        with c2:
            st.markdown(f"""
            <div class="schema-box">
                <div class="dose-header">{get_text(lang, 'ddmvac_title')}</div>
                <hr>
                {get_text(lang, 'ddmvac_details')}
            </div>
            """, unsafe_allow_html=True)
            
        # 3. NIAGARA
        with c3:
            st.markdown(f"""
            <div class="schema-box">
                <div class="dose-header">{get_text(lang, 'niagara_title')}</div>
                <hr>
                {get_text(lang, 'niagara_details')}
            </div>
            """, unsafe_allow_html=True)
            
    # CONTRAINDICATIONS
    st.markdown(f"""
    <div class="warning-box">
        <strong>{get_text(lang, 'nac_contra_title')}</strong>
        {get_text(lang, 'nac_contra_list')}
    </div>
    """, unsafe_allow_html=True)

def render_metastatic_full(lang):
    st.markdown(f"## {get_text(lang, 'meta_title')}")
    
    st.markdown(f"""<div class="success-box"><h3>{get_text(lang, 'ev_pembro_header')}</h3></div>""", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    # Schema
    with c1:
        st.markdown(f"""
        <div class="schema-box">
            <div class="dose-header">Dosing Schema</div>
            <hr>
            <p>{get_text(lang, 'ev_dose')}</p>
            <p>{get_text(lang, 'pembro_dose')}</p>
            <p><strong>Cycle:</strong> 21 Days (3 Weeks)</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Contraindications
    with c2:
        st.markdown(f"""
        <div class="alert-box">
            <strong>{get_text(lang, 'meta_contra_title')}</strong><br>
            {get_text(lang, 'meta_contra_list')}
        </div>
        """, unsafe_allow_html=True)

def render_surgery_compass(lang):
    st.markdown(f"## {get_text(lang, 'surg_title')}")
    tab1, tab2, tab3 = st.tabs([get_text(lang, 'nb_ind'), get_text(lang, 'ic_ind'), get_text(lang, 'ucn_ind')])
    with tab1:
        st.error(get_text(lang, 'nb_contra_title'))
        st.write(get_text(lang, 'nb_contra_list'))
    with tab2:
        st.info("Standard for those unfit for Neobladder.")
    with tab3:
        st.warning("Palliative / Last Resort.")

# --- MAIN APP FLOW ---

def main():
    with st.sidebar:
        st.header(TRANS["EN"]["lang_select"])
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

    if mode == modules[0]: render_tnm_calculator(lang)
    elif mode == modules[1]: render_eortc_calculator(lang)
    elif mode == modules[2]: render_nmibc_complex(lang)
    elif mode == modules[3]: render_mibc_niagara_dosings(lang)
    elif mode == modules[4]: render_metastatic_full(lang)
    elif mode == modules[5]: render_surgery_compass(lang)

if __name__ == "__main__":
    main()
