"""Kenya KICD curriculum — subjects and topic hierarchy."""

KCPE_SUBJECTS = {
    "Mathematics": [
        "Numbers and Operations", "Fractions and Decimals", "Percentages",
        "Measurement — Length, Area, Volume", "Time and Money",
        "Geometry — Shapes and Angles", "Data Handling", "Algebra Basics",
    ],
    "English": [
        "Reading Comprehension", "Grammar and Language Use", "Composition Writing",
        "Oral Skills", "Literature — Oral and Written",
    ],
    "Kiswahili": [
        "Usomaji na Ufahamu", "Sarufi", "Insha", "Fasihi Simulizi", "Mazungumzo",
    ],
    "Science and Technology": [
        "Living Things", "Environment", "Health", "Matter", "Energy",
        "Force and Simple Machines",
    ],
    "Social Studies": [
        "Kenya Geography", "Kenya History", "Civic Education",
        "East Africa", "Africa", "World Geography",
    ],
    "CRE": [
        "Creation", "Family", "Jesus Christ", "Early Church", "Social Issues",
    ],
}

KCSE_SUBJECTS = {
    "Mathematics": [
        "Algebra", "Quadratic Equations", "Logarithms", "Trigonometry",
        "Statistics and Probability", "Matrices", "Vectors", "Calculus",
    ],
    "English": [
        "Comprehension", "Grammar", "Composition", "Literature — Novels",
        "Literature — Drama", "Literature — Poetry",
    ],
    "Kiswahili": [
        "Ufahamu", "Sarufi", "Insha", "Fasihi — Hadithi Fupi",
        "Fasihi — Tamthiliya", "Fasihi — Ushairi",
    ],
    "Biology": [
        "Cell Biology", "Classification", "Ecology", "Reproduction",
        "Nutrition", "Transport", "Respiration", "Genetics",
    ],
    "Chemistry": [
        "Atomic Structure", "Chemical Equations", "Acids and Bases",
        "Organic Chemistry", "Electrochemistry", "Rates of Reaction",
    ],
    "Physics": [
        "Mechanics", "Optics", "Waves", "Electricity", "Magnetism",
        "Radioactivity", "Thermodynamics",
    ],
    "History": [
        "Pre-colonial Africa", "Colonial Period", "Independence Movements",
        "Post-independence Kenya", "International Relations",
    ],
    "Geography": [
        "Physical Geography", "Human Geography", "Kenya Geography",
        "East Africa", "Mapwork and Statistics",
    ],
}

ALL_SUBJECTS = {**KCPE_SUBJECTS, **KCSE_SUBJECTS}
BILINGUAL_SUBJECTS = {"Kiswahili", "Social Studies", "History", "Geography"}
