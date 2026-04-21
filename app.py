import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import urllib.error

try:
    from shule_ai.subjects import KCPE_SUBJECTS, KCSE_SUBJECTS, ALL_SUBJECTS
    HAS_SHULE = True
except ImportError:
    HAS_SHULE = False

# ── AI helper — Gemini first (free tier), Anthropic fallback ────────────
_GEMINI_BASE = "https://generativelanguage.googleapis.com"
_GEMINI_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-8b"]

def _get_gemini_key():
    try:
        k = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if k: return k
    except Exception:
        pass
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", "")

def _get_anthropic_key():
    try:
        k = st.secrets.get("ANTHROPIC_API_KEY")
        if k: return k
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY", "")

def _call_gemini(system: str, user: str, api_key: str) -> str:
    import urllib.request as _req, json as _json
    payload = {
        "contents": [{"role": "user", "parts": [{"text": f"{system}\n\n{user}"}]}],
        "generationConfig": {"maxOutputTokens": 1024, "temperature": 0.3},
    }
    for model in _GEMINI_MODELS:
        url = f"{_GEMINI_BASE}/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            r = _req.urlopen(_req.Request(url,
                data=_json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"), timeout=20)
            d = _json.loads(r.read())
            return d["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                continue
            raise
    raise RuntimeError("All Gemini models unavailable")

def _call_anthropic(system: str, user: str, api_key: str) -> str:
    import anthropic as _ant
    client = _ant.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001", max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user}])
    return msg.content[0].text

def ai_call(system: str, user: str,
            gemini_key: str = "", anthropic_key: str = "") -> str:
    """Try Gemini first (free tier), fall back to Anthropic."""
    gkey = gemini_key or _get_gemini_key()
    akey = anthropic_key or _get_anthropic_key()
    if gkey:
        try:
            return _call_gemini(system, user, gkey)
        except Exception:
            pass
    if akey:
        return _call_anthropic(system, user, akey)
    raise RuntimeError("No AI key available")

def has_any_key() -> bool:
    return bool(_get_gemini_key() or _get_anthropic_key())

def which_provider() -> str:
    if _get_gemini_key(): return "gemini"
    if _get_anthropic_key(): return "anthropic"
    return "none"
# ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="ShuleAI", page_icon="📚", layout="centered")
st.markdown("""<style>
    .main > div { padding: 0.5rem 0.8rem 2rem; }
    .stTextInput > div > div > input { font-size: 1rem; }
    h1 { font-size: 1.5rem !important; }
</style>""", unsafe_allow_html=True)

if not HAS_SHULE:
    st.error("ShuleAI is temporarily unavailable. Please try again shortly.")
    st.stop()

st.title("📚 ShuleAI")
st.caption("Msaidizi wako wa masomo · Your AI study companion")

# ── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.subheader("Settings")
    provider = which_provider()
    if provider != "none":
        st.success(f"✅ AI ready ({provider.title()})")
        user_gemini_key = ""
        user_ant_key    = ""
    else:
        st.markdown(
            "**Activate the AI tutor:**\n\n"
            "Use a **free Google Gemini key** — no credit card needed.\n\n"
            "1. Go to [aistudio.google.com](https://aistudio.google.com/apikey)\n"
            "2. Click **Get API key** (free)\n"
            "3. Paste it below"
        )
        user_gemini_key = st.text_input("Google Gemini key (free):",
            type="password", placeholder="AIza...",
            help="Free at aistudio.google.com — no credit card needed.")
        st.caption("— or use Anthropic —")
        user_ant_key = st.text_input("Anthropic key (optional):",
            type="password", placeholder="sk-ant-...",
            help="Alternative to Gemini. Get one at console.anthropic.com")

    st.divider()
    level    = st.radio("Level:", ["KCPE", "KCSE"], horizontal=True)
    subjects = KCPE_SUBJECTS if level == "KCPE" else KCSE_SUBJECTS
    subject  = st.selectbox("Subject:", ["(All subjects)"] + list(subjects.keys()))
    language = st.radio("Language:", ["English", "Kiswahili"], horizontal=True)
    if st.button("🔄 New session", use_container_width=True):
        st.session_state.pop("messages", None)
        st.rerun()

active_gemini = user_gemini_key or _get_gemini_key()
active_ant    = user_ant_key    or _get_anthropic_key()

if not active_gemini and not active_ant:
    st.info(
        "👋 Welcome to ShuleAI — a free AI tutor for Kenya students "
        "(KCPE · KCSE · CBC syllabus).\n\n"
        "Add a **free Google Gemini key** in the sidebar to start studying. "
        "No credit card needed — just a Google account."
    )
    st.stop()

TUTOR_SYSTEM = """You are ShuleAI, a friendly AI tutor for Kenyan KCPE and KCSE students.
Rules:
1. Never just give answers — explain the concept first, then the solution.
2. Use the Kenya KICD curriculum as your reference.
3. If asked in Kiswahili or subject is Kiswahili/Social Studies, respond bilingually (English + Kiswahili).
4. Keep language simple and age-appropriate (ages 8–18).
5. For maths and science, always show step-by-step working.
6. Be encouraging. Acknowledge effort.
7. Stay strictly within the Kenya curriculum.
Safe content only — ages 8–18."""

if "messages" not in st.session_state:
    st.session_state.messages = []

subj_arg  = subject if subject != "(All subjects)" else None
lang_note = " [Respond bilingually EN+SW]" if language == "Kiswahili" else ""
context   = f"[Level: {level}]" + (f" [Subject: {subj_arg}]" if subj_arg else "") + lang_note

cols = st.columns(3)
if cols[0].button("📝 Practice questions", use_container_width=True):
    subj_label = subj_arg or "Mathematics"
    with st.spinner("Generating..."):
        try:
            ans = ai_call(TUTOR_SYSTEM,
                f"Generate 5 practice questions on mixed topics for {subj_label} {level}. "
                f"Show worked solutions after all questions.",
                active_gemini, active_ant)
            st.session_state.messages.append(("assistant", ans))
        except Exception:
            st.error("Could not generate questions. Please try again.")

if cols[1].button("💡 Explain concept", use_container_width=True):
    st.session_state.messages.append(("assistant",
        "Type the concept below and I'll explain it step by step. "
        "E.g. *photosynthesis*, *quadratic equations*, *mapwork skills*."))

if cols[2].button("📖 Revision tips", use_container_width=True):
    subj_label = subj_arg or "all subjects"
    with st.spinner("Thinking..."):
        try:
            tips = ai_call(TUTOR_SYSTEM,
                f"Give me 5 targeted revision tips for {subj_label} {level} in Kenya.",
                active_gemini, active_ant)
            st.session_state.messages.append(("assistant", tips))
        except Exception:
            st.error("Could not load revision tips.")

for role, msg in st.session_state.messages[-10:]:
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
                answer = ai_call(TUTOR_SYSTEM, f"{context}\n\n{user_input}",
                                 active_gemini, active_ant)
            except RuntimeError:
                answer = ("Your API key doesn't seem to be working. "
                          "Please check it in the sidebar and try again.")
            except Exception:
                answer = "Something went wrong. Please try again."
        st.markdown(answer)
    st.session_state.messages.append(("assistant", answer))

st.divider()
st.caption("© 2026 Gabriel Mahia · KICD aligned · [GitHub](https://github.com/gabrielmahia/shule-ai) · Free to use")
