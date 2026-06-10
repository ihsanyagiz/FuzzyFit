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
        goal = st.selectbox("🎯 Workout Goal / Antrenman Hedefi", 
                            ["Strength (Kuvvet Gelişimi)", 
                             "Hypertrophy (Kas Büyümesi)", 
                             "Endurance / Cardio (Dayanıklılık)", 
                             "Active Recovery (Aktif Yenilenme)"])
        
        # New Feature: Target Muscle Groups selection
        target_muscles = st.multiselect("💪 Target Muscle Groups / Çalışılacak Bölgeler",
                                        ["Chest (Göğüs)", "Back (Sırt)", "Shoulders (Omuz)", "Legs (Bacak)", "Biceps (Pazı)", "Triceps (Arka Kol)", "Core (Karın)"],
                                        default=["Chest (Göğüs)", "Back (Sırt)", "Legs (Bacak)"])
                               
        calculate_btn = st.button("🚀 Calculate Optimal Workout", use_container_width=True)

# Complete exercise database mapped by muscle group, workout goal, and output intensity level
EXERCISE_DATABASE = {
    "Chest (Göğüs)": {
        "Strength": {
            "high": {"Exercise": "Barbell Bench Press", "Reps/Duration": "4-5 reps", "Target Load / RPE": "80%+ 1RM / RPE 9"},
            "mod": {"Exercise": "Dumbbell Bench Press", "Reps/Duration": "6-8 reps", "Target Load / RPE": "70-80% 1RM / RPE 8"},
            "low": {"Exercise": "Push-ups (Controlled Tempo)", "Reps/Duration": "10-12 reps", "Target Load / RPE": "Bodyweight / RPE 6"}
        },
        "Hypertrophy": {
            "high": {"Exercise": "Incline Dumbbell Press", "Reps/Duration": "8-10 reps", "Target Load / RPE": "RPE 9"},
            "mod": {"Exercise": "Chest Press Machine", "Reps/Duration": "10-12 reps", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Pec Deck Flyes (Light)", "Reps/Duration": "12-15 reps", "Target Load / RPE": "RPE 6"}
        },
        "Endurance / Cardio": {
            "high": {"Exercise": "Push-ups (AMRAP Intervals)", "Reps/Duration": "45 sec work / 30 sec rest", "Target Load / RPE": "Max Heart Rate"},
            "mod": {"Exercise": "Dumbbell Flyes (High Rep)", "Reps/Duration": "15 reps", "Target Load / RPE": "RPE 7"},
            "low": {"Exercise": "Kettlebell Halos", "Reps/Duration": "10 reps each side", "Target Load / RPE": "Light"}
        },
        "Active Recovery": {
            "high": {"Exercise": "Push-ups on Knees (Slow)", "Reps/Duration": "8 reps", "Target Load / RPE": "RPE 4"},
            "mod": {"Exercise": "Chest Wall Stretch", "Reps/Duration": "30 sec hold", "Target Load / RPE": "Gentle stretch"},
            "low": {"Exercise": "Foam Roll Chest / Pecs", "Reps/Duration": "2 min", "Target Load / RPE": "Relaxation"}
        }
    },
    "Back (Sırt)": {
        "Strength": {
            "high": {"Exercise": "Conventional Deadlift", "Reps/Duration": "3 reps", "Target Load / RPE": "85%+ 1RM / RPE 9"},
            "mod": {"Exercise": "Barbell Row", "Reps/Duration": "6-8 reps", "Target Load / RPE": "75% 1RM / RPE 8"},
            "low": {"Exercise": "Chest-Supported Dumbbell Row", "Reps/Duration": "10 reps", "Target Load / RPE": "Light / RPE 6"}
        },
        "Hypertrophy": {
            "high": {"Exercise": "Weighted Pull-ups", "Reps/Duration": "6-8 reps", "Target Load / RPE": "RPE 9"},
            "mod": {"Exercise": "Lat Pulldown (Wide Grip)", "Reps/Duration": "10-12 reps", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Seated Cable Row (Light)", "Reps/Duration": "12-15 reps", "Target Load / RPE": "RPE 6"}
        },
        "Endurance / Cardio": {
            "high": {"Exercise": "Kettlebell Swings", "Reps/Duration": "1 min work / 30 sec rest", "Target Load / RPE": "High Intensity"},
            "mod": {"Exercise": "Inverted Bodyweight Rows", "Reps/Duration": "12-15 reps", "Target Load / RPE": "RPE 7"},
            "low": {"Exercise": "Resistance Band Lat Pulldowns", "Reps/Duration": "15-20 reps", "Target Load / RPE": "Light tension"}
        },
        "Active Recovery": {
            "high": {"Exercise": "Cat-Cow Stretch", "Reps/Duration": "10 repetitions", "Target Load / RPE": "Gentle mobility"},
            "mod": {"Exercise": "Prone Cobra (Lower Back)", "Reps/Duration": "20 sec holds", "Target Load / RPE": "Bodyweight"},
            "low": {"Exercise": "Foam Roll Upper Back", "Reps/Duration": "3 min", "Target Load / RPE": "Relaxation"}
        }
    },
    "Shoulders (Omuz)": {
        "Strength": {
            "high": {"Exercise": "Barbell Overhead Press (OHP)", "Reps/Duration": "4-5 reps", "Target Load / RPE": "80%+ 1RM / RPE 9"},
            "mod": {"Exercise": "Standing Dumbbell Press", "Reps/Duration": "6-8 reps", "Target Load / RPE": "75% 1RM / RPE 8"},
            "low": {"Exercise": "Dumbbell Arnold Press (Light)", "Reps/Duration": "10 reps", "Target Load / RPE": "RPE 6"}
        },
        "Hypertrophy": {
            "high": {"Exercise": "Dumbbell Lateral Raise", "Reps/Duration": "12-15 reps", "Target Load / RPE": "RPE 9.5"},
            "mod": {"Exercise": "Seated Dumbbell Shoulder Press", "Reps/Duration": "10-12 reps", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Face Pulls", "Reps/Duration": "15 reps", "Target Load / RPE": "RPE 7"}
        },
        "Endurance / Cardio": {
            "high": {"Exercise": "Battle Ropes (Intervals)", "Reps/Duration": "30 sec work / 30 sec rest", "Target Load / RPE": "Max Effort"},
            "mod": {"Exercise": "Dumbbell Front-to-Lateral Raises", "Reps/Duration": "12 reps", "Target Load / RPE": "Light / RPE 7"},
            "low": {"Exercise": "Standing Band Pull-Aparts", "Reps/Duration": "20 reps", "Target Load / RPE": "High Reps"}
        },
        "Active Recovery": {
            "high": {"Exercise": "Y-T-W Shoulder Raises", "Reps/Duration": "8 reps per letter", "Target Load / RPE": "No weight"},
            "mod": {"Exercise": "Shoulder Dislocations (with band/broom)", "Reps/Duration": "10 reps", "Target Load / RPE": "Gentle mobility"},
            "low": {"Exercise": "Child's Pose", "Reps/Duration": "45 sec hold", "Target Load / RPE": "Relaxation"}
        }
    },
    "Legs (Bacak)": {
        "Strength": {
            "high": {"Exercise": "Barbell Back Squat", "Reps/Duration": "4-5 reps", "Target Load / RPE": "80%+ 1RM / RPE 9"},
            "mod": {"Exercise": "Leg Press", "Reps/Duration": "6-8 reps", "Target Load / RPE": "75% 1RM / RPE 8"},
            "low": {"Exercise": "Dumbbell Goblet Squat (Light)", "Reps/Duration": "10 reps", "Target Load / RPE": "RPE 6"}
        },
        "Hypertrophy": {
            "high": {"Exercise": "Romanian Deadlift (RDL)", "Reps/Duration": "10 reps", "Target Load / RPE": "RPE 8.5"},
            "mod": {"Exercise": "Bulgarian Split Squats", "Reps/Duration": "10 reps each side", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Leg Extensions", "Reps/Duration": "12-15 reps", "Target Load / RPE": "RPE 7"}
        },
        "Endurance / Cardio": {
            "high": {"Exercise": "Jumping Squats (Intervals)", "Reps/Duration": "30 sec work / 30 sec rest", "Target Load / RPE": "Max Heart Rate"},
            "mod": {"Exercise": "Dumbbell Walking Lunges", "Reps/Duration": "20 paces", "Target Load / RPE": "RPE 7"},
            "low": {"Exercise": "Bodyweight Squats (Constant Tempo)", "Reps/Duration": "20 reps", "Target Load / RPE": "Zone 2"}
        },
        "Active Recovery": {
            "high": {"Exercise": "Bodyweight Air Squats (Slow)", "Reps/Duration": "10 reps", "Target Load / RPE": "RPE 4"},
            "mod": {"Exercise": "Couch Stretch (Quads/Hip Flexors)", "Reps/Duration": "30 sec each side", "Target Load / RPE": "Gentle stretch"},
            "low": {"Exercise": "Foam Roll Quads and Hamstrings", "Reps/Duration": "3 min", "Target Load / RPE": "Relaxation"}
        }
    },
    "Biceps (Pazı)": {
        "Strength": {
            "high": {"Exercise": "Barbell Bicep Curl", "Reps/Duration": "6 reps", "Target Load / RPE": "Heavy / RPE 8.5"},
            "mod": {"Exercise": "Dumbbell Bicep Curl", "Reps/Duration": "8 reps", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Incline Dumbbell Curl (Light)", "Reps/Duration": "10 reps", "Target Load / RPE": "RPE 6"}
        },
        "Hypertrophy": {
            "high": {"Exercise": "Incline Dumbbell Curl", "Reps/Duration": "10 reps", "Target Load / RPE": "RPE 9"},
            "mod": {"Exercise": "Dumbbell Hammer Curl", "Reps/Duration": "12 reps", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Concentration Curls", "Reps/Duration": "12 reps", "Target Load / RPE": "RPE 7"}
        },
        "Endurance / Cardio": {
            "high": {"Exercise": "Empty Barbell Curls (Max Reps)", "Reps/Duration": "1 min work", "Target Load / RPE": "Burnout"},
            "mod": {"Exercise": "Cable Curls (High Rep)", "Reps/Duration": "15-20 reps", "Target Load / RPE": "RPE 7"},
            "low": {"Exercise": "Resistance Band Bicep Curls", "Reps/Duration": "20 reps", "Target Load / RPE": "High rep pump"}
        },
        "Active Recovery": {
            "high": {"Exercise": "Dumbbell Curls (Very Light)", "Reps/Duration": "12 reps", "Target Load / RPE": "RPE 4"},
            "mod": {"Exercise": "Bicep Wall Stretch", "Reps/Duration": "20 sec holds", "Target Load / RPE": "Gentle stretch"},
            "low": {"Exercise": "Light Forearm Rollout", "Reps/Duration": "1 min", "Target Load / RPE": "Mobility"}
        }
    },
    "Triceps (Arka Kol)": {
        "Strength": {
            "high": {"Exercise": "Close Grip Bench Press", "Reps/Duration": "5 reps", "Target Load / RPE": "80% 1RM / RPE 9"},
            "mod": {"Exercise": "Weighted Dips", "Reps/Duration": "6-8 reps", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Lying Tricep Extensions", "Reps/Duration": "10 reps", "Target Load / RPE": "Light / RPE 6"}
        },
        "Hypertrophy": {
            "high": {"Exercise": "Overhead Cable Tricep Extension", "Reps/Duration": "10-12 reps", "Target Load / RPE": "RPE 9"},
            "mod": {"Exercise": "Cable Tricep Pushdowns", "Reps/Duration": "12 reps", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Dumbbell Kickbacks", "Reps/Duration": "12-15 reps", "Target Load / RPE": "RPE 7"}
        },
        "Endurance / Cardio": {
            "high": {"Exercise": "Bench Dips (Max Reps)", "Reps/Duration": "45 sec work", "Target Load / RPE": "Burnout"},
            "mod": {"Exercise": "Cable Pushdowns (High Rep)", "Reps/Duration": "20 reps", "Target Load / RPE": "RPE 7"},
            "low": {"Exercise": "Band Overhead Pushdowns", "Reps/Duration": "25 reps", "Target Load / RPE": "High rep pump"}
        },
        "Active Recovery": {
            "high": {"Exercise": "Tricep Overhead Stretch", "Reps/Duration": "30 sec each side", "Target Load / RPE": "Gentle stretch"},
            "mod": {"Exercise": "Wall Push-ups (Triceps focus)", "Reps/Duration": "10 reps", "Target Load / RPE": "Very light"},
            "low": {"Exercise": "Light Elbow Mobility Extensions", "Reps/Duration": "2 min", "Target Load / RPE": "No weight"}
        }
    },
    "Core (Karın)": {
        "Strength": {
            "high": {"Exercise": "Weighted Hanging Leg Raises", "Reps/Duration": "8 reps", "Target Load / RPE": "RPE 9"},
            "mod": {"Exercise": "Ab Wheel Rollouts", "Reps/Duration": "8-10 reps", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Decline Bench Crunches", "Reps/Duration": "12 reps", "Target Load / RPE": "Bodyweight"}
        },
        "Hypertrophy": {
            "high": {"Exercise": "Hanging Leg Raises", "Reps/Duration": "10-12 reps", "Target Load / RPE": "RPE 9"},
            "mod": {"Exercise": "Cable Woodchoppers", "Reps/Duration": "12 reps each side", "Target Load / RPE": "RPE 8"},
            "low": {"Exercise": "Plank (Squeeze focus)", "Reps/Duration": "45 sec", "Target Load / RPE": "Bodyweight"}
        },
        "Endurance / Cardio": {
            "high": {"Exercise": "Mountain Climbers (Fast)", "Reps/Duration": "1 min work", "Target Load / RPE": "High Heart Rate"},
            "mod": {"Exercise": "Russian Twists (High Rep)", "Reps/Duration": "20 reps each side", "Target Load / RPE": "RPE 7"},
            "low": {"Exercise": "Plank (Steady State)", "Reps/Duration": "60 sec", "Target Load / RPE": "Zone 2"}
        },
        "Active Recovery": {
            "high": {"Exercise": "Bird-Dog Pose", "Reps/Duration": "10 reps each side", "Target Load / RPE": "Bodyweight / Core stability"},
            "mod": {"Exercise": "Dead Bug Pose", "Reps/Duration": "10 reps each side", "Target Load / RPE": "Bodyweight / Core stability"},
            "low": {"Exercise": "Cobra Stretch (Abs focus)", "Reps/Duration": "30 sec hold", "Target Load / RPE": "Gentle stretch"}
        }
    }
}

# Helper function to generate workout routine
def generate_workout_routine_dynamic(goal, intensity, volume, target_muscles):
    intensity = float(intensity)
    volume = float(volume)
    
    # 1. Determine Level based on intensity
    if intensity >= 75:
        level = "high"
    elif intensity >= 50:
        level = "mod"
    else:
        level = "low"
        
    # 2. Determine Primary Goal string matching database keys
    goal_key = "Strength"
    if "Hypertrophy" in goal:
        goal_key = "Hypertrophy"
    elif "Endurance" in goal:
        goal_key = "Endurance / Cardio"
    elif "Active Recovery" in goal:
        goal_key = "Active Recovery"
        
    # 3. Determine Dynamic Set Count based on fuzzy volume recommendation
    # Connects fuzzy volume directly to physical sets count
    if volume >= 80:
        sets_val = "4"
    elif volume >= 40:
        sets_val = "3"
    else:
        sets_val = "2"
        
    # 4. Generate routine title
    routine_title = f"🏃 Adaptive Workout Routine ({goal_key} - {level.upper()} intensity, {sets_val} sets per exercise)"
    
    # 5. Extract exercises from database for selected muscle groups
    exercises = []
    
    # Fallback to Chest, Back, Legs if no muscle selected
    selected_muscles = target_muscles if target_muscles else ["Chest (Göğüs)", "Back (Sırt)", "Legs (Bacak)"]
    
    for muscle in selected_muscles:
        if muscle in EXERCISE_DATABASE:
            ex_data = EXERCISE_DATABASE[muscle][goal_key][level].copy()
            # Inject dynamic sets matching fuzzy volume
            ex_data["Sets"] = sets_val
            # Reorder columns for display
            exercises.append({
                "Muscle Group": muscle.split(" ")[0],
                "Exercise": ex_data["Exercise"],
                "Sets": ex_data["Sets"],
                "Reps / Duration": ex_data["Reps/Duration"],
                "Target Load / RPE": ex_data["Target Load / RPE"]
            })
            
    return routine_title, exercises

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
                
                # Dynamic Workout Generator based on Selected Muscle Groups
                st.markdown("---")
                st.markdown("### 🏃 Actionable Workout Protocol")
                routine_desc, exercises_list = generate_workout_routine_dynamic(goal, intensity_res, volume_res, target_muscles)
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
                        "Target Muscles": ", ".join([m.split(" ")[0] for m in target_muscles]),
                        "Defuzz Method": defuzz_method.upper(),
                        "Intensity (%)": round(intensity_res, 1),
                        "Volume (Min)": round(volume_res, 1)
                    }
                    st.session_state.workout_logs.append(log_entry)
                    st.toast("Workout logged successfully! Check the history dashboard at the bottom.", icon="💾")
        else:
            st.info("Awaiting input. Please adjust the sliders and click calculate.")

# Defuzzification Comparison Panel
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
