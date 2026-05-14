"""
TheMealDB API Service — LittleWell
Fetches meal recipes, images, and ingredient data.
Free, unlimited, no API key required for educational use.
API key "1" is the public test key.
"""

import re
from typing import Optional

import httpx

BASE_URL = "https://www.themealdb.com/api/json/v1/1"


# ── SEARCH ────────────────────────────────────────────────────────────────────

async def search_meals_by_name(name: str) -> list[dict]:
    """Search meals by name. Returns list of meal objects with images."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/search.php", params={"s": name})
        r.raise_for_status()
        data = r.json()
        return data.get("meals") or []


async def filter_meals_by_category(category: str) -> list[dict]:
    """
    Filter meals by category.
    Available: Beef, Chicken, Dessert, Lamb, Miscellaneous,
               Pasta, Pork, Seafood, Side, Starter, Vegan,
               Vegetarian, Breakfast, Goat
    Returns: list with idMeal, strMeal, strMealThumb (image URL)
    """
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/filter.php", params={"c": category})
        r.raise_for_status()
        data = r.json()
        return data.get("meals") or []


async def filter_meals_by_ingredient(ingredient: str) -> list[dict]:
    """Filter meals by main ingredient, e.g. chicken, salmon, lentils."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/filter.php", params={"i": ingredient})
        r.raise_for_status()
        data = r.json()
        return data.get("meals") or []


async def get_meal_by_id(meal_id: str) -> Optional[dict]:
    """Get full meal details including ingredients, instructions, and image."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/lookup.php", params={"i": meal_id})
        r.raise_for_status()
        data = r.json()
        meals = data.get("meals")
        return meals[0] if meals else None


async def get_random_meal() -> Optional[dict]:
    """Get a single random meal with full details."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/random.php")
        r.raise_for_status()
        data = r.json()
        meals = data.get("meals")
        return meals[0] if meals else None


async def list_categories() -> list[dict]:
    """List all meal categories with thumbnail and description."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/categories.php")
        r.raise_for_status()
        data = r.json()
        return data.get("categories") or []


# ── PARSING HELPERS ───────────────────────────────────────────────────────────

def parse_ingredients(meal: dict) -> list[dict]:
    """
    TheMealDB stores ingredients as strIngredient1..20 and strMeasure1..20.
    This parses them into a clean list safely, even when values are None.
    """
    ingredients = []

    for i in range(1, 21):
        ingredient = (meal.get(f"strIngredient{i}") or "").strip()
        measure = (meal.get(f"strMeasure{i}") or "").strip()

        if ingredient:
            ingredients.append({
                "ingredient": ingredient,
                "measure": measure,
                "image": f"https://www.themealdb.com/images/ingredients/{ingredient}-Small.png",
            })

    return ingredients


def parse_instructions(instructions: Optional[str]) -> list[str]:
    """
    Clean MealDB instructions into a step list.

    Handles cases like:
    - blank lines
    - standalone numbering lines: "1", "2", "3"
    - prefixes like "Step 1", "STEP 2 -", etc.
    """
    if not instructions:
        return []

    # Normalize line breaks
    text = instructions.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return []

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    cleaned_steps = []

    for line in lines:
        # Skip pure numbers like "1", "2", "3"
        if line.isdigit():
            continue

        # Remove prefixes like "Step 1", "STEP 2 -", "3.", "4)"
        line = re.sub(r"^step\s*\d+\s*[-:.)]?\s*", "", line, flags=re.IGNORECASE)
        line = re.sub(r"^\d+\s*[-:.)]\s*", "", line)

        line = line.strip()
        if line:
            cleaned_steps.append(line)

    return cleaned_steps


def parse_tags(tags: Optional[str]) -> list[str]:
    """Convert comma-separated tag string into a clean list."""
    if not tags:
        return []

    return [tag.strip() for tag in tags.split(",") if tag.strip()]


def format_meal_card(meal: dict) -> dict:
    """
    Returns a clean meal card dict ready for the Vue frontend.
    Compatible with LittleWell's meal browse page and recipe page.
    """
    image = meal.get("strMealThumb")

    return {
        "id": meal.get("idMeal"),
        "name": meal.get("strMeal"),
        "category": meal.get("strCategory"),
        "area": meal.get("strArea"),
        "image": image,
        "thumbnail": f"{image}/preview" if image else None,
        "instructions": parse_instructions(meal.get("strInstructions")),
        "ingredients": parse_ingredients(meal),
        "tags": parse_tags(meal.get("strTags")),
        "youtube": meal.get("strYoutube"),
        "source": meal.get("strSource"),
    }


# ── LUNCHBOX → MATCHED MEALDB RECIPE ─────────────────────────────────────────

LUNCHBOX_RECIPE_KEYWORDS = [
    {
        "name": "beef",
        "lunchbox_words": ["beef", "steak", "mince", "meatball", "burger"],
        "mealdb_categories": ["Beef"],
        "ingredients": ["beef"],
        "search_terms": ["beef"],
    },
    {
        "name": "chicken",
        "lunchbox_words": ["chicken", "poultry"],
        "mealdb_categories": ["Chicken"],
        "ingredients": ["chicken"],
        "search_terms": ["chicken"],
    },
    {
        "name": "fish",
        "lunchbox_words": ["fish", "salmon", "tuna", "seafood"],
        "mealdb_categories": ["Seafood"],
        "ingredients": ["salmon", "tuna", "fish"],
        "search_terms": ["fish", "salmon", "tuna"],
    },
    {
        "name": "egg",
        "lunchbox_words": ["egg", "omelette", "frittata"],
        "mealdb_categories": ["Breakfast"],
        "ingredients": ["egg"],
        "search_terms": ["egg"],
    },
    {
        "name": "rice",
        "lunchbox_words": ["rice", "fried rice", "brown rice"],
        "mealdb_categories": ["Chicken", "Beef", "Seafood", "Vegetarian"],
        "ingredients": ["rice"],
        "search_terms": ["rice"],
    },
    {
        "name": "noodle",
        "lunchbox_words": ["noodle", "noodles", "pasta", "spaghetti", "macaroni"],
        "mealdb_categories": ["Pasta"],
        "ingredients": ["pasta", "noodles"],
        "search_terms": ["pasta", "noodle", "spaghetti"],
    },
    {
        "name": "vegetarian",
        "lunchbox_words": ["vegetarian", "vegan", "tofu", "bean", "beans", "lentil", "chickpea"],
        "mealdb_categories": ["Vegetarian", "Vegan", "Side"],
        "ingredients": ["tofu", "beans", "lentils", "chickpea"],
        "search_terms": ["vegetarian", "lentil", "bean"],
    },
]

def _normalise_match_text(value) -> str:
    return str(value or "").lower()


def get_lunchbox_match_text(lunchbox: dict) -> str:
    title = lunchbox.get("title") or ""

    items = lunchbox.get("items") or []
    item_text = " ".join(
        f"{item.get('name', '')} {item.get('section', '')}"
        for item in items
        if isinstance(item, dict)
    )

    focus = lunchbox.get("nutritionFocus") or []
    focus_text = " ".join(focus) if isinstance(focus, list) else str(focus)

    return _normalise_match_text(f"{title} {item_text} {focus_text}")


def detect_lunchbox_keywords(lunchbox: dict) -> list[dict]:
    text = get_lunchbox_match_text(lunchbox)

    matched = []

    for group in LUNCHBOX_RECIPE_KEYWORDS:
        if any(word in text for word in group["lunchbox_words"]):
            matched.append(group)

    return matched


def meal_to_recipe_card(meal: dict, match_reason: str = "") -> dict:
    return {
        "id": meal.get("idMeal"),
        "source": "mealdb",
        "title": meal.get("strMeal") or "Recipe Inspiration",
        "image": meal.get("strMealThumb") or "",
        "category": meal.get("strCategory") or "",
        "area": meal.get("strArea") or "",
        "nutritionFocus": [],
        "whyThisMeal": match_reason or "This recipe was selected to match the lunchbox ingredients.",
    }


def score_meal_against_lunchbox(lunchbox: dict, meal: dict) -> int:
    lunchbox_text = get_lunchbox_match_text(lunchbox)

    meal_text = _normalise_match_text(
        " ".join(
            [
                meal.get("strMeal") or "",
                meal.get("strCategory") or "",
                meal.get("strArea") or "",
                " ".join(
                    [
                        str(meal.get(f"strIngredient{i}") or "")
                        for i in range(1, 21)
                    ]
                ),
            ]
        )
    )

    score = 0

    for group in LUNCHBOX_RECIPE_KEYWORDS:
        lunchbox_has_group = any(word in lunchbox_text for word in group["lunchbox_words"])
        recipe_has_group = (
            any(word in meal_text for word in group["lunchbox_words"])
            or any(word in meal_text for word in group["ingredients"])
            or any(word in meal_text for word in group["search_terms"])
        )

        if lunchbox_has_group and recipe_has_group:
            score += 10

        if lunchbox_has_group and not recipe_has_group:
            score -= 3

    lunchbox_words = [
        word for word in lunchbox_text.split()
        if len(word) >= 4
    ]

    for word in lunchbox_words:
        if word in meal_text:
            score += 1

    return score


async def find_best_recipe_for_lunchbox(
    lunchbox: dict,
    used_recipe_ids: set[str] | None = None,
) -> dict:
    """
    Match one database lunchbox to one MealDB recipe.
    This reduces mismatches like beef lunchbox + noodle recipe.
    """
    if used_recipe_ids is None:
        used_recipe_ids = set()

    keyword_groups = detect_lunchbox_keywords(lunchbox)

    candidate_meals = []

    for group in keyword_groups:
        for ingredient in group["ingredients"]:
            try:
                candidate_meals.extend(await filter_meals_by_ingredient(ingredient))
            except Exception:
                continue

        for category in group["mealdb_categories"]:
            try:
                candidate_meals.extend(await filter_meals_by_category(category))
            except Exception:
                continue

        for term in group["search_terms"]:
            try:
                candidate_meals.extend(await search_meals_by_name(term))
            except Exception:
                continue

    if not candidate_meals:
        try:
            random_meal = await get_random_meal()
            if random_meal:
                return meal_to_recipe_card(
                    random_meal,
                    "Fallback recipe selected because no close ingredient match was found.",
                )
        except Exception:
            pass

        return {
            "id": None,
            "source": "mealdb",
            "title": "Recipe Inspiration",
            "image": "",
            "category": "",
            "area": "",
            "nutritionFocus": [],
            "whyThisMeal": "No matched recipe was available.",
        }

    deduped = {}
    for meal in candidate_meals:
        meal_id = meal.get("idMeal")
        if meal_id:
            deduped[str(meal_id)] = meal

    full_meals = []

    for meal_id, meal in list(deduped.items())[:12]:
        if meal_id in used_recipe_ids:
            continue

        try:
            full = await get_meal_by_id(meal_id)
            if full:
                full_meals.append(full)
        except Exception:
            continue

    if not full_meals:
        for meal_id, meal in list(deduped.items())[:12]:
            try:
                full = await get_meal_by_id(meal_id)
                if full:
                    full_meals.append(full)
            except Exception:
                continue

    if not full_meals:
        fallback = list(deduped.values())[0]
        return meal_to_recipe_card(
            fallback,
            "Fallback recipe selected from MealDB candidates.",
        )

    best_meal = sorted(
        full_meals,
        key=lambda meal: score_meal_against_lunchbox(lunchbox, meal),
        reverse=True,
    )[0]

    matched_keywords = [group["name"] for group in keyword_groups]

    return meal_to_recipe_card(
        best_meal,
        f"Matched with lunchbox ingredients: {', '.join(matched_keywords) or 'general'}."
    )