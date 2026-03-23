"""
Rule-Based Medical Diagnosis Expert System

Main entry point. Orchestrates knowledge base + inference engine + UI.
"""

from collections.abc import Set
from typing import Dict

from knowledge_base import build_knowledge_base
from inference_engine import forward_chaining, extract_diagnoses, build_reasoning_trace





def diagnose(symptoms: Set[str]) -> Dict[str, object]:
    """
    Run the complete expert system diagnosis pipeline.
    
    KEY CONCEPT - MAIN WORKFLOW:
    1. Load knowledge base (IF-THEN rules)
    2. Run forward chaining inference from symptoms
    3. Extract final diagnoses from inferred facts
    4. Build explanation of reasoning
    5. Return all results
    
    This is the main entry point that orchestrates the entire system.
    """

    # Step 1: Load all medical knowledge
    rules = build_knowledge_base()
    
    # Step 2: Run inference - start from symptoms, apply rules repeatedly
    final_facts, fired_rules = forward_chaining(symptoms, rules)
    
    # Step 3: Extract disease diagnoses from final facts
    diagnoses = extract_diagnoses(final_facts)

    # Step 4: Package results for display
    return {
        "input_symptoms": sorted(symptoms),
        "final_facts": sorted(final_facts),
        "diagnoses": diagnoses,
        "fired_rules": fired_rules,
        "reasoning": build_reasoning_trace(fired_rules, diagnoses),
    }


def ask_yes_no(prompt: str) -> bool:
    """
    Prompt user for yes/no input.
    
    Simple helper that keeps asking until valid input received.
    """

    while True:
        answer = input(prompt).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def collect_user_symptoms() -> Set[str]:
    """
    Collect symptoms from user via CLI prompts.
    
    KEY CONCEPT - USER INTERFACE:
    This function handles the human interaction layer.
    We ask yes/no questions for each possible symptom
    and collect only those the user confirms.
    """

    print("\nEnter patient symptoms (y/n):")

    symptom_questions = [
        ("sneezing", "Sneezing?"),
        ("runny_nose", "Runny nose?"),
        ("sore_throat", "Sore throat?"),
        ("cough", "Cough?"),
        ("nasal_congestion", "Nasal congestion?"),
        ("mild_fever", "Mild fever?"),
        ("high_fever", "High fever?"),
        ("no_fever", "No fever?"),
        ("body_ache", "Body ache?"),
        ("fatigue", "Fatigue?"),
        ("headache", "Headache?"),
        ("chills", "Chills?"),
        ("itchy_eyes", "Itchy eyes?"),
    ]

    symptoms: Set[str] = set()
    for code, question in symptom_questions:
        if ask_yes_no(f"- {question} "):
            symptoms.add(code)

    return symptoms


def display_result(result: Dict[str, object]) -> None:
    """
    Print diagnosis result clearly for CLI users.
    
    Shows symptoms, diagnosis, and complete reasoning trace.
    """

    print("\n--- Expert System Result ---")
    print("Input Symptoms:", ", ".join(result["input_symptoms"]) or "None")

    diagnoses = result["diagnoses"]
    if diagnoses:
        print("Possible Diagnosis:", ", ".join(diagnoses))
    else:
        print("Possible Diagnosis: No clear diagnosis")

    print()
    print(result["reasoning"])

    if "input_conflict" in result["final_facts"]:
        print("\nWarning: Inconsistent fever input detected (both high fever and no fever).")


def run_cli() -> None:
    """
    Run the system in interactive CLI mode.
    
    KEY CONCEPT - INTERACTIVE SESSION:
    This function provides the conversational interface where:
    1. User answers symptom questions
    2. System runs diagnosis
    3. Results are displayed with full reasoning
    """

    print("Medical Diagnosis Expert System (Rule-Based)")
    print("Diseases covered: Cold, Flu, Allergies")

    symptoms = collect_user_symptoms()
    result = diagnose(symptoms)
    display_result(result)


def run_test_cases() -> None:
    """
    Execute predefined test cases for quick validation.
    
    Used to verify the system works correctly without user interaction.
    """

    test_cases = [
        {
            "name": "TC1 - Typical Cold",
            "symptoms": {"sneezing", "runny_nose", "sore_throat", "cough"},
            "expected": {"Common Cold"},
        },
        {
            "name": "TC2 - Typical Flu",
            "symptoms": {"high_fever", "body_ache", "fatigue", "headache", "chills"},
            "expected": {"Flu"},
        },
        {
            "name": "TC3 - Typical Allergies",
            "symptoms": {"sneezing", "runny_nose", "itchy_eyes", "no_fever"},
            "expected": {"Allergies"},
        },
        {
            "name": "TC4 - Cold and Allergies Overlap",
            "symptoms": {"sneezing", "runny_nose", "itchy_eyes", "sore_throat", "cough", "no_fever"},
            "expected": {"Common Cold", "Allergies"},
        },
        {
            "name": "TC5 - Insufficient Evidence",
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

