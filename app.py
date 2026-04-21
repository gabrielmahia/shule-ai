import sys, os, json, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

try:
    from shule_ai.tutor import ShuleTutor
    from shule_ai.subjects import KCPE_SUBJECTS, KCSE_SUBJECTS, ALL_SUBJECTS
    HAS_SHULE = True
except ImportError:
    HAS_SHULE = False


def _get_api_key():
    """Gemini key from Streamlit secrets or env. Free at aistudio.google.com"""
    try:
        import streamlit as st
        k = (st.secrets.get("GOOGLE_API_KEY")
             or st.secrets.get("GEMINI_API_KEY"))
        if k:
            return k
    except Exception:
        pass
    return (os.environ.get("GOOGLE_API_KEY")
            or os.environ.get("GEMINI_API_KEY", ""))


def _call_gemini(system: str, user: str, api_key: str) -> str:
    """Call Gemini REST API directly — no SDK needed. Free tier works."""
    _BASE = "https://generativelanguage.googleapis.com"
    models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-8b"]
    payload = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"maxOutputTokens": 800, "temperature": 0.3},
    }
    last_err = ""
    for model in models:
        url = f"{_BASE}/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code in (400, 404):
                continue   # try next model
            raise
        except Exception as e:
            last_err = str(e)
            continue
    raise RuntimeError(f"All Gemini models failed. Last error: {last_err}")


st.set_page_config(page_title="ShuleAI", page_icon="📚", layout="centered")
st.markdown("""<style>
    .main > div { padding: 0.5rem 0.8rem 2rem; }
    h1 { font-size: 1.5rem !important; }
</style>""", unsafe_allow_html=True)

if not HAS_SHULE:
    st.error("ShuleAI is temporarily unavailable. Please try again shortly.")
    st.stop()

st.title("📚 ShuleAI")
st.caption("Msaidizi wako wa masomo · Your AI study companion")

api_key = _get_api_key()

with st.sidebar:
    st.subheader("Settings")
    if api_key:
        st.success("✅ AI tutor ready")
    else:
        st.markdown(
            "**Activate the AI tutor — it's free:**\n\n"
            "1. Go to [aistudio.google.com](https://aistudio.google.com)\n"
            "2. Sign in with Google\n"
            "3. Click **Get API key**\n"
            "4. Paste it below"
        )
        api_key = st.text_input("Google AI / Gemini key:",
                                 type="password",
                                 placeholder="AIza...",
                                 help="Free at aistudio.google.com. Never stored or logged here.")

    st.divider()
    level    = st.radio("Exam level:", ["KCPE", "KCSE"], horizontal=True)
    subjects = KCPE_SUBJECTS if level == "KCPE" else KCSE_SUBJECTS
    subject  = st.selectbox("Subject:", ["(All subjects)"] + list(subjects.keys()))
    language = st.radio("Language:", ["English", "Kiswahili"], horizontal=True)
    if st.button("🔄 New session", use_container_width=True):
        for k in ["messages"]: st.session_state.pop(k, None)
        st.rerun()

if not api_key:
    st.info(
        "👋 Welcome to ShuleAI — a free AI study companion for Kenya students.\n\n"
        "Get a **free** Google AI key at [aistudio.google.com](https://aistudio.google.com) "
        "— no credit card required."
    )
    st.caption("Covers KCPE and KCSE · KICD curriculum · English and Kiswahili")
    st.stop()

SYSTEM = """You are ShuleAI, a friendly AI tutor for Kenya students preparing for KCPE and KCSE.
Rules:
1. Never just give the answer — explain the concept first, then show the solution
2. Use the KICD Kenya curriculum as your frame of reference
3. For Kiswahili questions or when asked in Kiswahili, respond bilingually (EN + SW)
4. Keep language simple and age-appropriate (primary and secondary school level)
5. For maths and sciences, always show step-by-step working
6. Encourage students — be warm and supportive
7. Stay strictly within the Kenya curriculum
8. Do not do assignments or exams for students — teach the method"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick actions
cols = st.columns(3)
if cols[0].button("📝 Practice questions", use_container_width=True):
    subj = subject if subject != "(All subjects)" else "Mathematics"
    with st.spinner("Generating questions..."):
        try:
            ans = _call_gemini(SYSTEM,
                f"Generate 5 {level} practice questions on {subj}, mixed topics. "
                f"Number them. Then provide full worked solutions with mark allocation.",
                api_key)
            st.session_state.messages.append(("assistant", ans))
        except Exception:
            st.error("Could not generate questions. Please check your API key.")

if cols[1].button("💡 Explain concept", use_container_width=True):
    st.session_state.messages.append(("assistant",
        "Sure! Type the concept below, e.g. *photosynthesis* or *quadratic equations*."))

if cols[2].button("📖 Revision tips", use_container_width=True):
    subj_label = subject if subject != "(All subjects)" else "all KCSE subjects"
    with st.spinner("Thinking..."):
        try:
            tips = _call_gemini(SYSTEM,
                f"Give 5 targeted revision tips for {subj_label} {level} in Kenya.",
                api_key)
            st.session_state.messages.append(("assistant", tips))
        except Exception:
            st.error("Could not load tips. Please try again.")

for role, msg in st.session_state.get("messages", [])[-10:]:
    with st.chat_message(role):
        st.markdown(msg)

user_input = st.chat_input("Uliza swali · Ask a question...")
if user_input:
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Nafikiri... · Thinking..."):
            try:
                lang_note = " Respond bilingually in English and Kiswahili." if language == "Kiswahili" else ""
                subj_note = f" Subject: {subject}." if subject != "(All subjects)" else ""
                answer = _call_gemini(SYSTEM,
                    f"[{level}]{subj_note}{lang_note}\n\n{user_input}",
                    api_key)
            except urllib.error.HTTPError as e:
                if e.code == 400:
                    answer = "That question couldn't be processed. Please try rephrasing it."
                elif e.code == 403:
                    answer = "API key not recognised. Please check your key in the sidebar."
                elif e.code == 429:
                    answer = "Too many requests — please wait a moment and try again."
                else:
                    answer = "Something went wrong. Please try again."
            except Exception:
                answer = "Something went wrong. Please try again — if it continues, contact contact@aikungfu.dev"
        st.markdown(answer)
    st.session_state.messages.append(("assistant", answer))

st.divider()
st.caption("© 2026 Gabriel Mahia · KICD aligned · [GitHub](https://github.com/gabrielmahia/shule-ai) · Powered by Google Gemini · Free to use")
