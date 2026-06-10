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
        
        # New Feature: Live Fuzzification Dashboard (Gestalt Law of Proximity)
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
        goal = st.selectbox("🎯 Workout Goal / Antrenman Hedefi", 
                            ["Strength (Kuvvet Gelişimi)", 
                             "Hypertrophy (Kas Büyümesi)", 
                             "Endurance / Cardio (Dayanıklılık)", 
                             "Active Recovery (Aktif Yenilenme)"])
                               
        calculate_btn = st.button("🚀 Calculate Optimal Workout", use_container_width=True)

# Helper function to generate routine
def generate_workout_routine(goal, intensity, volume):
    intensity = float(intensity)
    volume = float(volume)
    
    if "Strength" in goal:
        if intensity >= 80:
            desc = "🔥 High Intensity Strength Protocol (Focus: Maximum Force Production)"
            exercises = [
                {"Exercise": "Barbell Back Squat", "Sets": "4", "Reps/Duration": "4-5 reps", "Target Load / RPE": f"~{intensity:.1f}% 1RM / RPE 9"},
                {"Exercise": "Barbell Bench Press", "Sets": "4", "Reps/Duration": "4-5 reps", "Target Load / RPE": f"~{intensity:.1f}% 1RM / RPE 9"},
                {"Exercise": "Conventional Deadlift", "Sets": "3", "Reps/Duration": "3 reps", "Target Load / RPE": f"~{intensity:.1f}% 1RM / RPE 9"},
                {"Exercise": "Weighted Pull-ups", "Sets": "3", "Reps/Duration": "5 reps", "Target Load / RPE": "RPE 8.5"}
            ]
        elif intensity >= 60:
            desc = "⚡ Moderate Intensity Strength Protocol (Focus: Technical Consistency & Power)"
            exercises = [
                {"Exercise": "Barbell Back Squat", "Sets": "3", "Reps/Duration": "6-8 reps", "Target Load / RPE": f"~{intensity:.1f}% 1RM / RPE 8"},
                {"Exercise": "Overhead Press (OHP)", "Sets": "3", "Reps/Duration": "6-8 reps", "Target Load / RPE": f"~{intensity:.1f}% 1RM / RPE 8"},
                {"Exercise": "Pendlay Rows", "Sets": "3", "Reps/Duration": "8 reps", "Target Load / RPE": "RPE 8"},
                {"Exercise": "Hanging Leg Raises", "Sets": "3", "Reps/Duration": "10-12 reps", "Target Load / RPE": "Bodyweight"}
            ]
        else:
            desc = "🌱 Deload Strength Protocol (Focus: Joint Recovery & Movement Mechanics)"
            exercises = [
                {"Exercise": "Goblet Squats", "Sets": "2", "Reps/Duration": "10 reps", "Target Load / RPE": "Light Load / RPE 6"},
                {"Exercise": "Dumbbell Bench Press", "Sets": "2", "Reps/Duration": "10 reps", "Target Load / RPE": "Light Load / RPE 6"},
                {"Exercise": "Face Pulls", "Sets": "3", "Reps/Duration": "15 reps", "Target Load / RPE": "Low Tension / RPE 6"},
                {"Exercise": "Plank", "Sets": "3", "Reps/Duration": "45-60 sec", "Target Load / RPE": "Bodyweight"}
            ]
    elif "Hypertrophy" in goal:
        if intensity >= 75:
            desc = "💪 High Volume Muscle Growth Protocol (Focus: Mechanical Tension)"
            exercises = [
                {"Exercise": "Incline Dumbbell Press", "Sets": "4", "Reps/Duration": "8-10 reps", "Target Load / RPE": f"RPE 9 (Approx {intensity:.0f}% 1RM)"},
                {"Exercise": "Romanian Deadlift (RDL)", "Sets": "3", "Reps/Duration": "10 reps", "Target Load / RPE": "RPE 8.5"},
                {"Exercise": "Lat Pulldown (Wide Grip)", "Sets": "4", "Reps/Duration": "10-12 reps", "Target Load / RPE": "RPE 9"},
                {"Exercise": "Dumbbell Lateral Raise", "Sets": "3", "Reps/Duration": "12-15 reps", "Target Load / RPE": "RPE 9 (Drop-set on last set)"}
            ]
        elif intensity >= 50:
            desc = "🏋️ Standard Hypertrophy Protocol (Focus: Metabolic Stress)"
            exercises = [
                {"Exercise": "Dumbbell Bench Press", "Sets": "3", "Reps/Duration": "10-12 reps", "Target Load / RPE": f"RPE 8 (Approx {intensity:.0f}% 1RM)"},
                {"Exercise": "Leg Press", "Sets": "3", "Reps/Duration": "12 reps", "Target Load / RPE": "RPE 8"},
                {"Exercise": "Seated Cable Row", "Sets": "3", "Reps/Duration": "12 reps", "Target Load / RPE": "RPE 8"},
                {"Exercise": "Incline Bicep Curls", "Sets": "3", "Reps/Duration": "12 reps", "Target Load / RPE": "RPE 8"}
            ]
        else:
            desc = "🛌 Active Deload Hypertrophy Protocol (Focus: Recovery & Joint Flushing)"
            exercises = [
                {"Exercise": "Chest Press Machine", "Sets": "2", "Reps/Duration": "12-15 reps", "Target Load / RPE": "Low Load / RPE 6"},
                {"Exercise": "Lat Pulldown Machine", "Sets": "2", "Reps/Duration": "12-15 reps", "Target Load / RPE": "Low Load / RPE 6"},
                {"Exercise": "Leg Extensions", "Sets": "2", "Reps/Duration": "15 reps", "Target Load / RPE": "Low Load / RPE 6"},
                {"Exercise": "Lying Leg Curls", "Sets": "2", "Reps/Duration": "15 reps", "Target Load / RPE": "Low Load / RPE 6"}
            ]
    elif "Endurance" in goal:
        if intensity >= 80:
            desc = "🏃 Anaerobic Capacity Protocol (Focus: VO2 Max & Lactate Threshold)"
            exercises = [
                {"Exercise": "Warm-up Jog", "Sets": "1", "Reps/Duration": "10 min", "Target Load / RPE": "RPE 4-5"},
                {"Exercise": "High-Intensity Interval Sprinting", "Sets": "8-10", "Reps/Duration": "30 sec work / 30 sec rest", "Target Load / RPE": f"~{intensity:.0f}% Max HR / RPE 9.5"},
                {"Exercise": "Rowing Machine Tempo Interval", "Sets": "3", "Reps/Duration": "3 min work / 2 min rest", "Target Load / RPE": "RPE 8.5"},
                {"Exercise": "Cool-down Walk", "Sets": "1", "Reps/Duration": "5 min", "Target Load / RPE": "RPE 3"}
            ]
        elif intensity >= 60:
            desc = "🚴 Aerobic Base Protocol (Focus: Cardiovascular Endurance)"
            exercises = [
                {"Exercise": "Dynamic Warm-up", "Sets": "1", "Reps/Duration": "5 min", "Target Load / RPE": "Low Intensity"},
                {"Exercise": "Steady State Running/Cycling", "Sets": "1", "Reps/Duration": f"{volume - 15:.0f} min", "Target Load / RPE": f"Zone 2/3 ({intensity:.0f}% Max HR) / RPE 7"},
                {"Exercise": "Elliptical Machine", "Sets": "1", "Reps/Duration": "10 min", "Target Load / RPE": "RPE 6.5"},
                {"Exercise": "Stretching Flow", "Sets": "1", "Reps/Duration": "5 min", "Target Load / RPE": "Relaxation"}
            ]
        else:
            desc = "🚶 Active Recovery Endurance Protocol (Focus: Aerobic Regeneration)"
            exercises = [
                {"Exercise": "Low-Intensity Steady State Walk (LISS)", "Sets": "1", "Reps/Duration": f"{volume - 10:.0f} min", "Target Load / RPE": "RPE 4-5 / Zone 1"},
                {"Exercise": "Recumbent Cycling", "Sets": "1", "Reps/Duration": "10 min", "Target Load / RPE": "Very light resistance"},
                {"Exercise": "Full Body Mobility & Foam Roll", "Sets": "1", "Reps/Duration": "10 min", "Target Load / RPE": "Low strain"}
            ]
    else:
        desc = "🧘 Full-Body Restorative Protocol (Focus: Parasympathetic Activation & Mobility)"
        exercises = [
            {"Exercise": "Self-Myofascial Release (Foam Rolling)", "Sets": "1", "Reps/Duration": "10 min", "Target Load / RPE": "Tight areas focus"},
            {"Exercise": "Dynamic Mobility Flow (Yoga-inspired)", "Sets": "1", "Reps/Duration": "15 min", "Target Load / RPE": "Deep breathing focus"},
            {"Exercise": "Low-Intensity Walking or Cycling", "Sets": "1", "Reps/Duration": f"{max(10.0, volume - 35.0):.0f} min", "Target Load / RPE": f"~{intensity:.0f}% Max HR / RPE 3-4"},
            {"Exercise": "Static Stretching (Hamstrings, Hip Flexors, Pecs)", "Sets": "1", "Reps/Duration": "10 min", "Target Load / RPE": "Mild discomfort threshold"}
        ]
        
    return desc, exercises

with col2:
    # Common Region: Grouping outputs inside a bounded container
    with st.container(border=True):
        st.markdown("### 🎯 Workout Recommendation (Outputs)")
        
        if calculate_btn:
            with st.spinner("Computing Fuzzy Inference..."):
                result = engine.evaluate(sleep_val, soreness_val, energy_val, stress_val, defuzz_method=defuzz_method)
                intensity_res = result['intensity']
                volume_res = result['volume']
                
                # Similarity: Metrics have consistent typography and glow
                metric_col1, metric_col2 = st.columns(2)
                metric_col1.metric("Recommended Intensity", f"{intensity_res:.1f} %")
                metric_col2.metric("Recommended Volume", f"{volume_res:.1f} Min")
                
                st.success(f"Inference completed successfully! (Method: {defuzz_method.upper()})")
                
                # Dynamic Workout Generator
                st.markdown("---")
                st.markdown("### 🏃 Actionable Workout Protocol")
                routine_desc, exercises_list = generate_workout_routine(goal, intensity_res, volume_res)
                st.write(f"**{routine_desc}**")
                
                df_exercises = pd.DataFrame(exercises_list)
                st.table(df_exercises)
                
                # Logging Feature
                if st.button("💾 Save Recommendation to History Log", use_container_width=True):
                    log_entry = {
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Sleep Quality": sleep_val,
                        "Muscle Soreness": soreness_val,
                        "Energy Level": energy_val,
                        "Stress Level": stress_val,
                        "Workout Goal": goal,
                        "Defuzz Method": defuzz_method.upper(),
                        "Intensity (%)": round(intensity_res, 1),
                        "Volume (Min)": round(volume_res, 1)
                    }
                    st.session_state.workout_logs.append(log_entry)
                    st.toast("Workout logged successfully! Check the history dashboard at the bottom.", icon="💾")
        else:
            st.info("Awaiting input. Please adjust the sliders and click calculate.")

# Defuzzification Comparison Panel (New Feature)
if calculate_btn:
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

if calculate_btn:
    st.divider()
    with st.expander("🔍 Show Fuzzy Logic Details (Fuzzification & Defuzzification Graphs)"):
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

# Historical Analytics Dashboard (New Tab/Container at the bottom)
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
