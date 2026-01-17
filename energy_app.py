from pathlib import Path
from typing import Dict, List

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "steel_industry_data_sample.csv"
MODEL_PATH = BASE_DIR / "steel_energy_model.pkl"

FEATURE_COLUMNS: List[str] = [
    "Usage_kWh",
    "Lagging_Current_Reactive.Power_kVarh",
    "Leading_Current_Reactive_Power_kVarh",
    "CO2(tCO2)",
    "Lagging_Current_Power_Factor",
    "Leading_Current_Power_Factor",
    "NSM",
    "WeekStatus",
    "Day_of_week",
]
TARGET_COLUMN = "Load_Type"


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure column names match the expected schema."""
    rename_map = {
        "Leading_Current_Reactive_Power_KVarh": "Leading_Current_Reactive_Power_kVarh",
    }
    return df.rename(columns=rename_map)


def train_energy_model() -> Dict[str, object]:
    """Train a RandomForest (bagging) classifier on the steel industry sample data."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df = _normalize_columns(df)

    missing_cols = [col for col in FEATURE_COLUMNS + [TARGET_COLUMN] if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset missing required columns: {missing_cols}")

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN]

    categorical = ["Day_of_week", "WeekStatus"]
    numeric = [c for c in FEATURE_COLUMNS if c not in categorical]

    preprocessor = ColumnTransformer(
        [
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("numeric", "passthrough", numeric),
        ]
    )

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    pipeline = Pipeline([("preprocess", preprocessor), ("model", model)])
    pipeline.fit(X, y)

    bundle = {"model": pipeline, "feature_columns": FEATURE_COLUMNS}
    joblib.dump(bundle, MODEL_PATH)
    return bundle


def load_energy_model() -> Dict[str, object]:
    """Load the trained model bundle, training a fresh one if needed."""
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return train_energy_model()


model_bundle = load_energy_model()
model = model_bundle["model"]
feature_columns = model_bundle["feature_columns"]

app = Flask(__name__)


@app.route("/api/energy/predict", methods=["POST"])
def predict_energy_load():
    """Predict load type for provided steel industry energy metrics."""
    payload = request.get_json(silent=True) or {}
    missing = [col for col in feature_columns if col not in payload]
    if missing:
        return (
            jsonify({"error": f"Missing required fields: {', '.join(sorted(missing))}"}),
            400,
        )

    try:
        input_frame = pd.DataFrame(
            [{col: payload[col] for col in feature_columns}],
            columns=feature_columns,
        )
        prediction = model.predict(input_frame)[0]

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_frame)[0].max()
        else:
            proba = None

        response = {"load_type": str(prediction)}
        if proba is not None:
            response["confidence"] = float(proba)
        return jsonify(response)
    except Exception as exc:  # pragma: no cover - defensive
        return jsonify({"error": str(exc)}), 500


@app.route("/api/energy/health", methods=["GET"])
def healthcheck():
    return jsonify({"status": "ok"})


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=False, port=5001)
