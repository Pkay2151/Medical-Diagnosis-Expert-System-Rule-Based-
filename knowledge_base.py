"""
Knowledge base for a rule-based medical diagnosis expert system.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    """Represents a single IF-THEN rule."""

    id: str
    premises: set[str]
    conclusion: str
    explanation: str


SYMPTOM_QUESTIONS: list[tuple[str, str]] = [
    ("fever", "Fever?"),
    ("cough", "Cough?"),
    ("sore_throat", "Sore throat?"),
    ("sneezing", "Sneezing?"),
    ("body_ache", "Body ache?"),
    ("runny_nose", "Runny nose?"),
    ("fatigue", "Fatigue?"),
    ("headache", "Headache?"),
    ("itchy_eyes", "Itchy eyes?"),
    ("chills", "Chills?"),
    ("swollen_glands", "Swollen glands?"),
    ("nasal_congestion", "Nasal congestion?"),
    ("facial_pressure", "Facial pressure?"),
    ("chest_discomfort", "Chest discomfort?"),
]


DIAGNOSIS_LABELS: dict[str, str] = {
    "diagnosis:cold": "Common Cold",
    "diagnosis:flu": "Flu",
    "diagnosis:allergies": "Allergies",
    "diagnosis:strep_throat": "Strep Throat",
    "diagnosis:sinusitis": "Sinusitis",
    "diagnosis:bronchitis": "Bronchitis",
}


DISEASE_PROFILES: dict[str, set[str]] = {
    "diagnosis:cold": {"cough", "sore_throat", "runny_nose", "sneezing", "nasal_congestion"},
    "diagnosis:flu": {"fever", "cough", "body_ache", "fatigue", "headache", "chills"},
    "diagnosis:allergies": {"sneezing", "runny_nose", "itchy_eyes", "nasal_congestion"},
    "diagnosis:strep_throat": {"fever", "sore_throat", "headache", "swollen_glands"},
    "diagnosis:sinusitis": {"headache", "nasal_congestion", "facial_pressure", "runny_nose"},
    "diagnosis:bronchitis": {"cough", "fatigue", "chest_discomfort", "sore_throat"},
}


def build_knowledge_base() -> list[Rule]:
    """Create the rule base for common educational demo diagnoses."""

    return [
        Rule(
            id="R1",
            premises={"cough", "sore_throat"},
            conclusion="cold_pattern_a",
            explanation="IF cough AND sore throat THEN upper respiratory cold pattern.",
        ),
        Rule(
            id="R2",
            premises={"runny_nose", "sneezing"},
            conclusion="cold_pattern_b",
            explanation="IF runny nose AND sneezing THEN nasal cold pattern.",
        ),
        Rule(
            id="R3",
            premises={"cold_pattern_a", "cold_pattern_b"},
            conclusion="diagnosis:cold",
            explanation="IF cold pattern A AND cold pattern B THEN diagnosis is Common Cold.",
        ),
        Rule(
            id="R4",
            premises={"fever", "body_ache"},
            conclusion="flu_pattern_a",
            explanation="IF fever AND body ache THEN influenza body-response pattern.",
        ),
        Rule(
            id="R5",
            premises={"fatigue", "headache"},
            conclusion="flu_pattern_b",
            explanation="IF fatigue AND headache THEN influenza fatigue pattern.",
        ),
        Rule(
            id="R6",
            premises={"flu_pattern_a", "flu_pattern_b"},
            conclusion="diagnosis:flu",
            explanation="IF flu pattern A AND flu pattern B THEN diagnosis is Flu.",
        ),
        Rule(
            id="R7",
            premises={"fever", "cough", "chills"},
            conclusion="diagnosis:flu",
            explanation="IF fever AND cough AND chills THEN diagnosis is Flu.",
        ),
        Rule(
            id="R8",
            premises={"sneezing", "itchy_eyes"},
            conclusion="allergy_pattern_a",
            explanation="IF sneezing AND itchy eyes THEN allergic irritation pattern.",
        ),
        Rule(
            id="R9",
            premises={"runny_nose", "allergy_pattern_a"},
            conclusion="diagnosis:allergies",
            explanation="IF runny nose AND allergic irritation pattern THEN diagnosis is Allergies.",
        ),
        Rule(
            id="R10",
            premises={"runny_nose", "sneezing", "itchy_eyes"},
            conclusion="diagnosis:allergies",
            explanation="IF runny nose AND sneezing AND itchy eyes THEN diagnosis is Allergies.",
        ),
        Rule(
            id="R11",
            premises={"fever", "sore_throat"},
            conclusion="strep_pattern_a",
            explanation="IF fever AND sore throat THEN bacterial throat pattern.",
        ),
        Rule(
            id="R12",
            premises={"swollen_glands", "headache"},
            conclusion="strep_pattern_b",
            explanation="IF swollen glands AND headache THEN throat infection support pattern.",
        ),
        Rule(
            id="R13",
            premises={"strep_pattern_a", "strep_pattern_b"},
            conclusion="diagnosis:strep_throat",
            explanation="IF strep pattern A AND strep pattern B THEN diagnosis is Strep Throat.",
        ),
        Rule(
            id="R14",
            premises={"nasal_congestion", "facial_pressure"},
            conclusion="sinus_pattern_a",
            explanation="IF nasal congestion AND facial pressure THEN sinus inflammation pattern.",
        ),
        Rule(
            id="R15",
            premises={"headache", "runny_nose"},
            conclusion="sinus_pattern_b",
            explanation="IF headache AND runny nose THEN sinus support pattern.",
        ),
        Rule(
            id="R16",
            premises={"sinus_pattern_a", "sinus_pattern_b"},
            conclusion="diagnosis:sinusitis",
            explanation="IF sinus pattern A AND sinus pattern B THEN diagnosis is Sinusitis.",
        ),
        Rule(
            id="R17",
            premises={"cough", "chest_discomfort"},
            conclusion="bronchitis_pattern_a",
            explanation="IF cough AND chest discomfort THEN lower airway irritation pattern.",
        ),
        Rule(
            id="R18",
            premises={"fatigue", "sore_throat"},
            conclusion="bronchitis_pattern_b",
            explanation="IF fatigue AND sore throat THEN bronchitis support pattern.",
        ),
        Rule(
            id="R19",
            premises={"bronchitis_pattern_a", "bronchitis_pattern_b"},
            conclusion="diagnosis:bronchitis",
            explanation="IF bronchitis pattern A AND bronchitis pattern B THEN diagnosis is Bronchitis.",
        ),
    ]
