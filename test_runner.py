"""
Test runner for Medical Diagnosis Expert System
Executes all test cases without interactive prompts
"""

from medical_expert_system import diagnose

def run_all_tests():
    """Execute all test cases and report results."""

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
