import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import datetime
from fuzzy_engine import FuzzyFitSystem

# Page Configuration
st.set_page_config(page_title="FuzzyFit Assistant", page_icon="⚡", layout="wide")

# Initialize Session State for Workout History
if 'workout_logs' not in st.session_state:
    st.session_state.workout_logs = []

# Custom CSS for Premium Look & Gestalt Principles (Proximity, Similarity, Figure/Ground)
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

# Main Title (Symmetry & Strong Figure)
st.markdown('<h1 class="gradient-text">⚡ FuzzyFit</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Fuzzy Logic-Powered Smart Workout & Recovery Assistant</p>', unsafe_allow_html=True)

# Sidebar for Settings (Proximity: Keep settings away from main data flow)
st.sidebar.header("⚙️ Engine Settings")
st.sidebar.markdown("Test different defuzzification methods for the fuzzy inference system.")
defuzz_method = st.sidebar.selectbox("Defuzzification Method", 
                                     ["centroid", "bisector", "mom", "som", "lom"], 
                                     help="Centroid is the most common. Others use different mathematical area calculations.")

# Initialize Fuzzy System (No caching to avoid stale states)
def get_fuzzy_system():
    return FuzzyFitSystem()

engine = get_fuzzy_system()

st.divider()

# Left column for inputs, Right for outputs (Law of Symmetry and Balance)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    # Common Region: Grouping inputs inside a bounded container
    with st.container(border=True):
        st.markdown("### 📋 Daily Physical Status (Inputs)")
        
        sleep_val = st.slider("😴 Sleep Quality", min_value=0.0, max_value=10.0, value=7.0, step=0.1, 
                               help="0: Very Poor, 10: Excellent")
        
        soreness_val = st.slider("🤕 Muscle Soreness & Fatigue", min_value=0.0, max_value=10.0, value=3.0, step=0.1,
                                 help="0: No soreness, 10: Severe pain")
                                  
        energy_val = st.slider("⚡ Energy & Nutrition Level", min_value=0.0, max_value=10.0, value=6.0, step=0.1,
                               help="0: Severe Deficit/Hungry, 10: High Energy/Caloric Surplus")
                               
        stress_val = st.slider("🤯 Stress Level", min_value=0.0, max_value=10.0, value=4.0, step=0.1,
                               help="0: Very relaxed, 10: Highly stressed")
        
        # Live Fuzzification Dashboard (Gestalt Law of Proximity)
        st.markdown("#### 🔍 Live Fuzzification (Bulanıklaştırma Dereceleri)")
        m_vals = engine.get_membership_values(sleep_val, soreness_val, energy_val, stress_val)
        
        for var_name, terms in m_vals.items():
            st.markdown(f"**{var_name}**")
            cols = st.columns(3)
            for idx, (term_name, term_val) in enumerate(terms.items()):
                with cols[idx]:
                    st.caption(f"{term_name}: {term_val*100:.1f}%")
                    st.progress(min(max(term_val, 0.0), 1.0))
        
        st.markdown("---")
        # Target Muscle Groups selection
        target_muscles = st.multiselect("💪 Target Muscle Groups / Çalışılacak Bölgeler",
                                        ["Chest (Göğüs)", "Back (Sırt)", "Shoulders (Omuz)", "Legs (Bacak)", "Biceps (Pazı)", "Triceps (Arka Kol)", "Core (Karın)"],
                                        default=["Chest (Göğüs)", "Back (Sırt)", "Legs (Bacak)"])
        
        # Add Cardio checkbox
        add_cardio = st.checkbox("🏃 Add Cardio Session / Kardiyo Ekle", value=False,
                                 help="Aktif edilirse antrenman süresinin %30'u kardiyoya ayrılır ve ayrı olarak gösterilir.")

# Pool of general exercises for each muscle group
EXERCISE_POOL = {
    "Chest (Göğüs)": [
        "Flat Barbell Bench Press",
        "Incline Dumbbell Press",
        "Pec Deck Flyes",
        "Dumbbell Flat Bench Press"
    ],
    "Back (Sırt)": [
        "Pull-ups / Lat Pulldown",
        "Bent-over Barbell Row",
        "Seated Cable Row",
        "Conventional Deadlift"
    ],
    "Shoulders (Omuz)": [
        "Barbell Overhead Press (OHP)",
        "Dumbbell Lateral Raise",
        "Face Pulls",
        "Seated Dumbbell Shoulder Press"
    ],
    "Legs (Bacak)": [
        "Barbell Back Squat",
        "Romanian Deadlift (RDL)",
        "Leg Press",
        "Leg Extensions / Curls"
    ],
    "Biceps (Pazı)": [
        "Barbell Bicep Curl",
        "Dumbbell Hammer Curl",
        "Incline Dumbbell Curl",
        "Cable Curls"
    ],
    "Triceps (Arka Kol)": [
        "Close-grip Bench Press / Dips",
        "Cable Tricep Pushdown",
        "Lying Tricep Extensions (Skullcrushers)",
        "Overhead Dumbbell Extension"
    ],
    "Core (Karın)": [
        "Hanging Leg Raise",
        "Plank (Bodyweight Plank)",
        "Ab Wheel Rollouts",
        "Russian Twists"
    ]
}

# Helper function to generate workout routine dynamically based on volume and muscles
def generate_workout_routine_dynamic(intensity, volume, target_muscles, add_cardio):
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
        rpe_desc = f"Heavy ({intensity:.1f}% 1RM / RPE 9)"
    elif intensity >= 50:
        reps_desc = "8-12 reps"
        rpe_desc = f"Moderate (RPE 8)"
    else:
        reps_desc = "12-15 reps"
        rpe_desc = f"Light (RPE 6)"
        
    # 3. Calculate Total Target Sets for Strength
    # Assume 4 minutes per set (execution + 2-3 min rest)
    total_sets = max(3, int(strength_min / 4))
    
    # 4. Allocate Sets to Selected Muscles
    selected_muscles = target_muscles if target_muscles else ["Chest (Göğüs)", "Back (Sırt)", "Legs (Bacak)"]
    N = len(selected_muscles)
    
    sets_per_muscle = total_sets // N
    remainder = total_sets % N
    
    exercises = []
    
    for idx, muscle in enumerate(selected_muscles):
        # Add remainder set to earlier muscles in selection
        muscle_sets_target = sets_per_muscle + (1 if idx < remainder else 0)
        
        # Get exercise pool for this muscle
        pool = EXERCISE_POOL.get(muscle, ["General Exercise"])
        
        # Distribute sets target across multiple exercises to avoid 1 exercise doing 10 sets
        # We aim for ~3 to 4 sets per exercise
        num_exercises = max(1, int(np.ceil(muscle_sets_target / 4.0)))
        
        base_sets = muscle_sets_target // num_exercises
        ex_remainder = muscle_sets_target % num_exercises
        
        for ex_idx in range(num_exercises):
            ex_sets = base_sets + (1 if ex_idx < ex_remainder else 0)
            if ex_sets <= 0:
                continue
                
            ex_name = pool[ex_idx % len(pool)]
            
            # Special case for Plank (which is duration based, not reps)
            current_reps = reps_desc
            if "plank" in ex_name.lower():
                current_reps = "30-60 sec hold"
                
            exercises.append({
                "Muscle Group": muscle.split(" ")[0],
                "Exercise": ex_name,
                "Sets": str(ex_sets),
                "Reps / Duration": current_reps,
                "Target Load / RPE": rpe_desc
            })
            
    # 5. Build Cardio recommendation
    cardio_recommendation = None
    if add_cardio and cardio_min > 0:
        # Cardio intensity adapts to fuzzy intensity output
        cardio_intensity = f"Zone 2 (~{intensity:.0f}% Max HR / RPE 6)"
        if intensity >= 80:
            cardio_intensity = f"HIIT Intervals (~{intensity:.0f}% Max HR / RPE 9)"
        cardio_recommendation = {
            "Activity": "Cardio Session (Run/Cycle/Row)",
            "Duration": f"{cardio_min} Min",
            "Intensity": cardio_intensity
        }
        
    routine_title = f"🏃 Workout Routine ({total_sets} Total Strength Sets"
    if add_cardio:
        routine_title += f" + {cardio_min} Min Cardio)"
    else:
        routine_title += ")"
        
    return routine_title, exercises, cardio_recommendation

# Dynamic Evaluation of Fuzzy Logic (Runs automatically on slider change)
result = engine.evaluate(sleep_val, soreness_val, energy_val, stress_val, defuzz_method=defuzz_method)
intensity_res = result['intensity']
volume_res = result['volume']

with col2:
    # Common Region: Grouping outputs inside a bounded container
    with st.container(border=True):
        st.markdown("### 🎯 Workout Recommendation (Outputs)")
        
        # Similarity: Metrics have consistent typography and glow
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("Recommended Intensity", f"{intensity_res:.1f} %")
        metric_col2.metric("Recommended Volume", f"{volume_res:.1f} Min")
        
        st.success(f"Inference completed dynamically! (Method: {defuzz_method.upper()})")
        
        # Dynamic Workout Generator based on Selected Muscle Groups
        st.markdown("---")
        st.markdown("### 🏃 Actionable Workout Protocol")
        routine_desc, exercises_list, cardio_rec = generate_workout_routine_dynamic(intensity_res, volume_res, target_muscles, add_cardio)
        st.write(f"**{routine_desc}**")
        
        df_exercises = pd.DataFrame(exercises_list)
        st.table(df_exercises)
        
        if cardio_rec:
            st.markdown("#### 🏃 Cardio Session Finisher")
            st.table(pd.DataFrame([cardio_rec]))
        
        # Logging Feature
        if st.button("💾 Save Recommendation to History Log", use_container_width=True):
            log_entry = {
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Sleep Quality": sleep_val,
                "Muscle Soreness": soreness_val,
                "Energy Level": energy_val,
                "Stress Level": stress_val,
                "Target Muscles": ", ".join([m.split(" ")[0] for m in target_muscles]),
                "Cardio Included": "Yes" if add_cardio else "No",
                "Defuzz Method": defuzz_method.upper(),
                "Intensity (%)": round(intensity_res, 1),
                "Volume (Min)": round(volume_res, 1)
            }
            st.session_state.workout_logs.append(log_entry)
            st.toast("Workout logged successfully! Check the history dashboard at the bottom.", icon="💾")

# Defuzzification Comparison Panel (Always visible, recomputes dynamically)
st.divider()
with st.container(border=True):
    st.markdown("### 📊 Defuzzification Methods Comparison")
    st.markdown("See how different mathematical techniques compute Workout Intensity and Workout Volume given your current physical inputs.")
    
    # Calculate results for all methods
    methods = ["centroid", "bisector", "mom", "som", "lom"]
    comp_results = []
    for m in methods:
        res = engine.evaluate(sleep_val, soreness_val, energy_val, stress_val, defuzz_method=m)
        comp_results.append({
            "Method": m.upper(),
            "Intensity (%)": round(res['intensity'], 2),
            "Volume (Min)": round(res['volume'], 2)
        })
        
    comp_df = pd.DataFrame(comp_results)
    
    comp_col1, comp_col2 = st.columns([1, 1], gap="large")
    
    with comp_col1:
        st.markdown("#### Comparison Table")
        st.table(comp_df)
        
    with comp_col2:
        st.markdown("#### Comparison Chart")
        # Build bar chart using Plotly
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=comp_df["Method"],
            y=comp_df["Intensity (%)"],
            name='Workout Intensity (%)',
            marker_color='#00F0FF'
        ))
        fig_comp.add_trace(go.Bar(
            x=comp_df["Method"],
            y=comp_df["Volume (Min)"],
            name='Workout Volume (Min)',
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
with st.expander("🔍 Show Fuzzy Logic Details (Fuzzification & Defuzzification Graphs)", expanded=True):
    st.markdown("The black vertical line represents the Crisp (Defuzzified) value.")
    
    # Enclose graphs in a container
    with st.container(border=True):
        graph_col1, graph_col2 = st.columns(2)
        
        with graph_col1:
            st.markdown("#### Intensity Output")
            fig_int, ax_int = plt.subplots(figsize=(8, 4))
            try:
                engine.intensity.view(sim=engine.fitness_sim)
            except (KeyError, ValueError, Exception):
                st.warning("Could not generate graph (No rule intersection).")
            st.pyplot(plt.gcf())
            plt.close(fig_int)
            
        with graph_col2:
            st.markdown("#### Volume Output")
            fig_vol, ax_vol = plt.subplots(figsize=(8, 4))
            try:
                engine.volume.view(sim=engine.fitness_sim)
            except (KeyError, ValueError, Exception):
                pass
            st.pyplot(plt.gcf())
            plt.close(fig_vol)
            
        st.divider()
        st.markdown("#### Input Variables (Fuzzification)")
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
st.markdown("### 📈 Interactive 3D Control Surfaces")
st.markdown("""
Visualize how two primary inputs affect the output in 3D. 
**The fixed variables in these 3D graphs are automatically synced with the Daily Physical Status sliders you adjusted at the top!** 
If you change your Stress or Muscle Soreness above, the entire 3D surface will shift when you regenerate it.
""")

col_3d_1, col_3d_2 = st.columns(2, gap="large")

with col_3d_1:
    with st.container(border=True):
        st.markdown("#### Sleep vs Energy ➡️ Intensity")
        st.markdown(f"**Current Fixed Variables:** Muscle Soreness = {soreness_val:.1f}, Stress = {stress_val:.1f}")
        
        if st.button("Generate Intensity 3D Plot (~3s)"):
            with st.spinner("Calculating 3D Surface..."):
                grid_size = 20
                x = np.linspace(0, 10, grid_size)
                y = np.linspace(0, 10, grid_size)
                x_grid, y_grid = np.meshgrid(x, y)
                z_grid = np.zeros_like(x_grid)
                
                for i in range(grid_size):
                    for j in range(grid_size):
                        res = engine.evaluate(sleep_val=x_grid[i, j], 
                                              soreness_val=soreness_val, 
                                              energy_val=y_grid[i, j], 
                                              stress_val=stress_val,
                                              defuzz_method=defuzz_method)
                        z_grid[i, j] = res['intensity']
                
                fig_3d_int = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Tealgrn')])
                fig_3d_int.update_layout(scene=dict(
                                            xaxis_title='Sleep',
                                            yaxis_title='Energy',
                                            zaxis_title='Intensity (%)'),
                                         margin=dict(l=0, r=0, b=0, t=30), height=500)
                st.plotly_chart(fig_3d_int, use_container_width=True)

with col_3d_2:
    with st.container(border=True):
        st.markdown("#### Sleep vs Soreness ➡️ Volume")
        st.markdown(f"**Current Fixed Variables:** Energy Level = {energy_val:.1f}, Stress = {stress_val:.1f}")
        
        if st.button("Generate Volume 3D Plot (~3s)"):
            with st.spinner("Calculating 3D Surface..."):
                grid_size = 20
                x = np.linspace(0, 10, grid_size)
                y = np.linspace(0, 10, grid_size)
                x_grid, y_grid = np.meshgrid(x, y)
                z_grid = np.zeros_like(x_grid)
                
                for i in range(grid_size):
                    for j in range(grid_size):
                        res = engine.evaluate(sleep_val=x_grid[i, j], 
                                              soreness_val=y_grid[i, j], 
                                              energy_val=energy_val, 
                                              stress_val=stress_val,
                                              defuzz_method=defuzz_method)
                        z_grid[i, j] = res['volume']
                
                fig_3d_vol = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Plotly3')])
                fig_3d_vol.update_layout(scene=dict(
                                            xaxis_title='Sleep',
                                            yaxis_title='Soreness',
                                            zaxis_title='Volume (Min)'),
                                         margin=dict(l=0, r=0, b=0, t=30), height=500)
                st.plotly_chart(fig_3d_vol, use_container_width=True)

# Historical Analytics Dashboard
st.divider()
with st.container(border=True):
    st.markdown("### 📅 Workout History & Analytics Dashboard")
    st.markdown("Track your workouts over time. Each saved configuration is logged below with detailed charts.")
    
    if not st.session_state.workout_logs:
        st.info("No logs saved yet. Click the **'💾 Save Recommendation to History Log'** button above to save your first training recommendation!")
    else:
        df_logs = pd.DataFrame(st.session_state.workout_logs)
        
        history_col1, history_col2 = st.columns([2, 3], gap="large")
        
        with history_col1:
            st.markdown("#### Saved Workouts Log")
            st.dataframe(df_logs, use_container_width=True)
            
            # Export CSV Button
            csv_data = df_logs.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export History as CSV",
                data=csv_data,
                file_name="fuzzyfit_workout_history.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with history_col2:
            st.markdown("#### Performance Trend Chart")
            
            # Line chart showing how Intensity and Volume recommended change over time
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=df_logs["Timestamp"],
                y=df_logs["Intensity (%)"],
                mode='lines+markers',
                name='Intensity (%)',
                line=dict(color='#00F0FF', width=3),
                marker=dict(size=8)
            ))
            
            fig_trend.add_trace(go.Scatter(
                x=df_logs["Timestamp"],
                y=df_logs["Volume (Min)"],
                mode='lines+markers',
                name='Volume (Min)',
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
