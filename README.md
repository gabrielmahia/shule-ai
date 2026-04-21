# 📚 ShuleAI — Kenya Curriculum AI Tutor

> AI tutor for KCPE and KCSE students. CBC syllabus. Answers in Kiswahili and English. Runs on any phone with a browser — no app install required.

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)](https://shule-ai.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)

## What it does

ShuleAI is a free AI study companion grounded in the Kenya Institute of Curriculum Development (KICD) syllabus. It answers exam questions, explains concepts, generates practice problems, and gives worked solutions — all in plain language.

| Feature | Description |
|---------|-------------|
| 📖 **Subject coverage** | Mathematics, English, Kiswahili, Sciences, History, Geography, CRE |
| 🗣️ **Bilingual** | Explains in English and Kiswahili on request |
| 📝 **Practice generator** | Generates KCPE/KCSE-style practice questions with worked answers |
| 🧮 **Worked solutions** | Step-by-step math and science solutions |
| 📱 **Mobile-first** | Designed for phone screens — no app download needed |
| 🔒 **Safe** | Content-filtered for age-appropriate responses; no personal data stored |

## Live demo

🌐 [shule-ai.streamlit.app](https://shule-ai.streamlit.app)

## Quickstart

```bash
git clone https://github.com/gabrielmahia/shule-ai
cd shule-ai
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
streamlit run app.py
```

## Why this exists

Kenya has 9 million primary school pupils and 3.5 million secondary students. The average pupil-to-teacher ratio is 45:1. Most students in rural areas have no access to private tutors. A phone with data and ShuleAI changes that.

ShuleAI is grounded in the KICD syllabus — it won't answer questions outside the curriculum, and it won't do students' homework without teaching the concept first.

## Example interactions

```
Student: Explain photosynthesis for Form 2 Biology
ShuleAI: Photosynthesis ni mchakato ambao mimea hutumia jua, maji, na dioksidi ya kaboni
         kutengeneza chakula...
         [Full bilingual explanation follows]

Student: Give me 5 KCPE maths practice questions on fractions
ShuleAI: [Generates 5 graded questions with worked solutions]

Student: I got 45/100 in my last test. What should I focus on?
ShuleAI: [Subject-specific revision plan based on common weak areas]
```

## Architecture

```
shule_ai/
  ├── tutor.py        ← Core tutor engine (syllabus-grounded prompting)
  ├── subjects.py     ← KICD subject/topic hierarchy for KCPE + KCSE
  ├── safety.py       ← Content filter for age-appropriate responses
  └── practice.py     ← Practice question generator + answer checker
app.py                ← Streamlit mobile-first UI
```

## Roadmap

- [ ] SMS interface via Africa's Talking (works on feature phones)
- [ ] Offline mode with cached responses for low-connectivity areas
- [ ] Teacher dashboard (class performance analytics)
- [ ] Integration with Kenya's Digital Literacy Programme devices

## Partnerships

Interested in deploying ShuleAI in your school, NGO, or county? [contact@aikungfu.dev](mailto:contact@aikungfu.dev)

## Related

- [Jibu](https://github.com/gabrielmahia/jibu) — AI civic rights assistant (EN/SW)
- [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) — M-Pesa MCP server
- [gabrielmahia.github.io](https://gabrielmahia.github.io) — Full portfolio

## IP & Collaboration

© 2026 Gabriel Mahia · [contact@aikungfu.dev](mailto:contact@aikungfu.dev)
License: CC BY-NC-ND 4.0
Not affiliated with KICD, KNEC, or the Kenya Ministry of Education.
