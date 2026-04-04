"""
Inference Engine - Forward Chaining Algorithm

"""

from typing import List, Set, Tuple

from knowledge_base import Rule


def forward_chaining(initial_facts: Set[str], rules: List[Rule]) -> Tuple[Set[str], List[Rule]]:
    
    # Initialize with user symptoms
    facts = set(initial_facts)
    fired_rules: List[Rule] = []

    # Keep looping until no new facts are derived
    changed = True
    while changed:
        changed = False
        
        # Try to fire each rule
        for rule in rules:
            # KEY: Check if ALL premises (IF conditions) are in current facts
            # AND the conclusion hasn't been inferred yet (avoid duplicates)
            if rule.premises.issubset(facts) and rule.conclusion not in facts:
                # FIRE the rule: add its conclusion to our fact set
                facts.add(rule.conclusion)
                fired_rules.append(rule)
                changed = True

    return facts, fired_rules


def extract_diagnoses(facts: Set[str]) -> List[str]:
    """
    Extract final disease diagnoses from the inferred fact set.
    
    KEY CONCEPT - DIAGNOSIS EXTRACTION:
    Final diagnoses are facts that start with "diagnosis:" in our system.
    We filter all inferred facts to find only these diagnosis facts.
    This maps internal fact names to human-readable disease names.
    """

    diagnosis_map = {
        "diagnosis:gastroenteritis": "Gastroenteritis",
        "diagnosis:ibs": "Irritable Bowel Syndrome",
        "diagnosis:food_poisoning": "Food Poisoning",
    }

    # Extract only diagnosis facts and map to readable names
    diagnoses = [name for fact, name in diagnosis_map.items() if fact in facts]
    return sorted(diagnoses)


def build_reasoning_trace(fired_rules: List[Rule], diagnoses: List[str]) -> str:
    
    lines: List[str] = []
    lines.append("Reasoning Trace (Forward Chaining):")

    if not fired_rules:
        lines.append("- No rules fired. Not enough evidence for diagnosis.")
    else:
        # Show each fired rule in the order it was applied
        for rule in fired_rules:
            premises_text = ", ".join(sorted(rule.premises))
            lines.append(f"- {rule.id}: IF [{premises_text}] THEN [{rule.conclusion}]")

    if diagnoses:
        lines.append("Final Diagnosis: " + ", ".join(diagnoses))
    else:
        lines.append("Final Diagnosis: No clear diagnosis from current rules.")

    return "\n".join(lines)
