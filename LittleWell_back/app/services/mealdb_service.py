"""
TheMealDB API Service — LittleWell
Fetches meal recipes, images, and ingredient data.
Free, unlimited, no API key required for educational use.
API key "1" is the public test key.
"""
import httpx
from typing import Optional

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
               Pasta, Pork, Seafood, Side, Starter, Vegan, Vegetarian, Breakfast, Goat
    Returns: list with idMeal, strMeal, strMealThumb (image URL)
    """
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/filter.php", params={"c": category})
        r.raise_for_status()
        data = r.json()
        return data.get("meals") or []


async def filter_meals_by_ingredient(ingredient: str) -> list[dict]:
    """Filter meals by main ingredient e.g. 'chicken', 'salmon', 'lentils'."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/filter.php", params={"i": ingredient})
        r.raise_for_status()
        data = r.json()
        return data.get("meals") or []


async def get_meal_by_id(meal_id: str) -> Optional[dict]:
    """Get full meal details including ingredients, instructions, image."""
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
    This parses them into a clean list.
    """
    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}", "").strip()
        measure    = meal.get(f"strMeasure{i}", "").strip()
        if ingredient:
            ingredients.append({
                "ingredient": ingredient,
                "measure":    measure,
                # Ingredient thumbnail image from TheMealDB
                "image": f"https://www.themealdb.com/images/ingredients/{ingredient}-Small.png"
            })
    return ingredients


def format_meal_card(meal: dict) -> dict:
    """
    Returns a clean meal card dict ready to send to the Vue frontend.
    Compatible with LittleWell's meal browse page card component.
    """
    return {
        "id":           meal.get("idMeal"),
        "name":         meal.get("strMeal"),
        "category":     meal.get("strCategory"),
        "area":         meal.get("strArea"),
        "image":        meal.get("strMealThumb"),
        "thumbnail":    meal.get("strMealThumb") + "/preview" if meal.get("strMealThumb") else None,
        "instructions": meal.get("strInstructions"),
        "ingredients":  parse_ingredients(meal) if "strIngredient1" in meal else [],
        "tags":         meal.get("strTags", "").split(",") if meal.get("strTags") else [],
        "youtube":      meal.get("strYoutube"),
        "source":       meal.get("strSource"),
    }
