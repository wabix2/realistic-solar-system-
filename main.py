import streamlit as st
from pythreejs import *
import math
import time
import random

st.set_page_config(page_title="Ultimate 3D Solar System", layout="wide")
st.title("🌌 Ultimate Realistic 3D Solar System Simulation")

# --- Sidebar Controls ---
st.sidebar.title("⚙️ Controls")
speed = st.sidebar.slider("Simulation Speed", 0.01, 0.5, 0.05)
start_btn = st.sidebar.button("▶ Start")
pause_btn = st.sidebar.button("⏸ Pause")
reset_btn = st.sidebar.button("🔄 Reset")

# --- Session State ---
if "time" not in st.session_state:
    st.session_state.time = 0
if "running" not in st.session_state:
    st.session_state.running = False

if start_btn:
    st.session_state.running = True
if pause_btn:
    st.session_state.running = False
if reset_btn:
    st.session_state.running = False
    st.session_state.time = 0

# --- Planet Data ---
planets = [
    {"name":"Mercury","radius":0.38,"distance":0.39,"texture":"https://upload.wikimedia.org/wikipedia/commons/4/4a/Mercury_in_true_color.jpg"},
    {"name":"Venus","radius":0.95,"distance":0.72,"texture":"https://upload.wikimedia.org/wikipedia/commons/e/e5/Venus-real_color.jpg"},
    {"name":"Earth","radius":1.0,"distance":1.0,"texture":"https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg","clouds":"https://upload.wikimedia.org/wikipedia/commons/e/ed/Blue_Marble_2002.png"},
    {"name":"Mars","radius":0.53,"distance":1.52,"texture":"https://upload.wikimedia.org/wikipedia/commons/0/02/OSIRIS_Mars_true_color.jpg"},
    {"name":"Jupiter","radius":11.2,"distance":5.20,"texture":"https://upload.wikimedia.org/wikipedia/commons/e/e2/Jupiter.jpg"},
    {"name":"Saturn","radius":9.45,"distance":9.58,"texture":"https://upload.wikimedia.org/wikipedia/commons/2/29/Saturn_true_color.jpg","rings":"https://upload.wikimedia.org/wikipedia/commons/c/c7/Saturn_rings_texture.jpg"},
    {"name":"Uranus","radius":4.0,"distance":19.18,"texture":"https://upload.wikimedia.org/wikipedia/commons/3/3d/Uranus2.jpg"},
    {"name":"Neptune","radius":3.88,"distance":30.07,"texture":"https://upload.wikimedia.org/wikipedia/commons/5/56/Neptune_Full.jpg"},
]

distance_scale = 10
radius_scale = 0.2

# --- Scene and Lighting ---
scene = Scene()
scene.add(AmbientLight(intensity=0.5))
sun_geom = SphereGeometry(radius=3)
sun_mat = MeshStandardMaterial(color='yellow')
sun = Mesh(geometry=sun_geom, material=sun_mat, position=[0,0,0])
scene.add(sun)

# --- Add stars background ---
for _ in range(200):
    star = Mesh(
        geometry=SphereGeometry(radius=0.1),
        material=MeshStandardMaterial(color='white'),
        position=[random.uniform(-150,150), random.uniform(-150,150), random.uniform(-150,150)]
    )
    scene.add(star)

# --- Planets and special features ---
planet_meshes = []
for p in planets:
    geom = SphereGeometry(radius=p["radius"]*radius_scale)
    mat = MeshStandardMaterial(map=TextureLoader(texture=p["texture"]).texture)
    mesh = Mesh(geometry=geom, material=mat)
    
    # Earth clouds layer
    if "clouds" in p:
        cloud_geom = SphereGeometry(radius=p["radius"]*radius_scale*1.02)
        cloud_mat = MeshStandardMaterial(map=TextureLoader(texture=p["clouds"]).texture, transparent=True, opacity=0.5)
        cloud_mesh = Mesh(geometry=cloud_geom, material=cloud_mat)
        mesh.add(cloud_mesh)
    
    # Saturn rings
    if "rings" in p:
        ring_geom = RingGeometry(innerRadius=p["radius"]*radius_scale*1.1, outerRadius=p["radius"]*radius_scale*1.8)
        ring_mat = MeshStandardMaterial(map=TextureLoader(texture=p["rings"]).texture, side="DoubleSide", transparent=True)
        ring_mesh = Mesh(geometry=ring_geom, material=ring_mat, rotation=[math.pi/2,0,0])
        mesh.add(ring_mesh)
    
    planet_meshes.append({"mesh":mesh, "distance":p["distance"]*distance_scale, "name":p["name"]})
    scene.add(mesh)

# --- Camera ---
camera = PerspectiveCamera(position=[50,50,50], fov=45)
controls = OrbitControls(controlling=camera)
renderer = Renderer(camera=camera, scene=scene, controls=[controls], width=900, height=650)
st.components.v1.html(renderer.to_html(), height=700)

# --- Animation ---
while st.session_state.running:
    st.session_state.time += speed
    for p in planet_meshes:
        angle = st.session_state.time / p["distance"]
        p["mesh"].position = [p["distance"]*math.cos(angle), p["distance"]*math.sin(angle), 0]
        # Rotate planets on axis
        p["mesh"].rotation = [0, st.session_state.time, 0]
    time.sleep(0.05)
    st.experimental_rerun()
