# Medical Diagnosis Expert System

Rule-based expert system developed for an Artificial Intelligence project. The system diagnoses three common medical conditions using a knowledge base of IF-THEN rules, a forward chaining inference engine, and both CLI and GUI interfaces.

## Conditions Covered

- Common Cold
- Flu
- Allergies

## Core AI Concepts Demonstrated

- Knowledge representation through structured IF-THEN rules
- Forward chaining inference from user-provided symptoms
- Explainable reasoning trace showing the order of fired rules
- Optional confidence scores based on symptom coverage
- Human-friendly interaction through command line and Tkinter GUI

## Project Structure

```text
knowledge_base.py         # Symptoms, disease profiles, IF-THEN rules
inference_engine.py       # Forward chaining, confidence, reasoning trace
medical_expert_system.py  # Main program and CLI workflow
gui_app.py                # Tkinter desktop interface
test_runner.py            # Automated validation scenarios
README.md                 # Project overview and usage
```

## Knowledge Base

The rule base models common conditions and uses intermediate facts before making a final diagnosis.

### Common Cold

- IF cough AND sore throat THEN `cold_pattern_a`
- IF runny nose AND sneezing THEN `cold_pattern_b`
- IF `cold_pattern_a` AND `cold_pattern_b` THEN diagnosis is Common Cold

### Flu

- IF fever AND body ache THEN `flu_pattern_a`
- IF fatigue AND headache THEN `flu_pattern_b`
- IF `flu_pattern_a` AND `flu_pattern_b` THEN diagnosis is Flu
- IF fever AND cough AND chills THEN diagnosis is Flu

### Allergies

- IF sneezing AND itchy eyes THEN `allergy_pattern_a`
- IF runny nose AND `allergy_pattern_a` THEN diagnosis is Allergies
- IF runny nose AND sneezing AND itchy eyes THEN diagnosis is Allergies

## Inference Process

1. The user selects symptoms.
2. The system stores them as initial facts.
3. Forward chaining checks all rules repeatedly.
4. Matching rules fire and add new facts.
5. The process stops when no more facts can be inferred.
6. Diagnosis labels, confidence scores, and reasoning trace are displayed.

## How to Run

### Run the main program

```bash
python medical_expert_system.py
```

Modes:

- `1`: Interactive CLI diagnosis
- `2`: Built-in test cases
- `3`: Desktop GUI

### Run the GUI directly

```bash
python gui_app.py
```

### Run automated tests

```bash
python test_runner.py
```

## Sample Test Scenarios

- Typical Common Cold
- Typical Flu
- Typical Allergies
- Overlap between Cold and Allergies
- Insufficient evidence

## Limitations

- Educational system only and not a medical device
- Covers only three conditions
- Confidence is heuristic, not clinical probability
- Does not consider symptom duration, age, or patient history

## Possible Improvements

- Add more diseases and medical rules
- Support follow-up questions based on previous answers
- Add symptom duration and severity handling
- Export diagnosis reports for documentation
- Build a web-based interface
