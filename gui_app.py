"""Tkinter GUI for the Medical Diagnosis Expert System."""

import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from medical_expert_system import diagnose


SYMPTOM_FIELDS = [
    ("nausea", "Nausea"),
    ("vomiting", "Vomiting"),
    ("diarrhea", "Diarrhea"),
    ("abdominal_pain", "Abdominal pain"),
    ("bloating", "Bloating"),
    ("fatigue", "Fatigue"),
    ("loss_of_appetite", "Loss of appetite"),
    ("dehydration", "Dehydration"),
    ("fever", "Fever"),
    ("no_fever", "No fever"),
    ("cramps", "Stomach cramps"),
    ("headache", "Headache"),
    ("dizziness", "Dizziness"),
]


class ExpertSystemGUI:
    """Simple desktop UI for symptom selection and diagnosis."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Medical Diagnosis Expert System")
        self.root.geometry("920x620")
        self.root.minsize(860, 560)

        self.symptom_vars: dict[str, tk.BooleanVar] = {}
        self._build_layout()

    def _build_layout(self) -> None:
        header = tk.Label(
            self.root,
            text="Rule-Based Medical Diagnosis Expert System",
            font=("Segoe UI", 16, "bold"),
            pady=10,
        )
        header.pack()

        subtitle = tk.Label(
            self.root,
            text="Select patient symptoms and click Diagnose",
            font=("Segoe UI", 10),
            fg="#333333",
            pady=2,
        )
        subtitle.pack()

        content = tk.Frame(self.root, padx=14, pady=10)
        content.pack(fill="both", expand=True)

        left = tk.LabelFrame(content, text="Symptoms", padx=12, pady=12)
        left.pack(side="left", fill="y")

        right = tk.LabelFrame(content, text="Diagnosis Output", padx=12, pady=12)
        right.pack(side="right", fill="both", expand=True)

        # Render symptom checkboxes in two columns for readability.
        for idx, (code, label) in enumerate(SYMPTOM_FIELDS):
            var = tk.BooleanVar(value=False)
            self.symptom_vars[code] = var
            row = idx % 7
            col = idx // 7
            chk = tk.Checkbutton(left, text=label, variable=var, anchor="w", width=18)
            chk.grid(row=row, column=col, sticky="w", padx=6, pady=4)

        button_bar = tk.Frame(left, pady=10)
        button_bar.grid(row=8, column=0, columnspan=2, sticky="ew")

        diagnose_btn = tk.Button(button_bar, text="Diagnose", width=14, command=self.on_diagnose)
        diagnose_btn.pack(side="left", padx=4)

        clear_btn = tk.Button(button_bar, text="Clear", width=14, command=self.on_clear)
        clear_btn.pack(side="left", padx=4)

        sample_btn = tk.Button(button_bar, text="Load Food Poisoning Example", width=25, command=self.load_food_poisoning_example)
        sample_btn.pack(side="left", padx=4)

        self.result_label = tk.Label(
            right,
            text="Possible Diagnosis: -",
            font=("Segoe UI", 12, "bold"),
            fg="#0b3d91",
            anchor="w",
            justify="left",
        )
        self.result_label.pack(fill="x", pady=(0, 8))

        self.trace_box = ScrolledText(right, wrap="word", font=("Consolas", 10), height=24)
        self.trace_box.pack(fill="both", expand=True)
        self.trace_box.insert("1.0", "Reasoning trace will appear here after diagnosis.\n")
        self.trace_box.configure(state="disabled")

    def _get_selected_symptoms(self) -> set[str]:
        return {code for code, var in self.symptom_vars.items() if var.get()}

    def _set_trace_text(self, text: str) -> None:
        self.trace_box.configure(state="normal")
        self.trace_box.delete("1.0", tk.END)
        self.trace_box.insert(tk.END, text)
        self.trace_box.configure(state="disabled")

    def on_diagnose(self) -> None:
        symptoms = self._get_selected_symptoms()
        if not symptoms:
            messagebox.showinfo("No Symptoms", "Please select at least one symptom.")
            return

        result = diagnose(symptoms)
        diagnoses = result["diagnoses"]

        if diagnoses:
            self.result_label.config(text="Possible Diagnosis: " + ", ".join(diagnoses), fg="#0b3d91")
        else:
            self.result_label.config(text="Possible Diagnosis: No clear diagnosis", fg="#8a1c1c")

        details = [
            "Input Symptoms: " + (", ".join(result["input_symptoms"]) or "None"),
            "",
            str(result["reasoning"]),
        ]

        if "input_conflict" in result["final_facts"]:
            details.append("\nWarning: Inconsistent fever input (fever + no fever).")

        self._set_trace_text("\n".join(details))

    def on_clear(self) -> None:
        for var in self.symptom_vars.values():
            var.set(False)
        self.result_label.config(text="Possible Diagnosis: -", fg="#0b3d91")
        self._set_trace_text("Reasoning trace will appear here after diagnosis.\n")

    def load_food_poisoning_example(self) -> None:
        example = {"fever", "cramps", "diarrhea", "vomiting", "headache"}
        for code, var in self.symptom_vars.items():
            var.set(code in example)


def run_gui() -> None:
    root = tk.Tk()
    ExpertSystemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
