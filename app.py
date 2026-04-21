import sys, os
# shule_ai/ is at repo root — auto-importable on Streamlit Cloud
# But add explicit path for safety across environments
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# Graceful imports
try:
    from shule_ai.tutor import ShuleTutor
    from shule_ai.subjects import KCPE_SUBJECTS, KCSE_SUBJECTS, ALL_SUBJECTS
    HAS_SHULE = True
except ImportError:
    HAS_SHULE = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

st.set_page_config(page_title="ShuleAI", page_icon="📚", layout="centered")

# Mobile-first CSS
st.markdown("""<style>
    .main > div { padding: 0.5rem 0.8rem 2rem; }
    .stTextInput > div > div > input { font-size: 1rem; }
    .stSelectbox > div > div { font-size: 1rem; }
    h1 { font-size: 1.5rem !important; }
</style>""", unsafe_allow_html=True)

if not HAS_SHULE:
    st.error("ShuleAI is temporarily unavailable. Please try again shortly.")
    st.stop()

st.title("📚 ShuleAI")
st.caption("Msaidizi wako wa masomo · Your AI study companion")

# ── API key handling — safe and context-aware ─────────────────
ENV_KEY = os.getenv("ANTHROPIC_API_KEY", "")

with st.sidebar:
    st.subheader("Settings")

    if ENV_KEY:
        # Key already configured server-side — don't expose it
        api_key = ENV_KEY
        st.success("✅ AI tutor ready")
    elif not HAS_ANTHROPIC:
        st.warning("AI features unavailable.")
        api_key = ""
    else:
        st.markdown(
            "**To activate the AI tutor:**\n\n"
            "You need a free Anthropic API key.\n\n"
            "1. Go to [console.anthropic.com](https://console.anthropic.com)\n"
            "2. Create a free account\n"
            "3. Generate an API key\n"
            "4. Paste it below"
        )
        api_key = st.text_input(
            "API key:",
            type="password",
            placeholder="sk-ant-...",
            help="Your key is used only to connect to Anthropic — it is never stored or logged."
        )
        if api_key and not api_key.startswith("sk-ant-"):
            st.warning("That doesn't look like a valid Anthropic key. Keys start with sk-ant-")

    st.divider()
    level   = st.radio("Exam level:", ["KCPE", "KCSE"], horizontal=True)
    subjects = KCPE_SUBJECTS if level == "KCPE" else KCSE_SUBJECTS
    subject  = st.selectbox("Subject:", ["(All subjects)"] + list(subjects.keys()))
    language = st.radio("Language:", ["English", "Kiswahili"], horizontal=True)

    if st.button("🔄 New session", use_container_width=True):
        for k in ["tutor","messages"]:
            st.session_state.pop(k, None)
        st.rerun()

if not api_key:
    st.info(
        "👋 Welcome to ShuleAI — a free AI tutor for Kenya students.\n\n"
        "**To get started:** add your Anthropic API key in the sidebar. "
        "A free account at [console.anthropic.com](https://console.anthropic.com) gives you enough credits to study."
    )
    st.caption("ShuleAI covers KCPE and KCSE · Aligned with KICD curriculum · Answers in English and Kiswahili")
    st.stop()

# Initialise session
if "tutor" not in st.session_state:
    try:
        st.session_state.tutor    = ShuleTutor(api_key=api_key)
        st.session_state.messages = []
    except Exception:
        st.error("Could not start the tutor. Please check your API key and try again.")
        st.stop()

# Quick actions
cols = st.columns(3)
if cols[0].button("📝 Practice questions", use_container_width=True):
    subj = subject if subject != "(All subjects)" else "Mathematics"
    with st.spinner("Generating practice questions..."):
        try:
            ans = st.session_state.tutor.generate_practice(subj, "mixed topics", 5, level)
            st.session_state.messages.append(("assistant", ans))
        except Exception:
            st.error("Could not generate questions right now. Please try again.")

if cols[1].button("💡 Explain concept", use_container_width=True):
    st.session_state.messages.append(("assistant",
        "Sure! Type the concept you want explained below, e.g. *photosynthesis* or *quadratic equations*."))

if cols[2].button("📖 Revision tips", use_container_width=True):
    subj_label = subject if subject != "(All subjects)" else "all subjects"
    with st.spinner("Thinking..."):
        try:
            tips = st.session_state.tutor.ask(
                f"Give me 5 targeted revision tips for {subj_label} {level} in Kenya.",
                subject=subj_label if subject != "(All subjects)" else None,
                level=level)
            st.session_state.messages.append(("assistant", tips))
        except Exception:
            st.error("Could not load revision tips right now.")

# Chat history
for role, msg in st.session_state.get("messages", [])[-10:]:
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
            try:
                lang     = "sw" if language == "Kiswahili" else "en"
                subj_arg = subject if subject != "(All subjects)" else None
                answer   = st.session_state.tutor.ask(user_input, subject=subj_arg, level=level)
            except anthropic.AuthenticationError:
                answer = "Your API key doesn't seem to be working. Please check it in the sidebar and try again."
            except anthropic.RateLimitError:
                answer = "You've hit the rate limit on your API key. Please wait a moment and try again."
            except Exception:
                answer = "Something went wrong. Please try again — if the problem continues, contact contact@aikungfu.dev"
        st.markdown(answer)
    st.session_state.messages.append(("assistant", answer))

st.divider()
st.caption("© 2026 Gabriel Mahia · KICD syllabus aligned · [GitHub](https://github.com/gabrielmahia/shule-ai) · Free to use · Not affiliated with KICD or KNEC")
