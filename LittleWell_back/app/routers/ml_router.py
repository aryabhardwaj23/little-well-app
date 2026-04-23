"""
ML Recommendations Router — LittleWell
Exposes the ML recommendation engine via FastAPI endpoints.

New endpoints added by Suryansh Sharma (ssha0314):
    POST /ml/recommend          — ML-ranked meal recommendations
    GET  /ml/train              — trigger model training
    GET  /ml/evaluate           — run model evaluation report
    GET  /ml/health             — check model status
    GET  /ml/clusters           — get cluster analysis
"""

import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models
from ..services.mealdb_service import (
    filter_meals_by_category,
    get_meal_by_id,
    format_meal_card,
    search_meals_by_name,
)
from ..services.ausnut_service import get_food_by_name_fuzzy
from ..ml.recommender import (
    train_models,
    evaluate_models,
    rank_meals_by_ml,
    get_ideal_categories_for_age,
    generate_ml_explanation,
    get_models,
    NUTRIENT_FEATURES,
    AGE_BAND_PROFILES,
)

router = APIRouter(prefix="/ml", tags=["ML Recommendations"])


# ── HELPER: enrich meal with AUSNUT nutrition ──────────────────────────────────

def enrich_meal_with_nutrition(meal_card: dict) -> dict:
    """
    Look up AUSNUT nutrition for a meal's main ingredients.
    Aggregates nutrients across top 3 ingredients.
    """
    nutrients = {f: 0.0 for f in NUTRIENT_FEATURES}
    matched_ingredients = []

    for ing in meal_card.get("ingredients", [])[:5]:
        food_name = ing.get("ingredient", "")
        ausnut = get_food_by_name_fuzzy(food_name)
        if ausnut:
            matched_ingredients.append(food_name)
            for feat in NUTRIENT_FEATURES:
                nutrients[feat] += float(ausnut.get(feat, 0) or 0)

    meal_card["nutrients"]            = nutrients
    meal_card["matched_ingredients"]  = matched_ingredients
    meal_card["nutrition_match_rate"] = (
        round(len(matched_ingredients) / max(len(meal_card.get("ingredients", [])), 1), 2)
    )
    return meal_card


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/recommend")
async def ml_recommend(
    child_id: Optional[int] = Query(None, description="Child ID from database"),
    age_band: Optional[str] = Query("4-8", description="Age band: 2-3, 4-8, 9-13, 14-18"),
    needs_support: Optional[str] = Query("", description="Comma-separated: iron,calcium,vitamin_d,variety"),
    limit: int = Query(6, ge=1, le=20),
    db: Session = Depends(get_db),
):
    """
    ML-powered meal recommendations using Content-Based Filtering.

    Algorithm:
    1. Look up child profile from DB (if child_id provided)
    2. Map age band + nutrition needs to TheMealDB categories
    3. Fetch candidate meals from TheMealDB API
    4. Enrich each meal with AUSNUT nutritional data
    5. Score each meal using cosine similarity to age-band ideal profile
    6. Apply Random Forest to predict food group
    7. Assign KMeans cluster
    8. Rank by ML score and return top N

    MAI: Demonstrates Predictive Analytics (classification + clustering) +
         Content-based filtering + Open dataset integration
    """
    # Get child from DB if ID provided
    child_name = None
    if child_id:
        child = db.query(models.UserChild).filter(
            models.UserChild.child_id == child_id
        ).first()
        if not child:
            raise HTTPException(status_code=404, detail="Child not found")
        age_band     = child.age_band or age_band
        child_name   = child.child_name
        support_list = []
        if child.iron_status      == "needs_support": support_list.append("iron")
        if child.calcium_status   == "needs_support": support_list.append("calcium")
        if child.vitamin_d_status == "needs_support": support_list.append("vitamin_d")
        if child.variety_status   == "needs_support": support_list.append("variety")
    else:
        support_list = [s.strip() for s in (needs_support or "").split(",") if s.strip()]

    # Get appropriate meal categories from ML mapping
    categories = get_ideal_categories_for_age(age_band, support_list)

    # Fetch candidate meals from TheMealDB
    all_meals = []
    tasks = [filter_meals_by_category(cat) for cat in categories[:3]]
    category_results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in category_results:
        if isinstance(result, list):
            all_meals.extend(result[:4])

    if not all_meals:
        raise HTTPException(status_code=503, detail="Could not fetch meals from TheMealDB")

    # Get full meal details in parallel
    meal_ids = list({m["idMeal"]: m for m in all_meals}.keys())[:limit * 2]
    detail_tasks = [get_meal_by_id(mid) for mid in meal_ids]
    full_meals = await asyncio.gather(*detail_tasks, return_exceptions=True)

    # Format and enrich with AUSNUT nutrition
    enriched_meals = []
    for meal in full_meals:
        if not isinstance(meal, dict):
            continue
        card = format_meal_card(meal)
        card = enrich_meal_with_nutrition(card)
        enriched_meals.append(card)

    # ML ranking — cosine similarity + RF classification + KMeans clustering
    ranked = rank_meals_by_ml(enriched_meals, age_band, support_list, limit=limit)

    # Add plain-language ML explanation for each meal
    for meal in ranked:
        meal["ml_explanation"] = generate_ml_explanation(
            meal_name      = meal.get("name", "This meal"),
            score          = meal.get("ml_score", 0),
            percentages    = meal.get("percentages", {}),
            age_band       = age_band,
            predicted_group= meal.get("predicted_group", ""),
        )

    return {
        "recommendations": ranked,
        "total":           len(ranked),
        "child_name":      child_name,
        "age_band":        age_band,
        "needs_support":   support_list,
        "categories_used": categories,
        "ml_method":       "Content-Based Filtering + KMeans Clustering + Random Forest",
        "datasets":        [
            "AUSNUT 2023 Classifications (FSANZ, CC BY 4.0)",
            "TheMealDB API (recipes + images)",
            "Australian Dietary Guidelines (Dept of Health, CC BY 4.0)",
        ],
    }


@router.get("/train")
def trigger_training(force: bool = Query(False, description="Force retrain even if models exist")):
    """
    Train ML models from AUSNUT data.
    Run once after deployment — models saved to app/models/
    MAI: Demonstrates model training workflow.
    """
    try:
        result = train_models(force_retrain=force)
        return {
            "status":           "trained",
            "n_samples":        result.get("n_samples"),
            "n_clusters":       result.get("n_clusters"),
            "silhouette_score": round(result.get("silhouette_score", 0), 4),
            "accuracy":         round(
                result.get("classification_report", {}).get("accuracy", 0), 4
            ),
            "feature_importances": {
                k: round(v, 4)
                for k, v in sorted(
                    result.get("feature_importances", {}).items(),
                    key=lambda x: -x[1]
                )
            },
            "model_path": "/app/models/",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evaluate")
def run_evaluation():
    """
    Run full model evaluation — accuracy, F1, silhouette, bias analysis.
    MAI: Evaluating trained models for performance, robustness and bias.
    """
    try:
        result = evaluate_models()
        return {
            "accuracy":          round(result["accuracy"], 4),
            "macro_f1":          round(result["macro_f1"], 4),
            "silhouette_score":  round(result["silhouette_score"], 4),
            "n_clusters":        result["n_clusters"],
            "interpretation": {
                "accuracy":    "% of foods correctly classified into ADG food groups",
                "macro_f1":    "Average F1 across all food groups — checks for bias",
                "silhouette":  "Cluster quality (0-1, higher = better separated clusters)",
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def ml_health():
    """Check if ML models are trained and ready."""
    import os
    from ..ml.recommender import SCALER_PATH, CLUSTER_PATH, CLASSIFIER_PATH

    models_ready = all([
        os.path.exists(SCALER_PATH),
        os.path.exists(CLUSTER_PATH),
        os.path.exists(CLASSIFIER_PATH),
    ])

    return {
        "status":       "ready" if models_ready else "not_trained",
        "models_ready": models_ready,
        "message":      "Models trained and ready" if models_ready else "Run GET /ml/train first",
        "ml_method":    "Content-Based Filtering + KMeans + Random Forest",
        "datasets":     "AUSNUT 2023 + Australian Dietary Guidelines",
    }


@router.get("/clusters")
def get_cluster_analysis():
    """
    Return cluster analysis — what nutritional patterns each cluster represents.
    MAI: Demonstrates clustering results and interpretation.
    """
    try:
        from ..ml.recommender import build_ml_dataset, NUTRIENT_FEATURES
        models = get_models()
        df = build_ml_dataset()
        X = models["scaler"].transform(df[NUTRIENT_FEATURES].fillna(0))
        df["cluster"] = models["kmeans"].predict(X)

        clusters = []
        for cluster_id in sorted(df["cluster"].unique()):
            cluster_df = df[df["cluster"] == cluster_id]
            profile = {
                feat: round(float(cluster_df[feat].mean()), 2)
                for feat in NUTRIENT_FEATURES
                if feat in cluster_df.columns
            }
            # Determine dominant characteristic
            top_nutrients = sorted(
                profile.items(), key=lambda x: -x[1]
            )[:3]
            clusters.append({
                "cluster_id":    cluster_id,
                "size":          len(cluster_df),
                "avg_nutrients": profile,
                "dominant":      [n for n, _ in top_nutrients],
                "top_foods":     cluster_df["food_name"].head(5).tolist()
                                  if "food_name" in cluster_df else [],
            })

        return {
            "n_clusters": models["kmeans"].n_clusters,
            "clusters":   clusters,
            "method":     "KMeans clustering on AUSNUT nutrient profiles",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/age-profiles")
def get_age_profiles():
    """Return the ideal nutritional profiles for each age band."""
    return {
        "age_profiles":  AGE_BAND_PROFILES,
        "nutrient_units":{
            "protein_g": "grams/day", "fat_g": "grams/day",
            "carbs_g": "grams/day",   "sugar_g": "grams/day (max)",
            "fibre_g": "grams/day",   "calcium_mg": "mg/day",
            "iron_mg": "mg/day",      "sodium_mg": "mg/day (max)",
            "vitamin_c_mg": "mg/day", "zinc_mg": "mg/day",
            "calories_kcal": "kcal/day",
        },
        "source": "Australian Dietary Guidelines — Dept of Health, CC BY 4.0",
    }
