"""ShuleAI Streamlit app — mobile-first Kenya curriculum tutor."""
import os, streamlit as st
from shule_ai.tutor import ShuleTutor
from shule_ai.subjects import KCPE_SUBJECTS, KCSE_SUBJECTS, ALL_SUBJECTS

st.set_page_config(page_title="ShuleAI", page_icon="📚", layout="centered")

# Mobile-first CSS
st.markdown("""<style>
    .main > div { padding: 0.5rem 0.8rem 2rem; }
    .stTextInput > div > div > input { font-size: 1rem; }
    .stSelectbox > div > div { font-size: 1rem; }
    h1 { font-size: 1.5rem !important; }
</style>""", unsafe_allow_html=True)

st.title("📚 ShuleAI")
st.caption("Msaidizi wako wa masomo · Your AI study companion")

with st.sidebar:
    api_key = st.text_input("Anthropic API Key:", type="password",
                             value=os.getenv("ANTHROPIC_API_KEY",""), key="api_key_input")
    level   = st.radio("Level:", ["KCPE", "KCSE"], horizontal=True)
    subjects = KCPE_SUBJECTS if level == "KCPE" else KCSE_SUBJECTS
    subject  = st.selectbox("Subject:", ["(General)"] + list(subjects.keys()))
    language = st.radio("Language:", ["English", "Kiswahili"], horizontal=True)
    if st.button("New session"):
        st.session_state.pop("tutor", None)
        st.session_state.pop("messages", None)
        st.rerun()

if not api_key:
    st.info("Add your Anthropic API key in the sidebar to start studying.")
    st.caption("Get a free key at [anthropic.com](https://anthropic.com)")
    st.stop()

if "tutor" not in st.session_state:
    st.session_state.tutor    = ShuleTutor(api_key=api_key)
    st.session_state.messages = []

# Quick actions
cols = st.columns(3)
if cols[0].button("📝 Practice questions", use_container_width=True):
    subj = subject if subject != "(General)" else "Mathematics"
    with st.spinner("Generating questions..."):
        ans = st.session_state.tutor.generate_practice(subj, "mixed topics", 5, level)
    st.session_state.messages.append(("assistant", ans))

if cols[1].button("💡 Explain a concept", use_container_width=True):
    st.session_state.messages.append(("assistant",
        "Sure! Type the concept you want explained below."))

if cols[2].button("📖 Revision tips", use_container_width=True):
    with st.spinner("Thinking..."):
        subj = subject if subject != "(General)" else "all subjects"
        tip  = st.session_state.tutor.ask(
            f"Give me 5 targeted revision tips for {subj} {level}.",
            subject=subj if subject != "(General)" else None,
            level=level)
    st.session_state.messages.append(("assistant", tip))

# Chat display
for role, msg in st.session_state.messages[-10:]:
    with st.chat_message(role):
        st.markdown(msg)

# Input
user_input = st.chat_input("Uliza swali · Ask a question...")
if user_input:
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Nafikiri... · Thinking..."):
            lang = "sw" if language == "Kiswahili" else "en"
            subj_arg = subject if subject != "(General)" else None
            answer = st.session_state.tutor.ask(user_input, subject=subj_arg, level=level)
            st.markdown(answer)
    st.session_state.messages.append(("assistant", answer))

st.divider()
st.caption("© 2026 Gabriel Mahia · KICD syllabus aligned · [GitHub](https://github.com/gabrielmahia/shule-ai)")
