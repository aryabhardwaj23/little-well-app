"""
LittleWell — ML Meal Recommendation Engine
Feature: Content-Based Filtering + Clustering
MAI Requirements: Predictive Analytics — Classifiers, Clustering

Author: Suryansh Sharma (ssha0314) — AI/ML student
Branch: feature/meal-recommendation-ml

Architecture:
    1. Load AUSNUT 2023 classification data
    2. Build nutrient feature vectors per food group
    3. Train KMeans clustering to group foods by nutritional profile
    4. Train Random Forest classifier to predict optimal food group per age band
    5. Score and rank TheMealDB meals using cosine similarity to ideal child profile
    6. Return ranked recommendations with explanation

Datasets used:
    - AUSNUT classifications-Table 1.csv (FSANZ, CC BY 4.0)
    - AUSNUT 2023 nutrient profiles (via ausnut_service.py)
    - TheMealDB API (recipes + images)
    - Australian Dietary Guidelines age-band targets (Dept of Health, CC BY 4.0)
"""

import os
import pickle
import warnings
from functools import lru_cache
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

warnings.filterwarnings("ignore")

# ── PATHS ──────────────────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(__file__)
DATA_DIR        = os.path.join(BASE_DIR, "../data")
AUSNUT_CLASS    = os.path.join(DATA_DIR, "AUSNUT classifications-Table 1.csv")
MODEL_DIR       = os.path.join(BASE_DIR, "../models")
os.makedirs(MODEL_DIR, exist_ok=True)

SCALER_PATH     = os.path.join(MODEL_DIR, "nutrient_scaler.pkl")
CLUSTER_PATH    = os.path.join(MODEL_DIR, "kmeans_clusters.pkl")
CLASSIFIER_PATH = os.path.join(MODEL_DIR, "rf_classifier.pkl")
ENCODER_PATH    = os.path.join(MODEL_DIR, "label_encoder.pkl")

# ── NUTRIENT FEATURES used as ML input ────────────────────────────────────────
NUTRIENT_FEATURES = [
    "protein_g", "fat_g", "carbs_g", "sugar_g",
    "fibre_g", "calcium_mg", "iron_mg", "sodium_mg",
    "vitamin_c_mg", "zinc_mg", "calories_kcal",
]

# ── AGE-BAND IDEAL PROFILES (Australian Dietary Guidelines) ───────────────────
# Values represent daily targets per 100g serve equivalent
# Source: Dept of Health — Physical Activity and Exercise Guidelines, CC BY 4.0
AGE_BAND_PROFILES = {
    "2-3": {
        "protein_g": 14, "fat_g": 30, "carbs_g": 130, "sugar_g": 12,
        "fibre_g": 14, "calcium_mg": 500, "iron_mg": 7, "sodium_mg": 1000,
        "vitamin_c_mg": 35, "zinc_mg": 3, "calories_kcal": 1000,
    },
    "4-8": {
        "protein_g": 20, "fat_g": 35, "carbs_g": 155, "sugar_g": 15,
        "fibre_g": 18, "calcium_mg": 700, "iron_mg": 10, "sodium_mg": 1200,
        "vitamin_c_mg": 35, "zinc_mg": 4, "calories_kcal": 1200,
    },
    "9-13": {
        "protein_g": 40, "fat_g": 45, "carbs_g": 200, "sugar_g": 20,
        "fibre_g": 20, "calcium_mg": 1000, "iron_mg": 8, "sodium_mg": 1400,
        "vitamin_c_mg": 40, "zinc_mg": 6, "calories_kcal": 1600,
    },
    "14-18": {
        "protein_g": 65, "fat_g": 55, "carbs_g": 265, "sugar_g": 25,
        "fibre_g": 22, "calcium_mg": 1300, "iron_mg": 11, "sodium_mg": 1600,
        "vitamin_c_mg": 40, "zinc_mg": 8, "calories_kcal": 2200,
    },
}

# Nutrition support → boost weights for those nutrients in ranking
SUPPORT_WEIGHTS = {
    "iron":      {"iron_mg": 3.0, "vitamin_c_mg": 1.5},
    "calcium":   {"calcium_mg": 3.0, "protein_g": 1.5},
    "vitamin_d": {"calcium_mg": 2.0, "protein_g": 2.0},
    "variety":   {"fibre_g": 2.0, "vitamin_c_mg": 2.0},
}


# ═══════════════════════════════════════════════════════════════════════════════
# 1. DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════

@lru_cache(maxsize=1)
def load_ausnut_classifications() -> pd.DataFrame:
    """
    Load AUSNUT 2023 classification concordance.
    This maps foods to ADG food groups — used as cluster labels.
    """
    if not os.path.exists(AUSNUT_CLASS):
        raise FileNotFoundError(
            f"AUSNUT classifications CSV not found at {AUSNUT_CLASS}. "
            "Download from: https://www.foodstandards.gov.au/science-data/"
            "food-nutrient-databases/ausnut/data-files"
        )

    # Skip header rows — actual data starts at row 3
    df = pd.read_csv(AUSNUT_CLASS, skiprows=2, encoding="latin-1")
    df.columns = df.columns.str.strip()

    # Keep relevant columns
    keep = ["Food name", "2023 Australian Dietary Guidelines classification",
            "Name 1", "Code 1"]
    existing = [c for c in keep if c in df.columns]
    df = df[existing].dropna(subset=["Food name"] if "Food name" in existing else [])

    if "Food name" in df.columns:
        df["Food name"] = df["Food name"].astype(str).str.strip()

    return df


def build_ml_dataset() -> pd.DataFrame:
    """
    Build the ML training dataset by combining:
    - AUSNUT nutrient profiles (from ausnut_service)
    - AUSNUT ADG food group classifications (cluster labels)
    - Age-band targets (for supervised classification labels)

    Returns DataFrame with nutrient features + food_group label
    """
    try:
        from .ausnut_service import load_ausnut
        nutrient_df = load_ausnut()
    except ImportError:
        from app.services.ausnut_service import load_ausnut
        nutrient_df = load_ausnut()

    # Check we have nutrient features
    available = [f for f in NUTRIENT_FEATURES if f in nutrient_df.columns]
    if not available:
        raise ValueError(
            "No nutrient columns found in AUSNUT data. "
            "Check AUSNUT CSV has correct column names."
        )

    # Load classification data
    try:
        class_df = load_ausnut_classifications()
        has_classifications = "Food name" in class_df.columns and "Name 1" in class_df.columns
    except FileNotFoundError:
        has_classifications = False
        class_df = pd.DataFrame()

    # Merge on food name if classifications available
    if has_classifications and "food_name" in nutrient_df.columns:
        merged = nutrient_df.merge(
            class_df[["Food name", "Name 1"]].rename(
                columns={"Food name": "food_name", "Name 1": "adg_group"}
            ),
            on="food_name",
            how="left"
        )
        merged["adg_group"] = merged["adg_group"].fillna("Miscellaneous")
    else:
        merged = nutrient_df.copy()
        merged["adg_group"] = "Miscellaneous"

    # Fill missing nutrients with 0
    for col in NUTRIENT_FEATURES:
        if col not in merged.columns:
            merged[col] = 0.0
        merged[col] = pd.to_numeric(merged[col], errors="coerce").fillna(0)

    return merged


# ═══════════════════════════════════════════════════════════════════════════════
# 2. MODEL TRAINING
# ═══════════════════════════════════════════════════════════════════════════════

def train_models(force_retrain: bool = False) -> dict:
    """
    Train all ML models:
    1. StandardScaler — normalise nutrient features
    2. KMeans — cluster foods by nutritional profile (unsupervised)
    3. RandomForestClassifier — classify optimal food group per age band

    Models saved to app/models/ as pickle files.
    Returns evaluation metrics for MAI report.
    """
    models_exist = all([
        os.path.exists(SCALER_PATH),
        os.path.exists(CLUSTER_PATH),
        os.path.exists(CLASSIFIER_PATH),
    ])

    if models_exist and not force_retrain:
        print("Models already trained. Loading from disk.")
        return load_models()

    print("Building ML dataset from AUSNUT...")
    df = build_ml_dataset()

    features_df = df[NUTRIENT_FEATURES].fillna(0)

    # ── STEP 1: Scale features ─────────────────────────────────────────────────
    print("Fitting StandardScaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features_df)

    # ── STEP 2: KMeans Clustering ──────────────────────────────────────────────
    # Find optimal k using silhouette score (MAI metric)
    print("Training KMeans clustering (finding optimal k)...")
    best_k, best_score, best_kmeans = 5, -1, None

    for k in range(3, 9):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels, sample_size=min(1000, len(X_scaled)))
        print(f"  k={k} silhouette score: {score:.4f}")
        if score > best_score:
            best_score = score
            best_k = k
            best_kmeans = km

    print(f"Best k={best_k} with silhouette score={best_score:.4f}")
    df["cluster"] = best_kmeans.labels_

    # ── STEP 3: Random Forest Classifier ──────────────────────────────────────
    # Label = ADG food group — predicts which group a food belongs to
    print("Training Random Forest classifier...")
    le = LabelEncoder()
    y = le.fit_transform(df["adg_group"].astype(str))

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    report = classification_report(
        y_test, y_pred,
        target_names=le.classes_,
        output_dict=True,
        zero_division=0,
    )

    print("Random Forest Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0))

    # Feature importance — MAI requirement (selecting metrics)
    importances = dict(zip(NUTRIENT_FEATURES, rf.feature_importances_))
    print("\nFeature Importances:")
    for feat, imp in sorted(importances.items(), key=lambda x: -x[1]):
        print(f"  {feat}: {imp:.4f}")

    # ── SAVE MODELS ────────────────────────────────────────────────────────────
    with open(SCALER_PATH,     "wb") as f: pickle.dump(scaler,     f)
    with open(CLUSTER_PATH,    "wb") as f: pickle.dump(best_kmeans, f)
    with open(CLASSIFIER_PATH, "wb") as f: pickle.dump(rf,          f)
    with open(ENCODER_PATH,    "wb") as f: pickle.dump(le,          f)

    print(f"\nModels saved to {MODEL_DIR}")

    return {
        "scaler":          scaler,
        "kmeans":          best_kmeans,
        "classifier":      rf,
        "label_encoder":   le,
        "n_clusters":      best_k,
        "silhouette_score":best_score,
        "classification_report": report,
        "feature_importances":   importances,
        "n_samples":       len(df),
    }


def load_models() -> dict:
    """Load trained models from disk."""
    with open(SCALER_PATH,     "rb") as f: scaler = pickle.load(f)
    with open(CLUSTER_PATH,    "rb") as f: kmeans = pickle.load(f)
    with open(CLASSIFIER_PATH, "rb") as f: rf     = pickle.load(f)
    with open(ENCODER_PATH,    "rb") as f: le     = pickle.load(f)
    return {"scaler": scaler, "kmeans": kmeans, "classifier": rf, "label_encoder": le}


@lru_cache(maxsize=1)
def get_models() -> dict:
    """Get models — train if not exist, load if exist. Cached."""
    if all(os.path.exists(p) for p in [SCALER_PATH, CLUSTER_PATH, CLASSIFIER_PATH, ENCODER_PATH]):
        return load_models()
    return train_models()


# ═══════════════════════════════════════════════════════════════════════════════
# 3. SCORING ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def score_meal_nutrients(
    meal_nutrients: dict,
    age_band: str,
    needs_support: list[str] = None,
) -> dict:
    """
    Score a meal's nutrient profile against the ideal profile for a child's age band.

    Uses cosine similarity between meal nutrient vector and ideal profile vector.
    Applies support weights if child has specific nutritional needs.

    Returns:
        score (float 0-1): overall match score
        nutrient_scores (dict): per-nutrient contribution
        percentages (dict): % of daily target met by this meal
        cluster (int): which nutritional cluster this meal belongs to
        predicted_group (str): predicted ADG food group
    """
    if needs_support is None:
        needs_support = []

    ideal = AGE_BAND_PROFILES.get(age_band, AGE_BAND_PROFILES["4-8"])

    # Build feature vectors
    meal_vec   = np.array([meal_nutrients.get(f, 0) for f in NUTRIENT_FEATURES]).reshape(1, -1)
    ideal_vec  = np.array([ideal.get(f, 0)          for f in NUTRIENT_FEATURES]).reshape(1, -1)

    # Apply support weights — boost important nutrients
    weight_vec = np.ones(len(NUTRIENT_FEATURES))
    for support in needs_support:
        weights = SUPPORT_WEIGHTS.get(support, {})
        for i, feat in enumerate(NUTRIENT_FEATURES):
            if feat in weights:
                weight_vec[i] = max(weight_vec[i], weights[feat])

    meal_weighted  = meal_vec  * weight_vec
    ideal_weighted = ideal_vec * weight_vec

    # Cosine similarity score
    similarity = cosine_similarity(meal_weighted, ideal_weighted)[0][0]
    score = float(np.clip(similarity, 0, 1))

    # % of daily target per nutrient
    percentages = {}
    for feat in NUTRIENT_FEATURES:
        target = ideal.get(feat, 1)
        value  = meal_nutrients.get(feat, 0)
        percentages[feat] = round(min((value / target) * 100, 100), 1) if target > 0 else 0

    # ML predictions
    try:
        models     = get_models()
        meal_scaled = models["scaler"].transform(meal_vec)
        cluster     = int(models["kmeans"].predict(meal_scaled)[0])
        group_idx   = models["classifier"].predict(meal_scaled)[0]
        group       = models["label_encoder"].inverse_transform([group_idx])[0]
    except Exception:
        cluster = -1
        group   = "Unknown"

    return {
        "score":           round(score, 4),
        "percentages":     percentages,
        "cluster":         cluster,
        "predicted_group": group,
    }


def get_ideal_categories_for_age(age_band: str, needs_support: list[str]) -> list[str]:
    """
    Map age band + nutrition needs to TheMealDB categories.
    Used to fetch appropriate meals before ML scoring.
    """
    base_categories = {
        "2-3":  ["Vegetarian", "Pasta", "Breakfast"],
        "4-8":  ["Chicken", "Pasta", "Vegetarian", "Seafood"],
        "9-13": ["Chicken", "Beef", "Seafood", "Pasta"],
        "14-18":["Beef", "Chicken", "Seafood", "Lamb"],
    }

    support_categories = {
        "iron":      ["Chicken", "Lamb", "Beef", "Seafood"],
        "calcium":   ["Pasta", "Vegetarian", "Breakfast", "Seafood"],
        "vitamin_d": ["Seafood", "Breakfast"],
        "variety":   ["Vegan", "Vegetarian", "Side"],
    }

    categories = list(base_categories.get(age_band, ["Chicken", "Vegetarian"]))

    for support in needs_support:
        for cat in support_categories.get(support, []):
            if cat not in categories:
                categories.insert(0, cat)

    return categories[:4]


def rank_meals_by_ml(
    meals_with_nutrients: list[dict],
    age_band: str,
    needs_support: list[str] = None,
    limit: int = 6,
) -> list[dict]:
    """
    Rank a list of meals using the ML scoring engine.
    Each meal must have a 'nutrients' dict with NUTRIENT_FEATURES keys.
    Returns top meals sorted by ML score descending.
    """
    if needs_support is None:
        needs_support = []

    scored = []
    for meal in meals_with_nutrients:
        nutrients = meal.get("nutrients") or {}
        if not any(nutrients.get(f, 0) > 0 for f in NUTRIENT_FEATURES):
            meal["ml_score"] = 0.0
            meal["percentages"] = {}
            meal["cluster"] = -1
            meal["predicted_group"] = "Unknown"
            scored.append(meal)
            continue

        result = score_meal_nutrients(nutrients, age_band, needs_support)
        meal["ml_score"]        = result["score"]
        meal["percentages"]     = result["percentages"]
        meal["cluster"]         = result["cluster"]
        meal["predicted_group"] = result["predicted_group"]
        scored.append(meal)

    scored.sort(key=lambda x: x["ml_score"], reverse=True)
    return scored[:limit]


def generate_ml_explanation(
    meal_name: str,
    score: float,
    percentages: dict,
    age_band: str,
    predicted_group: str,
) -> str:
    """
    Generate a plain-language explanation of why this meal was recommended.
    Used in the LittleWell UI to explain the ML decision.
    """
    top_nutrients = sorted(
        [(k, v) for k, v in percentages.items() if v > 20],
        key=lambda x: -x[1]
    )[:3]

    nutrient_names = {
        "protein_g": "protein", "calcium_mg": "calcium", "iron_mg": "iron",
        "fibre_g": "fibre", "vitamin_c_mg": "vitamin C", "zinc_mg": "zinc",
        "calories_kcal": "energy",
    }

    if top_nutrients:
        highlights = ", ".join(
            f"{nutrient_names.get(k, k)} ({v:.0f}% of daily needs)"
            for k, v in top_nutrients
        )
        return (
            f"{meal_name} scored {score:.0%} match for the {age_band} age group. "
            f"It is a good source of {highlights}. "
            f"Classified as: {predicted_group}."
        )
    return (
        f"{meal_name} was recommended based on its overall nutritional balance "
        f"for the {age_band} age group."
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 4. EVALUATION (MAI requirement — evaluate model performance + bias)
# ═══════════════════════════════════════════════════════════════════════════════

def evaluate_models() -> dict:
    """
    Evaluate trained models for performance, robustness, and bias.
    MAI requirement: evaluating trained models for performance, robustness and bias.

    Run this and include results in your MAI report.
    """
    print("="*60)
    print("MODEL EVALUATION REPORT — LittleWell ML Recommender")
    print("MAI Requirement: Evaluating models for performance, robustness, bias")
    print("="*60)

    df = build_ml_dataset()
    features_df = df[NUTRIENT_FEATURES].fillna(0)
    models = get_models()

    X_scaled = models["scaler"].transform(features_df)
    y = models["label_encoder"].transform(df["adg_group"].astype(str))

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    y_pred = models["classifier"].predict(X_test)

    # Overall metrics
    report = classification_report(
        y_test, y_pred,
        target_names=models["label_encoder"].classes_,
        output_dict=True,
        zero_division=0,
    )

    overall_accuracy = report["accuracy"]
    macro_f1 = report["macro avg"]["f1-score"]

    print(f"\nOverall Accuracy:  {overall_accuracy:.4f}")
    print(f"Macro F1 Score:    {macro_f1:.4f}")

    # Bias analysis by food group
    print("\nPer-group Performance (bias check):")
    for group in models["label_encoder"].classes_:
        if group in report:
            m = report[group]
            print(f"  {group[:30]:<30} P={m['precision']:.2f}  R={m['recall']:.2f}  F1={m['f1-score']:.2f}  n={m['support']}")

    # Clustering quality
    cluster_labels = models["kmeans"].predict(X_scaled)
    sil = silhouette_score(X_scaled, cluster_labels, sample_size=min(1000, len(X_scaled)))
    print(f"\nClustering Silhouette Score: {sil:.4f} (higher is better, max=1.0)")
    print(f"Number of clusters: {models['kmeans'].n_clusters}")

    # Robustness — score on edge cases
    print("\nRobustness Check — Edge Cases:")
    edge_cases = [
        {"name": "All zeros",       "nutrients": {f: 0 for f in NUTRIENT_FEATURES}},
        {"name": "Very high sugar",  "nutrients": {**{f: 0 for f in NUTRIENT_FEATURES}, "sugar_g": 100}},
        {"name": "High iron meal",   "nutrients": {**{f: 0 for f in NUTRIENT_FEATURES}, "iron_mg": 15, "protein_g": 20}},
    ]
    for ec in edge_cases:
        result = score_meal_nutrients(ec["nutrients"], "4-8", [])
        print(f"  {ec['name']}: score={result['score']:.4f}, cluster={result['cluster']}")

    return {
        "accuracy":          overall_accuracy,
        "macro_f1":          macro_f1,
        "silhouette_score":  sil,
        "n_clusters":        models["kmeans"].n_clusters,
        "classification_report": report,
    }
