"""
USDA FoodData Central API Service — LittleWell
Free, unlimited, government-verified nutrition data.
Get your free API key at: https://fdc.nal.usda.gov/api-key-signup
No credit card required.
"""
import httpx
import os
from typing import Optional

BASE_URL = "https://api.nal.usda.gov/fdc/v1"

# Store key in .env file — never hardcode it
USDA_API_KEY = os.getenv("USDA_API_KEY", "DEMO_KEY")


# ── NUTRIENT IDs (USDA standard IDs) ─────────────────────────────────────────
NUTRIENT_IDS = {
    "calories":  1008,  # Energy (kcal)
    "protein":   1003,  # Protein (g)
    "fat":       1004,  # Total lipid/fat (g)
    "carbs":     1005,  # Carbohydrate (g)
    "sugar":     2000,  # Total sugars (g)
    "fibre":     1079,  # Dietary fibre (g)
    "calcium":   1087,  # Calcium (mg)
    "iron":      1089,  # Iron (mg)
    "sodium":    1093,  # Sodium (mg)
    "vitamin_c": 1162,  # Vitamin C (mg)
    "vitamin_d": 1114,  # Vitamin D (IU)
    "zinc":      1095,  # Zinc (mg)
}

# Australian Dietary Guidelines — child requirements (ages 4–8 as a guide)
CHILD_DAILY_REQUIREMENTS = {
    "calories":  1200,  # kcal/day
    "protein":   20,    # g/day
    "calcium":   700,   # mg/day
    "iron":      10,    # mg/day
    "fibre":     18,    # g/day
    "sugar":     25,    # g/day max (WHO guideline)
    "vitamin_c": 35,    # mg/day
}


# ── SEARCH ────────────────────────────────────────────────────────────────────

async def search_nutrition(food_name: str, page_size: int = 10) -> list[dict]:
    """
    Search for food nutrition data by name.
    Returns list of food items with full nutrient breakdown.
    """
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{BASE_URL}/foods/search",
            params={
                "query":    food_name,
                "pageSize": page_size,
                "api_key":  USDA_API_KEY,
                "dataType": "Survey (FNDDS),SR Legacy",  # Most reliable food types
            }
        )
        r.raise_for_status()
        data = r.json()
        return data.get("foods", [])


async def get_food_by_id(fdc_id: int) -> Optional[dict]:
    """Get detailed nutrition data for a specific food by FDC ID."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{BASE_URL}/food/{fdc_id}",
            params={"api_key": USDA_API_KEY}
        )
        r.raise_for_status()
        return r.json()


# ── NUTRIENT EXTRACTION ───────────────────────────────────────────────────────

def extract_nutrients(food_item: dict) -> dict:
    """
    Extract key nutrients from a USDA food item into a clean dict.
    Works with both search results and individual food lookups.
    """
    nutrients_raw = food_item.get("foodNutrients", [])

    # Build lookup by nutrient ID
    nutrient_lookup = {}
    for n in nutrients_raw:
        nid   = n.get("nutrientId") or n.get("nutrient", {}).get("id")
        value = n.get("value") or n.get("amount") or 0
        if nid:
            nutrient_lookup[nid] = value

    return {
        "calories_kcal":  nutrient_lookup.get(NUTRIENT_IDS["calories"],  0),
        "protein_g":      nutrient_lookup.get(NUTRIENT_IDS["protein"],   0),
        "fat_g":          nutrient_lookup.get(NUTRIENT_IDS["fat"],       0),
        "carbs_g":        nutrient_lookup.get(NUTRIENT_IDS["carbs"],     0),
        "sugar_g":        nutrient_lookup.get(NUTRIENT_IDS["sugar"],     0),
        "fibre_g":        nutrient_lookup.get(NUTRIENT_IDS["fibre"],     0),
        "calcium_mg":     nutrient_lookup.get(NUTRIENT_IDS["calcium"],   0),
        "iron_mg":        nutrient_lookup.get(NUTRIENT_IDS["iron"],      0),
        "sodium_mg":      nutrient_lookup.get(NUTRIENT_IDS["sodium"],    0),
        "vitamin_c_mg":   nutrient_lookup.get(NUTRIENT_IDS["vitamin_c"], 0),
        "zinc_mg":        nutrient_lookup.get(NUTRIENT_IDS["zinc"],      0),
    }


def get_nutrition_labels(nutrients: dict) -> list[str]:
    """
    Returns plain-language nutrition labels for LittleWell UI.
    e.g. ['High Iron', 'Good source of Calcium', 'Low Sugar']
    Based on Australian Dietary Guidelines thresholds for children.
    """
    labels = []

    if nutrients.get("iron_mg", 0) >= 2.5:
        labels.append("High Iron")

    if nutrients.get("calcium_mg", 0) >= 120:
        labels.append("High Calcium")

    if nutrients.get("sugar_g", 0) <= 5:
        labels.append("Low Sugar")

    if nutrients.get("fibre_g", 0) >= 3:
        labels.append("Good source of Fibre")

    if nutrients.get("protein_g", 0) >= 10:
        labels.append("High Protein")

    if nutrients.get("vitamin_c_mg", 0) >= 7:
        labels.append("Contains Vitamin C")

    if nutrients.get("calories_kcal", 0) <= 300:
        labels.append("Low Calorie")

    return labels


def get_child_percentage(nutrients: dict) -> dict:
    """
    Returns what % of a child's daily needs each nutrient provides.
    Used for the LittleWell nutritional summary card.
    """
    result = {}
    for key, daily in CHILD_DAILY_REQUIREMENTS.items():
        nutrient_key = f"{key}_{'kcal' if key == 'calories' else 'g' if key not in ['calcium','iron','vitamin_c'] else 'mg'}"
        value = nutrients.get(nutrient_key, 0)
        pct = round((value / daily) * 100, 1) if daily > 0 else 0
        result[key] = min(pct, 100)  # cap at 100%
    return result
