"""ShuleAI tutor — Kenya KICD curriculum AI. Uses llm_router (Gemini/Anthropic)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_router import ask as _ask

SYSTEM = """You are ShuleAI, a friendly AI tutor for Kenyan students preparing for KCPE and KCSE.

Rules:
1. NEVER just give the answer — explain the concept first, then show the working
2. Use only the Kenya KICD curriculum as your reference
3. Keep language simple and age-appropriate (ages 8–18)
4. For maths and sciences, show step-by-step working
5. Encourage students warmly
6. When the subject is Kiswahili, Social Studies or History respond bilingually (EN + SW)
7. Stay strictly within the Kenya curriculum — no content outside it
8. If asked anything non-educational, reply: "Ninaomba uniulize swali la masomo tu."
"""

class ShuleTutor:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.history: list[dict] = []

    def ask(self, question: str, subject: str = None, level: str = "KCSE") -> str:
        context = f"[Level: {level}]"
        if subject:
            context += f" [Subject: {subject}]"
        prompt = f"{context}\n\n{question}"
        return _ask(prompt, system=SYSTEM, user_key=self.api_key)

    def generate_practice(self, subject: str, topic: str, count: int = 5, level: str = "KCSE") -> str:
        prompt = (
            f"Generate exactly {count} practice questions on {topic} ({subject}, {level} level). "
            f"Kenya KICD syllabus only. Show numbered questions first, then all worked solutions. "
            f"Include mark allocation for each question."
        )
        return _ask(prompt, system=SYSTEM, user_key=self.api_key)

    def reset(self):
        self.history = []
