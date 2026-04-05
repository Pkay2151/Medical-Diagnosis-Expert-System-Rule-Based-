"""
Main entry point for the medical diagnosis expert system.
"""

from knowledge_base import SYMPTOM_QUESTIONS, build_knowledge_base
from inference_engine import (
    build_reasoning_trace,
    calculate_confidence_scores,
    extract_diagnoses,
    forward_chaining,
    suggest_possible_conditions,
)


def diagnose(symptoms: set[str]) -> dict[str, object]:
    """Run the full diagnosis pipeline."""

    rules = build_knowledge_base()
    final_facts, fired_rules = forward_chaining(symptoms, rules)
    diagnoses = extract_diagnoses(final_facts)
    confidence_results = calculate_confidence_scores(symptoms, final_facts)
    suggestions = suggest_possible_conditions(symptoms, set(diagnoses))

    return {
        "input_symptoms": sorted(symptoms),
        "final_facts": sorted(final_facts),
        "diagnoses": diagnoses,
        "fired_rules": fired_rules,
        "confidence_results": confidence_results,
        "suggestions": suggestions,
        "reasoning": build_reasoning_trace(symptoms, fired_rules, confidence_results, suggestions),
    }


def ask_yes_no(prompt: str) -> bool:
    """Prompt until the user enters y/yes or n/no."""

    while True:
        answer = input(prompt).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def collect_user_symptoms() -> set[str]:
    """Collect symptoms from the user."""

    print("\nEnter patient symptoms (y/n):")
    symptoms: set[str] = set()

    for code, question in SYMPTOM_QUESTIONS:
        if ask_yes_no(f"- {question} "):
            symptoms.add(code)

    return symptoms


def display_result(result: dict[str, object]) -> None:
    """Show diagnosis results and the reasoning trace."""

    print("\n--- Expert System Result ---")
    print("Input Symptoms:", ", ".join(result["input_symptoms"]) or "None")

    diagnoses = result["diagnoses"]
    if diagnoses:
        print("Possible Diagnosis:", ", ".join(diagnoses))
    else:
        print("Possible Diagnosis: No clear diagnosis")

    confidence_results = result["confidence_results"]
    if confidence_results:
        print("Confidence Levels:")
        for item in confidence_results:
            print(f"- {item['label']}: {item['score']}%")
    elif result["suggestions"]:
        print("Closest Matches:")
        for item in result["suggestions"]:
            print(f"- {item['label']}: {item['score']}% symptom overlap")

    print()
    print(result["reasoning"])


def run_cli() -> None:
    """Launch the interactive command-line interface."""

    print("Medical Diagnosis Expert System (Rule-Based)")
    print("Diseases covered: Common Cold, Flu, Allergies, Strep Throat, Sinusitis, Bronchitis")

    while True:
        symptoms = collect_user_symptoms()
        result = diagnose(symptoms)
        display_result(result)

        if not ask_yes_no("\nWould you like to diagnose another patient? (y/n): "):
            print("Exiting expert system.")
            break


def run_test_cases() -> None:
    """Run built-in test cases."""

    test_cases = [
        {
            "name": "TC1 - Typical Common Cold",
            "symptoms": {"cough", "sore_throat", "runny_nose", "sneezing"},
            "expected": {"Common Cold"},
        },
        {
            "name": "TC2 - Typical Flu",
            "symptoms": {"fever", "body_ache", "fatigue", "headache"},
            "expected": {"Flu"},
        },
        {
            "name": "TC3 - Typical Allergies",
            "symptoms": {"sneezing", "itchy_eyes", "runny_nose"},
            "expected": {"Allergies"},
        },
        {
            "name": "TC4 - Typical Strep Throat",
            "symptoms": {"fever", "sore_throat", "swollen_glands", "headache"},
            "expected": {"Strep Throat"},
        },
        {
            "name": "TC5 - Typical Sinusitis",
            "symptoms": {"nasal_congestion", "facial_pressure", "headache", "runny_nose"},
            "expected": {"Sinusitis"},
        },
        {
            "name": "TC6 - Typical Bronchitis",
            "symptoms": {"cough", "chest_discomfort", "fatigue", "sore_throat"},
            "expected": {"Bronchitis"},
        },
        {
            "name": "TC7 - Cold and Allergies Overlap",
            "symptoms": {"cough", "sore_throat", "runny_nose", "sneezing", "itchy_eyes"},
            "expected": {"Allergies", "Common Cold"},
        },
        {
            "name": "TC8 - Partial Symptoms Only",
            "symptoms": {"headache"},
            "expected": set(),
        },
    ]

    print("Running test cases...\n")
    passed = 0

    for case in test_cases:
        result = diagnose(case["symptoms"])
        actual = set(result["diagnoses"])
        expected = case["expected"]

        is_pass = actual == expected
        if is_pass:
            passed += 1

        print(case["name"])
        print("- Symptoms:", ", ".join(sorted(case["symptoms"])))
        print("- Expected:", ", ".join(sorted(expected)) or "No clear diagnosis")
        print("- Actual:", ", ".join(sorted(actual)) or "No clear diagnosis")
        print("- Result:", "PASS" if is_pass else "FAIL")
        print()

    print(f"Summary: {passed}/{len(test_cases)} tests passed.")


if __name__ == "__main__":
    print("Select mode:")
    print("1. Interactive Diagnosis")
    print("2. Run Built-in Test Cases")
    print("3. Launch Desktop GUI")

    choice = input("Enter choice (1/2/3): ").strip()
    if choice == "2":
        run_test_cases()
    elif choice == "3":
        try:
            from gui_app import run_gui

            run_gui()
        except Exception as exc:
            print(f"Unable to launch GUI: {exc}")
            print("Run 'python gui_app.py' directly to debug GUI startup.")
    else:
        run_cli()
