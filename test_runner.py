"""
Test runner for Medical Diagnosis Expert System
Executes all test cases without interactive prompts
"""

from medical_expert_system import diagnose

def run_all_tests():
    """Execute all test cases and report results."""

    test_cases = [
        {
            "name": "TC1 - Typical Gastroenteritis",
            "symptoms": {"nausea", "vomiting", "diarrhea", "abdominal_pain"},
            "expected": {"Gastroenteritis"},
        },
        {
            "name": "TC2 - Typical Food Poisoning",
            "symptoms": {"fever", "cramps", "diarrhea", "vomiting", "headache"},
            "expected": {"Food Poisoning"},
        },
        {
            "name": "TC3 - Typical IBS",
            "symptoms": {"abdominal_pain", "bloating", "loss_of_appetite", "fatigue", "dizziness"},
            "expected": {"Irritable Bowel Syndrome"},
        },
        {
            "name": "TC4 - Gastroenteritis and Food Poisoning Overlap",
            "symptoms": {"nausea", "vomiting", "diarrhea", "abdominal_pain", "fever", "cramps", "headache"},
            "expected": {"Gastroenteritis", "Food Poisoning"},
        },
        {
            "name": "TC5 - Insufficient Evidence",
            "symptoms": {"dizziness"},
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

        status = "✓ PASS" if is_pass else "✗ FAIL"
        print(f"{case['name']} ... {status}")
        print(f"  Input Symptoms: {', '.join(sorted(case['symptoms'])) or 'None'}")
        print(f"  Expected: {', '.join(sorted(expected)) or 'No clear diagnosis'}")
        print(f"  Actual:   {', '.join(sorted(actual)) or 'No clear diagnosis'}")

        if not is_pass:
            print(f"  Fired Rules: {[r.id for r in result['fired_rules']]}")

        print()

    print("=" * 70)
    print(f"SUMMARY: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
