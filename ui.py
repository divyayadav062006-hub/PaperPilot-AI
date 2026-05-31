import streamlit as st


def load_custom_css():

    st.markdown("""
    <style>

    .stApp{
        background:
        linear-gradient(
        180deg,
        #0F172A 0%,
        #111827 100%
        );
    }

    .hero{
        padding:40px;
        border-radius:25px;
        background:
        linear-gradient(
        135deg,
        #2563EB,
        #06B6D4
        );
        color:white;
        text-align:center;
        margin-bottom:25px;
        box-shadow:
        0px 10px 40px rgba(0,0,0,0.35);
    }

    .glass-card{
        background:
        rgba(255,255,255,0.05);

        backdrop-filter: blur(12px);

        border:
        1px solid rgba(255,255,255,0.08);

        border-radius:20px;

        padding:20px;

        transition:0.3s;
    }

    .glass-card:hover{
        transform:
        translateY(-5px);
    }

    .section-card{
        background:#111827;
        border-radius:20px;
        padding:20px;
        margin-top:15px;
        border:
        1px solid rgba(255,255,255,0.08);
    }

    </style>
    """,
    unsafe_allow_html=True)


def show_hero():

    st.markdown("""
    <div class="hero">

    <h1>🧭 PaperPilot AI</h1>

    <h3>
    Transform Documents into Intelligence
    </h3>

    <p>
    AI-powered analysis for research papers, syllabi, reports, and study materials.
    </p>

    </div>
    """,
    unsafe_allow_html=True)