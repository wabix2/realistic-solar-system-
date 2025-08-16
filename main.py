import streamlit as st
import plotly.graph_objects as go
import math
import time
import random

# --- Page Setup ---
st.set_page_config(page_title="3D Realistic Solar System", layout="wide")
st.title("🌌 3D Realistic Solar System Simulation")

# --- Sidebar Controls ---
st.sidebar.title("⚙️ Controls")
speed = st.sidebar.slider("Simulation Speed", 1, 50, 10)
start_btn = st.sidebar.button("▶ Start")
pause_btn = st.sidebar.button("⏸ Pause")
reset_btn = st.sidebar.button("🔄 Reset")

# --- Planet Data ---
planets = [
    {"name": "Mercury", "radius": 0.38, "distance": 0.39},
    {"name": "Venus", "radius": 0.95, "distance": 0.72},
    {"name": "Earth", "radius": 1.0, "distance": 1.0},
    {"name": "Mars", "radius": 0.53, "distance": 1.52},
    {"name": "Jupiter", "radius": 11.2, "distance": 5.20},
    {"name": "Saturn", "radius": 9.45, "distance": 9.58},
    {"name": "Uranus", "radius": 4.0, "distance": 19.18},
    {"name": "Neptune", "radius": 3.88, "distance": 30.07}
]

distance_scale = 50
radius_scale = 0.3

# --- Initialize session state ---
if "time" not in st.session_state:
    st.session_state.time = 0
if "running" not in st.session_state:
    st.session_state.running = False

# --- Button Logic ---
if start_btn:
    st.session_state.running = True
if pause_btn:
    st.session_state.running = False
if reset_btn:
    st.session_state.running = False
    st.session_state.time = 0

# --- Create 3D Figure ---
fig = go.Figure()

# Add stars
star_x = [random.uniform(-1500, 1500) for _ in range(200)]
star_y = [random.uniform(-1500, 1500) for _ in range(200)]
star_z = [random.uniform(-1500, 1500) for _ in range(200)]
fig.add_trace(go.Scatter3d(
    x=star_x, y=star_y, z=star_z,
    mode='markers',
    marker=dict(size=1, color='white'),
    showlegend=False
))

# Add Sun
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers+text',
    marker=dict(size=30, color='yellow'),
    text=["☀ Sun"], textposition="top center",
    showlegend=False
))

# Add planets and orbits
for planet in planets:
    angle = st.session_state.time * (0.05 / planet["distance"])
    x = planet["distance"] * distance_scale * math.cos(angle)
    y = planet["distance"] * distance_scale * math.sin(angle)
    z = 0

    # Planet marker
    fig.add_trace(go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode='markers+text',
        marker=dict(size=planet["radius"]*radius_scale*10, color='white'),
        text=[planet["name"]],
        textposition="top center",
        showlegend=False
    ))

    # Orbit line
    orbit_theta = [i*0.1 for i in range(0,63)]
    orbit_x = [planet["distance"]*distance_scale*math.cos(t) for t in orbit_theta]
    orbit_y = [planet["distance"]*distance_scale*math.sin(t) for t in orbit_theta]
    orbit_z = [0]*len(orbit_theta)
    fig.add_trace(go.Scatter3d(
        x=orbit_x, y=orbit_y, z=orbit_z,
        mode='lines', line=dict(color='gray', width=1),
        showlegend=False
    ))

# Layout
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode='data'
    ),
    margin=dict(l=0,r=0,t=0,b=0),
    paper_bgcolor='black',
    plot_bgcolor='black',
    scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1))
)

st.plotly_chart(fig, use_container_width=True)

# --- Animation ---
if st.session_state.running:
    st.session_state.time += speed * 0.1
    time.sleep(0.1)
    st.experimental_rerun()
