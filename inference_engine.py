"""
Inference engine for the medical diagnosis expert system.
"""

from knowledge_base import DIAGNOSIS_LABELS, DISEASE_PROFILES, Rule


def forward_chaining(initial_facts: set[str], rules: list[Rule]) -> tuple[set[str], list[Rule]]:
    """Apply rules repeatedly until no new facts can be inferred."""

    facts = set(initial_facts)
    fired_rules: list[Rule] = []

    changed = True
    while changed:
        changed = False
        for rule in rules:
            if rule.premises.issubset(facts) and rule.conclusion not in facts:
                facts.add(rule.conclusion)
                fired_rules.append(rule)
                changed = True

    return facts, fired_rules


def extract_diagnoses(facts: set[str]) -> list[str]:
    """Map internal diagnosis facts to readable labels."""

    diagnoses = [label for fact, label in DIAGNOSIS_LABELS.items() if fact in facts]
    return sorted(diagnoses)


def calculate_confidence_scores(symptoms: set[str], facts: set[str]) -> list[dict[str, object]]:
    """Estimate confidence using symptom coverage for each inferred disease."""

    confidence_results: list[dict[str, object]] = []

    for diagnosis_fact, label in DIAGNOSIS_LABELS.items():
        if diagnosis_fact not in facts:
            continue

        expected_symptoms = DISEASE_PROFILES[diagnosis_fact]
        matched_symptoms = sorted(symptoms & expected_symptoms)
        score = round((len(matched_symptoms) / len(expected_symptoms)) * 100)

        confidence_results.append(
            {
                "label": label,
                "score": score,
                "matched_symptoms": matched_symptoms,
                "expected_symptoms": sorted(expected_symptoms),
            }
        )

    confidence_results.sort(key=lambda item: (-int(item["score"]), str(item["label"])))
    return confidence_results


def suggest_possible_conditions(symptoms: set[str], diagnosed_labels: set[str]) -> list[dict[str, object]]:
    """Offer best-fit matches when rules do not fully diagnose a condition."""

    suggestions: list[dict[str, object]] = []

    for diagnosis_fact, label in DIAGNOSIS_LABELS.items():
        if label in diagnosed_labels:
            continue

        expected_symptoms = DISEASE_PROFILES[diagnosis_fact]
        matched_symptoms = sorted(symptoms & expected_symptoms)
        if not matched_symptoms:
            continue

        score = round((len(matched_symptoms) / len(expected_symptoms)) * 100)
        suggestions.append(
            {
                "label": label,
                "score": score,
                "matched_symptoms": matched_symptoms,
            }
        )

    suggestions.sort(key=lambda item: (-int(item["score"]), str(item["label"])))
    return suggestions[:3]


def build_reasoning_trace(
    input_symptoms: set[str],
    fired_rules: list[Rule],
    confidence_results: list[dict[str, object]],
    suggestions: list[dict[str, object]],
) -> str:
    """Build a readable forward-chaining explanation."""

    lines: list[str] = [
        "Reasoning Trace (Forward Chaining):",
        "Initial facts: " + (", ".join(sorted(input_symptoms)) or "None"),
        "",
    ]

    if not fired_rules:
        lines.append("No rules fired. The selected symptoms did not fully satisfy a diagnosis rule.")
    else:
        lines.append("Rules fired in order:")
        for rule in fired_rules:
            premises_text = ", ".join(sorted(rule.premises))
            lines.append(f"- {rule.id}: IF [{premises_text}] THEN [{rule.conclusion}]")
            lines.append(f"  Explanation: {rule.explanation}")

    lines.append("")
    if confidence_results:
        lines.append("Diagnosis summary:")
        for item in confidence_results:
            matched_text = ", ".join(item["matched_symptoms"]) or "No direct symptom overlap"
            lines.append(f"- {item['label']} ({item['score']}% confidence)")
            lines.append(f"  Supporting symptoms: {matched_text}")
    else:
        lines.append("Diagnosis summary: No clear diagnosis from current rules.")

    if suggestions:
        lines.append("")
        lines.append("Closest rule-based matches:")
        for item in suggestions:
            matched_text = ", ".join(item["matched_symptoms"])
            lines.append(f"- {item['label']} ({item['score']}% symptom overlap)")
            lines.append(f"  Matching symptoms: {matched_text}")

    return "\n".join(lines)
