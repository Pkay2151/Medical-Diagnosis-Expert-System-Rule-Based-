# Medical Diagnosis Expert System (Rule-Based)

A beginner-friendly academic project that diagnoses simple diseases using:
- Rule-based knowledge representation (IF-THEN)
- Forward chaining inference
- Explainable reasoning trace
- CLI and desktop GUI interfaces

Diseases covered:
- Common Cold
- Flu
- Allergies

## Project Structure

```text
d:\33/
├── knowledge_base.py         # Rule definitions (R1-R14)
├── inference_engine.py       # Forward chaining + diagnosis extraction
├── medical_expert_system.py  # Main entry point, CLI, tests
├── gui_app.py                # Tkinter desktop GUI
├── test_runner.py            # Automated 5 test cases
├── README.md                 # Project documentation
└── __pycache__/              # Auto-generated Python cache
```

## 1. System Architecture

### Knowledge Base (`knowledge_base.py`)
- Stores medical expertise as structured IF-THEN rules.
- Uses `Rule` dataclass: `id`, `premises`, `conclusion`, `explanation`.
- Contains 14 logically consistent rules.

### Inference Engine (`inference_engine.py`)
- `forward_chaining()`: Applies rules repeatedly until no new facts are generated.
- `extract_diagnoses()`: Maps internal diagnosis facts to readable disease names.
- `build_reasoning_trace()`: Produces a transparent explanation of fired rules.

### User Interface
- CLI in `medical_expert_system.py`
- Desktop GUI in `gui_app.py` (Tkinter)

## 2. Knowledge Base Design (IF-THEN Rules)

Implemented rules (`R1` to `R14`) in `knowledge_base.py`:

1. IF `sneezing` AND `runny_nose` THEN `cold_pattern_a`
2. IF `sore_throat` AND `cough` THEN `upper_respiratory_irritation`
3. IF `upper_respiratory_irritation` AND `cold_pattern_a` THEN `diagnosis:cold`
4. IF `cough` AND `mild_fever` AND `nasal_congestion` THEN `cold_pattern_b`
5. IF `cold_pattern_b` AND `sore_throat` THEN `diagnosis:cold`
6. IF `high_fever` AND `body_ache` THEN `flu_pattern_a`
7. IF `fatigue` AND `headache` AND `chills` THEN `flu_pattern_b`
8. IF `flu_pattern_a` AND `flu_pattern_b` THEN `diagnosis:flu`
9. IF `flu_pattern_a` AND `cough` THEN `diagnosis:flu`
10. IF `sneezing` AND `itchy_eyes` THEN `allergy_pattern_a`
11. IF `runny_nose` AND `itchy_eyes` AND `no_fever` THEN `allergy_pattern_b`
12. IF `allergy_pattern_a` AND `runny_nose` THEN `diagnosis:allergies`
13. IF `allergy_pattern_b` AND `sneezing` THEN `diagnosis:allergies`
14. IF `high_fever` AND `no_fever` THEN `input_conflict`

Consistency notes:
- Multiple rules can support the same diagnosis (robustness).
- No rules negate or overwrite another diagnosis directly.
- `R14` flags inconsistent fever input instead of forcing a disease diagnosis.

## 3. Inference Engine

### Forward Chaining Steps

1. Start with user symptoms as initial facts.
2. Scan all rules.
3. Fire rules whose premises are fully satisfied.
4. Add rule conclusions as new facts.
5. Repeat until no new facts can be added.
6. Extract diagnosis facts and show reasoning trace.

### Pseudocode

```text
facts <- user_symptoms
fired_rules <- []
changed <- true

WHILE changed:
    changed <- false
    FOR each rule in knowledge_base:
        IF rule.premises subset of facts AND rule.conclusion not in facts:
            add rule.conclusion to facts
            append rule to fired_rules
            changed <- true

return facts, fired_rules
```

Actual implementation:
- `inference_engine.py`: `forward_chaining(...)`
- `medical_expert_system.py`: `diagnose(...)`

## 4. Implementation Notes

- Clean modular design (separation of concerns).
- Rule structure via `Rule` dataclass.
- Explainable outputs through reasoning trace.
- Beginner-friendly function naming and flow.

## 5. User Interface

### CLI

Run:

```bash
python medical_expert_system.py
```

Menu options:
- `1`: Interactive diagnosis (CLI prompts)
- `2`: Run built-in test cases
- `3`: Launch desktop GUI

### Desktop GUI

Run directly:

```bash
python gui_app.py
```

GUI features:
- Symptom checkboxes
- Diagnose button
- Clear button
- Sample Flu preset button
- Diagnosis result panel
- Scrollable reasoning trace

## 6. Testing (5 Cases)

Run:

```bash
python test_runner.py
```

Cases covered:
1. Typical Cold -> Expected: Common Cold
2. Typical Flu -> Expected: Flu
3. Typical Allergies -> Expected: Allergies
4. Cold + Allergies overlap -> Expected: Common Cold, Allergies
5. Insufficient evidence -> Expected: No clear diagnosis

## 7. Report-Friendly Explanation

### How It Works (Simple)
The user provides symptoms. The system applies IF-THEN rules repeatedly using forward chaining. Each matched rule adds a new fact. When no more facts can be inferred, the system reports possible diagnoses and explains which rules fired.

### Limitations
- Only 3 diseases are modeled.
- No confidence/probability scoring.
- No temporal analysis (symptom duration/severity progression).
- Educational prototype; not a clinical tool.

### Possible Improvements
- Add more diseases and symptom sets.
- Add confidence scores and ranking.
- Include age/history/risk-factor rules.
- Add PDF export for diagnosis reports.
- Build a web version (Flask/FastAPI frontend).
