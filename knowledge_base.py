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
    
    Example: IF nausea AND vomiting THEN acute_gi_pattern_a
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
    
    14 rules covering: Gastroenteritis, IBS, Food Poisoning detection patterns.
    """

    rules = [
        Rule(
            id="R1",
            premises={"nausea", "vomiting"},
            conclusion="acute_gi_pattern_a",
            explanation="IF nausea AND vomiting THEN acute Gastrointestinal distress pattern.",
        ),
        Rule(
            id="R2",
            premises={"diarrhea", "abdominal_pain"},
            conclusion="bowel_dysfunction",
            explanation="IF diarrhea AND abdominal pain THEN bowel dysfunction.",
        ),
        Rule(
            id="R3",
            premises={"bowel_dysfunction", "acute_gi_pattern_a"},
            conclusion="diagnosis:gastroenteritis",
            explanation="IF bowel dysfunction AND acute Gastrointestinal distress THEN diagnosis is Gastroenteritis.",
        ),
        Rule(
            id="R4",
            premises={"vomiting", "fever", "dehydration"},
            conclusion="acute_gi_pattern_b",
            explanation="IF vomiting AND fever AND dehydration THEN acute infectious pattern.",
        ),
        Rule(
            id="R5",
            premises={"acute_gi_pattern_b", "diarrhea"},
            conclusion="diagnosis:gastroenteritis",
            explanation="IF acute infectious pattern AND diarrhea THEN diagnosis is Gastroenteritis.",
        ),
        Rule(
            id="R6",
            premises={"fever", "cramps"},
            conclusion="food_poison_pattern_a",
            explanation="IF fever AND cramps THEN foodborne illness pattern.",
        ),
        Rule(
            id="R7",
            premises={"diarrhea", "vomiting", "headache"},
            conclusion="food_poison_pattern_b",
            explanation="IF diarrhea AND vomiting AND headache THEN systemic food poison response.",
        ),
        Rule(
            id="R8",
            premises={"food_poison_pattern_a", "food_poison_pattern_b"},
            conclusion="diagnosis:food_poisoning",
            explanation="IF foodborne pattern AND systemic response THEN diagnosis is Food Poisoning.",
        ),
        Rule(
            id="R9",
            premises={"food_poison_pattern_a", "nausea"},
            conclusion="diagnosis:food_poisoning",
            explanation="IF foodborne pattern AND nausea THEN diagnosis is Food Poisoning.",
        ),
        Rule(
            id="R10",
            premises={"abdominal_pain", "bloating"},
            conclusion="ibs_pattern_a",
            explanation="IF abdominal pain AND bloating THEN IBS pattern A.",
        ),
        Rule(
            id="R11",
            premises={"loss_of_appetite", "fatigue", "dizziness"},
            conclusion="ibs_pattern_b",
            explanation="IF loss of appetite AND fatigue AND dizziness THEN IBS pattern B.",
        ),
        Rule(
            id="R12",
            premises={"ibs_pattern_a", "diarrhea"},
            conclusion="diagnosis:ibs",
            explanation="IF IBS pattern A AND diarrhea THEN diagnosis is Irritable Bowel Syndrome.",
        ),
        Rule(
            id="R13",
            premises={"ibs_pattern_b", "abdominal_pain"},
            conclusion="diagnosis:ibs",
            explanation="IF IBS pattern B AND abdominal pain THEN diagnosis is Irritable Bowel Syndrome.",
        ),
        Rule(
            id="R14",
            premises={"fever", "no_fever"},
            conclusion="input_conflict",
            explanation="IF fever AND no fever THEN inconsistent fever input.",
        ),
    ]
    return rules
