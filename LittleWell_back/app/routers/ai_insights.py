from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Any

from ..services.why_this_meal_service import (
    generate_why_this_meal,
    generate_weekly_nutrition_story,
)
from ..services.nutrition_classifier_service import predict

router = APIRouter(prefix="/ai-insights", tags=["AI Insights"])


class WhyThisMealRequest(BaseModel):
    meal_name: str
    child_age: int
    allergens: list[str] = Field(default_factory=list)
    dietary_restrictions: list[str] = Field(default_factory=list)
    season: Optional[str] = "autumn"
    meal_type: Optional[str] = "lunchbox"


class WeeklyStoryMeal(BaseModel):
    title: Optional[str] = ""
    recipe_title: Optional[str] = ""
    cook_day: Optional[str] = ""
    explanation: Optional[str] = ""
    nutrition_focus: list[str] = Field(default_factory=list)
    meal_context: Optional[str] = ""


class WeeklyStoryRequest(BaseModel):
    # Compatible with both old frontend list[str] and new frontend list[object]
    meals: list[WeeklyStoryMeal | str]
    child_age: int
    child_name: Optional[str] = "your child"


class ClassifyRequest(BaseModel):
    nutriments: dict[str, Any]
    child_age: Optional[int] = 7


@router.post("/why-this-meal")
async def why_this_meal(request: WhyThisMealRequest):
    try:
        explanation = generate_why_this_meal(
            meal_name=request.meal_name,
            child_age=request.child_age,
            allergens=request.allergens,
            dietary_restrictions=request.dietary_restrictions,
            season=request.season or "seasonal",
            meal_type=request.meal_type or "lunchbox",
        )

        return {
            "meal_name": request.meal_name,
            "explanation": explanation,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/weekly-story")
async def weekly_story(request: WeeklyStoryRequest):
    try:
        normalised_meals: list[str] = []

        for meal in request.meals:
            if isinstance(meal, str):
                if meal.strip():
                    normalised_meals.append(meal.strip())
                continue

            parts = [
                f"Meal title: {meal.title}" if meal.title else "",
                f"Recipe inspiration: {meal.recipe_title}" if meal.recipe_title else "",
                f"Cook day: {meal.cook_day}" if meal.cook_day else "",
                (
                    f"Nutrition focus: {', '.join(meal.nutrition_focus)}"
                    if meal.nutrition_focus
                    else ""
                ),
                f"Meal context: {meal.meal_context}" if meal.meal_context else "",
                (
                    f"Meal explanation already generated: {meal.explanation}"
                    if meal.explanation
                    else ""
                ),
            ]

            meal_text = ". ".join([part for part in parts if part]).strip()

            if meal_text:
                normalised_meals.append(meal_text)

        story = generate_weekly_nutrition_story(
            meals=normalised_meals,
            child_age=request.child_age,
            child_name=request.child_name or "your child",
        )

        return {
            "story": story,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/classify-nutrition")
async def classify_nutrition(request: ClassifyRequest):
    try:
        return predict(request.nutriments, request.child_age)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train-classifier")
async def train_classifier():
    try:
        import os
        import pickle
        import pandas as pd

        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report

        ausnut_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "ausnut.csv",
        )

        model_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "nutrition_classifier.pkl",
        )

        df = pd.read_csv(ausnut_path)

        features = [
            "energy_kj",
            "protein_g",
            "fat_g",
            "carbs_g",
            "sugars_g",
            "fibre_g",
            "calcium_mg",
            "iron_mg",
            "sodium_mg",
        ]

        df = df.dropna(subset=features)

        def label(row):
            if row.sugars_g > 15 or row.sodium_mg > 400 or row.fat_g > 20:
                return "at-risk"

            if (
                row.fibre_g >= 2
                and row.sugars_g < 8
                and row.sodium_mg < 200
                and row.protein_g > 1
            ):
                return "balanced"

            return "moderate"

        df["label"] = df.apply(label, axis=1)

        X = df[features].values
        y = df["label"].values

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
        )

        clf = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced",
        )

        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)

        report_dict = classification_report(
            y_test,
            y_pred,
            output_dict=True,
        )

        report_str = classification_report(y_test, y_pred)

        with open(model_path, "wb") as f:
            pickle.dump(
                {
                    "model": clf,
                    "features": features,
                    "report": report_str,
                },
                f,
            )

        return {
            "status": "trained",
            "dataset": "AUSNUT 2011-13 (real Australian food data)",
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "accuracy": round(report_dict["accuracy"] * 100, 1),
            "label_distribution": df["label"].value_counts().to_dict(),
            "classification_report": report_dict,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))