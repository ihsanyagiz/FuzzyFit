import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import datetime
from fuzzy_engine import FuzzyFitSystem

# Page Configuration
st.set_page_config(page_title="FuzzyFit Assistant", page_icon="⚡", layout="wide")

# Initialize Session State for Workout History and Sliders
if 'workout_logs' not in st.session_state:
    st.session_state.workout_logs = []
if 'sleep_val' not in st.session_state:
    st.session_state.sleep_val = 7.0
if 'soreness_val' not in st.session_state:
    st.session_state.soreness_val = 3.0
if 'energy_val' not in st.session_state:
    st.session_state.energy_val = 6.0
if 'stress_val' not in st.session_state:
    st.session_state.stress_val = 4.0

# Localization Dictionary
LANG_DICT = {
    "EN": {
        "title": "⚡ FuzzyFit",
        "subtitle": "Fuzzy Logic-Powered Smart Workout & Recovery Assistant",
        "engine_settings": "⚙️ Engine Settings",
        "defuzz_help": "Test different defuzzification methods for the fuzzy inference system.",
        "defuzz_label": "Defuzzification Method",
        "lang_label": "🌐 Language / Dil",
        "inputs_header": "📋 Daily Physical Status (Inputs)",
        "sleep_label": "😴 Sleep Quality",
        "sleep_help": "0: Very Poor, 10: Excellent",
        "soreness_label": "🤕 Muscle Soreness & Fatigue",
        "soreness_help": "0: No soreness, 10: Severe pain",
        "energy_label": "⚡ Energy & Nutrition Level",
        "energy_help": "0: Severe Deficit/Hungry, 10: High Energy/Caloric Surplus",
        "stress_label": "🤯 Stress Level",
        "stress_help": "0: Very relaxed, 10: Highly stressed",
        "live_fuzz": "🔍 Live Fuzzification (Membership Degrees)",
        "muscles_label": "💪 Target Muscle Groups / Çalışılacak Bölgeler",
        "cardio_label": "🏃 Add Cardio Session / Kardiyo Ekle",
        "cardio_help": "If active, 30% of workout volume is allocated to cardio and shown separately.",
        "outputs_header": "🎯 Workout Recommendation (Outputs)",
        "intensity_res": "Recommended Intensity",
        "volume_res": "Recommended Volume",
        "success_msg": "Inference completed dynamically! (Model: {model}, Method: {method})",
        "protocol_header": "🏃 Actionable Workout Protocol",
        "cardio_header": "🏃 Cardio Session Finisher",
        "cardio_activity": "Cardio Session (Run/Cycle/Row)",
        "cardio_intensity_mod": "Zone 2 (~{intensity:.0f}% Max HR / RPE 6)",
        "cardio_intensity_high": "HIIT Intervals (~{intensity:.0f}% Max HR / RPE 9)",
        "save_log_btn": "💾 Save Recommendation to History Log",
        "save_success": "Workout logged successfully! Check the history dashboard at the bottom.",
        "comp_header": "### 📊 Defuzzification Methods Comparison (Mamdani Only)",
        "comp_desc": "See how different mathematical techniques compute Workout Intensity and Workout Volume given your current physical inputs.",
        "comp_table_title": "Comparison Table",
        "comp_chart_title": "Comparison Chart",
        "details_header": "🔍 Show Fuzzy Logic Details (Fuzzification & Defuzzification Graphs)",
        "details_desc": "The black vertical line represents the Crisp (Defuzzified) value.",
        "int_out": "#### Intensity Output",
        "vol_out": "#### Volume Output",
        "input_fuzz": "#### Input Variables (Fuzzification)",
        "surf_header": "### 📈 Interactive 3D Control Surfaces",
        "surf_desc": "Visualize how two primary inputs affect the output in 3D. Fixed variables are automatically synced with the sliders above!",
        "surf_fixed_soreness_stress": "**Current Fixed Variables:** Muscle Soreness = {soreness:.1f}, Stress = {stress:.1f}",
        "surf_fixed_energy_stress": "**Current Fixed Variables:** Energy Level = {energy:.1f}, Stress = {stress:.1f}",
        "gen_plot_btn_int": "Generate Intensity 3D Plot (~3s)",
        "gen_plot_btn_vol": "Generate Volume 3D Plot (~3s)",
        "calc_surf": "Calculating 3D Surface...",
        "history_header": "📅 Workout History & Analytics Dashboard",
        "history_desc": "Track your workouts over time. Each saved configuration is logged below with detailed charts.",
        "history_empty": "No logs saved yet. Click the 'Save Recommendation to History Log' button above to save your first training recommendation!",
        "history_table_title": "Saved Workouts Log",
        "export_csv_btn": "📥 Export History as CSV",
        "history_chart_title": "Performance Trend Chart",
        "exercise_cols": ["Muscle Group", "Exercise", "Sets", "Reps / Duration", "Target Load / RPE"],
        "cardio_cols": ["Activity", "Duration", "Intensity"],
        "routine_title": "🏃 Workout Routine ({total_sets} Total Strength Sets)",
        "sugeno_msg": "Output membership graphs are specific to Mamdani inference. In Sugeno inference, outputs are calculated as weighted averages of constant singletons: Intensity (Very Light=15%, Light=35%, Moderate=55%, High=75%, Maximum=95%) and Volume (Low=25, Medium=65, High=105 Min)."
    },
    "TR": {
        "title": "⚡ FuzzyFit",
        "subtitle": "Bulanık Mantık Destekli Akıllı Antrenman ve Yenilenme Asistanı",
        "engine_settings": "⚙️ Motor Ayarları",
        "defuzz_help": "Bulanık çıkarım sistemi için farklı durulaştırma yöntemlerini test edin.",
        "defuzz_label": "Durulaştırma Yöntemi",
        "lang_label": "🌐 Dil / Language",
        "inputs_header": "📋 Günlük Fiziksel Durum (Girdiler)",
        "sleep_label": "😴 Uyku Kalitesi",
        "sleep_help": "0: Çok Kötü, 10: Mükemmel",
        "soreness_label": "🤕 Kas Ağrısı ve Yorgunluk",
        "soreness_help": "0: Ağrı yok, 10: Şiddetli acı",
        "energy_label": "⚡ Enerji ve Beslenme Seviyesi",
        "energy_help": "0: Ciddi Kalori Açığı/Açlık, 10: Yüksek Enerji/Kalori Fazlası",
        "stress_label": "🤯 Stres Seviyesi",
        "stress_help": "0: Çok rahat, 10: Çok stresli",
        "live_fuzz": "🔍 Canlı Bulanıklaştırma (Üyelik Dereceleri)",
        "muscles_label": "💪 Çalışılacak Kas Grupları / Bölgeler",
        "cardio_label": "🏃 Kardiyo Seansı Ekle",
        "cardio_help": "Aktif edilirse, antrenman süresinin %30'u kardiyoya ayrılır ve ayrı gösterilir.",
        "outputs_header": "🎯 Antrenman Tavsiyesi (Çıktılar)",
        "intensity_res": "Önerilen Yoğunluk",
        "volume_res": "Önerilen Süre",
        "success_msg": "Bulanık çıkarım dinamik olarak hesaplandı! (Model: {model}, Yöntem: {method})",
        "protocol_header": "🏃 Uygulanabilir Antrenman Programı",
        "cardio_header": "🏃 Kardiyo Bitirici Seansı",
        "cardio_activity": "Kardiyo Seansı (Koşu/Bisiklet/Kürek)",
        "cardio_intensity_mod": "Zone 2 (~%{intensity:.0f} Maks Nabız / RPE 6)",
        "cardio_intensity_high": "HIIT İnterval (~%{intensity:.0f} Maks Nabız / RPE 9)",
        "save_log_btn": "💾 Öneriyi Günlüğe Kaydet",
        "save_success": "Antrenman başarıyla kaydedildi! Sayfanın altındaki geçmiş panelini inceleyin.",
        "comp_header": "### 📊 Durulaştırma Yöntemlerinin Karşılaştırması (Sadece Mamdani)",
        "comp_desc": "Farklı matematiksel durulaştırma tekniklerinin o anki girdilere göre Yoğunluk ve Süreyi nasıl hesapladığını görün.",
        "comp_table_title": "Karşılaştırma Tablosu",
        "comp_chart_title": "Karşılaştırma Grafiği",
        "details_header": "🔍 Bulanık Mantık Detaylarını Göster (Bulanıklaştırma ve Durulaştırma Grafikleri)",
        "details_desc": "Siyah dikey çizgi durulaştırılmış net (crisp) değeri temsil eder.",
        "int_out": "#### Yoğunluk Çıktısı",
        "vol_out": "#### Süre Çıktısı",
        "input_fuzz": "#### Girdi Değişkenleri (Bulanıklaştırma)",
        "surf_header": "### 📈 Etkileşimli 3D Karar Yüzeyleri",
        "surf_desc": "İki temel girdinin çıktıyı 3D uzayda nasıl etkilediğini görselleştirin. Sabit tutulan girdiler yukarıdaki slider'lar ile senkronizedir!",
        "surf_fixed_soreness_stress": "**Sabit Tutulan Değişkenler:** Kas Ağrısı = {soreness:.1f}, Stres = {stress:.1f}",
        "surf_fixed_energy_stress": "**Sabit Tutulan Değişkenler:** Enerji Seviyesi = {energy:.1f}, Stres = {stress:.1f}",
        "gen_plot_btn_int": "Yoğunluk 3D Grafiğini Çiz (~3sn)",
        "gen_plot_btn_vol": "Süre 3D Grafiğini Çiz (~3sn)",
        "calc_surf": "3D Karar Yüzeyi Hesaplanıyor...",
        "history_header": "📅 Antrenman Geçmişi ve Analiz Paneli",
        "history_desc": "Antrenmanlarınızı zaman içinde takip edin. Kaydedilen her öneri aşağıdaki grafikte görselleştirilir.",
        "history_empty": "Henüz kayıtlı antrenman yok. İlk öneriyi kaydetmek için yukarıdaki 'Öneriyi Günlüğe Kaydet' butonuna basın!",
        "history_table_title": "Kaydedilen Antrenman Günlüğü",
        "export_csv_btn": "📥 Geçmişi CSV Olarak İndir",
        "history_chart_title": "Performans Trend Grafiği",
        "exercise_cols": ["Çalışılan Bölge", "Egzersiz", "Set Sayısı", "Tekrar / Süre", "Hedef Ağırlık / RPE"],
        "cardio_cols": ["Aktivite", "Süre", "Yoğunluk"],
        "routine_title": "🏃 Antrenman Programı ({total_sets} Toplam Güç Seti)",
        "sugeno_msg": "Çıktı üyelik grafikleri Mamdani çıkarımına özeldir. Sugeno çıkarımında çıktılar, sabit tekil değerlerin (singletons) ağırlıklı ortalaması olarak hesaplanır: Yoğunluk (Çok Hafif=15, Hafif=35, Orta=55, Yüksek=75, Maksimum=95) ve Süre (Düşük=25, Orta=65, Yüksek=105 Dk)."
    }
}

# Custom CSS
st.markdown("""
<style>
    /* Glow effect for metrics */
    div[data-testid="stMetricValue"] {
        color: #00F0FF !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        font-weight: 800;
        font-size: 3rem !important;
    }
    
    /* Calculate Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #00F0FF 0%, #0080FF 100%);
        color: #000 !important;
        font-weight: 900;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 240, 255, 0.3);
        transition: all 0.3s ease;
        margin-top: 10px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 240, 255, 0.5);
    }
    
    /* Header Gradient Text */
    .gradient-text {
        background: linear-gradient(90deg, #00F0FF, #A855F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0px;
    }
    
    .sub-text {
        color: #94A3B8;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Section Headers */
    h3 {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Page Header with Split Columns for Top-Right Language Option
header_left, header_right = st.columns([6, 1])

with header_right:
    # Small, clean selector placed at the top-right
    lang = st.selectbox("Language / Dil Selection", ["EN", "TR"], label_visibility="collapsed")
    t = LANG_DICT[lang]

with header_left:
    st.markdown(f'<h1 class="gradient-text" style="margin: 0; padding: 0;">{t["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-text" style="margin-top: -5px; margin-bottom: 20px;">{t["subtitle"]}</p>', unsafe_allow_html=True)

# Sidebar for Preset Profiles
st.sidebar.header("📋 Preset Profiles / Hazır Durumlar")
preset_options = {
    "Custom / Özel": "Custom",
    "Rested / Dinlenmiş": "Rested",
    "Exhausted / Çok Yorgun": "Exhausted",
    "Post Leg-Day / Bacak Sonrası": "Post Leg-Day",
    "High Stress / Yüksek Stres": "High Stress"
}
preset_select = st.sidebar.selectbox("Select Profile / Profil Seçin", list(preset_options.keys()))

presets_data = {
    "Custom": None,
    "Rested": {"sleep": 9.0, "soreness": 1.0, "energy": 9.0, "stress": 2.0},
    "Exhausted": {"sleep": 3.0, "soreness": 8.0, "energy": 2.0, "stress": 8.0},
    "Post Leg-Day": {"sleep": 7.0, "soreness": 8.0, "energy": 6.0, "stress": 3.0},
    "High Stress": {"sleep": 4.0, "soreness": 3.0, "energy": 4.0, "stress": 9.0}
}
selected_preset = preset_options[preset_select]

if selected_preset != "Custom":
    preset_vals = presets_data[selected_preset]
    st.session_state.sleep_val = preset_vals["sleep"]
    st.session_state.soreness_val = preset_vals["soreness"]
    st.session_state.energy_val = preset_vals["energy"]
    st.session_state.stress_val = preset_vals["stress"]

# Sidebar for Inference Model (Mamdani vs Sugeno)
st.sidebar.header("🔀 Inference Model / Çıkarım Modeli")
model_type = st.sidebar.selectbox("Model Selection", ["Mamdani", "Sugeno"], 
                                   help="Mamdani outputs are fuzzy sets. Sugeno outputs are weighted singletons.")

# Sidebar for Defuzzification Settings
st.sidebar.header(t["engine_settings"])
st.sidebar.markdown(t["defuzz_help"])
defuzz_method = st.sidebar.selectbox(t["defuzz_label"], 
                                     ["centroid", "bisector", "mom", "som", "lom"], 
                                     help="Centroid is the most common. Others use different mathematical area calculations.")

# Initialize Fuzzy System
def get_fuzzy_system():
    return FuzzyFitSystem()

engine = get_fuzzy_system()

st.divider()

# Left column for inputs, Right for outputs (Law of Symmetry and Balance)
col1, col2 = st.columns([1, 1], gap="large")

# Muscle Group translations mapping for display and database
MUSCLES_LOC = {
    "EN": ["Chest (Göğüs)", "Back (Sırt)", "Shoulders (Omuz)", "Legs (Bacak)", "Biceps (Pazı)", "Triceps (Arka Kol)", "Core (Karın)"],
    "TR": ["Chest (Göğüs)", "Back (Sırt)", "Shoulders (Omuz)", "Legs (Bacak)", "Biceps (Pazı)", "Triceps (Arka Kol)", "Core (Karın)"]
}

with col1:
    # Common Region: Grouping inputs inside a bounded container
    with st.container(border=True):
        st.markdown(f"### {t['inputs_header']}")
        
        # Calculate dynamic dominant linguistic label *before* rendering slider
        m_vals_temp = engine.get_membership_values(st.session_state.sleep_val, st.session_state.soreness_val, st.session_state.energy_val, st.session_state.stress_val)
        
        def get_dominant_label(var_key, lang):
            terms = m_vals_temp[var_key]
            dom_term = max(terms, key=terms.get)
            dom_val = terms[dom_term]
            
            t_map = {
                "EN": {"Poor": "Poor", "Average": "Average", "Good": "Good", "Low": "Low", "Moderate": "Moderate", "High": "High", "Deficit": "Deficit", "Balanced": "Balanced", "Surplus": "Surplus", "Normal": "Normal"},
                "TR": {"Poor": "Kötü", "Average": "Ortalama", "Good": "İyi", "Low": "Düşük", "Moderate": "Orta", "High": "Yüksek", "Deficit": "Açık", "Balanced": "Dengeli", "Surplus": "Fazla", "Normal": "Normal"}
            }
            return f" [{t_map[lang][dom_term]} - {dom_val*100:.0f}%]" if dom_val > 0 else ""

        # Sliders bound to session state
        sleep_label_full = t["sleep_label"] + get_dominant_label("Sleep Quality", lang)
        sleep_val = st.slider(sleep_label_full, min_value=0.0, max_value=10.0, key="sleep_val", help=t["sleep_help"])
        
        soreness_label_full = t["soreness_label"] + get_dominant_label("Muscle Soreness", lang)
        soreness_val = st.slider(soreness_label_full, min_value=0.0, max_value=10.0, key="soreness_val", help=t["soreness_help"])
                                  
        energy_label_full = t["energy_label"] + get_dominant_label("Energy Level", lang)
        energy_val = st.slider(energy_label_full, min_value=0.0, max_value=10.0, key="energy_val", help=t["energy_help"])
                               
        stress_label_full = t["stress_label"] + get_dominant_label("Stress Level", lang)
        stress_val = st.slider(stress_label_full, min_value=0.0, max_value=10.0, key="stress_val", help=t["stress_help"])
        
        # Live Fuzzification Dashboard (Gestalt Law of Proximity)
        st.markdown(f"#### {t['live_fuzz']}")
        m_vals = engine.get_membership_values(sleep_val, soreness_val, energy_val, stress_val)
        
        for var_name, terms in m_vals.items():
            translated_var = var_name
            if lang == "TR":
                if var_name == "Sleep Quality": translated_var = "Uyku Kalitesi"
                elif var_name == "Muscle Soreness": translated_var = "Kas Ağrısı & Yorgunluk"
                elif var_name == "Energy Level": translated_var = "Enerji Seviyesi"
                elif var_name == "Stress Level": translated_var = "Stres Seviyesi"
                
            st.markdown(f"**{translated_var}**")
            cols = st.columns(3)
            
            term_keys = list(terms.keys())
            for idx, term_name in enumerate(term_keys):
                term_val = terms[term_name]
                translated_term = term_name
                if lang == "TR":
                    if term_name == "Poor": translated_term = "Kötü"
                    elif term_name == "Average": translated_term = "Ortalama"
                    elif term_name == "Good": translated_term = "İyi"
                    elif term_name == "Low": translated_term = "Düşük"
                    elif term_name == "Moderate": translated_term = "Orta"
                    elif term_name == "High": translated_term = "Yüksek"
                    elif term_name == "Deficit": translated_term = "Açık"
                    elif term_name == "Balanced": translated_term = "Dengeli"
                    elif term_name == "Surplus": translated_term = "Fazla"
                    elif term_name == "Normal": translated_term = "Normal"
                    
                with cols[idx]:
                    st.caption(f"{translated_term}: {term_val*100:.1f}%")
                    st.progress(min(max(term_val, 0.0), 1.0))
        
        st.markdown("---")
        # Target Muscle Groups selection
        target_muscles = st.multiselect(t["muscles_label"],
                                        MUSCLES_LOC[lang],
                                        default=["Chest (Göğüs)", "Back (Sırt)", "Legs (Bacak)"])
        
        # Add Cardio checkbox
        add_cardio = st.checkbox(t["cardio_label"], value=False, help=t["cardio_help"])

# Pool of general exercises for each muscle group (with TR/EN display versions)
EXERCISE_POOL = {
    "Chest (Göğüs)": {
        "EN": ["Flat Barbell Bench Press", "Incline Dumbbell Press", "Pec Deck Flyes", "Dumbbell Flat Bench Press"],
        "TR": ["Düz Bar Bench Press", "Eğimli Dambıl Bench Press", "Pec Deck Kelebek Fly", "Düz Sehpa Dambıl Bench Press"]
    },
    "Back (Sırt)": {
        "EN": ["Pull-ups / Lat Pulldown", "Bent-over Barbell Row", "Seated Cable Row", "Conventional Deadlift"],
        "TR": ["Barfiks / Lat Pulldown", "Eğilerek Barbell Row", "Oturarak Seated Cable Row", "Klasik Deadlift"]
    },
    "Shoulders (Omuz)": {
        "EN": ["Barbell Overhead Press (OHP)", "Dumbbell Lateral Raise", "Face Pulls", "Seated Dumbbell Shoulder Press"],
        "TR": ["Barbell Overhead Press (OHP)", "Dambıl Lateral Omuz Açış", "Face Pulls (Arka Omuz)", "Oturarak Dambıl Omuz Press"]
    },
    "Legs (Bacak)": {
        "EN": ["Barbell Back Squat", "Romanian Deadlift (RDL)", "Leg Press", "Leg Extensions / Curls"],
        "TR": ["Barbell Back Squat", "Romen Deadlift (RDL)", "Leg Press Makinesi", "Bacak Açma ve Bükme (Extensions/Curls)"]
    },
    "Biceps (Pazı)": {
        "EN": ["Barbell Bicep Curl", "Dumbbell Hammer Curl", "Incline Dumbbell Curl", "Cable Curls"],
        "TR": ["Barbell Biceps Curls", "Dambıl Çekiç Curls (Hammer)", "Eğimli Sehpa Dambıl Curls", "Kablo Curls"]
    },
    "Triceps (Arka Kol)": {
        "EN": ["Close-grip Bench Press / Dips", "Cable Tricep Pushdown", "Lying Tricep Extensions (Skullcrushers)", "Overhead Dumbbell Extension"],
        "TR": ["Dar Tutuş Bench Press / Dips", "Kablo Triceps Pushdown", "Alına Triceps Extension (Skullcrusher)", "Baş Üstü Dambıl Extension"]
    },
    "Core (Karın)": {
        "EN": ["Hanging Leg Raise", "Plank (Bodyweight Plank)", "Ab Wheel Rollouts", "Russian Twists"],
        "TR": ["Bara Asılı Bacak Kaldırma (Hanging)", "Plank Duruşu", "Karın Tekerleği (Ab Wheel)", "Rus Rotasyonu (Russian Twist)"]
    }
}

# Helper function to generate workout routine dynamically based on volume and muscles
def generate_workout_routine_dynamic(intensity, volume, target_muscles, add_cardio, lang):
    intensity = float(intensity)
    volume = float(volume)
    
    # 1. Cardio Allocation
    if add_cardio:
        cardio_ratio = 0.3
        cardio_min = round(volume * cardio_ratio, 1)
        strength_min = volume * (1 - cardio_ratio)
    else:
        cardio_min = 0
        strength_min = volume
        
    # 2. Determine Reps and RPE based on intensity
    if intensity >= 75:
        reps_desc = "4-6 reps" if intensity >= 85 else "6-8 reps"
        if lang == "TR":
            rpe_desc = f"Ağır (%{intensity:.1f} 1RM / RPE 9)"
        else:
            rpe_desc = f"Heavy ({intensity:.1f}% 1RM / RPE 9)"
    elif intensity >= 50:
        reps_desc = "8-12 reps"
        if lang == "TR":
            rpe_desc = "Orta Şiddet (RPE 8)"
        else:
            rpe_desc = "Moderate (RPE 8)"
    else:
        reps_desc = "12-15 reps"
        if lang == "TR":
            rpe_desc = "Hafif Şiddet (RPE 6)"
        else:
            rpe_desc = "Light (RPE 6)"
        
    # 3. Calculate Total Target Sets for Strength
    total_sets = max(3, int(strength_min / 4))
    
    # 4. Allocate Sets to Selected Muscles
    selected_muscles = target_muscles if target_muscles else ["Chest (Göğüs)", "Back (Sırt)", "Legs (Bacak)"]
    N = len(selected_muscles)
    
    sets_per_muscle = total_sets // N
    remainder = total_sets % N
    
    exercises = []
    
    for idx, muscle in enumerate(selected_muscles):
        muscle_sets_target = sets_per_muscle + (1 if idx < remainder else 0)
        
        canonical_key = "Chest (Göğüs)"
        for k in EXERCISE_POOL.keys():
            if k.split(" ")[0].lower() in muscle.lower():
                canonical_key = k
                break
                
        pool = EXERCISE_POOL[canonical_key][lang]
        num_exercises = max(1, int(np.ceil(muscle_sets_target / 4.0)))
        
        base_sets = muscle_sets_target // num_exercises
        ex_remainder = muscle_sets_target % num_exercises
        
        for ex_idx in range(num_exercises):
            ex_sets = base_sets + (1 if ex_idx < ex_remainder else 0)
            if ex_sets <= 0:
                continue
                
            ex_name = pool[ex_idx % len(pool)]
            
            current_reps = reps_desc
            if "plank" in ex_name.lower():
                current_reps = "30-60 sec hold" if lang == "EN" else "30-60 sn bekleme"
                
            exercises.append({
                "Muscle Group": muscle.split(" ")[0] if lang == "EN" else (muscle.split(" ")[1].strip("()") if len(muscle.split(" ")) > 1 else muscle),
                "Exercise": ex_name,
                "Sets": str(ex_sets),
                "Reps / Duration": current_reps,
                "Target Load / RPE": rpe_desc
            })
            
    # 5. Build Cardio recommendation
    cardio_recommendation = None
    if add_cardio and cardio_min > 0:
        if lang == "TR":
            cardio_intensity = f"Zone 2 (~%{intensity:.0f} Maks Nabız / RPE 6)"
            if intensity >= 80:
                cardio_intensity = f"HIIT İnterval (~%{intensity:.0f} Maks Nabız / RPE 9)"
            cardio_recommendation = {
                "Aktivite": "Kardiyo Seansı (Koşu/Bisiklet/Kürek)",
                "Süre": f"{cardio_min} Dakika",
                "Yoğunluk": cardio_intensity
            }
        else:
            cardio_intensity = f"Zone 2 (~{intensity:.0f}% Max HR / RPE 6)"
            if intensity >= 80:
                cardio_intensity = f"HIIT Intervals (~{intensity:.0f}% Max HR / RPE 9)"
            cardio_recommendation = {
                "Activity": "Cardio Session (Run/Cycle/Row)",
                "Duration": f"{cardio_min} Min",
                "Intensity": cardio_intensity
            }
        
    routine_title = t["routine_title"].format(total_sets=total_sets, cardio_min=cardio_min)
        
    return routine_title, exercises, cardio_recommendation

# Dynamic Evaluation based on selected Inference Model (Mamdani vs Sugeno)
if model_type == "Sugeno":
    result = engine.evaluate_sugeno(sleep_val, soreness_val, energy_val, stress_val)
else:
    result = engine.evaluate(sleep_val, soreness_val, energy_val, stress_val, defuzz_method=defuzz_method)

intensity_res = result['intensity']
volume_res = result['volume']

with col2:
    # Common Region: Grouping outputs inside a bounded container
    with st.container(border=True):
        st.markdown(f"### {t['outputs_header']}")
        
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric(t["intensity_res"], f"{intensity_res:.1f} %")
        metric_col2.metric(t["volume_res"], f"{volume_res:.1f} Min")
        
        st.success(t["success_msg"].format(model=model_type, method=defuzz_method.upper()))
        
        # Dynamic Workout Generator based on Selected Muscle Groups
        st.markdown("---")
        st.markdown(f"### {t['protocol_header']}")
        routine_desc, exercises_list, cardio_rec = generate_workout_routine_dynamic(intensity_res, volume_res, target_muscles, add_cardio, lang)
        st.write(f"**{routine_desc}**")
        
        df_exercises = pd.DataFrame(exercises_list)
        df_exercises.columns = t["exercise_cols"]
        st.table(df_exercises)
        
        if cardio_rec:
            st.markdown(f"#### {t['cardio_header']}")
            df_cardio = pd.DataFrame([cardio_rec])
            df_cardio.columns = t["cardio_cols"]
            st.table(df_cardio)
        
        # Logging Feature
        if st.button(t["save_log_btn"], use_container_width=True):
            log_entry = {
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Sleep Quality": sleep_val,
                "Muscle Soreness": soreness_val,
                "Energy Level": energy_val,
                "Stress Level": stress_val,
                "Target Muscles": ", ".join([m.split(" ")[0] if lang == "EN" else m.split(" ")[-1].strip("()") for m in target_muscles]),
                "Cardio Included": "Yes" if add_cardio else "No",
                "Inference Model": model_type,
                "Defuzz Method": defuzz_method.upper() if model_type == "Mamdani" else "WEIGHTED AVG",
                "Intensity (%)": round(intensity_res, 1),
                "Volume (Min)": round(volume_res, 1)
            }
            st.session_state.workout_logs.append(log_entry)
            st.toast(t["save_success"], icon="💾")

# Defuzzification Comparison Panel (Only visible for Mamdani)
if model_type == "Mamdani":
    st.divider()
    with st.container(border=True):
        st.markdown(t["comp_header"])
        st.markdown(t["comp_desc"])
        
        methods = ["centroid", "bisector", "mom", "som", "lom"]
        comp_results = []
        for m in methods:
            res = engine.evaluate(sleep_val, soreness_val, energy_val, stress_val, defuzz_method=m)
            comp_results.append({
                "Method" if lang == "EN" else "Yöntem": m.upper(),
                "Intensity (%)" if lang == "EN" else "Yoğunluk (%)": round(res['intensity'], 2),
                "Volume (Min)" if lang == "EN" else "Süre (Dk)": round(res['volume'], 2)
            })
            
        comp_df = pd.DataFrame(comp_results)
        comp_col1, comp_col2 = st.columns([1, 1], gap="large")
        
        with comp_col1:
            st.markdown(f"#### {t['comp_table_title']}")
            st.table(comp_df)
            
        with comp_col2:
            st.markdown(f"#### {t['comp_chart_title']}")
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                x=comp_df["Method" if lang == "EN" else "Yöntem"],
                y=comp_df["Intensity (%)" if lang == "EN" else "Yoğunluk (%)"],
                name='Workout Intensity (%)' if lang == "EN" else 'Antrenman Yoğunluğu (%)',
                marker_color='#00F0FF'
            ))
            fig_comp.add_trace(go.Bar(
                x=comp_df["Method" if lang == "EN" else "Yöntem"],
                y=comp_df["Volume (Min)" if lang == "EN" else "Süre (Dk)"],
                name='Workout Volume (Min)' if lang == "EN" else 'Antrenman Süresi (Dk)',
                marker_color='#A855F7'
            ))
            fig_comp.update_layout(
                barmode='group',
                height=300,
                margin=dict(l=20, r=20, t=10, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E2E8F0'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_comp, use_container_width=True)

# Fuzzy Engine Graphs (Always visible, recomputes dynamically)
st.divider()
with st.expander(t["details_header"], expanded=True):
    st.markdown(t["details_desc"])
    
    with st.container(border=True):
        graph_col1, graph_col2 = st.columns(2)
        
        with graph_col1:
            st.markdown(t["int_out"])
            if model_type == "Mamdani":
                fig_int, ax_int = plt.subplots(figsize=(8, 4))
                try:
                    engine.intensity.view(sim=engine.fitness_sim)
                except (KeyError, ValueError, Exception):
                    st.warning("Could not generate graph (No rule intersection).")
                st.pyplot(plt.gcf())
                plt.close(fig_int)
            else:
                st.info(t["sugeno_msg"])
            
        with graph_col2:
            st.markdown(t["vol_out"])
            if model_type == "Mamdani":
                fig_vol, ax_vol = plt.subplots(figsize=(8, 4))
                try:
                    engine.volume.view(sim=engine.fitness_sim)
                except (KeyError, ValueError, Exception):
                    pass
                st.pyplot(plt.gcf())
                plt.close(fig_vol)
            else:
                st.info(t["sugeno_msg"])
            
        st.divider()
        st.markdown(t["input_fuzz"])
        inputs_col1, inputs_col2 = st.columns(2)
        
        with inputs_col1:
            fig1, ax1 = plt.subplots(figsize=(6, 3))
            engine.sleep.view()
            st.pyplot(plt.gcf())
            plt.close(fig1)
            
            fig2, ax2 = plt.subplots(figsize=(6, 3))
            engine.energy.view()
            st.pyplot(plt.gcf())
            plt.close(fig2)
            
        with inputs_col2:
            fig3, ax3 = plt.subplots(figsize=(6, 3))
            engine.soreness.view()
            st.pyplot(plt.gcf())
            plt.close(fig3)
            
            fig4, ax4 = plt.subplots(figsize=(6, 3))
            engine.stress.view()
            st.pyplot(plt.gcf())
            plt.close(fig4)

st.divider()
st.markdown(f"### {t['surf_header']}")
st.markdown(t["surf_desc"])

col_3d_1, col_3d_2 = st.columns(2, gap="large")

with col_3d_1:
    with st.container(border=True):
        st.markdown("#### Sleep vs Energy ➡️ Intensity")
        st.markdown(t["surf_fixed_soreness_stress"].format(soreness=soreness_val, stress=stress_val))
        
        if st.button(t["gen_plot_btn_int"]):
            with st.spinner(t["calc_surf"]):
                grid_size = 20
                x = np.linspace(0, 10, grid_size)
                y = np.linspace(0, 10, grid_size)
                x_grid, y_grid = np.meshgrid(x, y)
                z_grid = np.zeros_like(x_grid)
                
                for i in range(grid_size):
                    for j in range(grid_size):
                        if model_type == "Sugeno":
                            res = engine.evaluate_sugeno(sleep_val=x_grid[i, j], 
                                                         soreness_val=soreness_val, 
                                                         energy_val=y_grid[i, j], 
                                                         stress_val=stress_val)
                        else:
                            res = engine.evaluate(sleep_val=x_grid[i, j], 
                                                  soreness_val=soreness_val, 
                                                  energy_val=y_grid[i, j], 
                                                  stress_val=stress_val,
                                                  defuzz_method=defuzz_method)
                        z_grid[i, j] = res['intensity']
                
                fig_3d_int = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Tealgrn')])
                fig_3d_int.update_layout(scene=dict(
                                            xaxis_title='Sleep' if lang == "EN" else 'Uyku',
                                            yaxis_title='Energy' if lang == "EN" else 'Enerji',
                                            zaxis_title='Intensity (%)' if lang == "EN" else 'Yoğunluk (%)'),
                                         margin=dict(l=0, r=0, b=0, t=30), height=500)
                st.plotly_chart(fig_3d_int, use_container_width=True)

with col_3d_2:
    with st.container(border=True):
        st.markdown("#### Sleep vs Soreness ➡️ Volume")
        st.markdown(t["surf_fixed_energy_stress"].format(energy=energy_val, stress=stress_val))
        
        if st.button(t["gen_plot_btn_vol"]):
            with st.spinner(t["calc_surf"]):
                grid_size = 20
                x = np.linspace(0, 10, grid_size)
                y = np.linspace(0, 10, grid_size)
                x_grid, y_grid = np.meshgrid(x, y)
                z_grid = np.zeros_like(x_grid)
                
                for i in range(grid_size):
                    for j in range(grid_size):
                        if model_type == "Sugeno":
                            res = engine.evaluate_sugeno(sleep_val=x_grid[i, j], 
                                                         soreness_val=y_grid[i, j], 
                                                         energy_val=energy_val, 
                                                         stress_val=stress_val)
                        else:
                            res = engine.evaluate(sleep_val=x_grid[i, j], 
                                                  soreness_val=y_grid[i, j], 
                                                  energy_val=energy_val, 
                                                  stress_val=stress_val,
                                                  defuzz_method=defuzz_method)
                        z_grid[i, j] = res['volume']
                
                fig_3d_vol = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Plotly3')])
                fig_3d_vol.update_layout(scene=dict(
                                            xaxis_title='Sleep' if lang == "EN" else 'Uyku',
                                            yaxis_title='Soreness' if lang == "EN" else 'Yorgunluk/Ağrı',
                                            zaxis_title='Volume (Min)' if lang == "EN" else 'Süre (Dk)'),
                                         margin=dict(l=0, r=0, b=0, t=30), height=500)
                st.plotly_chart(fig_3d_vol, use_container_width=True)

# Historical Analytics Dashboard
st.divider()
with st.container(border=True):
    st.markdown(f"### {t['history_header']}")
    st.markdown(t["history_desc"])
    
    if not st.session_state.workout_logs:
        st.info(t["history_empty"])
    else:
        df_logs = pd.DataFrame(st.session_state.workout_logs)
        
        if lang == "TR":
            df_logs_display = df_logs.rename(columns={
                "Timestamp": "Zaman Damgası",
                "Sleep Quality": "Uyku Kalitesi",
                "Muscle Soreness": "Kas Ağrısı",
                "Energy Level": "Enerji Seviyesi",
                "Stress Level": "Stres Seviyesi",
                "Target Muscles": "Çalisilan Bölgeler",
                "Cardio Included": "Kardiyo Eklendi",
                "Inference Model": "Cikarim Modeli",
                "Defuzz Method": "Durulastirma Yöntemi",
                "Intensity (%)": "Yogunluk (%)",
                "Volume (Min)": "Süre (Dk)"
            })
        else:
            df_logs_display = df_logs
            
        history_col1, history_col2 = st.columns([2, 3], gap="large")
        
        with history_col1:
            st.markdown(f"#### {t['history_table_title']}")
            st.dataframe(df_logs_display, use_container_width=True)
            
            # Export CSV Button
            csv_data = df_logs.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=t["export_csv_btn"],
                data=csv_data,
                file_name="fuzzyfit_workout_history.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with history_col2:
            st.markdown(f"#### {t['history_chart_title']}")
            
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=df_logs["Timestamp"],
                y=df_logs["Intensity (%)"],
                mode='lines+markers',
                name='Intensity (%)' if lang == "EN" else 'Yoğunluk (%)',
                line=dict(color='#00F0FF', width=3),
                marker=dict(size=8)
            ))
            
            fig_trend.add_trace(go.Scatter(
                x=df_logs["Timestamp"],
                y=df_logs["Volume (Min)"],
                mode='lines+markers',
                name='Volume (Min)' if lang == "EN" else 'Süre (Dk)',
                line=dict(color='#A855F7', width=3),
                marker=dict(size=8)
            ))
            
            fig_trend.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E2E8F0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_trend, use_container_width=True)
