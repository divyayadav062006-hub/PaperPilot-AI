import os
import streamlit as st

from dotenv import load_dotenv
from google import genai

from ui import (
    load_custom_css,
    show_hero
)

from services import (
    extract_text_from_pdf,
    calculate_reading_time
)
def extract_section(text, start, end=None):

    try:

        start_index = text.index(start) + len(start)

        if end and end in text:

            end_index = text.index(end)

            return text[start_index:end_index].strip()

        return text[start_index:].strip()

    except ValueError:

        return ""
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found.")
    st.stop()

client = genai.Client(
    api_key=API_KEY
)

MAX_TEXT_LENGTH = 80000
st.set_page_config(
    page_title="PaperPilot AI",
    page_icon="🧭",
    layout="wide"
)

load_custom_css()

show_hero()
if "messages" not in st.session_state:
    st.session_state.messages = []

if "analysis" not in st.session_state:
    st.session_state.analysis = None

st.markdown("""
### 📚 AI-Powered Document Analysis

Upload any PDF and PaperPilot AI will:

✅ Detect document type

✅ Generate intelligent insights

✅ Create study roadmaps

✅ Generate project ideas (when applicable)

✅ Answer your questions
""")

uploaded_file = st.file_uploader(
    "📂 Upload PDF (Research Papers, Notes, Syllabus, Reports)",
    type=["pdf"]
)

if uploaded_file:

    pdf_data = extract_text_from_pdf(
        uploaded_file
    )

    text = pdf_data["text"]

    pages = pdf_data["pages"]

    reading_time = calculate_reading_time(
        text
    )

    time_saved = max(
        0,
        reading_time - 3
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📄 Pages",
            pages
        )

    with col2:
        st.metric(
            "⏱ Reading Time",
            f"{reading_time} min"
        )

    with col3:
        st.metric(
            "⚡ Time Saved",
            f"{time_saved} min"
        )

    with col4:
        st.metric(
            "🔤 Characters",
            len(text)
        )

    with st.expander(
        "📖 Preview PDF"
    ):

        st.text_area(
            "",
            text[:3000],
            height=250
        )
    if st.button(
        "🚀 Generate Insights",
        use_container_width=True
    ):

        with st.spinner(
            "🧠 Analyzing Document..."
        ):

            prompt = f"""
You are PaperPilot AI.

Analyze the uploaded document.

First determine its document type.

Possible document types:

- Research Paper
- Study Material
- Syllabus
- Technical Documentation
- Report
- Book Chapter

Return in EXACT format:

DOCUMENT_TYPE:
<document type>

EXECUTIVE_SUMMARY:
<summary>

KEY_TAKEAWAYS:
<5 bullet points>

TARGET_AUDIENCE:
<audience>

READING_DIFFICULTY:
<Beginner/Intermediate/Advanced>

If document type is Research Paper also include:

RESEARCH_GAPS:
...

PROJECT_IDEAS:
...

VIVA_QUESTIONS:
...

If document type is Study Material also include:

REVISION_NOTES:
...

IMPORTANT_TOPICS:
...

PRACTICE_QUESTIONS:
...

If document type is Syllabus also include:

IMPORTANT_SUBJECTS:
...

STUDY_ROADMAP:
...

PREPARATION_STRATEGY:
...

Document:

{text[:MAX_TEXT_LENGTH]}
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.session_state.analysis = response.text

            st.session_state.messages = []
if st.session_state.analysis:

    analysis = st.session_state.analysis

    document_type = extract_section(
        analysis,
        "DOCUMENT_TYPE:",
        "EXECUTIVE_SUMMARY:"
    )

    summary = extract_section(
        analysis,
        "EXECUTIVE_SUMMARY:",
        "KEY_TAKEAWAYS:"
    )

    takeaways = extract_section(
        analysis,
        "KEY_TAKEAWAYS:",
        "TARGET_AUDIENCE:"
    )

    audience = extract_section(
        analysis,
        "TARGET_AUDIENCE:",
        "READING_DIFFICULTY:"
    )

    difficulty = extract_section(
        analysis,
        "READING_DIFFICULTY:"
    )
    
    

    st.success(
        f"🧠 PaperPilot detected this document as: {document_type}"
    )

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 Summary",
            "🎯 Takeaways",
            "👥 Audience",
            "📈 Difficulty",
            "💬 Chat"
        ]
    )

    with tab1:

        st.markdown(summary)

    with tab2:

        st.markdown(takeaways)

    with tab3:

        st.markdown(audience)

    with tab4:

        st.markdown(difficulty)

    with tab5:

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )

        question = st.chat_input(
            "Ask anything about the document..."
        )

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message(
                "user"
            ):

                st.markdown(question)

            chat_prompt = f"""
Document Type:

{document_type}

Document Analysis:

{analysis}

User Question:

{question}

Instructions:

Answer based on the uploaded document.
If the answer is not present in the document,
say so clearly.
"""

            with st.spinner(
                "Thinking..."
            ):

                answer = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=chat_prompt
                ).text

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()