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
        "caption": "EAU 2024/25 & German S3 (V3.0) | NIAGARA, EV-302, Full Dosing Schemas",
        "lang_select": "Select Language / Sprache / Idioma",
        "nav_title": "Navigation",
        "nav_modules": [
            "Diagnosis (TNM)", 
            "EORTC Calculator (Full)", 
            "NMIBC: Treatment & Contraindications", 
            "MIBC: Neoadjuvant (Dosing & NIAGARA)", 
            "Metastatic (EV+Pembro Schema)", 
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
        "nmibc_title": "🟢 NMIBC: Risk, Re-TURB & Instillations",
        "returb_header": "🛑 Re-TURB (Nach-TUR-B) Check",
        "returb_req": "Re-TURB REQUIRED",
        "returb_reasons": "Indications: T1 Stage, Incomplete Resection, or No Muscle in High Risk specimen.",
        "returb_ok": "Re-TURB likely not needed",
        "proto_header": "💉 Instillation Protocols & Contraindications",
        "bcg_tab": "BCG Immunotherapy",
        "mmc_tab": "Mitomycin C",
        "bcg_sched": "**Induction:** Weekly x 6 inst.\n\n**Maintenance (SWOG):** 3 weekly instillations at months 3, 6, 12, 18, 24, 30, 36 (Total 3 years).",
        "bcg_contra_title": "❌ BCG Contraindications:",
        "bcg_contra_list": """
        * **Traumatic Catheterization:** Wait > 7-14 days.
        * **Macroscopic Hematuria:** Risk of systemic absorption.
        * **Active Tuberculosis:** Absolute contraindication.
        * **Immunosuppression:** (HIV, Steroids, Chemo) - Risk of BCG Sepsis.
        * **Febrile Illness / UTI:** Treat infection first.
        """,
        "mmc_sched": "**Early Instillation (SI):** Within 24h post-TURBT (40mg). *Optimized: Dehydration + Alkalinization.*\n\n**Adjuvant:** Weekly x 6, then Monthly x 11 (Total 1 year).",
        "mmc_contra_title": "❌ Mitomycin Contraindications:",
        "mmc_contra_list": """
        * **Bladder Perforation:** High risk of extraperitoneal extravasation (Chemical Peritonitis).
        * **Uncontrolled UTI.**
        * **Known Hypersensitivity** to Mitomycin.
        """,

        # MIBC Dosing
        "mibc_title": "🟠 MIBC: Neoadjuvant Therapy (NAC)",
        "cis_fit_q": "Is patient Cisplatin-eligible?",
        "nac_schemas_title": "💊 Neoadjuvant Dosing Schemas (Standard & NIAGARA)",
        
        # 1. Gem-Cis
        "gc_title": "Standard: Gemcitabine + Cisplatin (GC)",
        "gc_details": """
        <span class='sub-dose'>Gemcitabine:</span> 1000 mg/m² IV (Days 1 & 8)<br>
        <span class='sub-dose'>Cisplatin:</span> 70 mg/m² IV (Day 1)<br>
        <span class='sub-dose'>Cycle:</span> Every 21 days (q3w)<br>
        <span class='sub-dose'>Duration:</span> 4 Cycles
        """,
        
        # 2. ddMVAC
        "ddmvac_title": "Alternative: Dose-Dense MVAC (ddMVAC)",
        "ddmvac_details": """
        <span class='sub-dose'>Methotrexate:</span> 30 mg/m² IV (Day 1)<br>
        <span class='sub-dose'>Vinblastine:</span> 3 mg/m² IV (Day 2)<br>
        <span class='sub-dose'>Doxorubicin:</span> 30 mg/m² IV (Day 2)<br>
        <span class='sub-dose'>Cisplatin:</span> 70 mg/m² IV (Day 2)<br>
        <span class='sub-dose'>Support:</span> G-CSF (Pegfilgrastim) Day 3 (or 3-9)<br>
        <span class='sub-dose'>Cycle:</span> Every 14 days (q2w)<br>
        <span class='sub-dose'>Duration:</span> 4 Cycles
        """,
        
        # 3. NIAGARA
        "niagara_title": "🆕 NIAGARA: Durvalumab + Gem/Cis",
        "niagara_details": """
        **Pre-Operative (4 Cycles, q3w):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg IV (Day 1)<br>
        <span class='sub-dose'>Gemcitabine:</span> 1000 mg/m² IV (Days 1 & 8)<br>
        <span class='sub-dose'>Cisplatin:</span> 70 mg/m² IV (Day 1)<br>
        <hr>
        **-- RADICAL CYSTECTOMY --**
        <hr>
        **Post-Operative (Adjuvant):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg IV every 4 weeks<br>
        <span class='sub-dose'>Duration:</span> 8 Cycles (Total 1 year span)
        """,

        "nac_contra_title": "🚫 Contraindications for Cisplatin (Galsky Criteria):",
        "nac_contra_list": """
        1.  **ECOG Performance Status ≥ 2.**
        2.  **GFR < 60 ml/min** (Split dose 45-59 possible, but Carboplatin usually inferior for NAC).
        3.  **Hearing Loss:** Audiometric loss Grade ≥ 2.
        4.  **Peripheral Neuropathy:** Grade ≥ 2.
        5.  **Heart Failure:** NYHA Class III/IV.
        """,

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
        1. Tumor infiltration of Urethra or Bladder Neck.
        2. Renal Insufficiency (GFR < 50 ml/min).
        3. Severe Hepatic Dysfunction.
        4. Inability to perform self-catheterization (mental/physical).
        5. Inflammatory Bowel Disease (Crohn's/Colitis).
        6. Prior high-dose pelvic radiation (risk of anastomotic leak/failure).
        """
    },
    
    "DE": {
        "title": "Klinische Entscheidungshilfe: Harnblasenkarzinom",
        "caption": "EAU 2025 & S3 (V3.0) | NIAGARA, EV-302, Dosis-Schemata",
        "lang_select": "Sprache wählen",
        "nav_title": "Navigation",
        "nav_modules": [
            "Diagnose (TNM)", 
            "EORTC Rechner (Voll)", 
            "NMIBC: Therapie & Kontraindikation", 
            "MIBC: Neoadjuvant (Dosis & NIAGARA)", 
            "Metastasiert (EV+Pembro Schema)", 
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
        "nmibc_title": "🟢 NMIBC: Risiko, Nach-TUR-B & Instillationen",
        "returb_header": "🛑 Nach-TUR-B Check",
        "returb_req": "Nach-TUR-B ERFORDERLICH",
        "returb_reasons": "Indikation: T1-Stadium, Inkomplett, oder kein Muskel bei High Risk.",
        "returb_ok": "Nach-TUR-B wahrscheinlich nicht nötig",
        "proto_header": "💉 Protokolle & Kontraindikationen",
        "bcg_tab": "BCG Immuntherapie",
        "mmc_tab": "Mitomycin C",
        "bcg_sched": "**Induktion:** Wöchentlich x 6.\n\n**Erhaltung (SWOG):** 3 wöchentliche Gaben in den Monaten 3, 6, 12, 18, 24, 30, 36.",
        "bcg_contra_title": "❌ BCG Kontraindikationen:",
        "bcg_contra_list": """
        * **Traumatischer Katheter:** Wartezeit > 7-14 Tage.
        * **Makrohämaturie:** Gefahr der systemischen Absorption.
        * **Aktive Tuberkulose:** Absolute Kontraindikation.
        * **Immunsuppression:** (HIV, Steroide) - Gefahr der BCG-Sepsis.
        * **Fieberhafter Infekt / HWI.**
        """,
        "mmc_sched": "**Frühinstillation (SI):** <24h nach TUR-B (40mg). *Opt: Dehydratation + Alkalisierung.*\n\n**Adjuvant:** Wöchentlich x 6, dann Monatlich x 11.",
        "mmc_contra_title": "❌ Mitomycin Kontraindikationen:",
        "mmc_contra_list": """
        * **Blasenperforation:** Gefahr der extraperitonealen Extravasation.
        * **Unkontrollierter HWI.**
        * **Überempfindlichkeit** gegen Mitomycin.
        """,

        # MIBC Dosing
        "mibc_title": "🟠 MIBC: Neoadjuvante Therapie (NAC)",
        "cis_fit_q": "Ist Patient Cisplatin-geeignet?",
        "nac_schemas_title": "💊 Neoadjuvante Dosis-Schemata",
        
        # 1. Gem-Cis
        "gc_title": "Standard: Gemcitabin + Cisplatin (GC)",
        "gc_details": """
        <span class='sub-dose'>Gemcitabin:</span> 1000 mg/m² i.v. (Tag 1 & 8)<br>
        <span class='sub-dose'>Cisplatin:</span> 70 mg/m² i.v. (Tag 1)<br>
        <span class='sub-dose'>Zyklus:</span> Alle 21 Tage (q3w)<br>
        <span class='sub-dose'>Dauer:</span> 4 Zyklen
        """,
        
        # 2. ddMVAC
        "ddmvac_title": "Alternativ: Dosis-intensiviertes MVAC (ddMVAC)",
        "ddmvac_details": """
        <span class='sub-dose'>Methotrexat:</span> 30 mg/m² i.v. (Tag 1)<br>
        <span class='sub-dose'>Vinblastin:</span> 3 mg/m² i.v. (Tag 2)<br>
        <span class='sub-dose'>Doxorubicin:</span> 30 mg/m² i.v. (Tag 2)<br>
        <span class='sub-dose'>Cisplatin:</span> 70 mg/m² i.v. (Tag 2)<br>
        <span class='sub-dose'>Support:</span> G-CSF (Pegfilgrastim) Tag 3 od. 3-9<br>
        <span class='sub-dose'>Zyklus:</span> Alle 14 Tage (q2w)<br>
        <span class='sub-dose'>Dauer:</span> 4 Zyklen
        """,
        
        # 3. NIAGARA
        "niagara_title": "🆕 NIAGARA: Durvalumab + Gem/Cis",
        "niagara_details": """
        **Prä-Operativ (4 Zyklen, q3w):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg i.v. (Tag 1)<br>
        <span class='sub-dose'>Gemcitabin:</span> 1000 mg/m² i.v. (Tag 1 & 8)<br>
        <span class='sub-dose'>Cisplatin:</span> 70 mg/m² i.v. (Tag 1)<br>
        <hr>
        **-- OPERATION (RC) --**
        <hr>
        **Post-Operativ (Adjuvant):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg i.v. alle 4 Wochen<br>
        <span class='sub-dose'>Dauer:</span> 8 Zyklen (Gesamt 1 Jahr)
        """,

        "nac_contra_title": "🚫 Cisplatin-Kontraindikationen (Galsky):",
        "nac_contra_list": """
        1.  **ECOG PS ≥ 2**
        2.  **GFR < 60 ml/min** (Split-Dose 45-59 möglich).
        3.  **Hörverlust:** Grad ≥ 2 (Audiometrie).
        4.  **Neuropathie:** Grad ≥ 2.
        5.  **Herzinsuffizienz:** NYHA III/IV.
        """,

        # Metastatic
        "meta_title": "🔴 Metastasiert (mUC): EV + Pembro",
        "ev_pembro_header": "🏆 Standard: Enfortumab Vedotin + Pembrolizumab (EV-302)",
        "ev_dose": "**Enfortumab Vedotin:** 1,25 mg/kg (Max 125 mg) i.v. Tage 1 & 8",
        "pembro_dose": "**Pembrolizumab:** 200 mg i.v. Tag 1 (q3w) ODER 400 mg q6w",
        "meta_contra_title": "⚠️ EV+Pembro Kontraindikationen:",
        "meta_contra_list": """
        * **Unkontrollierter Diabetes:** (Hyperglykämie-Risiko!)
        * **Schwere Hautreaktionen:** (SJS/TEN)
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
        1. Tumor in Harnröhre / Blasenhals.
        2. GFR < 50 ml/min.
        3. Leberversagen.
        4. Unfähigkeit zum Selbstkatheterismus.
        5. Chronisch entzündliche Darmerkrankungen (Crohn).
        6. Hochdosis-Bestrahlung Becken.
        """
    },

    "ES": {
        "title": "Soporte de Decisión Clínica: Cáncer de Vejiga",
        "caption": "Guías EAU 2025 & S3 (V3.0) | NIAGARA, EV-302, Esquemas Completos",
        "lang_select": "Seleccionar Idioma",
        "nav_title": "Navegación",
        "nav_modules": [
            "Diagnóstico (TNM)", 
            "Calculadora EORTC (Completa)", 
            "NMIBC: Tratamiento y Contraindicaciones", 
            "MIBC: Neoadyuvancia (Dosis y NIAGARA)", 
            "Metastásico (Esquema EV+Pembro)", 
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
        "nmibc_title": "🟢 NMIBC: Riesgo y Re-RTU",
        "returb_header": "🛑 Chequeo Re-RTU",
        "returb_req": "Re-RTU REQUERIDA",
        "returb_reasons": "Indicación: Estadio T1, Incompleta, o sin músculo en Alto Riesgo.",
        "returb_ok": "No requiere Re-RTU",
        "proto_header": "💉 Protocolos y Contraindicaciones",
        "bcg_tab": "Inmunoterapia BCG",
        "mmc_tab": "Mitomicina C",
        "bcg_sched": "**Inducción:** Semanal x 6.\n\n**Mantenimiento (SWOG):** 3 dosis sem en meses 3, 6, 12, 18, 24, 30, 36 (Total 3 años).",
        "bcg_contra_title": "❌ Contraindicaciones BCG:",
        "bcg_contra_list": """
        * **Catéter Traumático / Hematuria:** Esperar > 7-14 días.
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

        # MIBC Dosing
        "mibc_title": "🟠 MIBC: Neoadyuvancia (NAC)",
        "cis_fit_q": "¿Elegible para Cisplatino?",
        "nac_schemas_title": "💊 Esquemas de Dosis Neoadyuvantes",
        
        # 1. Gem-Cis
        "gc_title": "Estándar: Gemcitabina + Cisplatino (GC)",
        "gc_details": """
        <span class='sub-dose'>Gemcitabina:</span> 1000 mg/m² IV (Días 1 y 8)<br>
        <span class='sub-dose'>Cisplatino:</span> 70 mg/m² IV (Día 1)<br>
        <span class='sub-dose'>Ciclo:</span> Cada 21 días (q3w)<br>
        <span class='sub-dose'>Duración:</span> 4 Ciclos
        """,
        
        # 2. ddMVAC
        "ddmvac_title": "Alternativo: MVAC Dosis-Densa (ddMVAC)",
        "ddmvac_details": """
        <span class='sub-dose'>Metotrexato:</span> 30 mg/m² IV (Día 1)<br>
        <span class='sub-dose'>Vinblastina:</span> 3 mg/m² IV (Día 2)<br>
        <span class='sub-dose'>Doxorrubicina:</span> 30 mg/m² IV (Día 2)<br>
        <span class='sub-dose'>Cisplatino:</span> 70 mg/m² IV (Día 2)<br>
        <span class='sub-dose'>Soporte:</span> G-CSF (Pegfilgrastim) Día 3 o 3-9<br>
        <span class='sub-dose'>Ciclo:</span> Cada 14 días (q2w)<br>
        <span class='sub-dose'>Duración:</span> 4 Ciclos
        """,
        
        # 3. NIAGARA
        "niagara_title": "🆕 NIAGARA: Durvalumab + Gem/Cis",
        "niagara_details": """
        **Pre-Operatorio (4 Ciclos, q3w):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg IV (Día 1)<br>
        <span class='sub-dose'>Gemcitabina:</span> 1000 mg/m² IV (Días 1 y 8)<br>
        <span class='sub-dose'>Cisplatino:</span> 70 mg/m² IV (Día 1)<br>
        <hr>
        **-- CIRUGÍA (RC) --**
        <hr>
        **Post-Operatorio (Adyuvante):**<br>
        <span class='sub-dose'>Durvalumab:</span> 1500 mg IV cada 4 semanas<br>
        <span class='sub-dose'>Duración:</span> 8 Ciclos (Total 1 año)
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
        1. Tumor en Uretra / Cuello.
        2. TFG < 50 ml/min.
        3. Falla Hepática.
        4. Incapaz de Autocateterismo.
        5. EII (Crohn).
        6. Radiación Previa.
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
    # RESTORED FULL LOGIC AS REQUESTED
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
    
    # Num Tumors
    if n_tum == "2-7": rec_score += 3; prog_score += 3
    elif n_tum == "≥ 8": rec_score += 6; prog_score += 3
    # Size
    if size == "≥ 3 cm": rec_score += 3; prog_score += 3
    # Prior
    if prior == "≤ 1/y": rec_score += 2; prog_score += 2
    elif prior == "> 1/y": rec_score += 4; prog_score += 2
    # T
    if t_cat == "T1": rec_score += 1; prog_score += 4
    # CIS
    if cis == "Yes": rec_score += 1; prog_score += 6
    # Grade
    if grade == "G2": rec_score += 1
    elif grade == "G3": rec_score += 2; prog_score += 5

    # Lookup (Simplified text output for brevity of code, but accurate to tables)
    st.divider()
    k1, k2 = st.columns(2)
    with k1:
        st.metric(get_text(lang, 'risk_rec'), f"{rec_score} Points")
        if rec_score == 0: st.write("Risk: Low (15% 1y)")
        elif rec_score <= 4: st.write("Risk: Int-Low (24% 1y)")
        elif rec_score <= 9: st.write("Risk: Int-High (38% 1y)")
        else: st.write("Risk: High (61% 1y)")
        
    with k2:
        st.metric(get_text(lang, 'risk_prog'), f"{prog_score} Points")
        if prog_score == 0: st.write("Risk: Low (0.2% 1y)")
        elif prog_score <= 6: st.write("Risk: Int-Low (1% 1y)")
        elif prog_score <= 13: st.write("Risk: Int-High (5% 1y)")
        else: st.write("Risk: High (17% 1y)")

def render_nmibc_complex(lang):
    st.markdown(f"## {get_text(lang, 'nmibc_title')}")
    
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
                {get_text(lang, 'gc_details')}
            </div>
            """, unsafe_allow_html=True)
            
        # 2. ddMVAC
        with c2:
            st.markdown(f"""
            <div class="schema-box">
                <div class="dose-header">{get_text(lang, 'ddmvac_title')}</div>
                {get_text(lang, 'ddmvac_details')}
            </div>
            """, unsafe_allow_html=True)
            
        # 3. NIAGARA
        with c3:
            st.markdown(f"""
            <div class="schema-box">
                <div class="dose-header">{get_text(lang, 'niagara_title')}</div>
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
    elif mode == modules[1]: render_eortc_calculator_full(lang)
    elif mode == modules[2]: render_nmibc_complex(lang)
    elif mode == modules[3]: render_mibc_niagara_dosings(lang)
    elif mode == modules[4]: render_metastatic_full(lang)
    elif mode == modules[5]: render_surgery_compass(lang)

if __name__ == "__main__":
    main()
