# gui/vm_sim_streamlit.py

import streamlit as st
import sys, os

# Add parent directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.paging_core import PagingSimulation
from core.segmentation_core import SegmentationSimulation
from visualization.visualizer import plot_paging, plot_segmentation

# ==========================
# 🌈 Streamlit Page Config
# ==========================
st.set_page_config(
    page_title="Virtual Memory Optimization Challenge",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# 🎨 Load External CSS
# ==========================
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = os.path.join(os.path.dirname(__file__), "style.css")
load_css(css_path)

# ==========================
# 🚀 App Header
# ==========================
st.markdown("<h1 style='text-align:center;'>🧠 Virtual Memory Optimization Challenge</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("⚙️ Navigation")
option = st.sidebar.radio("Choose Simulation Mode", ["Paging Simulation", "Segmentation Simulation"])

# ==========================
# 🧩 Paging Simulation
# ==========================
if option == "Paging Simulation":
    st.markdown("<h2>📄 Paging Simulation</h2>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        pages_input = st.text_input("Enter page reference string (comma separated):", "1,2,3,4,2,1,5,1,2,3,4,5")
        frames = st.number_input("Enter number of frames:", 1, 10, 3)
        algo = st.selectbox("Select Page Replacement Algorithm:", ["LRU", "Optimal"])
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("▶️ Run Paging Simulation"):
        pages = [int(x.strip()) for x in pages_input.split(",")]
        sim = PagingSimulation(reference_string=pages, n_frames=frames, algorithm=algo)
        if algo == "LRU":
            faults, history = sim.simulate_LRU()
        else:
            faults, history = sim.simulate_Optimal()

        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.subheader("📊 Simulation Results")
        st.write(f"**Total Page Faults:** {faults}")
        fig = plot_paging(history, f"Paging Simulation ({algo})")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# 📦 Segmentation Simulation
# ==========================
else:
    st.markdown("<h2>📦 Segmentation Simulation</h2>", unsafe_allow_html=True)
    total_memory = st.number_input("Enter total memory size:", 100, 1000, 300)
    sim = SegmentationSimulation(total_memory)

    if "segments" not in st.session_state:
        st.session_state["segments"] = sim

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        name = st.text_input("Segment Name")
        size = st.number_input("Segment Size", 1, total_memory)
        if st.button("🟢 Allocate Segment"):
            st.success(st.session_state["segments"].allocate(name, size))
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        name_del = st.text_input("Deallocate Segment Name")
        if st.button("🔴 Deallocate Segment"):
            st.warning(st.session_state["segments"].deallocate(name_del))
        st.markdown("</div>", unsafe_allow_html=True)

    segs = st.session_state["segments"].segments
    if segs:
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.subheader("🧩 Segmentation Memory Layout")
        fig = plot_segmentation(segs, total_memory)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# 🪶 Footer
# ==========================
st.markdown("<div class='footer'>Developed by <b>Souvik Mondal</b> | © 2025 Virtual Memory Lab</div>", unsafe_allow_html=True)
