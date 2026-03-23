"""
Medical Knowledge Base - IF-THEN Rules for Diagnosis

Stores all the medical rules in one place for easy management and updates.
"""

from dataclasses import dataclass
from typing import List, Set


@dataclass(frozen=True)
class Rule:
    """
    Represents a single IF-THEN rule in the knowledge base.
    
    KEY CONCEPT: Rules are the core of rule-based systems.
    - id: Unique identifier (e.g., "R1")
    - premises: SET of conditions that must ALL be true (the IF part)
    - conclusion: What we infer if premises are met (the THEN part)
    - explanation: Human-readable description of what this rule means
    
    Example: IF sneezing AND runny_nose THEN cold_pattern_a
    """

    id: str
    premises: Set[str]
    conclusion: str
    explanation: str


def build_knowledge_base() -> List[Rule]:
    """
    Create the rule base used by the inference engine.
    
    KEY CONCEPT - KNOWLEDGE BASE:
    This is where medical knowledge is stored as IF-THEN rules.
    The collection of rules represents all the domain expertise we have.
    In a real system, this might be extracted from medical textbooks or expert interviews.
    
    14 rules covering: Cold, Flu, Allergies detection patterns.
    """

    rules = [
        Rule(
            id="R1",
            premises={"sneezing", "runny_nose"},
            conclusion="cold_pattern_a",
            explanation="IF sneezing AND runny nose THEN early cold pattern.",
        ),
        Rule(
            id="R2",
            premises={"sore_throat", "cough"},
            conclusion="upper_respiratory_irritation",
            explanation="IF sore throat AND cough THEN upper respiratory irritation.",
        ),
        Rule(
            id="R3",
            premises={"upper_respiratory_irritation", "cold_pattern_a"},
            conclusion="diagnosis:cold",
            explanation="IF upper respiratory irritation AND early cold pattern THEN diagnosis is Cold.",
        ),
        Rule(
            id="R4",
            premises={"cough", "mild_fever", "nasal_congestion"},
            conclusion="cold_pattern_b",
            explanation="IF cough AND mild fever AND nasal congestion THEN alternate cold pattern.",
        ),
        Rule(
            id="R5",
            premises={"cold_pattern_b", "sore_throat"},
            conclusion="diagnosis:cold",
            explanation="IF alternate cold pattern AND sore throat THEN diagnosis is Cold.",
        ),
        Rule(
            id="R6",
            premises={"high_fever", "body_ache"},
            conclusion="flu_pattern_a",
            explanation="IF high fever AND body ache THEN primary flu pattern.",
        ),
        Rule(
            id="R7",
            premises={"fatigue", "headache", "chills"},
            conclusion="flu_pattern_b",
            explanation="IF fatigue AND headache AND chills THEN secondary flu pattern.",
        ),
        Rule(
            id="R8",
            premises={"flu_pattern_a", "flu_pattern_b"},
            conclusion="diagnosis:flu",
            explanation="IF primary flu pattern AND secondary flu pattern THEN diagnosis is Flu.",
        ),
        Rule(
            id="R9",
            premises={"flu_pattern_a", "cough"},
            conclusion="diagnosis:flu",
            explanation="IF primary flu pattern AND cough THEN diagnosis is Flu.",
        ),
        Rule(
            id="R10",
            premises={"sneezing", "itchy_eyes"},
            conclusion="allergy_pattern_a",
            explanation="IF sneezing AND itchy eyes THEN allergy pattern A.",
        ),
        Rule(
            id="R11",
            premises={"runny_nose", "itchy_eyes", "no_fever"},
            conclusion="allergy_pattern_b",
            explanation="IF runny nose AND itchy eyes AND no fever THEN allergy pattern B.",
        ),
        Rule(
            id="R12",
            premises={"allergy_pattern_a", "runny_nose"},
            conclusion="diagnosis:allergies",
            explanation="IF allergy pattern A AND runny nose THEN diagnosis is Allergies.",
        ),
        Rule(
            id="R13",
            premises={"allergy_pattern_b", "sneezing"},
            conclusion="diagnosis:allergies",
            explanation="IF allergy pattern B AND sneezing THEN diagnosis is Allergies.",
        ),
        Rule(
            id="R14",
            premises={"high_fever", "no_fever"},
            conclusion="input_conflict",
            explanation="IF high fever AND no fever THEN inconsistent fever input.",
        ),
    ]
    return rules
