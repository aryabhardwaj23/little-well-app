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


# Scoring settings.
# A lunchbox photo cannot confirm exact serving size, so 25% of daily target is
# more reasonable than treating the image as exactly one third of daily intake.
TARGET_SHARE = 0.25

MAX_VISUAL_BONUS = 6
MAX_VISUAL_PENALTY = -6

FALLBACK_MIN = 45
FALLBACK_MAX = 70

FINAL_MIN = 35
FINAL_MAX = 95

# Child safety settings.
# Critical items override normal nutrition scoring.
CRITICAL_SAFETY_SCORE = 15

# Caution items are not as severe as alcohol / nicotine / energy drinks,
# but should not receive a high score.
CAUTION_SAFETY_SCORE_CAP = 45


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
Look at this image and list every visible food item, drink item, or lunchbox-related item.
Return ONLY a JSON array of item name strings, nothing else.

Important:
- Include drinks if visible.
- Include items that are not suitable for children if visible.
- Do not hide unsafe or non-food items.
- Be specific when possible, for example "beer", "wine", "energy drink", "coffee", "vape", "cigarette", "soft drink", or "whole grapes".
- If the item is a branded drink, describe the type if you can, such as "energy drink", "soft drink", "sports drink", or "coffee".

Example:
["sandwich", "apple", "yoghurt", "water"]

Unsafe examples that should still be returned if visible:
["beer", "wine", "vodka", "energy drink", "coffee", "vape", "cigarette", "tobacco"]

If no food or drink is visible, return:
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
        max_tokens=180,
        temperature=0.1,
    )

    text = resp.choices[0].message.content.strip()

    match = re.search(r"\[.*?\]", text, re.DOTALL)

    if match:
        try:
            parsed = json.loads(match.group())
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()][:12]
        except Exception:
            pass

    words = re.sub(r'[\[\]"]', "", text).split(",")

    labels = [w.strip() for w in words if w.strip()]

    return labels[:10] or ["unknown food"]


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


def _safe_mean_from_columns(
    matched_df: pd.DataFrame,
    col_lower: dict,
    keywords: List[str],
):
    """
    Get average numeric value from AUSNUT matched rows.

    This is better than iloc[0] because one detected food can match
    several AUSNUT rows.
    """
    for kw in keywords:
        for lk, oc in col_lower.items():
            if kw in lk:
                try:
                    values = pd.to_numeric(
                        matched_df[oc],
                        errors="coerce",
                    ).dropna()

                    if not values.empty:
                        return float(values.mean())
                except Exception:
                    pass

    return None


def _build_food_text(food_labels: Optional[List[str]]) -> str:
    return " ".join(
        [
            str(item).lower().strip()
            for item in food_labels or []
            if str(item).strip()
        ]
    )


def _has_any(text: str, keywords: List[str]) -> bool:
    return any(keyword.lower() in text for keyword in keywords)


def _child_safety_check(food_labels: Optional[List[str]]) -> dict:
    """
    Detect items that are not suitable or not recommended for children's lunchboxes.

    Critical items override the normal nutrition score.
    Caution items cap the score and produce a clear warning.
    """
    text = _build_food_text(food_labels)

    warnings = []
    detected_categories = []

    alcohol_keywords = [
        "alcohol",
        "alcoholic drink",
        "alcoholic beverage",
        "beer",
        "lager",
        "ale",
        "stout",
        "wine",
        "red wine",
        "white wine",
        "sparkling wine",
        "champagne",
        "prosecco",
        "cider",
        "hard cider",
        "vodka",
        "whiskey",
        "whisky",
        "bourbon",
        "scotch",
        "rum",
        "gin",
        "tequila",
        "brandy",
        "liqueur",
        "liquor",
        "cocktail",
        "martini",
        "margarita",
        "mojito",
        "soju",
        "sake",
        "baijiu",
        "shochu",
        "spirits",
    ]

    energy_drink_keywords = [
        "energy drink",
        "red bull",
        "monster",
        "v energy",
        "rockstar",
        "mother energy",
        "prime energy",
        "bang energy",
        "reign",
        "celsius",
        "lucozade energy",
        "5-hour energy",
        "energy shot",
    ]

    tobacco_nicotine_keywords = [
        "tobacco",
        "cigarette",
        "cigarettes",
        "cigar",
        "cigars",
        "vape",
        "vaping",
        "vape pen",
        "e-cigarette",
        "e cigarette",
        "electronic cigarette",
        "nicotine",
        "nicotine pouch",
        "nicotine pouches",
        "snus",
        "hookah",
        "shisha",
    ]

    caffeine_keywords = [
        "coffee",
        "espresso",
        "latte",
        "cappuccino",
        "flat white",
        "iced coffee",
        "cold brew",
        "mocha",
        "macchiato",
        "americano",
        "strong tea",
        "black tea",
        "green tea",
        "matcha",
        "yerba mate",
    ]

    high_sugar_drink_keywords = [
        "soft drink",
        "soda",
        "cola",
        "coke",
        "pepsi",
        "sprite",
        "fanta",
        "lemonade",
        "sports drink",
        "gatorade",
        "powerade",
        "slurpee",
        "slushie",
        "bubble tea",
        "milk tea",
    ]

    choking_risk_keywords = [
        "whole grapes",
        "grapes",
        "hard candy",
        "hard lolly",
        "hard lollies",
        "popcorn",
        "marshmallow",
        "whole nuts",
        "peanuts",
        "almonds",
        "cashews",
    ]

    if _has_any(text, alcohol_keywords):
        detected_categories.append("alcohol")
        warnings.append(
            "Alcohol was detected. Alcohol is not suitable for children and should not be included in a child's lunchbox."
        )

    if _has_any(text, energy_drink_keywords):
        detected_categories.append("energy_drink")
        warnings.append(
            "An energy drink may be present. Energy drinks are not suitable for children."
        )

    if _has_any(text, tobacco_nicotine_keywords):
        detected_categories.append("tobacco_or_nicotine")
        warnings.append(
            "A tobacco or nicotine product may be present. This is not suitable or safe for children."
        )

    if _has_any(text, caffeine_keywords):
        detected_categories.append("caffeine")
        warnings.append(
            "A caffeinated drink may be present. Caffeinated drinks are not recommended for children's lunchboxes."
        )

    if _has_any(text, high_sugar_drink_keywords):
        detected_categories.append("high_sugar_drink")
        warnings.append(
            "A high-sugar drink may be present. Water or milk is usually a better lunchbox drink for children."
        )

    if _has_any(text, choking_risk_keywords):
        detected_categories.append("possible_choking_risk")
        warnings.append(
            "A possible choking-risk food may be present. Please prepare age-appropriate portions, such as cutting grapes and avoiding hard lollies."
        )

    critical_categories = {
        "alcohol",
        "energy_drink",
        "tobacco_or_nicotine",
    }

    caution_categories = {
        "caffeine",
        "high_sugar_drink",
        "possible_choking_risk",
    }

    is_critical = any(
        category in critical_categories for category in detected_categories
    )

    is_caution = any(
        category in caution_categories for category in detected_categories
    )

    return {
        "is_critical": is_critical,
        "is_caution": is_caution,
        "detected_categories": detected_categories,
        "warnings": warnings,
    }


def _visual_adjustment(food_labels: Optional[List[str]]) -> dict:
    """
    Small visual adjustment only.

    AUSNUT remains the main scoring source.
    This adjustment helps photo analysis handle visible food balance,
    because a photo cannot provide exact serving weight.
    """
    text = _build_food_text(food_labels)

    adjustment = 0
    reasons = []

    has_fruit = _has_any(
        text,
        [
            "apple",
            "banana",
            "orange",
            "grape",
            "berry",
            "berries",
            "strawberry",
            "blueberry",
            "pear",
            "melon",
            "kiwi",
            "mandarin",
            "peach",
            "pineapple",
            "fruit",
        ],
    )

    has_vegetable = _has_any(
        text,
        [
            "carrot",
            "cucumber",
            "lettuce",
            "tomato",
            "spinach",
            "broccoli",
            "corn",
            "peas",
            "pea",
            "vegetable",
            "salad",
            "capsicum",
            "avocado",
            "zucchini",
        ],
    )

    has_protein = _has_any(
        text,
        [
            "chicken",
            "beef",
            "egg",
            "eggs",
            "tuna",
            "salmon",
            "fish",
            "tofu",
            "beans",
            "lentils",
            "lentil",
            "chickpea",
            "turkey",
            "cheese",
            "yoghurt",
            "yogurt",
        ],
    )

    has_grain = _has_any(
        text,
        [
            "bread",
            "sandwich",
            "wrap",
            "rice",
            "pasta",
            "noodle",
            "crackers",
            "cracker",
            "oats",
            "cereal",
            "roll",
            "toast",
            "tortilla",
        ],
    )

    has_sweet_snack = _has_any(
        text,
        [
            "cake",
            "cookie",
            "cookies",
            "biscuit",
            "chocolate",
            "candy",
            "lolly",
            "lollies",
            "chips",
            "crisps",
            "soft drink",
            "soda",
            "donut",
            "doughnut",
            "muffin",
        ],
    )

    has_processed = _has_any(
        text,
        [
            "sausage",
            "salami",
            "bacon",
            "nugget",
            "nuggets",
            "processed",
            "fried",
            "hot dog",
            "pizza",
        ],
    )

    visible_count = len(
        set(
            [
                str(item).lower().strip()
                for item in food_labels or []
                if str(item).strip()
            ]
        )
    )

    if has_fruit:
        adjustment += 2
        reasons.append("fruit detected")

    if has_vegetable:
        adjustment += 2
        reasons.append("vegetable detected")

    if has_protein:
        adjustment += 2
        reasons.append("protein source detected")

    if has_grain:
        adjustment += 1
        reasons.append("grain or carbohydrate source detected")

    if visible_count >= 4:
        adjustment += 1
        reasons.append("good visible variety")

    if has_sweet_snack:
        adjustment -= 4
        reasons.append("sweet or snack food detected")

    if has_processed:
        adjustment -= 3
        reasons.append("processed food detected")

    # Keep visual adjustment small so AUSNUT remains the main scoring source.
    adjustment = max(MAX_VISUAL_PENALTY, min(MAX_VISUAL_BONUS, adjustment))

    return {
        "adjustment": adjustment,
        "reasons": reasons,
    }


def _get_grade_and_color(overall_score: int):
    if overall_score >= 85:
        return "Excellent", "green"

    if overall_score >= 70:
        return "Good", "blue"

    if overall_score >= 50:
        return "Fair", "amber"

    return "Needs improvement", "red"


def score_nutrition(
    matched_df: pd.DataFrame,
    child_age: int,
    food_labels: Optional[List[str]] = None,
) -> dict:
    """
    AUSNUT-first scoring with child-safety override.

    Frontend does not need to change because the main response fields stay:
    - overall_score
    - grade
    - color
    - nutrient_scores
    - ml_classification

    Main idea:
    - Critical child-safety issues override normal scoring.
    - AUSNUT nutrient data creates the base score.
    - Visible food labels only provide a small adjustment.
    - If AUSNUT matching fails, use a conservative visible-food estimate.
    """

    safety = _child_safety_check(food_labels)
    visual = _visual_adjustment(food_labels)

    # Critical safety override:
    # alcohol, energy drinks, tobacco or nicotine products should not receive
    # a normal nutrition score.
    if safety["is_critical"]:
        try:
            ml_result = predict(
                {
                    "energy_kj": None,
                    "protein_g": None,
                    "fat_g": None,
                    "carbs_g": None,
                    "fibre_g": None,
                    "calcium_mg": None,
                    "iron_mg": None,
                    "sodium_mg": None,
                },
                child_age,
            )
        except Exception:
            ml_result = {
                "label": "not_suitable",
                "display_label": "Not suitable for children",
            }

        return {
            "overall_score": CRITICAL_SAFETY_SCORE,
            "grade": "Not suitable",
            "color": "red",
            "nutrient_scores": {},
            "ml_classification": ml_result,
            "ausnut_score": None,
            "visual_adjustment": 0,
            "balance_reasons": [],
            "safety_warnings": safety["warnings"],
            "safety_categories": safety["detected_categories"],
            "scoring_method": "child_safety_override",
            "note": (
                "This item is not suitable for children. The normal nutrition score "
                "was overridden by child safety rules."
            ),
        }

    if matched_df.empty:
        fallback_score = 55 + visual["adjustment"]

        # Caution items are not as severe as alcohol/energy drinks/tobacco,
        # but they should not receive a high score either.
        if safety["is_caution"]:
            fallback_score = min(fallback_score, CAUTION_SAFETY_SCORE_CAP)

        fallback_score = max(FALLBACK_MIN, min(FALLBACK_MAX, round(fallback_score)))

        grade, color = _get_grade_and_color(fallback_score)

        return {
            "overall_score": fallback_score,
            "grade": grade,
            "color": color,
            "nutrient_scores": {},
            "ml_classification": {
                "label": "estimated",
                "display_label": "Estimated from visible foods",
            },
            "ausnut_score": None,
            "visual_adjustment": visual["adjustment"],
            "balance_reasons": visual["reasons"],
            "safety_warnings": safety["warnings"],
            "safety_categories": safety["detected_categories"],
            "scoring_method": (
                "visible_estimate_with_safety_caution"
                if safety["is_caution"]
                else "visible_estimate_no_ausnut_match"
            ),
            "note": "AUSNUT data not matched — score estimated from visible foods",
        }

    adg = get_adg(child_age)
    col_lower = {c.lower(): c for c in matched_df.columns}

    nutrients = {
        "energy_kj": _safe_mean_from_columns(
            matched_df,
            col_lower,
            ["energy_kj", "energy"],
        ),
        "protein_g": _safe_mean_from_columns(
            matched_df,
            col_lower,
            ["protein_g", "protein"],
        ),
        "fat_g": _safe_mean_from_columns(
            matched_df,
            col_lower,
            ["fat_g", "total_fat", "fat"],
        ),
        "carbs_g": _safe_mean_from_columns(
            matched_df,
            col_lower,
            ["carbs_g", "carbohydrate", "carb"],
        ),
        "fibre_g": _safe_mean_from_columns(
            matched_df,
            col_lower,
            ["fibre_g", "fiber", "fibre"],
        ),
        "calcium_mg": _safe_mean_from_columns(
            matched_df,
            col_lower,
            ["calcium_mg", "calcium"],
        ),
        "iron_mg": _safe_mean_from_columns(
            matched_df,
            col_lower,
            ["iron_mg", "iron"],
        ),
        "sodium_mg": _safe_mean_from_columns(
            matched_df,
            col_lower,
            ["sodium_mg", "sodium"],
        ),
    }

    nutrient_scores = {}

    for key, val in nutrients.items():
        if val is None:
            continue

        if key not in adg or adg[key] <= 0:
            continue

        lunchbox_target = adg[key] * TARGET_SHARE
        ratio = val / lunchbox_target

        # Positive nutrients.
        # Banded scoring is more stable than forcing every value to be exactly
        # close to the target.
        if key in [
            "energy_kj",
            "protein_g",
            "carbs_g",
            "fibre_g",
            "calcium_mg",
            "iron_mg",
        ]:
            if 0.8 <= ratio <= 1.3:
                score = 90
            elif 0.6 <= ratio < 0.8:
                score = 75
            elif 0.4 <= ratio < 0.6:
                score = 60
            elif 1.3 < ratio <= 1.8:
                score = 75
            elif ratio > 1.8:
                # Too much energy/carbs should be treated more carefully.
                # For protein, fibre, calcium and iron, being above target is
                # not necessarily as negative.
                if key in ["energy_kj", "carbs_g"]:
                    score = 60
                else:
                    score = 65
            else:
                score = 45

            nutrient_scores[key] = score

        # Fat should be moderate, but children also need some healthy fats.
        elif key == "fat_g":
            if 0.5 <= ratio <= 1.4:
                score = 85
            elif 1.4 < ratio <= 2.0:
                score = 70
            elif ratio > 2.0:
                score = 50
            else:
                score = 65

            nutrient_scores[key] = score

        # Sodium should be lower.
        elif key == "sodium_mg":
            if ratio <= 0.8:
                score = 90
            elif ratio <= 1.0:
                score = 80
            elif ratio <= 1.5:
                score = 60
            elif ratio <= 2.0:
                score = 45
            else:
                score = 30

            nutrient_scores[key] = score

    if nutrient_scores:
        ausnut_score = round(
            sum(nutrient_scores.values()) / len(nutrient_scores)
        )
    else:
        ausnut_score = 55

    overall_score = ausnut_score + visual["adjustment"]

    # Caution safety items should cap the score even if AUSNUT score looks okay.
    if safety["is_caution"]:
        overall_score = min(overall_score, CAUTION_SAFETY_SCORE_CAP)

    # Keep final score reasonable.
    overall_score = max(FINAL_MIN, min(FINAL_MAX, round(overall_score)))

    grade, color = _get_grade_and_color(overall_score)

    try:
        ml_result = predict(nutrients, child_age)
    except Exception:
        ml_result = {
            "label": "unknown",
            "display_label": "Not enough data",
        }

    return {
        "overall_score": overall_score,
        "grade": grade,
        "color": color,
        "nutrient_scores": nutrient_scores,
        "ml_classification": ml_result,

        # Extra fields are safe.
        # Frontend can ignore them if it does not use them.
        "ausnut_score": ausnut_score,
        "visual_adjustment": visual["adjustment"],
        "balance_reasons": visual["reasons"],
        "safety_warnings": safety["warnings"],
        "safety_categories": safety["detected_categories"],
        "scoring_method": (
            "ausnut_first_with_safety_caution"
            if safety["is_caution"]
            else "ausnut_first_with_small_visual_adjustment"
        ),
        "note": (
            "Overall score is mainly based on AUSNUT nutrient data. "
            "Visible food groups only provide a small adjustment because photo analysis cannot confirm exact portion size."
        ),
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
            allergen_keywords.extend(
                ["milk", "cheese", "yoghurt", "yogurt", "cream", "butter"]
            )

        if allergen_text in ["egg", "eggs"]:
            allergen_keywords.extend(["egg", "omelette", "mayonnaise"])

        if allergen_text in ["gluten", "wheat"]:
            allergen_keywords.extend(
                ["bread", "pasta", "cracker", "biscuit", "wrap", "wheat"]
            )

        if _contains_any(foods_text, allergen_keywords):
            allergy_warnings.append(
                f"Possible {allergen} allergen detected. Please check the ingredients carefully before serving."
            )

    # Dietary restriction warning using existing DietaryRestriction exclusion flags.
    if restriction:
        restriction_name = restriction.get(
            "restriction_name",
            "the selected dietary restriction",
        )

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

    safety_warnings = nutrition_score.get("safety_warnings", []) or []
    safety_categories = nutrition_score.get("safety_categories", []) or []
    scoring_method = nutrition_score.get("scoring_method", "")

    # Hard override for critical child-safety issues.
    # This avoids the LLM softening alcohol / energy drink / nicotine warnings.
    if scoring_method == "child_safety_override" and safety_warnings:
        warning_text = " ".join(safety_warnings)

        return (
            f"I detected {foods} in the lunchbox photo. "
            f"This is not suitable for {child_name}'s lunchbox. {warning_text} "
            "Please remove this item and replace it with child-friendly options such as water, fruit, yoghurt, wholegrain snacks, or a balanced sandwich."
        )

    # Softer direct handling for caution warnings, such as caffeine, high-sugar drinks,
    # or possible choking-risk foods.
    if safety_warnings:
        warning_text = " ".join(safety_warnings)

        return (
            f"I detected {foods} in the lunchbox photo. "
            f"The score is {score}/100, rated {grade}, but there is an important safety note: {warning_text} "
            "Please check the item carefully and choose an age-appropriate, child-friendly option where needed."
        )

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
- Safety categories: {safety_categories if safety_categories else "none"}
- Safety warnings: {safety_warnings if safety_warnings else "none"}
- Scoring method: {scoring_method if scoring_method else "standard nutrition scoring"}

Rule-based personalised findings:
- Allergy warnings: {allergy_warnings if allergy_warnings else "none"}
- Dietary warnings: {dietary_warnings if dietary_warnings else "none"}
- Nutrition focus feedback: {nutrition_focus_feedback if nutrition_focus_feedback else "none"}

Write a warm 3-sentence feedback paragraph for the parent:
1. Acknowledge the detected foods.
2. Explain the rating using the child's age band and profile.
3. Give one specific improvement tip based on allergy, dietary restriction, nutrition focus, or safety warning if relevant.

Important safety rules:
- If safety warnings are present, clearly state that the item is not suitable or not recommended for children.
- If alcohol, energy drinks, tobacco or nicotine products are detected, make this the main message.
- Do not soften alcohol, energy drink, nicotine, tobacco or vaping warnings as normal nutrition issues.
- Do not claim the image proves an allergen is definitely present.
- Use cautious wording such as "may contain" or "please check ingredients" for allergy and restriction issues.
- Be encouraging, but be direct when the item is unsafe or unsuitable for children.
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
        max_tokens=240,
        temperature=0.6,
    )

    return resp.choices[0].message.content.strip()