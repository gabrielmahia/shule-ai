"""ShuleAI core tutor engine."""
import os
import anthropic
from .subjects import ALL_SUBJECTS, BILINGUAL_SUBJECTS


SYSTEM_PROMPT = """You are ShuleAI, a friendly and encouraging AI tutor for Kenyan students preparing for KCPE and KCSE examinations.

Your teaching philosophy:
1. NEVER just give an answer — always explain the concept first, then show the solution
2. Use the KICD Kenya curriculum syllabus as your frame of reference
3. When asked in Kiswahili or if the subject is in BILINGUAL_SUBJECTS, respond bilingually (EN + SW)
4. Keep language simple and age-appropriate (primary and secondary school level)
5. For mathematics and sciences, always show step-by-step working
6. Encourage students — acknowledge effort, not just correct answers
7. Stay strictly within the Kenya curriculum — do not teach content outside it
8. Do not do assignments or exams for students — teach the method, not the answer

Safe content: Only respond to educational questions appropriate for ages 8–18.
If asked anything outside education, politely redirect: "Ninaomba uniulize swali la masomo."
"""

class ShuleTutor:
    """Kenya curriculum AI tutor powered by Claude."""

    def __init__(self, api_key: str = None):
        key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError("Set ANTHROPIC_API_KEY environment variable")
        self.client = anthropic.Anthropic(api_key=key)
        self.history = []

    def ask(self, question: str, subject: str = None, level: str = "KCSE") -> str:
        """Ask the tutor a question."""
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
        self.history.append({"role": "user", "content": user_msg})

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=self.history,
        )
        answer = response.content[0].text
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def generate_practice(self, subject: str, topic: str, count: int = 5, level: str = "KCSE") -> str:
        """Generate practice questions with worked answers."""
        prompt = (
            f"Generate exactly {count} practice questions on {topic} ({subject}, {level} level). "
            f"Format: numbered questions first, then all worked solutions. "
            f"Kenya KICD syllabus only. Include mark allocation for each question."
        )
        return self.ask(prompt, subject=subject, level=level)

    def explain_concept(self, concept: str, subject: str = None, language: str = "en") -> str:
        """Explain a concept in simple terms."""
        lang_note = "Explain in Kiswahili first, then English." if language == "sw" else ""
        prompt = f"Explain this concept for a Kenya student: {concept}. {lang_note} Use examples relevant to Kenya."
        return self.ask(prompt, subject=subject)

    def reset(self):
        self.history = []
