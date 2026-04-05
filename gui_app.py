"""Tkinter GUI for the Medical Diagnosis Expert System."""

import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from knowledge_base import SYMPTOM_QUESTIONS
from medical_expert_system import diagnose


COLORS = {
    "page": "#f4efe7",
    "panel": "#fffaf4",
    "panel_alt": "#f8f2ea",
    "ink": "#24323d",
    "muted": "#62707b",
    "accent": "#0e7a6d",
    "accent_dark": "#0a5c53",
    "highlight": "#d96c3f",
    "soft": "#efe2d1",
    "danger": "#a63f3f",
    "trace_bg": "#fffdf9",
}

SYMPTOM_FIELDS = [(code, prompt.rstrip("?")) for code, prompt in SYMPTOM_QUESTIONS]

EXAMPLES = {
    "Flu": {"fever", "body_ache", "fatigue", "headache", "chills"},
    "Cold": {"cough", "sore_throat", "runny_nose", "sneezing"},
    "Allergies": {"sneezing", "runny_nose", "itchy_eyes", "nasal_congestion"},
    "Strep": {"fever", "sore_throat", "swollen_glands", "headache"},
}


class ExpertSystemGUI:
    """Stylized desktop UI for symptom selection and diagnosis."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Medical Diagnosis Expert System")
        self.root.geometry("1180x700")
        self.root.minsize(920, 620)
        self.root.configure(bg=COLORS["page"])

        self.symptom_vars: dict[str, tk.BooleanVar] = {}
        self._build_layout()

    def _build_layout(self) -> None:
        hero = tk.Frame(self.root, bg=COLORS["accent"], padx=24, pady=18)
        hero.pack(fill="x", padx=16, pady=(14, 8))

        tk.Label(
            hero,
            text="Medical Diagnosis Expert System",
            font=("Georgia", 22, "bold"),
            bg=COLORS["accent"],
            fg="white",
        ).pack(anchor="w")

        tk.Label(
            hero,
            text="Educational rule-based assistant using forward chaining, explainable rules, and quick disease presets.",
            font=("Trebuchet MS", 11),
            bg=COLORS["accent"],
            fg="#e7f7f4",
            wraplength=840,
            justify="left",
        ).pack(anchor="w", pady=(8, 14))

        stat_row = tk.Frame(hero, bg=COLORS["accent"])
        stat_row.pack(anchor="w")

        for title, value in (
            ("Conditions", "6"),
            ("Symptoms", str(len(SYMPTOM_FIELDS))),
            ("Inference", "Forward Chaining"),
        ):
            card = tk.Frame(stat_row, bg=COLORS["accent_dark"], padx=12, pady=10)
            card.pack(side="left", padx=(0, 10))
            tk.Label(card, text=title, font=("Trebuchet MS", 9, "bold"), bg=COLORS["accent_dark"], fg="#bfe9e2").pack(anchor="w")
            tk.Label(card, text=value, font=("Georgia", 12, "bold"), bg=COLORS["accent_dark"], fg="white").pack(anchor="w")

        content = tk.Frame(self.root, bg=COLORS["page"])
        content.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        content.grid_columnconfigure(0, weight=4)
        content.grid_columnconfigure(1, weight=5)
        content.grid_rowconfigure(0, weight=1)

        left = tk.Frame(content, bg=COLORS["panel"], padx=18, pady=18, highlightbackground=COLORS["soft"], highlightthickness=1)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        right = tk.Frame(content, bg=COLORS["panel_alt"], padx=18, pady=18, highlightbackground=COLORS["soft"], highlightthickness=1)
        right.grid(row=0, column=1, sticky="nsew")

        self._build_symptom_panel(left)
        self._build_result_panel(right)

    def _build_symptom_panel(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="Select Symptoms",
            font=("Georgia", 18, "bold"),
            bg=COLORS["panel"],
            fg=COLORS["ink"],
        ).pack(anchor="w")

        actions = tk.Frame(parent, bg=COLORS["panel"])
        actions.pack(fill="x", pady=(10, 12))

        tk.Button(
            actions,
            text="Diagnose",
            command=self.on_diagnose,
            font=("Trebuchet MS", 10, "bold"),
            bg=COLORS["highlight"],
            fg="white",
            activebackground="#c75b2f",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            actions,
            text="Clear",
            command=self.on_clear,
            font=("Trebuchet MS", 10, "bold"),
            bg=COLORS["soft"],
            fg=COLORS["ink"],
            activebackground="#e6d5c0",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
        ).pack(side="left")

        tk.Label(
            parent,
            text="Choose one or more symptoms. The system will infer likely conditions from the rule base.",
            font=("Trebuchet MS", 10),
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            wraplength=420,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        grid_box = tk.Frame(parent, bg=COLORS["panel"])
        grid_box.pack(fill="x")

        for idx, (code, label) in enumerate(SYMPTOM_FIELDS):
            var = tk.BooleanVar(value=False)
            self.symptom_vars[code] = var
            row = idx // 3
            col = idx % 3

            chip = tk.Checkbutton(
                grid_box,
                text=label,
                variable=var,
                anchor="w",
                width=16,
                padx=8,
                pady=6,
                font=("Trebuchet MS", 10),
                bg=COLORS["trace_bg"],
                fg=COLORS["ink"],
                activebackground=COLORS["soft"],
                activeforeground=COLORS["ink"],
                selectcolor=COLORS["soft"],
                relief="flat",
                bd=0,
                highlightthickness=0,
            )
            chip.grid(row=row, column=col, sticky="ew", padx=5, pady=5)

        preset_wrap = tk.Frame(parent, bg=COLORS["panel"])
        preset_wrap.pack(fill="x", pady=(12, 0))

        tk.Label(
            preset_wrap,
            text="Quick Examples",
            font=("Trebuchet MS", 10, "bold"),
            bg=COLORS["panel"],
            fg=COLORS["ink"],
        ).pack(anchor="w", pady=(0, 8))

        button_row = tk.Frame(preset_wrap, bg=COLORS["panel"])
        button_row.pack(anchor="w")

        for idx, (label, symptom_set) in enumerate(EXAMPLES.items()):
            tk.Button(
                button_row,
                text=label,
                command=lambda symptoms=symptom_set: self.load_example(symptoms),
                font=("Trebuchet MS", 9, "bold"),
                bg=COLORS["accent"],
                fg="white",
                activebackground=COLORS["accent_dark"],
                activeforeground="white",
                relief="flat",
                padx=12,
                pady=7,
                cursor="hand2",
            ).grid(row=idx // 2, column=idx % 2, padx=(0, 8), pady=(0, 8), sticky="w")

        tk.Label(
            parent,
            text="Covered conditions: Common Cold, Flu, Allergies, Strep Throat, Sinusitis, Bronchitis",
            font=("Trebuchet MS", 10),
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            wraplength=420,
            justify="left",
        ).pack(anchor="w", pady=(10, 0))

    def _build_result_panel(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="Diagnosis Overview",
            font=("Georgia", 18, "bold"),
            bg=COLORS["panel_alt"],
            fg=COLORS["ink"],
        ).pack(anchor="w")

        summary_card = tk.Frame(parent, bg=COLORS["trace_bg"], padx=16, pady=16, highlightbackground=COLORS["soft"], highlightthickness=1)
        summary_card.pack(fill="x", pady=(14, 12))

        self.result_label = tk.Label(
            summary_card,
            text="Possible Diagnosis: -",
            font=("Georgia", 16, "bold"),
            bg=COLORS["trace_bg"],
            fg=COLORS["accent"],
            anchor="w",
            justify="left",
        )
        self.result_label.pack(fill="x")

        self.confidence_label = tk.Label(
            summary_card,
            text="Confidence: -",
            font=("Trebuchet MS", 10),
            bg=COLORS["trace_bg"],
            fg=COLORS["muted"],
            anchor="w",
            justify="left",
        )
        self.confidence_label.pack(fill="x", pady=(8, 4))

        self.suggestion_label = tk.Label(
            summary_card,
            text="Closest Matches: -",
            font=("Trebuchet MS", 10),
            bg=COLORS["trace_bg"],
            fg=COLORS["muted"],
            anchor="w",
            justify="left",
            wraplength=540,
        )
        self.suggestion_label.pack(fill="x")

        tk.Label(
            parent,
            text="Reasoning Trace",
            font=("Trebuchet MS", 11, "bold"),
            bg=COLORS["panel_alt"],
            fg=COLORS["ink"],
        ).pack(anchor="w", pady=(4, 8))

        self.trace_box = ScrolledText(
            parent,
            wrap="word",
            font=("Consolas", 10),
            height=24,
            bg=COLORS["trace_bg"],
            fg=COLORS["ink"],
            relief="flat",
            padx=12,
            pady=12,
            insertbackground=COLORS["ink"],
        )
        self.trace_box.pack(fill="both", expand=True)
        self.trace_box.insert(
            "1.0",
            "Reasoning trace will appear here after diagnosis.\n\nSelect symptoms on the left or load a quick example to begin.",
        )
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
        confidence_results = result["confidence_results"]
        suggestions = result["suggestions"]

        if diagnoses:
            self.result_label.config(
                text="Possible Diagnosis: " + ", ".join(diagnoses),
                fg=COLORS["accent"],
            )
            confidence_text = ", ".join(
                f"{item['label']} {item['score']}%" for item in confidence_results
            )
            self.confidence_label.config(text="Confidence: " + confidence_text, fg=COLORS["muted"])
        else:
            self.result_label.config(
                text="Possible Diagnosis: No clear diagnosis",
                fg=COLORS["danger"],
            )
            self.confidence_label.config(
                text="Confidence: No full rule match yet",
                fg=COLORS["danger"],
            )

        if suggestions:
            suggestion_text = ", ".join(f"{item['label']} {item['score']}%" for item in suggestions)
            self.suggestion_label.config(text="Closest Matches: " + suggestion_text, fg=COLORS["muted"])
        else:
            self.suggestion_label.config(text="Closest Matches: -", fg=COLORS["muted"])

        details = [
            "Input Symptoms: " + (", ".join(result["input_symptoms"]) or "None"),
            "",
            str(result["reasoning"]),
        ]
        self._set_trace_text("\n".join(details))

    def on_clear(self) -> None:
        for var in self.symptom_vars.values():
            var.set(False)
        self.result_label.config(text="Possible Diagnosis: -", fg=COLORS["accent"])
        self.confidence_label.config(text="Confidence: -", fg=COLORS["muted"])
        self.suggestion_label.config(text="Closest Matches: -", fg=COLORS["muted"])
        self._set_trace_text(
            "Reasoning trace will appear here after diagnosis.\n\nSelect symptoms on the left or load a quick example to begin."
        )

    def load_example(self, example: set[str]) -> None:
        for code, var in self.symptom_vars.items():
            var.set(code in example)


def run_gui() -> None:
    root = tk.Tk()
    ExpertSystemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
