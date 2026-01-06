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
    .schema-box { border: 1px solid #ddd; background-color: #ffffff; padding: 15px; border-radius: 5px; margin-top: 5px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .dose-header { font-weight: bold; color: #2c3e50; font-size: 1.1em; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-bottom: 10px; }
    .sub-dose { font-weight: bold; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- TRANSLATION DICTIONARY ---
TRANS = {
    "EN": {
        "title": "Bladder Cancer Clinical Decision Support",
        "caption": "EAU 2025 & German S3 (V3.0) | NIAGARA, EV-302, Full Protocols",
        "lang_select": "Select Language / Sprache / Idioma",
        "nav_title": "Navigation",
        "nav_modules": [
            "Diagnosis (TNM)", 
            "EORTC Calculator (Full)", 
            "NMIBC: Risk, Re-TURB & Protocols", 
            "MIBC: Neoadjuvant (NIAGARA Only)", 
            "Metastatic (EV+Pembro)", 
            "Surgical Compass (Diversions)"
        ],
        
        # EORTC
        "eortc_title": "🔢 EORTC Risk Calculator (Sylvester et al. 2006)",
        "nb_tumors": "Number of Tumors",
        "tum_size": "Tumor Diameter",
        "prior_rec": "Prior Recurrence Rate",
        "t_cat": "T Category",
        "cis": "Concomitant CIS",
        "grade": "Grade (WHO 1973)",
        "risk_rec": "Recurrence Risk",
        "risk_prog": "Progression Risk",
        
        # NMIBC
        "nmibc_title": "🟢 NMIBC: Complex Stratification & Treatment",
        "nmibc_risk_header": "1. Risk Stratification",
        "returb_header": "2. Re-TURB (Nach-TUR-B) Decision",
        "returb_req": "Re-TURB REQUIRED",
        "returb_reasons": "Indications: T1 Stage, Incomplete Resection, or No Muscle in High Risk specimen.",
        "returb_ok": "Re-TURB likely not needed",
        "proto_header": "3. Protocols & Contraindications",
        
        # Risk Groups
        "rg_low": "LOW RISK",
        "rg_inter": "INTERMEDIATE RISK",
        "rg_high": "HIGH RISK",
        "rg_vhigh": "VERY HIGH RISK",
        "rec_low": "Single Instillation (SI) within 24h. No adjuvant treatment.",
        "rec_inter": "Adjuvant: 1 Year Chemotherapy (MMC) OR BCG (Induction + 1y Maint).",
        "rec_high": "Adjuvant: BCG Full Dose (1-3 Years). Re-TURB Mandatory.",
        "rec_vhigh": "Discuss Early Radical Cystectomy. BCG only if unfit/refused.",

        "bcg_tab": "BCG Immunotherapy",
        "mmc_tab": "Mitomycin C",
        "bcg_sched": "**Induction:** Weekly x 6 instillations.\n\n**Maintenance (SWOG):** 3 weekly instillations at months 3, 6, 12, 18, 24, 30, 36 (Total 3 years for High Risk).",
        "bcg_contra_title": "❌ BCG Contraindications:",
        "bcg_contra_list": """
        * **Traumatic Catheterization:** Wait > 7-14 days.
        * **Macroscopic Hematuria:** Risk of systemic absorption (Sepsis).
        * **Active Tuberculosis:** Absolute contraindication.
        * **Immunosuppression:** (HIV, Steroids, Chemo) - Risk of BCG Sepsis.
        * **Febrile Illness / UTI:** Treat infection first.
        * **Previous BCG Sepsis.**
        """,
        "mmc_sched": "**Early Instillation (SI):** Within 24h post-TURBT (40mg). *Optimization: Dehydration (8h) + Oral Alkalinization (NaHCO3).*\n\n**Adjuvant:** Weekly x 6, then Monthly x 11 (Total 1 year).",
        "mmc_contra_title": "❌ Mitomycin Contraindications:",
        "mmc_contra_list": """
        * **Bladder Perforation:** High risk of extraperitoneal extravasation (Chemical Peritonitis/Cystitis).
        * **Uncontrolled UTI.**
        * **Known Hypersensitivity** to Mitomycin.
        """,

        # MIBC NIAGARA
        "mibc_title": "🟠 MIBC: Neoadjuvant Therapy (NAC)",
        "niagara_focus": "💊 REGIMEN: NIAGARA (Durvalumab + Gem/Cis)",
        "cis_fit_q": "Is patient Cisplatin-eligible?",
        "niagara_details": """
        **PRE-OPERATIVE (4 Cycles, q3w):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg IV (Day 1)<br>
        <span class='sub-dose'>Gemcitabine:</span> 1000 mg/m² IV (Days 1 & 8)<br>
        <span class='sub-dose'>Cisplatin:</span> 70 mg/m² IV (Day 1)<br>
        <hr>
        **-- RADICAL CYSTECTOMY (RC) --**
        <hr>
        **POST-OPERATIVE (Adjuvant):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg IV every 4 weeks<br>
        <span class='sub-dose'>Duration:</span> 8 Cycles (Total treatment span approx 1 year)
        """,

        "nac_contra_title": "🚫 Contraindications for Cisplatin (Galsky Criteria):",
        "nac_contra_list": """
        * **ECOG Performance Status ≥ 2.**
        * **GFR < 60 ml/min** (Split dose 45-59 possible, but risky).
        * **Hearing Loss:** Audiometric loss Grade ≥ 2.
        * **Peripheral Neuropathy:** Grade ≥ 2.
        * **Heart Failure:** NYHA Class III/IV.
        """,
        "unfit_msg": "Patient is **UNFIT** for Cisplatin (and thus NIAGARA). Proceed to **Upfront Radical Cystectomy**.",

        # Metastatic
        "meta_title": "🔴 Metastatic (mUC): EV + Pembro",
        "ev_pembro_header": "🏆 Standard: Enfortumab Vedotin + Pembrolizumab (EV-302)",
        "ev_dose": "**Enfortumab Vedotin (EV):** 1.25 mg/kg (Max 125 mg) IV Days 1 & 8",
        "pembro_dose": "**Pembrolizumab:** 200 mg IV Day 1 (q3w) OR 400 mg q6w",
        "meta_contra_title": "⚠️ EV+Pembro Contraindications & Safety:",
        "meta_contra_list": """
        * **Uncontrolled Diabetes:** EV causes severe hyperglycemia (Monitor Glucose!).
        * **Severe Cutaneous Reactions:** History of SJS/TEN.
        * **Severe Hepatic Impairment:** Avoid EV in Child-Pugh C.
        * **Pre-existing Neuropathy:** Grade > 2 (EV cumulative toxicity).
        * **Pneumonitis:** Monitor for IO-related AE.
        """,

        # Surgery
        "surg_title": "🔪 Surgical Compass: Urinary Diversion",
        "nb_ind": "Orthotopic Neobladder",
        "ic_ind": "Ileal Conduit",
        "ucn_ind": "UCN (Ureterocutaneostomy)",
        "nb_contra_title": "❌ Absolute Contraindications for Neobladder:",
        "nb_contra_list": """
        1. Tumor infiltration of **Urethra** or **Bladder Neck**.
        2. Renal Insufficiency (**GFR < 50 ml/min**).
        3. **Severe Hepatic Dysfunction**.
        4. Inability to perform **self-catheterization** (mental/physical/dexterity).
        5. **Inflammatory Bowel Disease** (Crohn's/Colitis).
        6. Prior **high-dose pelvic radiation** (risk of anastomotic leak/failure).
        """
    },
    
    "DE": {
        "title": "Klinische Entscheidungshilfe: Harnblasenkarzinom",
        "caption": "EAU 2025 & S3 (V3.0) | NIAGARA, EV-302, Protokolle",
        "lang_select": "Sprache wählen",
        "nav_title": "Navigation",
        "nav_modules": [
            "Diagnose (TNM)", 
            "EORTC Rechner (Voll)", 
            "NMIBC: Risiko & Therapie", 
            "MIBC: Neoadjuvant (NIAGARA)", 
            "Metastasiert (EV+Pembro)", 
            "Chirurgie Kompass (Ableitung)"
        ],
        
        # EORTC
        "eortc_title": "🔢 EORTC Risikokalkulator (Sylvester et al. 2006)",
        "nb_tumors": "Anzahl der Tumoren",
        "tum_size": "Tumordurchmesser",
        "prior_rec": "Frühere Rezidivrate",
        "t_cat": "T-Kategorie",
        "cis": "Begleitendes CIS",
        "grade": "Grading (WHO 1973)",
        "risk_rec": "Rezidivrisiko",
        "risk_prog": "Progressionsrisiko",
        
        # NMIBC
        "nmibc_title": "🟢 NMIBC: Komplexe Stratifizierung & Therapie",
        "nmibc_risk_header": "1. Risikostratifizierung",
        "returb_header": "2. Nach-TUR-B (Re-TURB) Entscheidung",
        "returb_req": "Nach-TUR-B ERFORDERLICH",
        "returb_reasons": "Indikation: T1-Stadium, Inkomplett, oder kein Muskel bei High Risk.",
        "returb_ok": "Nach-TUR-B wahrscheinlich nicht nötig",
        "proto_header": "3. Protokolle & Kontraindikationen",
        
        "rg_low": "NIEDRIGES RISIKO (Low Risk)",
        "rg_inter": "MITTLERES RISIKO (Intermediate Risk)",
        "rg_high": "HOHES RISIKO (High Risk)",
        "rg_vhigh": "SEHR HOHES RISIKO (Very High Risk)",
        "rec_low": "Einmalige Frühinstillation (SI) <24h. Keine weitere Therapie.",
        "rec_inter": "Adjuvant: 1 Jahr Chemotherapie (MMC) ODER BCG (Induktion + 1 Jahr Erhaltung).",
        "rec_high": "Adjuvant: BCG Volldosis (1-3 Jahre). Nach-TUR-B obligatorisch.",
        "rec_vhigh": "Frühe Zystektomie diskutieren. BCG nur wenn OP unmöglich/abgelehnt.",

        "bcg_tab": "BCG Immuntherapie",
        "mmc_tab": "Mitomycin C",
        "bcg_sched": "**Induktion:** Wöchentlich x 6 Instillationen.\n\n**Erhaltung (SWOG):** 3 wöchentliche Gaben in den Monaten 3, 6, 12, 18, 24, 30, 36 (Gesamt 3 Jahre).",
        "bcg_contra_title": "❌ BCG Kontraindikationen:",
        "bcg_contra_list": """
        * **Traumatischer Katheter:** Wartezeit > 7-14 Tage.
        * **Makrohämaturie:** Gefahr der systemischen Absorption (Sepsis).
        * **Aktive Tuberkulose:** Absolute Kontraindikation.
        * **Immunsuppression:** (HIV, Steroide) - Gefahr der BCG-Sepsis.
        * **Fieberhafter Infekt / HWI.**
        * **Vorherige BCG-Sepsis.**
        """,
        "mmc_sched": "**Frühinstillation (SI):** <24h nach TUR-B (40mg). *Opt: Dehydratation + Alkalisierung.*\n\n**Adjuvant:** Wöchentlich x 6, dann Monatlich x 11 (Gesamt 1 Jahr).",
        "mmc_contra_title": "❌ Mitomycin Kontraindikationen:",
        "mmc_contra_list": """
        * **Blasenperforation:** Gefahr der extraperitonealen Extravasation (Chemische Peritonitis).
        * **Unkontrollierter HWI.**
        * **Überempfindlichkeit** gegen Mitomycin.
        """,

        # MIBC
        "mibc_title": "🟠 MIBC: Neoadjuvante Therapie (NAC)",
        "niagara_focus": "💊 SCHEMA: NIAGARA (Durvalumab + Gem/Cis)",
        "cis_fit_q": "Ist Patient Cisplatin-geeignet?",
        "niagara_details": """
        **PRÄ-OPERATIV (4 Zyklen, q3w):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg i.v. (Tag 1)<br>
        <span class='sub-dose'>Gemcitabin:</span> 1000 mg/m² i.v. (Tag 1 & 8)<br>
        <span class='sub-dose'>Cisplatin:</span> 70 mg/m² i.v. (Tag 1)<br>
        <hr>
        **-- RADIKALE ZYSTEKTOMIE (RC) --**
        <hr>
        **POST-OPERATIV (Adjuvant):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg i.v. alle 4 Wochen<br>
        <span class='sub-dose'>Dauer:</span> 8 Zyklen (Gesamttherapiedauer ca. 1 Jahr)
        """,

        "nac_contra_title": "🚫 Cisplatin-Kontraindikationen (Galsky):",
        "nac_contra_list": """
        * **ECOG PS ≥ 2**
        * **GFR < 60 ml/min** (Split-Dose 45-59 möglich, aber NIAGARA erfordert Cisplatin).
        * **Hörverlust:** Grad ≥ 2 (Audiometrie).
        * **Neuropathie:** Grad ≥ 2.
        * **Herzinsuffizienz:** NYHA III/IV.
        """,
        "unfit_msg": "Patient ist **NICHT GEEIGNET** für Cisplatin (und somit NIAGARA). Vorgehen: **Direkte Radikale Zystektomie**.",

        # Metastatic
        "meta_title": "🔴 Metastasiert (mUC): EV + Pembro",
        "ev_pembro_header": "🏆 Standard: Enfortumab Vedotin + Pembrolizumab (EV-302)",
        "ev_dose": "**Enfortumab Vedotin:** 1,25 mg/kg (Max 125 mg) i.v. Tage 1 & 8",
        "pembro_dose": "**Pembrolizumab:** 200 mg i.v. Tag 1 (q3w) ODER 400 mg q6w",
        "meta_contra_title": "⚠️ EV+Pembro Kontraindikationen:",
        "meta_contra_list": """
        * **Unkontrollierter Diabetes:** (Risiko schwerer Hyperglykämie!)
        * **Schwere Hautreaktionen:** (SJS/TEN in Anamnese)
        * **Leberinsuffizienz:** (Child-Pugh C vermeiden)
        * **Vorbestehende Neuropathie:** > Grad 2
        * **Pneumonitis:** IO-Nebenwirkung beachten.
        """,

        # Surgery
        "surg_title": "🔪 Chirurgie Kompass",
        "nb_ind": "Neoblase",
        "ic_ind": "Conduit",
        "ucn_ind": "Harnleiterhautfistel (UCN)",
        "nb_contra_title": "❌ Absolute Neoblasen-Kontraindikationen:",
        "nb_contra_list": """
        1. Tumor in **Harnröhre** / **Blasenhals**.
        2. Niereninsuffizienz (**GFR < 50 ml/min**).
        3. **Schwere Leberfunktionsstörung**.
        4. Unfähigkeit zum **Selbstkatheterismus** (mental/physisch).
        5. **Chronisch entzündliche Darmerkrankungen** (Crohn).
        6. **Hochdosis-Bestrahlung** Becken.
        """
    },

    "ES": {
        "title": "Soporte de Decisión Clínica: Cáncer de Vejiga",
        "caption": "Guías EAU 2025 & S3 (V3.0) | NIAGARA, EV-302, Protocolos",
        "lang_select": "Seleccionar Idioma",
        "nav_title": "Navegación",
        "nav_modules": [
            "Diagnóstico (TNM)", 
            "Calculadora EORTC (Completa)", 
            "NMIBC: Riesgo & Tratamiento", 
            "MIBC: Neoadyuvancia (NIAGARA)", 
            "Metastásico (EV+Pembro)", 
            "Brújula Quirúrgica"
        ],
        
        # EORTC
        "eortc_title": "🔢 Calculadora EORTC (Sylvester et al. 2006)",
        "nb_tumors": "Número de Tumores",
        "tum_size": "Diámetro del Tumor",
        "prior_rec": "Tasa de Recurrencia Previa",
        "t_cat": "Categoría T",
        "cis": "CIS Concomitante",
        "grade": "Grado (WHO 1973)",
        "risk_rec": "Riesgo de Recurrencia",
        "risk_prog": "Riesgo de Progresión",

        # NMIBC
        "nmibc_title": "🟢 NMIBC: Estratificación y Protocolos",
        "nmibc_risk_header": "1. Estratificación de Riesgo",
        "returb_header": "2. Decisión de Re-RTU (Nach-TUR-B)",
        "returb_req": "Re-RTU REQUERIDA",
        "returb_reasons": "Indicación: Estadio T1, Incompleta, o sin músculo en Alto Riesgo.",
        "returb_ok": "No requiere Re-RTU",
        "proto_header": "3. Protocolos y Contraindicaciones",
        
        "rg_low": "BAJO RIESGO",
        "rg_inter": "RIESGO INTERMEDIO",
        "rg_high": "ALTO RIESGO",
        "rg_vhigh": "MUY ALTO RIESGO",
        "rec_low": "Instilación Única (SI) <24h. Sin tratamiento adicional.",
        "rec_inter": "Adyuvancia: 1 Año Quimioterapia (MMC) O BCG (Inducción + 1a Mantenimiento).",
        "rec_high": "Adyuvancia: BCG Dosis Completa (1-3 Años). Re-RTU Obligatoria.",
        "rec_vhigh": "Discutir Cistectomía Temprana. BCG solo si no apto.",

        "bcg_tab": "Inmunoterapia BCG",
        "mmc_tab": "Mitomicina C",
        "bcg_sched": "**Inducción:** Semanal x 6.\n\n**Mantenimiento (SWOG):** 3 dosis sem en meses 3, 6, 12, 18, 24, 30, 36 (Total 3 años).",
        "bcg_contra_title": "❌ Contraindicaciones BCG:",
        "bcg_contra_list": """
        * **Catéter Traumático:** Esperar > 7-14 días.
        * **Hematuria Macroscópica:** Riesgo de absorción sistémica.
        * **Tuberculosis Activa:** Contraindicación absoluta.
        * **Inmunosupresión:** (VIH, Esteroides) - Riesgo sepsis.
        * **Fiebre / ITU activa.**
        """,
        "mmc_sched": "**Temprana (SI):** <24h post-RTU (40mg). *Opt: Deshidratación + Alcalinización.*\n\n**Adyuvante:** Semanal x 6, luego Mensual x 11.",
        "mmc_contra_title": "❌ Contraindicaciones Mitomicina:",
        "mmc_contra_list": """
        * **Perforación Vesical:** Riesgo de extravasación (Peritonitis Química).
        * **ITU no controlada.**
        * **Hipersensibilidad.**
        """,

        # MIBC
        "mibc_title": "🟠 MIBC: Neoadyuvancia (NAC)",
        "niagara_focus": "💊 ESQUEMA: NIAGARA (Durvalumab + Gem/Cis)",
        "cis_fit_q": "¿Elegible para Cisplatino?",
        "niagara_details": """
        **PRE-OPERATORIO (4 Ciclos, q3w):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg IV (Día 1)<br>
        <span class='sub-dose'>Gemcitabina:</span> 1000 mg/m² IV (Días 1 y 8)<br>
        <span class='sub-dose'>Cisplatino:</span> 70 mg/m² IV (Día 1)<br>
        <hr>
        **-- CISTECTOMÍA RADICAL (RC) --**
        <hr>
        **POST-OPERATORIO (Adyuvante):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg IV cada 4 semanas<br>
        <span class='sub-dose'>Duración:</span> 8 Ciclos (Total 1 año)
        """,

        "nac_contra_title": "🚫 Contraindicaciones Cisplatino (Galsky):",
        "nac_contra_list": """
        * **ECOG PS ≥ 2**
        * **TFG < 60 ml/min** (Dosis dividida 45-59 posible, pero riesgo).
        * **Pérdida Auditiva:** Grado ≥ 2.
        * **Neuropatía:** Grado ≥ 2.
        * **Insuficiencia Cardíaca:** NYHA III/IV.
        """,
        "unfit_msg": "Paciente **NO APTO** para Cisplatino (y por tanto NIAGARA). Proceder a **Cistectomía Radical Directa**.",

        # Metastatic
        "meta_title": "🔴 Metastásico (mUC): EV + Pembro",
        "ev_pembro_header": "🏆 Estándar: Enfortumab Vedotin + Pembrolizumab (EV-302)",
        "ev_dose": "**Enfortumab Vedotin:** 1.25 mg/kg (Máx 125 mg) IV Días 1 y 8",
        "pembro_dose": "**Pembrolizumab:** 200 mg IV Día 1 (q3w) O 400 mg q6w",
        "meta_contra_title": "⚠️ Contraindicaciones EV+Pembro:",
        "meta_contra_list": """
        * **Diabetes Descontrolada:** (Riesgo Hiperglucemia)
        * **Reacciones Cutáneas Severas:** (SJS/TEN)
        * **Insuficiencia Hepática:** (Child-Pugh C)
        * **Neuropatía Previa:** > Grado 2
        """,

        # Surgery
        "surg_title": "🔪 Brújula Quirúrgica",
        "nb_ind": "Neovejiga",
        "ic_ind": "Conducto Ileal",
        "ucn_ind": "UCN (Paliativo)",
        "nb_contra_title": "❌ Contraindicaciones Neovejiga:",
        "nb_contra_list": """
        1. Tumor en **Uretra** / **Cuello**.
        2. **TFG < 50 ml/min**.
        3. **Falla Hepática**.
        4. Incapaz de **Autocateterismo**.
        5. **EII** (Crohn).
        6. **Radiación Previa**.
        """
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

def render_eortc_calculator_full(lang):
    st.markdown(f"## {get_text(lang, 'eortc_title')}")
    st.caption("Calculates Recurrence & Progression Scores (Sylvester et al. 2006)")
    
    # Inputs
    c1, c2 = st.columns(2)
    with c1:
        n_tum = st.radio(get_text(lang, 'nb_tumors'), ["Single", "2-7", "≥ 8"])
        size = st.radio(get_text(lang, 'tum_size'), ["< 3 cm", "≥ 3 cm"])
        prior = st.selectbox(get_text(lang, 'prior_rec'), ["Primary", "≤ 1/y", "> 1/y"])
    with c2:
        t_cat = st.radio(get_text(lang, 't_cat'), ["Ta", "T1"])
        cis = st.radio(get_text(lang, 'cis'), ["No", "Yes"])
        grade = st.radio(get_text(lang, 'grade'), ["G1", "G2", "G3"])

    # Logic
    rec_score, prog_score = 0, 0
    if n_tum == "2-7": rec_score += 3; prog_score += 3
    elif n_tum == "≥ 8": rec_score += 6; prog_score += 3
    if size == "≥ 3 cm": rec_score += 3; prog_score += 3
    if prior == "≤ 1/y": rec_score += 2; prog_score += 2
    elif prior == "> 1/y": rec_score += 4; prog_score += 2
    if t_cat == "T1": rec_score += 1; prog_score += 4
    if cis == "Yes": rec_score += 1; prog_score += 6
    if grade == "G2": rec_score += 1
    elif grade == "G3": rec_score += 2; prog_score += 5

    st.divider()
    k1, k2 = st.columns(2)
    with k1:
        st.metric(get_text(lang, 'risk_rec'), f"{rec_score} Points")
    with k2:
        st.metric(get_text(lang, 'risk_prog'), f"{prog_score} Points")

def render_nmibc_full_restore(lang):
    st.markdown(f"## {get_text(lang, 'nmibc_title')}")
    st.caption("EAU 2024/25 Risk Stratification")
    

[Image of bladder cancer staging diagram]

    
    # 1. RISK STRATIFICATION
    st.markdown(f"### {get_text(lang, 'nmibc_risk_header')}")
    c1, c2 = st.columns(2)
    with c1:
        grade = st.radio("Grade", ["Low Grade (LG)", "High Grade (HG)"])
        size = st.radio("Size", ["< 3 cm", "≥ 3 cm"])
        multifocal = st.checkbox("Multifocal / Multilocular?", value=False)
    with c2:
        is_t1 = st.checkbox("Stage T1?", value=False)
        cis = st.checkbox("Carcinoma In Situ (CIS)?", value=False)
        
    # Logic EAU 2024
    risk_res = ""
    risk_desc = ""
    color = "info-box"
    
    if is_t1 and "High Grade" in grade and (multifocal or "≥" in size or cis):
        risk_res = "rg_vhigh"
        risk_desc = "rec_vhigh"
        color = "alert-box"
    elif "High Grade" in grade or is_t1 or cis:
        risk_res = "rg_high"
        risk_desc = "rec_high"
        color = "warning-box"
    elif "Low Grade" in grade and (multifocal or "≥" in size):
        risk_res = "rg_inter"
        risk_desc = "rec_inter"
        color = "warning-box"
    else:
        risk_res = "rg_low"
        risk_desc = "rec_low"
        color = "success-box"

    st.markdown(f"""
    <div class="{color}">
        <h3>{get_text(lang, risk_res)}</h3>
        <p>{get_text(lang, risk_desc)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # 2. RE-TURB
    st.markdown(f"### {get_text(lang, 'returb_header')}")
    k1, k2 = st.columns(2)
    with k1:
        muscle = st.checkbox("Muscle in specimen?", value=True)
        complete = st.checkbox("Resection complete?", value=True)
    
    needs_returb = False
    if is_t1 or not complete: needs_returb = True
    if not muscle and ("High Grade" in grade or is_t1): needs_returb = True
    
    if needs_returb:
        st.markdown(f"""<div class="alert-box"><h4>{get_text(lang, 'returb_req')}</h4>{get_text(lang, 'returb_reasons')}</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="success-box">{get_text(lang, 'returb_ok')}</div>""", unsafe_allow_html=True)

    # 3. PROTOCOLS
    st.divider()
    st.markdown(f"### {get_text(lang, 'proto_header')}")
    tab_bcg, tab_mmc = st.tabs([get_text(lang, 'bcg_tab'), get_text(lang, 'mmc_tab')])
    
    with tab_bcg:
        st.markdown(get_text(lang, 'bcg_sched'))
        st.markdown(f"""<div class="alert-box"><strong>{get_text(lang, 'bcg_contra_title')}</strong><br>{get_text(lang, 'bcg_contra_list')}</div>""", unsafe_allow_html=True)
        
    with tab_mmc:
        st.markdown(get_text(lang, 'mmc_sched'))
        st.markdown(f"""<div class="alert-box"><strong>{get_text(lang, 'mmc_contra_title')}</strong><br>{get_text(lang, 'mmc_contra_list')}</div>""", unsafe_allow_html=True)

def render_mibc_niagara_only(lang):
    st.markdown(f"## {get_text(lang, 'mibc_title')}")
    
    fit = st.checkbox(get_text(lang, 'cis_fit_q'), value=True)
    
    if fit:
        # ONLY NIAGARA SHOWN
        st.markdown(f"""
        <div class="schema-box">
            <div class="dose-header">{get_text(lang, 'niagara_focus')}</div>
            {get_text(lang, 'niagara_details')}
        </div>
        """, unsafe_allow_html=True)
        
        # CISPLATIN CONTRAINDICATIONS
        st.markdown(f"""
        <div class="warning-box">
            <strong>{get_text(lang, 'nac_contra_title')}</strong>
            {get_text(lang, 'nac_contra_list')}
        </div>
        """, unsafe_allow_html=True)
    else:
        # UNFIT
        st.markdown(f"""<div class="alert-box">{get_text(lang, 'unfit_msg')}</div>""", unsafe_allow_html=True)

def render_metastatic_full(lang):
    st.markdown(f"## {get_text(lang, 'meta_title')}")
    st.markdown(f"""<div class="success-box"><h3>{get_text(lang, 'ev_pembro_header')}</h3></div>""", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="schema-box">
            <div class="dose-header">Dosing Schema</div>
            <p>{get_text(lang, 'ev_dose')}</p>
            <p>{get_text(lang, 'pembro_dose')}</p>
            <p><strong>Cycle:</strong> 21 Days (3 Weeks)</p>
        </div>
        """, unsafe_allow_html=True)
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
        st.markdown(get_text(lang, 'nb_contra_list'))
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
    elif mode == modules[1]: render_eortc_calculator_full(lang)
    elif mode == modules[2]: render_nmibc_full_restore(lang)
    elif mode == modules[3]: render_mibc_niagara_only(lang)
    elif mode == modules[4]: render_metastatic_full(lang)
    elif mode == modules[5]: render_surgery_compass(lang)

if __name__ == "__main__":
    main()
