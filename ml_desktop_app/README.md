# Advanced ML Studio (Tkinter + Scikit-learn)

A colorful, responsive desktop application that demonstrates a complete machine-learning workflow:

- Load CSV datasets
- Clean/preprocess data
- Train models (Random Forest, Logistic Regression, Linear Regression)
- Evaluate model performance (accuracy/R² + confusion matrix/actual-vs-predicted)
- Run real-time predictions with user input
- Visualize data (heatmap, scatter, line, bar)
- Save/load model and export predictions
- Toggle dark/light theme

## Project Structure

```text
ml_desktop_app/
├── app.py
├── requirements.txt
├── README.md
├── gui/
│   └── main_window.py
├── ml/
│   └── ml_engine.py
└── utils/
    └── helpers.py
```

## Module Walkthrough

### `ml/ml_engine.py`
Core machine learning logic:
- CSV loading, cleaning
- Task inference (classification vs regression)
- Preprocessing pipeline (imputation, scaling, one-hot encoding)
- Model training and evaluation
- Single-record prediction
- Correlation matrix generation

### `gui/main_window.py`
Main Tkinter application:
- Responsive layout using `grid`
- Sidebar navigation for Home/Dataset/Train/Predict/Visualize/About
- Embedded matplotlib charts with `FigureCanvasTkAgg`
- Progress bar during training
- File dialogs, message boxes, and reset/clear interactions

### `utils/helpers.py`
Shared UI utilities:
- Color palettes (dark/light)
- ttk theme styling
- Tooltip helper class

## Screen Layout

- **Home**: feature cards and quick overview
- **Dataset**: load/clean/reset and table preview
- **Train Model**: target/model selection, training metrics, confusion matrix chart
- **Predict**: dynamically generated feature form, prediction output, history chart, CSV export
- **Visualize**: heatmap + chart shortcuts
- **About**: project summary

## Run Instructions

1. Install dependencies:
   ```bash
   pip install -r ml_desktop_app/requirements.txt
   ```
2. Launch:
   ```bash
   python -m ml_desktop_app.app
   ```

## Future Upgrades

- Add model comparison dashboard (cross-validation and leaderboard)
- Add hyperparameter tuning panel (GridSearchCV/RandomizedSearchCV)
- Integrate SHAP-based explainability view
- Add dataset profiling (missingness map, outlier report)
- Add SQLite persistence for prediction history
