import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from fuzzy_engine import FuzzyFitSystem

# Page Configuration
st.set_page_config(page_title="FuzzyFit Assistant", page_icon="⚡", layout="wide")

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

# Initialize Fuzzy System (No caching to avoid stale states during development)
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
                               
        calculate_btn = st.button("🚀 Calculate Optimal Workout", use_container_width=True)

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
        else:
            st.info("Awaiting input. Please adjust the sliders and click calculate.")
            
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
                
            with graph_col2:
                st.markdown("#### Volume Output")
                fig_vol, ax_vol = plt.subplots(figsize=(8, 4))
                try:
                    engine.volume.view(sim=engine.fitness_sim)
                except (KeyError, ValueError, Exception):
                    pass
                st.pyplot(plt.gcf())
                
            st.divider()
            st.markdown("#### Input Variables (Fuzzification)")
            inputs_col1, inputs_col2 = st.columns(2)
            
            with inputs_col1:
                fig1, ax1 = plt.subplots(figsize=(6, 3))
                engine.sleep.view()
                st.pyplot(plt.gcf())
                
                fig2, ax2 = plt.subplots(figsize=(6, 3))
                engine.energy.view()
                st.pyplot(plt.gcf())
                
            with inputs_col2:
                fig3, ax3 = plt.subplots(figsize=(6, 3))
                engine.soreness.view()
                st.pyplot(plt.gcf())
                
                fig4, ax4 = plt.subplots(figsize=(6, 3))
                engine.stress.view()
                st.pyplot(plt.gcf())


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
