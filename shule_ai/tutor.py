"""ShuleAI core tutor engine — supports Gemini (default) and Anthropic."""
import os
from .subjects import ALL_SUBJECTS, BILINGUAL_SUBJECTS

SYSTEM_PROMPT = """You are ShuleAI, a friendly and encouraging AI tutor for Kenyan students preparing for KCPE and KCSE examinations.

Your teaching philosophy:
1. NEVER just give an answer — always explain the concept first, then show the solution
2. Use the KICD Kenya curriculum syllabus as your frame of reference
3. When asked in Kiswahili or if the subject is Kiswahili/Social Studies/History/Geography, respond bilingually (English + Kiswahili)
4. Keep language simple and age-appropriate (primary and secondary school level)
5. For mathematics and sciences, always show step-by-step working
6. Encourage students warmly — acknowledge effort, not just correct answers
7. Stay strictly within the Kenya curriculum — do not teach content outside it
8. Do not do assignments for students — teach the method, not just the answer

Safe content: Only respond to educational questions appropriate for ages 8–18.
If asked anything outside education, respond: "Ninaomba uniulize swali la masomo." / "Please ask me a school question."
"""


def _detect_provider(api_key: str) -> str:
    """Detect AI provider from key prefix."""
    if not api_key:
        return "none"
    if api_key.startswith("AIza"):
        return "gemini"
    if api_key.startswith("sk-ant-"):
        return "anthropic"
    return "unknown"


class ShuleTutor:
    """Kenya curriculum AI tutor — supports Gemini 2.0 Flash and Claude Haiku."""

    def __init__(self, api_key: str = None):
        self.api_key  = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        self.provider = _detect_provider(self.api_key) if self.api_key else "none"
        self.history  = []
        if not self.api_key:
            raise ValueError("Set GEMINI_API_KEY or ANTHROPIC_API_KEY")

    def ask(self, question: str, subject: str = None, level: str = "KCSE") -> str:
        context = f"[Level: {level}]"
        if subject:
            topics = ALL_SUBJECTS.get(subject, [])
            bilingual = subject in BILINGUAL_SUBJECTS
            context += f" [Subject: {subject}]"
            if bilingual:
                context += " [Respond bilingually EN+SW]"
            if topics:
                context += f" [Key topics: {', '.join(topics[:4])}]"
        user_msg = f"{context}\n\n{question}"

        if self.provider == "gemini":
            return self._ask_gemini(user_msg)
        elif self.provider == "anthropic":
            return self._ask_anthropic(user_msg)
        else:
            return "Please provide a valid Gemini (AIza...) or Anthropic (sk-ant-...) API key."

    def _ask_gemini(self, message: str) -> str:
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            "gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT
        )
        # Build history for multi-turn
        history = []
        for role, text in self.history[-8:]:  # last 4 turns
            g_role = "user" if role == "user" else "model"
            history.append({"role": g_role, "parts": [text]})
        chat = model.start_chat(history=history)
        resp = chat.send_message(message)
        answer = resp.text
        self.history.append(("user", message))
        self.history.append(("assistant", answer))
        return answer

    def _ask_anthropic(self, message: str) -> str:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        self.history.append({"role": "user", "content": message})
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=self.history,
        )
        answer = resp.content[0].text
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def generate_practice(self, subject: str, topic: str, count: int = 5, level: str = "KCSE") -> str:
        prompt = (
            f"Generate exactly {count} practice questions on {topic} ({subject}, {level} level). "
            f"Format: numbered questions first, then all worked solutions. "
            f"Kenya KICD syllabus only. Include mark allocation."
        )
        return self.ask(prompt, subject=subject, level=level)

    def reset(self):
        self.history = []
