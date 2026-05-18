import os
import base64
import json
import re
from typing import Dict, List, Any, Optional

import pandas as pd
from groq import Groq
from sqlalchemy.orm import Session

from .. import models
from .nutrition_classifier_service import predict


groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

AUSNUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "ausnut.csv",
)


ADG_BY_AGE = {
    2: {
        "energy_kj": 4800,
        "protein_g": 16,
        "fat_g": 35,
        "carbs_g": 155,
        "fibre_g": 18,
        "calcium_mg": 500,
        "iron_mg": 9,
        "sodium_mg": 700,
    },
    4: {
        "energy_kj": 6000,
        "protein_g": 20,
        "fat_g": 40,
        "carbs_g": 200,
        "fibre_g": 18,
        "calcium_mg": 700,
        "iron_mg": 10,
        "sodium_mg": 900,
    },
    7: {
        "energy_kj": 7200,
        "protein_g": 24,
        "fat_g": 50,
        "carbs_g": 250,
        "fibre_g": 20,
        "calcium_mg": 1000,
        "iron_mg": 10,
        "sodium_mg": 1200,
    },
    11: {
        "energy_kj": 8600,
        "protein_g": 40,
        "fat_g": 60,
        "carbs_g": 300,
        "fibre_g": 24,
        "calcium_mg": 1300,
        "iron_mg": 13,
        "sodium_mg": 1400,
    },
    14: {
        "energy_kj": 10000,
        "protein_g": 57,
        "fat_g": 70,
        "carbs_g": 345,
        "fibre_g": 28,
        "calcium_mg": 1300,
        "iron_mg": 15,
        "sodium_mg": 1600,
    },
}


def get_adg(child_age: int) -> dict:
    for age in sorted(ADG_BY_AGE.keys()):
        if child_age <= age:
            return ADG_BY_AGE[age]
    return ADG_BY_AGE[14]


def age_band_to_age(age_band: Optional[str]) -> int:
    """
    Convert LittleWell age bands into an approximate numeric age
    so the existing ADG-based scoring function can still work.
    """
    if not age_band:
        return 7

    age_band = age_band.lower().strip()

    if "5" in age_band or "6" in age_band:
        return 6

    if "7" in age_band or "8" in age_band or "9" in age_band:
        return 8

    if "10" in age_band or "11" in age_band or "12" in age_band:
        return 11

    return 7


def detect_food_labels(image_bytes: bytes) -> list:
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    prompt = """
Look at this image and list every food item you can see.
Return ONLY a JSON array of food name strings, nothing else.

Example:
["pasta", "tomato sauce", "cheese", "apple"]

If no food is visible, return:
["unknown food"]
"""

    resp = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64}",
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
        max_tokens=120,
        temperature=0.1,
    )

    text = resp.choices[0].message.content.strip()

    match = re.search(r"\[.*?\]", text, re.DOTALL)

    if match:
        try:
            parsed = json.loads(match.group())
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()][:10]
        except Exception:
            pass

    words = re.sub(r'[\[\]"]', "", text).split(",")

    labels = [w.strip() for w in words if w.strip()]

    return labels[:8] or ["unknown food"]


def match_ausnut(food_labels: list) -> pd.DataFrame:
    try:
        df = pd.read_csv(AUSNUT_PATH, encoding="latin-1")

        if df.empty:
            return pd.DataFrame()

        col_lower = {c.lower(): c for c in df.columns}

        name_col = next(
            (
                col_lower[k]
                for k in col_lower
                if "food_name" in k or k == "food_name"
            ),
            df.columns[0],
        )

        matched_frames = []

        for label in food_labels:
            if not label or label.lower() == "unknown food":
                continue

            label = str(label).strip()

            try:
                matched = df[
                    df[name_col]
                    .astype(str)
                    .str.contains(label, case=False, na=False, regex=False)
                ]

                if not matched.empty:
                    matched_frames.append(matched)

            except Exception:
                continue

        if not matched_frames:
            return pd.DataFrame()

        result = pd.concat(matched_frames).drop_duplicates()

        return result.head(5)

    except FileNotFoundError:
        return pd.DataFrame()

    except Exception:
        return pd.DataFrame()


def score_nutrition(matched_df: pd.DataFrame, child_age: int) -> dict:
    if matched_df.empty:
        return {
            "overall_score": 55,
            "grade": "Fair",
            "color": "amber",
            "nutrient_scores": {},
            "note": "AUSNUT data not matched — score estimated",
        }

    adg = get_adg(child_age)

    col_lower = {c.lower(): c for c in matched_df.columns}

    def get_val(keywords: List[str]):
        for kw in keywords:
            for lk, oc in col_lower.items():
                if kw in lk:
                    try:
                        return float(matched_df[oc].iloc[0])
                    except Exception:
                        pass
        return None

    nutrients = {
        "energy_kj": get_val(["energy_kj", "energy"]),
        "protein_g": get_val(["protein_g", "protein"]),
        "fat_g": get_val(["fat_g", "fat"]),
        "carbs_g": get_val(["carbs_g", "carb"]),
        "fibre_g": get_val(["fibre_g", "fibre", "fiber"]),
        "calcium_mg": get_val(["calcium_mg", "calcium"]),
        "iron_mg": get_val(["iron_mg", "iron"]),
        "sodium_mg": get_val(["sodium_mg", "sodium"]),
    }

    scores = {}

    for key, val in nutrients.items():
        if val is not None and key in adg and adg[key] > 0:
            ratio = val / (adg[key] * 0.33)
            scores[key] = round(max(0, min(100, 100 - abs(1 - ratio) * 100)))

    overall_score = round(sum(scores.values()) / len(scores)) if scores else 55

    if overall_score >= 80:
        grade, color = "Excellent", "green"
    elif overall_score >= 60:
        grade, color = "Good", "blue"
    elif overall_score >= 40:
        grade, color = "Fair", "amber"
    else:
        grade, color = "Needs improvement", "red"

    ml_result = predict(nutrients, child_age)

    return {
        "overall_score": overall_score,
        "grade": grade,
        "color": color,
        "nutrient_scores": scores,
        "ml_classification": ml_result,
    }


def build_child_profile_context(db: Session, child: models.UserChild) -> Dict[str, Any]:
    """
    Build child profile context from existing database tables:
    - user_child
    - dietary_restriction
    - user_search_allergen
    - allergens
    """
    nutrition_focus = []

    if getattr(child, "iron_status", 0) == 1:
        nutrition_focus.append("iron")

    if getattr(child, "calcium_status", 0) == 1:
        nutrition_focus.append("calcium")

    if getattr(child, "vitamin_d_status", 0) == 1:
        nutrition_focus.append("vitamin D")

    if getattr(child, "variety_status", 0) == 1:
        nutrition_focus.append("food variety")

    restriction = None
    dietary_restrictions = []

    if getattr(child, "restriction_id", None):
        restriction = (
            db.query(models.DietaryRestriction)
            .filter(
                models.DietaryRestriction.restriction_id == child.restriction_id,
                models.DietaryRestriction.is_active == 1,
            )
            .first()
        )

        if restriction:
            dietary_restrictions.append(restriction.restriction_name)

    allergen_rows = (
        db.query(models.Allergen)
        .join(
            models.UserSearchAllergen,
            models.UserSearchAllergen.allergen_id == models.Allergen.allergen_id,
        )
        .filter(
            models.UserSearchAllergen.user_id == child.user_id,
            models.UserSearchAllergen.child_id == child.child_id,
        )
        .all()
    )

    allergens = []

    for allergen in allergen_rows:
        name = (
            allergen.canonical_allergen
            or allergen.allergen_clean
            or allergen.allergen_name
            or allergen.allergen_code
        )

        if name:
            allergens.append(str(name).strip())

    return {
        "child_id": child.child_id,
        "child_name": child.child_name or "your child",
        "age_band": child.age_band or "school age",
        "child_age": age_band_to_age(child.age_band),
        "allergens": allergens,
        "dietary_restriction": {
            "restriction_id": restriction.restriction_id,
            "restriction_code": restriction.restriction_code,
            "restriction_name": restriction.restriction_name,
            "restriction_type": restriction.restriction_type,
            "excludes_meat": restriction.excludes_meat,
            "excludes_fish": restriction.excludes_fish,
            "excludes_dairy": restriction.excludes_dairy,
            "excludes_egg": restriction.excludes_egg,
            "excludes_pork": restriction.excludes_pork,
            "excludes_shellfish": restriction.excludes_shellfish,
            "excludes_gluten": restriction.excludes_gluten,
            "excludes_nuts": restriction.excludes_nuts,
        }
        if restriction
        else None,
        "dietary_restrictions": dietary_restrictions,
        "nutrition_focus": nutrition_focus,
    }


def _contains_any(text: str, keywords: List[str]) -> bool:
    return any(keyword.lower() in text for keyword in keywords)


def generate_personalised_checks(
    food_labels: List[str],
    child_context: Dict[str, Any],
) -> Dict[str, Any]:
    foods_text = " ".join([str(food).lower() for food in food_labels])

    allergy_warnings = []
    dietary_warnings = []
    nutrition_focus_feedback = []

    allergens = child_context.get("allergens", []) or []
    nutrition_focus = child_context.get("nutrition_focus", []) or []
    restriction = child_context.get("dietary_restriction") or {}

    # Allergy warning by simple keyword match.
    # Use cautious wording because image recognition cannot confirm ingredients.
    for allergen in allergens:
        allergen_text = str(allergen).lower().strip()

        if not allergen_text:
            continue

        allergen_keywords = [allergen_text]

        if allergen_text in ["peanut", "peanuts"]:
            allergen_keywords.extend(["peanut butter", "nuts", "nut"])

        if allergen_text in ["milk", "dairy"]:
            allergen_keywords.extend(["milk", "cheese", "yoghurt", "yogurt", "cream", "butter"])

        if allergen_text in ["egg", "eggs"]:
            allergen_keywords.extend(["egg", "omelette", "mayonnaise"])

        if allergen_text in ["gluten", "wheat"]:
            allergen_keywords.extend(["bread", "pasta", "cracker", "biscuit", "wrap", "wheat"])

        if _contains_any(foods_text, allergen_keywords):
            allergy_warnings.append(
                f"Possible {allergen} allergen detected. Please check the ingredients carefully before serving."
            )

    # Dietary restriction warning using existing DietaryRestriction exclusion flags.
    if restriction:
        restriction_name = restriction.get("restriction_name", "the selected dietary restriction")

        if restriction.get("excludes_meat") == 1 and _contains_any(
            foods_text,
            ["beef", "chicken", "lamb", "meat", "ham", "sausage", "bacon", "turkey"],
        ):
            dietary_warnings.append(
                f"This lunchbox may not match {restriction_name} because meat-like food was detected."
            )

        if restriction.get("excludes_fish") == 1 and _contains_any(
            foods_text,
            ["fish", "tuna", "salmon", "seafood"],
        ):
            dietary_warnings.append(
                f"This lunchbox may not match {restriction_name} because fish or seafood was detected."
            )

        if restriction.get("excludes_dairy") == 1 and _contains_any(
            foods_text,
            ["milk", "cheese", "yoghurt", "yogurt", "cream", "butter"],
        ):
            dietary_warnings.append(
                f"This lunchbox may not match {restriction_name} because dairy-like food was detected."
            )

        if restriction.get("excludes_egg") == 1 and _contains_any(
            foods_text,
            ["egg", "omelette", "mayonnaise"],
        ):
            dietary_warnings.append(
                f"This lunchbox may not match {restriction_name} because egg-like food was detected."
            )

        if restriction.get("excludes_pork") == 1 and _contains_any(
            foods_text,
            ["pork", "ham", "bacon", "salami"],
        ):
            dietary_warnings.append(
                f"This lunchbox may not match {restriction_name} because pork-like food was detected."
            )

        if restriction.get("excludes_shellfish") == 1 and _contains_any(
            foods_text,
            ["prawn", "shrimp", "crab", "lobster", "shellfish"],
        ):
            dietary_warnings.append(
                f"This lunchbox may not match {restriction_name} because shellfish-like food was detected."
            )

        if restriction.get("excludes_gluten") == 1 and _contains_any(
            foods_text,
            ["bread", "pasta", "cracker", "biscuit", "wrap", "wheat", "noodle"],
        ):
            dietary_warnings.append(
                f"This lunchbox may not match {restriction_name} because gluten-containing food may be present."
            )

        if restriction.get("excludes_nuts") == 1 and _contains_any(
            foods_text,
            ["nut", "nuts", "peanut", "almond", "cashew", "walnut"],
        ):
            dietary_warnings.append(
                f"This lunchbox may not match {restriction_name} because nut-like food was detected."
            )

    # Nutrition focus suggestions.
    if "iron" in nutrition_focus:
        if _contains_any(
            foods_text,
            ["beef", "meat", "egg", "beans", "lentils", "spinach", "tofu", "chickpea"],
        ):
            nutrition_focus_feedback.append(
                "This lunchbox appears to include foods that may support iron intake."
            )
        else:
            nutrition_focus_feedback.append(
                "This child has iron support marked. Consider adding iron-rich foods such as lean meat, eggs, beans, lentils, tofu, or iron-fortified bread."
            )

    if "calcium" in nutrition_focus:
        if _contains_any(
            foods_text,
            ["milk", "cheese", "yoghurt", "yogurt", "tofu"],
        ):
            nutrition_focus_feedback.append(
                "This lunchbox appears to include foods that may support calcium intake."
            )
        else:
            nutrition_focus_feedback.append(
                "This child has calcium support marked. Consider adding yoghurt, cheese, milk, or calcium-fortified alternatives."
            )

    if "vitamin D" in nutrition_focus:
        if _contains_any(
            foods_text,
            ["egg", "salmon", "tuna", "fish", "mushroom"],
        ):
            nutrition_focus_feedback.append(
                "This lunchbox may include foods that support vitamin D intake."
            )
        else:
            nutrition_focus_feedback.append(
                "This child has vitamin D support marked. Consider eggs, oily fish, fortified dairy, or fortified alternatives when suitable."
            )

    if "food variety" in nutrition_focus:
        if len(set([str(food).lower() for food in food_labels])) >= 4:
            nutrition_focus_feedback.append(
                "This lunchbox shows a good level of variety across different visible foods."
            )
        else:
            nutrition_focus_feedback.append(
                "This child has food variety support marked. Try adding different colours, textures, or food groups across the week."
            )

    return {
        "allergy_warnings": allergy_warnings,
        "dietary_warnings": dietary_warnings,
        "nutrition_focus_feedback": nutrition_focus_feedback,
    }


def generate_ai_feedback(
    food_labels: List[str],
    nutrition_score: Dict[str, Any],
    child_context: Optional[Dict[str, Any]] = None,
    personalised_checks: Optional[Dict[str, Any]] = None,
) -> str:
    foods = ", ".join(food_labels[:6]) if food_labels else "the food items"

    grade = nutrition_score.get("grade", "Fair")
    score = nutrition_score.get("overall_score", 50)

    ml = nutrition_score.get("ml_classification", {})
    ml_label = ml.get("display_label", "")

    child_context = child_context or {}
    personalised_checks = personalised_checks or {}

    child_name = child_context.get("child_name", "your child")
    age_band = child_context.get("age_band", "school age")
    child_age = child_context.get("child_age", age_band_to_age(age_band))

    allergens = child_context.get("allergens", []) or []
    dietary_restrictions = child_context.get("dietary_restrictions", []) or []
    nutrition_focus = child_context.get("nutrition_focus", []) or []

    allergy_warnings = personalised_checks.get("allergy_warnings", []) or []
    dietary_warnings = personalised_checks.get("dietary_warnings", []) or []
    nutrition_focus_feedback = personalised_checks.get("nutrition_focus_feedback", []) or []

    prompt = f"""
You are a friendly children's nutritionist for the LittleWell app in Australia.

A parent uploaded a lunchbox photo.

Child profile:
- Name: {child_name}
- Age band: {age_band}
- Approximate scoring age: {child_age}
- Recorded allergens: {", ".join(allergens) if allergens else "none recorded"}
- Dietary restrictions: {", ".join(dietary_restrictions) if dietary_restrictions else "none recorded"}
- Nutrition focus areas: {", ".join(nutrition_focus) if nutrition_focus else "general balanced eating"}

Detected lunchbox foods:
{foods}

Nutrition result:
- Score: {score}/100
- Rating: {grade}
- ML classification: {ml_label if ml_label else "not available"}

Rule-based personalised findings:
- Allergy warnings: {allergy_warnings if allergy_warnings else "none"}
- Dietary warnings: {dietary_warnings if dietary_warnings else "none"}
- Nutrition focus feedback: {nutrition_focus_feedback if nutrition_focus_feedback else "none"}

Write a warm 3-sentence feedback paragraph for the parent:
1. Acknowledge the detected foods.
2. Explain the rating using the child's age band and profile.
3. Give one specific improvement tip based on allergy, dietary restriction, or nutrition focus if relevant.

Important safety rules:
- Do not claim the image proves an allergen is definitely present.
- Use cautious wording such as "may contain" or "please check ingredients" for allergy and restriction issues.
- Be encouraging.
- No bullet points.
- Parent-friendly language.
"""

    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=220,
        temperature=0.7,
    )

    return resp.choices[0].message.content.strip()