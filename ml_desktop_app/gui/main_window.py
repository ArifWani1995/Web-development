from __future__ import annotations

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ml_desktop_app.ml.ml_engine import MLEngine
from ml_desktop_app.utils.helpers import ToolTip, apply_theme


class MLDesktopApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Advanced ML Studio")
        self.geometry("1320x780")
        self.minsize(1100, 680)

        self.engine = MLEngine()
        self.dark_mode = True
        self.colors = apply_theme(self, self.dark_mode)
        self.prediction_log: list[dict[str, str]] = []
        self.feature_entries: dict[str, ttk.Entry] = {}

        self._build_layout()

    def _build_layout(self) -> None:
        self.configure(bg=self.colors["bg"])
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(self, style="App.TFrame", padding=10)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content = ttk.Frame(self, style="Surface.TFrame", padding=14)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        ttk.Label(self.sidebar, text="⚙ Advanced ML Studio", font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, pady=(8, 16), sticky="w"
        )

        nav_items = ["Home", "Dataset", "Train Model", "Predict", "Visualize", "About"]
        for idx, item in enumerate(nav_items, start=1):
            btn = ttk.Button(self.sidebar, text=item, style="Sidebar.TButton", command=lambda tab=item: self.show_tab(tab))
            btn.grid(row=idx, column=0, pady=5, sticky="ew")
            btn.bind("<Enter>", lambda e, b=btn: b.configure(cursor="hand2"))

        mode_btn = ttk.Button(self.sidebar, text="🌗 Toggle Theme", style="Accent.TButton", command=self.toggle_theme)
        mode_btn.grid(row=8, column=0, pady=(20, 5), sticky="ew")

        self.status_var = tk.StringVar(value="Ready")
        self.progress = ttk.Progressbar(self.sidebar, mode="indeterminate", length=180)
        self.progress.grid(row=9, column=0, pady=8)
        ttk.Label(self.sidebar, textvariable=self.status_var).grid(row=10, column=0, sticky="w")

        self.header_label = ttk.Label(self.content, style="Title.TLabel", text="Welcome to Advanced ML Studio")
        self.header_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.page_holder = ttk.Frame(self.content, style="Surface.TFrame")
        self.page_holder.grid(row=1, column=0, sticky="nsew")
        self.page_holder.grid_rowconfigure(0, weight=1)
        self.page_holder.grid_columnconfigure(0, weight=1)

        self.pages: dict[str, ttk.Frame] = {}
        for page in ["Home", "Dataset", "Train Model", "Predict", "Visualize", "About"]:
            frame = ttk.Frame(self.page_holder, style="Surface.TFrame", padding=8)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[page] = frame

        self._build_home()
        self._build_dataset_tab()
        self._build_train_tab()
        self._build_predict_tab()
        self._build_visualize_tab()
        self._build_about_tab()
        self.show_tab("Home")

    def toggle_theme(self) -> None:
        self.dark_mode = not self.dark_mode
        self.colors = apply_theme(self, self.dark_mode)
        self._build_layout()

    def _build_home(self) -> None:
        frame = self.pages["Home"]
        ttk.Label(
            frame,
            text="Build, train, evaluate, and deploy ML models in a modern desktop dashboard.",
            style="Body.TLabel",
        ).grid(row=0, column=0, sticky="w", pady=8)

        cards = [
            "📁 Dataset import + preprocessing",
            "🧠 Classification/Regression training",
            "📈 Embedded charts + heatmaps",
            "🔮 Real-time predictions + export",
        ]
        for idx, text in enumerate(cards, start=1):
            card = ttk.Frame(frame, style="Card.TFrame", padding=10)
            card.grid(row=idx, column=0, sticky="ew", pady=5)
            ttk.Label(card, text=text).grid(row=0, column=0, sticky="w")

    def _build_dataset_tab(self) -> None:
        frame = self.pages["Dataset"]
        btn_frame = ttk.Frame(frame, style="Surface.TFrame")
        btn_frame.grid(row=0, column=0, sticky="w", pady=8)

        load_btn = ttk.Button(btn_frame, text="Load CSV", style="Accent.TButton", command=self.load_dataset)
        load_btn.grid(row=0, column=0, padx=4)
        ToolTip(load_btn, "Load a CSV dataset from your computer.")

        clean_btn = ttk.Button(btn_frame, text="Clean Data", command=self.clean_dataset)
        clean_btn.grid(row=0, column=1, padx=4)

        reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_all)
        reset_btn.grid(row=0, column=2, padx=4)

        self.dataset_preview = tk.Text(frame, height=26, wrap="none", bg="#0b1120", fg="#f8fafc")
        self.dataset_preview.grid(row=1, column=0, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def _build_train_tab(self) -> None:
        frame = self.pages["Train Model"]
        controls = ttk.Frame(frame, style="Surface.TFrame")
        controls.grid(row=0, column=0, sticky="w", pady=8)

        ttk.Label(controls, text="Target column:").grid(row=0, column=0, padx=5)
        self.target_combo = ttk.Combobox(controls, width=24, state="readonly")
        self.target_combo.grid(row=0, column=1, padx=5)

        ttk.Label(controls, text="Model:").grid(row=0, column=2, padx=5)
        self.model_combo = ttk.Combobox(
            controls,
            width=22,
            state="readonly",
            values=["Random Forest", "Logistic Regression", "Linear Regression"],
        )
        self.model_combo.current(0)
        self.model_combo.grid(row=0, column=3, padx=5)

        ttk.Button(controls, text="Train", style="Accent.TButton", command=self.train_model).grid(row=0, column=4, padx=8)
        ttk.Button(controls, text="Save Model", command=self.save_model).grid(row=0, column=5, padx=4)
        ttk.Button(controls, text="Load Model", command=self.load_model).grid(row=0, column=6, padx=4)

        self.metrics_var = tk.StringVar(value="Metrics will appear here after training.")
        ttk.Label(frame, textvariable=self.metrics_var, style="Body.TLabel").grid(row=1, column=0, sticky="w", pady=8)

        self.cm_fig, self.cm_ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.cm_canvas = FigureCanvasTkAgg(self.cm_fig, master=frame)
        self.cm_canvas.get_tk_widget().grid(row=2, column=0, sticky="nsew")
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def _build_predict_tab(self) -> None:
        frame = self.pages["Predict"]
        self.predict_form = ttk.Frame(frame, style="Surface.TFrame")
        self.predict_form.grid(row=0, column=0, sticky="nw")

        action_frame = ttk.Frame(frame, style="Surface.TFrame")
        action_frame.grid(row=1, column=0, sticky="w", pady=8)
        ttk.Button(action_frame, text="Predict", style="Accent.TButton", command=self.make_prediction).grid(row=0, column=0, padx=4)
        ttk.Button(action_frame, text="Export Predictions", command=self.export_predictions).grid(row=0, column=1, padx=4)
        ttk.Button(action_frame, text="Clear", command=self.clear_prediction_form).grid(row=0, column=2, padx=4)

        self.prediction_var = tk.StringVar(value="Prediction output will appear here.")
        ttk.Label(frame, textvariable=self.prediction_var, style="Body.TLabel").grid(row=2, column=0, sticky="w")

        self.pred_fig, self.pred_ax = plt.subplots(figsize=(6, 3), dpi=100)
        self.pred_canvas = FigureCanvasTkAgg(self.pred_fig, master=frame)
        self.pred_canvas.get_tk_widget().grid(row=3, column=0, sticky="nsew")
        frame.grid_rowconfigure(3, weight=1)

    def _build_visualize_tab(self) -> None:
        frame = self.pages["Visualize"]
        top = ttk.Frame(frame, style="Surface.TFrame")
        top.grid(row=0, column=0, sticky="w")
        ttk.Button(top, text="Correlation Heatmap", command=self.plot_heatmap).grid(row=0, column=0, padx=4, pady=5)
        ttk.Button(top, text="Scatter", command=self.plot_scatter).grid(row=0, column=1, padx=4, pady=5)
        ttk.Button(top, text="Line", command=self.plot_line).grid(row=0, column=2, padx=4, pady=5)
        ttk.Button(top, text="Bar", command=self.plot_bar).grid(row=0, column=3, padx=4, pady=5)

        self.viz_fig, self.viz_ax = plt.subplots(figsize=(7, 4), dpi=100)
        self.viz_canvas = FigureCanvasTkAgg(self.viz_fig, master=frame)
        self.viz_canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def _build_about_tab(self) -> None:
        frame = self.pages["About"]
        text = (
            "Advanced ML Studio\n\n"
            "• Responsive Tkinter app with modern multi-page layout\n"
            "• End-to-end ML workflow using scikit-learn\n"
            "• Interactive data visualizations with matplotlib + seaborn\n"
            "• Exportable predictions and model persistence\n\n"
            "Built for portfolio demos, interviews, and college submission."
        )
        ttk.Label(frame, text=text, style="Body.TLabel", justify="left").grid(row=0, column=0, sticky="nw")

    def show_tab(self, tab_name: str) -> None:
        self.header_label.config(text=tab_name)
        self.pages[tab_name].tkraise()

    def load_dataset(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        try:
            df = self.engine.load_csv(file_path)
            self.update_preview(df)
            self.target_combo["values"] = list(df.columns)
            if len(df.columns) > 0:
                self.target_combo.current(len(df.columns) - 1)
            self.status_var.set(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")
        except Exception as exc:
            messagebox.showerror("Load Error", str(exc))

    def clean_dataset(self) -> None:
        try:
            df = self.engine.clean_data()
            self.update_preview(df)
            self.target_combo["values"] = list(df.columns)
            self.status_var.set("Data cleaned: duplicates removed and columns normalized")
        except Exception as exc:
            messagebox.showerror("Clean Error", str(exc))

    def update_preview(self, df: pd.DataFrame) -> None:
        self.dataset_preview.delete("1.0", tk.END)
        self.dataset_preview.insert(tk.END, df.head(30).to_string())

    def train_model(self) -> None:
        target = self.target_combo.get()
        model_name = self.model_combo.get()
        if not target:
            messagebox.showwarning("Target Missing", "Select a target column first.")
            return

        def worker() -> None:
            try:
                self.progress.start(12)
                self.status_var.set("Training model...")
                result = self.engine.train_model(target, model_name)
                self.metrics_var.set(f"{result.model_name} | {result.score_label}: {result.score_value:.4f}")
                self._plot_confusion_or_residual(result)
                self._build_prediction_fields()
                self.status_var.set("Training completed")
            except Exception as exc:
                messagebox.showerror("Train Error", str(exc))
            finally:
                self.progress.stop()

        threading.Thread(target=worker, daemon=True).start()

    def _plot_confusion_or_residual(self, result) -> None:
        self.cm_ax.clear()
        if result.task_type == "classification" and result.confusion_matrix is not None:
            sns.heatmap(result.confusion_matrix, annot=True, fmt="d", cmap="mako", ax=self.cm_ax)
            self.cm_ax.set_title("Confusion Matrix")
            self.cm_ax.set_xlabel("Predicted")
            self.cm_ax.set_ylabel("Actual")
        else:
            self.cm_ax.scatter(result.y_test, result.y_pred, c="#22d3ee", alpha=0.7)
            self.cm_ax.set_title("Actual vs Predicted")
            self.cm_ax.set_xlabel("Actual")
            self.cm_ax.set_ylabel("Predicted")
        self.cm_fig.tight_layout()
        self.cm_canvas.draw()

    def _build_prediction_fields(self) -> None:
        for widget in self.predict_form.winfo_children():
            widget.destroy()
        self.feature_entries.clear()

        for idx, col in enumerate(self.engine.feature_columns):
            ttk.Label(self.predict_form, text=col).grid(row=idx, column=0, sticky="w", padx=4, pady=3)
            entry = ttk.Entry(self.predict_form, width=28)
            entry.grid(row=idx, column=1, padx=4, pady=3)
            self.feature_entries[col] = entry

    def make_prediction(self) -> None:
        try:
            payload: dict[str, object] = {}
            for feature, entry in self.feature_entries.items():
                raw = entry.get().strip()
                if raw == "":
                    payload[feature] = None
                    continue
                try:
                    payload[feature] = float(raw)
                except ValueError:
                    payload[feature] = raw

            prediction = self.engine.predict(payload)
            self.prediction_var.set(f"Prediction: {prediction}")
            self.prediction_log.append({**{k: str(v) for k, v in payload.items()}, "prediction": str(prediction)})
            self._plot_prediction_history()
        except Exception as exc:
            messagebox.showerror("Prediction Error", str(exc))

    def _plot_prediction_history(self) -> None:
        self.pred_ax.clear()
        if not self.prediction_log:
            self.pred_canvas.draw()
            return
        vals = [row["prediction"] for row in self.prediction_log]
        numeric_vals = pd.to_numeric(pd.Series(vals), errors="coerce")
        if numeric_vals.notna().all():
            self.pred_ax.plot(range(1, len(vals) + 1), numeric_vals, color="#a78bfa", marker="o")
            self.pred_ax.set_ylabel("Prediction Value")
        else:
            counts = pd.Series(vals).value_counts()
            self.pred_ax.bar(counts.index.astype(str), counts.values, color="#22d3ee")
            self.pred_ax.set_ylabel("Frequency")
        self.pred_ax.set_title("Prediction Result Visualization")
        self.pred_ax.set_xlabel("Request #")
        self.pred_fig.tight_layout()
        self.pred_canvas.draw()

    def export_predictions(self) -> None:
        if not self.prediction_log:
            messagebox.showwarning("No Data", "Run predictions first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        pd.DataFrame(self.prediction_log).to_csv(path, index=False)
        self.status_var.set(f"Predictions exported to {path}")

    def clear_prediction_form(self) -> None:
        for entry in self.feature_entries.values():
            entry.delete(0, tk.END)
        self.prediction_var.set("Prediction output will appear here.")

    def reset_all(self) -> None:
        self.engine = MLEngine()
        self.dataset_preview.delete("1.0", tk.END)
        self.target_combo.set("")
        self.metrics_var.set("Metrics will appear here after training.")
        self.clear_prediction_form()
        self.status_var.set("Reset complete")

    def save_model(self) -> None:
        if self.engine.pipeline is None:
            messagebox.showwarning("Missing Model", "Train a model before saving.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".joblib", filetypes=[("Joblib", "*.joblib")])
        if not path:
            return
        bundle = {
            "pipeline": self.engine.pipeline,
            "feature_columns": self.engine.feature_columns,
            "target_column": self.engine.target_column,
        }
        joblib.dump(bundle, path)
        self.status_var.set(f"Model saved to {path}")

    def load_model(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Joblib", "*.joblib")])
        if not path:
            return
        bundle = joblib.load(path)
        self.engine.pipeline = bundle["pipeline"]
        self.engine.feature_columns = bundle["feature_columns"]
        self.engine.target_column = bundle["target_column"]
        self._build_prediction_fields()
        self.status_var.set(f"Model loaded from {path}")

    def _safe_viz_columns(self) -> tuple[str, str]:
        if self.engine.dataframe is None:
            raise ValueError("Load a dataset first.")
        num_cols = self.engine.dataframe.select_dtypes(include="number").columns.tolist()
        if len(num_cols) < 2:
            raise ValueError("Need at least two numeric columns for this chart.")
        return num_cols[0], num_cols[1]

    def plot_heatmap(self) -> None:
        try:
            corr = self.engine.correlation_matrix()
            self.viz_ax.clear()
            sns.heatmap(corr, cmap="rocket", ax=self.viz_ax)
            self.viz_ax.set_title("Correlation Heatmap")
            self.viz_fig.tight_layout()
            self.viz_canvas.draw()
        except Exception as exc:
            messagebox.showerror("Visualization Error", str(exc))

    def plot_scatter(self) -> None:
        try:
            c1, c2 = self._safe_viz_columns()
            self.viz_ax.clear()
            self.viz_ax.scatter(self.engine.dataframe[c1], self.engine.dataframe[c2], c="#22d3ee", alpha=0.65)
            self.viz_ax.set_title(f"Scatter Plot: {c1} vs {c2}")
            self.viz_ax.set_xlabel(c1)
            self.viz_ax.set_ylabel(c2)
            self.viz_fig.tight_layout()
            self.viz_canvas.draw()
        except Exception as exc:
            messagebox.showerror("Visualization Error", str(exc))

    def plot_line(self) -> None:
        try:
            c1, c2 = self._safe_viz_columns()
            self.viz_ax.clear()
            self.viz_ax.plot(self.engine.dataframe[c1].head(100), self.engine.dataframe[c2].head(100), color="#a78bfa")
            self.viz_ax.set_title(f"Line Plot: {c1} to {c2}")
            self.viz_fig.tight_layout()
            self.viz_canvas.draw()
        except Exception as exc:
            messagebox.showerror("Visualization Error", str(exc))

    def plot_bar(self) -> None:
        try:
            if self.engine.dataframe is None:
                raise ValueError("Load a dataset first.")
            col = self.engine.dataframe.columns[0]
            counts = self.engine.dataframe[col].astype(str).value_counts().head(10)
            self.viz_ax.clear()
            self.viz_ax.bar(counts.index, counts.values, color="#38bdf8")
            self.viz_ax.set_title(f"Top categories in {col}")
            self.viz_ax.tick_params(axis="x", rotation=40)
            self.viz_fig.tight_layout()
            self.viz_canvas.draw()
        except Exception as exc:
            messagebox.showerror("Visualization Error", str(exc))
