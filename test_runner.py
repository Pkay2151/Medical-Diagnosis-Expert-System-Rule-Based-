"""
Automated tests for the Medical Diagnosis Expert System.
"""

from medical_expert_system import diagnose


def run_all_tests() -> None:
    """Execute test cases and report results."""

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

    print("=" * 70)
    print("MEDICAL DIAGNOSIS EXPERT SYSTEM - TEST RESULTS")
    print("=" * 70)
    print()

    passed = 0
    failed = 0

    for case in test_cases:
        result = diagnose(case["symptoms"])
        actual = set(result["diagnoses"])
        expected = case["expected"]

        is_pass = actual == expected
        if is_pass:
            passed += 1
        else:
            failed += 1

        status = "[PASS]" if is_pass else "[FAIL]"
        print(f"{case['name']} ... {status}")
        print(f"  Input Symptoms: {', '.join(sorted(case['symptoms'])) or 'None'}")
        print(f"  Expected: {', '.join(sorted(expected)) or 'No clear diagnosis'}")
        print(f"  Actual:   {', '.join(sorted(actual)) or 'No clear diagnosis'}")

        if result["confidence_results"]:
            confidence_text = ", ".join(
                f"{item['label']}={item['score']}%" for item in result["confidence_results"]
            )
            print(f"  Confidence: {confidence_text}")

        if not is_pass:
            print(f"  Fired Rules: {[rule.id for rule in result['fired_rules']]}")

        print()

    print("=" * 70)
    print(f"SUMMARY: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
