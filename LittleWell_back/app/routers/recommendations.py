from datetime import date
import random
import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..auth_utils import get_current_user
from .. import models

from ..services.mealdb_service import (
    filter_meals_by_category,
    get_meal_by_id,
    get_random_meal,
    list_categories,
    format_meal_card,
    search_meals_by_name,
)

from ..services.ausnut_service import (
    filter_by_nutrition,
    get_food_by_name_fuzzy,
)


router = APIRouter(prefix="/products/recommended", tags=["recommendations"])


# ---------------------------------------------------------------------------
# Age support: LittleWell only supports children aged 5-12.
# ---------------------------------------------------------------------------

ALLOWED_CHILD_AGE_BANDS = {
    "5-6 years",
    "7-9 years",
    "10-12 years",
}


def validate_supported_age_band(age_band: Optional[str]):
    if age_band not in ALLOWED_CHILD_AGE_BANDS:
        raise HTTPException(
            status_code=400,
            detail=(
                "LittleWell currently supports children aged 5-12 only. "
                "Allowed age bands: 5-6 years, 7-9 years, 10-12 years."
            ),
        )


STATUS_TO_CATEGORY = {
    "iron": ["Chicken", "Lamb", "Seafood", "Beef"],
    "calcium": ["Pasta", "Vegetarian", "Breakfast"],
    "vitamin_d": ["Seafood", "Breakfast"],
    "variety": ["Vegan", "Vegetarian", "Pasta", "Side"],
}


CHILD_AGE_BAND_TO_CATEGORY = {
    "5-6 years": ["Chicken", "Pasta", "Vegetarian", "Breakfast"],
    "7-9 years": ["Chicken", "Pasta", "Vegetarian", "Seafood"],
    "10-12 years": ["Chicken", "Beef", "Seafood", "Pasta"],
}


def get_current_season_name() -> str:
    month = date.today().month

    if month in [9, 10, 11]:
        return "spring"
    if month in [12, 1, 2]:
        return "summer"
    if month in [3, 4, 5]:
        return "autumn"

    return "winter"


def get_needs_support(child) -> list[str]:
    needs = []

    if int(child.iron_status or 0) == 1:
        needs.append("iron")
    if int(child.calcium_status or 0) == 1:
        needs.append("calcium")
    if int(child.vitamin_d_status or 0) == 1:
        needs.append("vitamin_d")
    if int(child.variety_status or 0) == 1:
        needs.append("variety")

    return needs


def focus_labels(needs: list[str]) -> list[str]:
    if not needs:
        return ["Balanced nutrition"]

    return [f"{n.replace('_', ' ').title()} Support" for n in needs]


def get_categories_for_child(child) -> list[str]:
    validate_supported_age_band(child.age_band)

    needs_support = get_needs_support(child)

    if not needs_support:
        return CHILD_AGE_BAND_TO_CATEGORY.get(
            child.age_band,
            ["Chicken", "Pasta", "Vegetarian"],
        )

    categories = []

    for need in needs_support:
        categories.extend(STATUS_TO_CATEGORY.get(need, []))

    deduped = list(dict.fromkeys(categories))

    return deduped or ["Chicken", "Vegetarian"]


def get_child_or_404(db: Session, child_id: int, user_id: int):
    child = (
        db.query(models.UserChild)
        .filter(
            models.UserChild.child_id == child_id,
            models.UserChild.user_id == user_id,
        )
        .first()
    )

    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    return child


def is_valid_product_name(name: Optional[str]) -> bool:
    if not name:
        return False

    cleaned = str(name).strip()

    if len(cleaned) < 3:
        return False

    if cleaned.lower() in {"a", "n/a", "unknown", "test", "none", "null"}:
        return False

    return True


# ---------------------------------------------------------------------------
# Dietary restriction helpers
# ---------------------------------------------------------------------------

def get_child_dietary_restriction(db: Session, child):
    restriction_id = getattr(child, "restriction_id", None)

    if not restriction_id:
        return None

    return (
        db.query(models.DietaryRestriction)
        .filter(models.DietaryRestriction.restriction_id == restriction_id)
        .filter(models.DietaryRestriction.is_active == 1)
        .first()
    )


def apply_dietary_filters_to_reference_food(query, restriction):
    if not restriction:
        return query

    code = (restriction.restriction_code or "").upper()

    if code == "VEGAN":
        query = query.filter(models.ReferenceFood.is_vegan == 1)

    if code == "VEGETARIAN" or int(restriction.excludes_meat or 0) == 1:
        query = query.filter(models.ReferenceFood.is_vegetarian == 1)

    if int(restriction.excludes_gluten or 0) == 1:
        query = query.filter(models.ReferenceFood.is_gluten_free == 1)

    if int(restriction.excludes_dairy or 0) == 1:
        query = query.filter(models.ReferenceFood.is_dairy_free == 1)

    if int(restriction.excludes_egg or 0) == 1:
        query = query.filter(models.ReferenceFood.is_egg_free == 1)

    if int(restriction.excludes_nuts or 0) == 1:
        query = query.filter(models.ReferenceFood.is_nut_free == 1)

    if int(restriction.excludes_pork or 0) == 1:
        query = query.filter(models.ReferenceFood.is_pork_free == 1)

    if code == "HALAL":
        query = query.filter(models.ReferenceFood.is_halal == 1)

    if code == "KOSHER":
        query = query.filter(models.ReferenceFood.is_kosher == 1)

    return query


def get_mealdb_categories_for_restriction(categories: list[str], restriction) -> list[str]:
    if not restriction:
        return categories

    code = (restriction.restriction_code or "").upper()

    if code == "VEGAN":
        return ["Vegan", "Vegetarian", "Side"]

    if code == "VEGETARIAN" or int(restriction.excludes_meat or 0) == 1:
        return ["Vegetarian", "Vegan", "Pasta", "Side"]

    filtered = categories[:]

    if int(restriction.excludes_pork or 0) == 1:
        filtered = [category for category in filtered if category != "Pork"]

    if int(restriction.excludes_shellfish or 0) == 1:
        filtered = [category for category in filtered if category != "Seafood"]

    return filtered or ["Chicken", "Vegetarian", "Pasta"]


# ---------------------------------------------------------------------------
# Reference food recommendation logic
# ---------------------------------------------------------------------------

def get_candidate_reference_foods(db: Session, restriction=None) -> list:
    query = db.query(models.ReferenceFood)
    query = query.filter(models.ReferenceFood.food_name.isnot(None))
    query = apply_dietary_filters_to_reference_food(query, restriction)

    foods = query.limit(800).all()

    return [
        food for food in foods
        if is_valid_product_name(food.food_name)
    ]


def reference_food_text(food) -> str:
    parts = [
        food.food_name or "",
        food.adg_group_code or "",
    ]

    return " ".join(parts).lower()


def score_reference_food_for_slot(food, slot: str, needs: list[str]) -> int:
    text = reference_food_text(food)
    score = 0

    if slot == "protein":
        keywords = [
            "chicken", "beef", "lamb", "fish", "salmon", "tuna",
            "egg", "tofu", "bean", "beans", "lentil", "lentils",
            "chickpea", "yoghurt", "yogurt", "milk", "cheese",
        ]
        if any(k in text for k in keywords):
            score += 8

    elif slot == "carbs":
        keywords = [
            "bread", "rice", "oat", "oats", "cracker", "cereal",
            "wrap", "pasta", "grain", "noodle", "noodles",
            "potato", "sweet potato",
        ]
        if any(k in text for k in keywords):
            score += 8

    elif slot == "fruit":
        keywords = [
            "apple", "banana", "pear", "orange", "mandarin",
            "berry", "berries", "grape", "melon", "kiwi",
            "peach", "plum",
        ]
        if any(k in text for k in keywords):
            score += 8

    elif slot == "veggies":
        keywords = [
            "carrot", "cucumber", "broccoli", "lettuce", "tomato",
            "spinach", "corn", "pea", "peas", "capsicum",
            "zucchini", "pumpkin", "celery",
        ]
        if any(k in text for k in keywords):
            score += 8

    if "iron" in needs:
        iron_keywords = [
            "beef", "lamb", "chicken", "lentil", "lentils",
            "bean", "beans", "spinach", "chickpea",
        ]
        if any(k in text for k in iron_keywords):
            score += 4

    if "calcium" in needs:
        calcium_keywords = [
            "milk", "cheese", "yoghurt", "yogurt", "tofu",
        ]
        if any(k in text for k in calcium_keywords):
            score += 4

    if "vitamin_d" in needs:
        vitamin_d_keywords = [
            "fish", "salmon", "tuna", "egg", "milk",
        ]
        if any(k in text for k in vitamin_d_keywords):
            score += 3

    if "variety" in needs:
        score += random.randint(0, 2)

    return score


def get_randomised_reference_candidates(
    foods: list,
    slot: str,
    needs: list[str],
    top_n: int = 50,
) -> list:
    ranked = sorted(
        foods,
        key=lambda food: score_reference_food_for_slot(food, slot, needs),
        reverse=True,
    )

    shortlisted = ranked[:top_n]
    random.shuffle(shortlisted)

    return shortlisted


def pick_next_unused_reference(candidates: list, used_ids: set[int]):
    for food in candidates:
        food_id = int(food.reference_food_id)

        if food_id not in used_ids:
            used_ids.add(food_id)
            return food

    return None


def make_reference_food_item(food, section: str):
    return {
        "reference_food_id": food.reference_food_id,
        "name": food.food_name,
        "amount": "1 child-friendly portion",
        "image": None,
        "section": section,
    }


def build_reference_lunchbox(
    child_name: Optional[str],
    lunchbox_id: str,
    index: int,
    protein_food,
    carb_food,
    fruit_food,
    veg_food,
    needs: list[str],
    restriction=None,
):
    support_type = needs[0] if needs else "general"

    items = []

    if protein_food:
        items.append(make_reference_food_item(protein_food, "protein"))

    if carb_food:
        items.append(make_reference_food_item(carb_food, "carbs"))

    if fruit_food:
        items.append(make_reference_food_item(fruit_food, "fruit"))

    if veg_food:
        items.append(make_reference_food_item(veg_food, "veggies"))

    restriction_label = (
        restriction.restriction_name
        if restriction
        else "the child’s selected needs"
    )

    return {
        "id": f"ref-{lunchbox_id}",
        "reference_food_id": protein_food.reference_food_id if protein_food else None,
        "source": "reference_food",
        "title": f"Lunchbox Option {index}",
        "heroImage": None,
        "childName": child_name,
        "items": items,
        "nutritionFocus": focus_labels(needs),
        "whyThisMeal": (
            f"This lunchbox uses reference food items filtered by {restriction_label}, "
            "allergy records, and the child’s nutrition support needs."
        ),
        "supportType": support_type,
    }


def get_child_allergen_ids(db: Session, child_id: int, user_id: Optional[int] = None) -> list[int]:
    query = (
        db.query(models.UserSearchAllergen)
        .filter(models.UserSearchAllergen.child_id == child_id)
    )

    if user_id is not None:
        query = query.filter(models.UserSearchAllergen.user_id == user_id)

    rows = query.all()

    return [int(row.allergen_id) for row in rows]


def get_blocked_reference_food_ids_by_allergens(
    db: Session,
    allergen_ids: list[int],
) -> set[int]:
    if not allergen_ids:
        return set()

    rows = (
        db.query(models.ReferenceAllergen)
        .filter(models.ReferenceAllergen.allergen_id.in_(allergen_ids))
        .all()
    )

    return {int(row.reference_food_id) for row in rows}


def remove_blocked_reference_foods(
    foods: list,
    blocked_reference_food_ids: set[int],
) -> list:
    if not blocked_reference_food_ids:
        return foods

    return [
        food for food in foods
        if int(food.reference_food_id) not in blocked_reference_food_ids
    ]


def generate_lunchboxes_for_child(
    db: Session,
    child,
    seasonal: bool = True,
    max_boxes: int = 3,
    user_id: Optional[int] = None,
):
    validate_supported_age_band(child.age_band)

    needs = get_needs_support(child)
    restriction = get_child_dietary_restriction(db, child)

    allergen_ids = get_child_allergen_ids(
        db=db,
        child_id=child.child_id,
        user_id=user_id,
    )

    blocked_reference_food_ids = get_blocked_reference_food_ids_by_allergens(
        db=db,
        allergen_ids=allergen_ids,
    )

    foods = get_candidate_reference_foods(
        db=db,
        restriction=restriction,
    )

    foods = remove_blocked_reference_foods(
        foods=foods,
        blocked_reference_food_ids=blocked_reference_food_ids,
    )

    protein_candidates = get_randomised_reference_candidates(foods, "protein", needs)
    carb_candidates = get_randomised_reference_candidates(foods, "carbs", needs)
    fruit_candidates = get_randomised_reference_candidates(foods, "fruit", needs)
    veg_candidates = get_randomised_reference_candidates(foods, "veggies", needs)

    lunchboxes = []
    used_ids = set()

    for i in range(max_boxes):
        protein_food = pick_next_unused_reference(protein_candidates, used_ids)
        carb_food = pick_next_unused_reference(carb_candidates, used_ids)
        fruit_food = pick_next_unused_reference(fruit_candidates, used_ids)
        veg_food = pick_next_unused_reference(veg_candidates, used_ids)

        if not any([protein_food, carb_food, fruit_food, veg_food]):
            break

        lunchboxes.append(
            build_reference_lunchbox(
                child_name=child.child_name,
                lunchbox_id=f"{child.child_id}-box-{i + 1}",
                index=i + 1,
                protein_food=protein_food,
                carb_food=carb_food,
                fruit_food=fruit_food,
                veg_food=veg_food,
                needs=needs,
                restriction=restriction,
            )
        )

    return {
        "needsSupport": needs,
        "restriction": {
            "restriction_id": restriction.restriction_id,
            "restriction_code": restriction.restriction_code,
            "restriction_name": restriction.restriction_name,
        } if restriction else None,
        "lunchboxes": lunchboxes,
    }


# ---------------------------------------------------------------------------
# MealDB + AUSNUT logic
# ---------------------------------------------------------------------------

def get_nutrition_labels(nutrients: dict) -> list[str]:
    labels = []

    if nutrients.get("iron_mg", 0) >= 2.5:
        labels.append("High Iron")
    if nutrients.get("calcium_mg", 0) >= 120:
        labels.append("High Calcium")
    if nutrients.get("sugar_g", 0) <= 5:
        labels.append("Low Sugar")
    if nutrients.get("protein_g", 0) >= 10:
        labels.append("High Protein")
    if nutrients.get("fibre_g", 0) >= 3:
        labels.append("Good Source of Fibre")
    if nutrients.get("vitamin_c_mg", 0) >= 7:
        labels.append("Contains Vitamin C")

    return labels


def dedupe_meals_by_id(meals: list[dict]) -> list[dict]:
    seen = set()
    unique_meals = []

    for meal in meals:
        meal_id = meal.get("idMeal")

        if meal_id and meal_id not in seen:
            seen.add(meal_id)
            unique_meals.append(meal)

    return unique_meals


async def fetch_full_meals_from_categories(
    categories: list[str],
    category_limit: int = 3,
    per_category_limit: int = 8,
    final_limit: int = 6,
) -> list[dict]:
    if not categories:
        return []

    shuffled_categories = categories[:]
    random.shuffle(shuffled_categories)
    selected_categories = shuffled_categories[:category_limit]

    category_results = await asyncio.gather(
        *[filter_meals_by_category(cat) for cat in selected_categories],
        return_exceptions=True,
    )

    raw_meals = []

    for result in category_results:
        if isinstance(result, list):
            meals = result[:]
            random.shuffle(meals)
            raw_meals.extend(meals[:per_category_limit])

    if not raw_meals:
        return []

    raw_meals = dedupe_meals_by_id(raw_meals)
    random.shuffle(raw_meals)

    selected_meals = raw_meals[:final_limit]

    full_meals = await asyncio.gather(
        *[
            get_meal_by_id(m["idMeal"])
            for m in selected_meals
            if m.get("idMeal")
        ],
        return_exceptions=True,
    )

    final_meals = [m for m in full_meals if isinstance(m, dict)]
    random.shuffle(final_meals)

    return final_meals


async def build_lunchbox_from_meal(
    meal,
    child_name: Optional[str] = None,
    support_type: str = "general",
    nutrition_focus: Optional[list[str]] = None,
):
    if nutrition_focus is None:
        nutrition_focus = ["Balanced nutrition"]

    card = format_meal_card(meal)

    nutrition_labels = []
    ausnut_nutrition = None

    candidate_ingredients = [
        ing["ingredient"]
        for ing in card.get("ingredients", [])[:3]
    ]

    for ingredient in candidate_ingredients:
        try:
            result = get_food_by_name_fuzzy(ingredient)

            if result:
                ausnut_nutrition = result
                nutrition_labels = get_nutrition_labels(result)
                break

        except FileNotFoundError:
            ausnut_nutrition = None
            nutrition_labels = []
            break

        except Exception:
            continue

    items = []

    for ing in card.get("ingredients", [])[:4]:
        items.append({
            "name": ing["ingredient"],
            "amount": ing["measure"],
            "image": ing.get("image"),
            "section": "ingredient",
        })

    merged_focus = list(dict.fromkeys(nutrition_focus + nutrition_labels))

    return {
        "id": card["id"],
        "source": "mealdb",
        "title": card.get("name", "Meal Recommendation"),
        "heroImage": card.get("image"),
        "childName": child_name,
        "mealName": card.get("name"),
        "mealImage": card.get("image"),
        "category": card.get("category"),
        "area": card.get("area"),
        "items": items,
        "nutritionFocus": merged_focus,
        "whyThisMeal": (
            f"{card.get('name', 'This meal')} provides "
            f"{', '.join(nutrition_focus).lower()} and is suitable for children’s lunchboxes."
        ),
        "supportType": support_type,
        "instructions": card.get("instructions"),
        "tags": card.get("tags"),
        "ausnutData": ausnut_nutrition,
    }


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

@router.get("")
def get_recommended_products(
    child_id: int,
    seasonal: bool = True,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    child = get_child_or_404(
        db=db,
        child_id=child_id,
        user_id=current_user.user_id,
    )

    validate_supported_age_band(child.age_band)

    return generate_lunchboxes_for_child(
        db=db,
        child=child,
        seasonal=seasonal,
        max_boxes=3,
        user_id=current_user.user_id,
    )


@router.get("/family")
def get_family_recommended_products(
    child_ids: str = Query(...),
    seasonal: bool = True,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    ids = [int(x) for x in child_ids.split(",") if x.strip()]

    children = (
        db.query(models.UserChild)
        .filter(
            models.UserChild.child_id.in_(ids),
            models.UserChild.user_id == current_user.user_id,
        )
        .all()
    )

    found_ids = {child.child_id for child in children}
    missing_ids = [child_id for child_id in ids if child_id not in found_ids]

    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Child profile(s) not found or not owned by this user: {missing_ids}",
        )

    if not children:
        raise HTTPException(status_code=404, detail="No children found")

    for child in children:
        validate_supported_age_band(child.age_band)

    class FamilyChild:
        pass

    family = FamilyChild()
    family.child_id = children[0].child_id
    family.child_name = " + ".join([c.child_name for c in children])
    family.age_band = children[0].age_band if children else None

    family.iron_status = 1 if any(int(c.iron_status or 0) == 1 for c in children) else 0
    family.calcium_status = 1 if any(int(c.calcium_status or 0) == 1 for c in children) else 0
    family.vitamin_d_status = 1 if any(int(c.vitamin_d_status or 0) == 1 for c in children) else 0
    family.variety_status = 1 if any(int(c.variety_status or 0) == 1 for c in children) else 0

    family.restriction_id = children[0].restriction_id if children else None

    return generate_lunchboxes_for_child(
        db=db,
        child=family,
        seasonal=seasonal,
        max_boxes=3,
        user_id=current_user.user_id,
    )


@router.get("/quick")
def get_quick_recommended_products(
    ageGroup: str,
    allergies: str = "",
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    validate_supported_age_band(ageGroup)

    class QuickChild:
        pass

    quick = QuickChild()
    quick.child_id = 0
    quick.child_name = None
    quick.age_band = ageGroup
    quick.iron_status = 0
    quick.calcium_status = 0
    quick.vitamin_d_status = 0
    quick.variety_status = 0
    quick.restriction_id = None

    result = generate_lunchboxes_for_child(
        db=db,
        child=quick,
        seasonal=seasonal,
        max_boxes=3,
        user_id=None,
    )

    result["quickInput"] = {
        "ageGroup": ageGroup,
        "allergies": [
            a.strip()
            for a in allergies.split(",")
            if a.strip()
        ],
        "seasonal": seasonal,
    }

    return result


@router.get("/meals/search")
async def search_meals(q: str = Query(...), limit: int = Query(10, ge=1, le=50)):
    try:
        meals = await search_meals_by_name(q)

        full_meals = await asyncio.gather(
            *[
                get_meal_by_id(m["idMeal"])
                for m in meals[:limit]
                if m.get("idMeal")
            ],
            return_exceptions=True,
        )

        return {
            "meals": [
                format_meal_card(m)
                for m in full_meals
                if isinstance(m, dict)
            ],
            "total": len([m for m in full_meals if isinstance(m, dict)]),
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search meals: {e}")


@router.get("/meals/random")
async def random_meal():
    try:
        meal = await get_random_meal()

        if not meal:
            raise HTTPException(status_code=404, detail="No meal found")

        return format_meal_card(meal)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch random meal: {e}")


@router.get("/meals/categories")
async def meal_categories():
    try:
        return {"categories": await list_categories()}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch meal categories: {e}")


@router.get("/mealdb/recommend")
async def get_general_meal_recommendations(
    category: Optional[str] = None,
    child_age: Optional[int] = None,
    limit: int = Query(6, ge=1, le=12),
):
    try:
        search_terms = ["chicken", "pasta", "vegetable", "rice", "fish", "egg"]

        if category:
            full_meals = await fetch_full_meals_from_categories(
                categories=[category],
                category_limit=1,
                per_category_limit=max(limit * 2, 6),
                final_limit=limit,
            )
            recommendations = [format_meal_card(m) for m in full_meals]

        else:
            term = random.choice(search_terms)
            meals = await search_meals_by_name(term)
            random.shuffle(meals)
            selected = meals[:limit]
            recommendations = [
                format_meal_card(m)
                for m in selected
                if isinstance(m, dict)
            ]

        return {
            "recommendations": recommendations,
            "total": len(recommendations),
            "filters_applied": {
                "category": category,
                "child_age": child_age,
            },
            "data_sources": ["TheMealDB"],
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate meal recommendations: {e}")


@router.get("/nutrition/filter")
async def nutrition_filter(
    high_iron: bool = Query(False),
    high_calcium: bool = Query(False),
    low_sugar: bool = Query(False),
    high_protein: bool = Query(False),
    high_fibre: bool = Query(False),
    limit: int = Query(20, ge=1, le=100),
):
    try:
        foods = filter_by_nutrition(
            high_iron=high_iron,
            high_calcium=high_calcium,
            low_sugar=low_sugar,
            high_protein=high_protein,
            high_fibre=high_fibre,
            limit=limit,
        )

        for food in foods:
            food["labels"] = get_nutrition_labels(food)

        return {
            "foods": foods,
            "total": len(foods),
            "data_source": "AUSNUT 2011-13 (FSANZ, CC BY 4.0)",
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to filter nutrition data: {e}")


@router.get("/mealdb/child")
async def get_child_meal_recommendations(
    child_id: int,
    limit: int = Query(6, ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        child = get_child_or_404(
            db=db,
            child_id=child_id,
            user_id=current_user.user_id,
        )

        validate_supported_age_band(child.age_band)

        needs_support = get_needs_support(child)
        restriction = get_child_dietary_restriction(db, child)

        categories = get_categories_for_child(child)
        categories = get_mealdb_categories_for_restriction(categories, restriction)

        full_meals = await fetch_full_meals_from_categories(
            categories=categories,
            category_limit=min(3, len(categories)),
            per_category_limit=max(limit * 2, 6),
            final_limit=limit,
        )

        nutrition_focus = focus_labels(needs_support)
        support_type = needs_support[0] if needs_support else "general"

        lunchboxes = []

        for meal in full_meals:
            card = await build_lunchbox_from_meal(
                meal=meal,
                child_name=child.child_name,
                support_type=support_type,
                nutrition_focus=nutrition_focus,
            )
            lunchboxes.append(card)

        return {
            "needsSupport": needs_support,
            "restriction": {
                "restriction_id": restriction.restriction_id,
                "restriction_code": restriction.restriction_code,
                "restriction_name": restriction.restriction_name,
            } if restriction else None,
            "lunchboxes": lunchboxes,
            "child": {
                "name": child.child_name,
                "age_band": child.age_band,
                "restriction_id": child.restriction_id,
            },
            "dataSource": "TheMealDB + AUSNUT 2011-13 FSANZ",
            "targetAgeRange": "5-12 years",
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate child meal recommendations: {e}",
        )


@router.get("/health")
async def api_health():
    return {
        "status": "ok",
        "services": {
            "mealdb": "TheMealDB",
            "ausnut": "AUSNUT",
            "backend": "FastAPI + SQLAlchemy + MySQL",
        },
        "targetAgeRange": "5-12 years",
        "allowedAgeBands": [
            "5-6 years",
            "7-9 years",
            "10-12 years",
        ],
    }


@router.get("/mealdb/recipe/{meal_id}")
async def get_meal_recipe_detail(
    meal_id: str,
    child_name: Optional[str] = None,
):
    try:
        meal = await get_meal_by_id(meal_id)

        if not meal:
            raise HTTPException(status_code=404, detail="Recipe not found")

        card = await build_lunchbox_from_meal(
            meal=meal,
            child_name=child_name,
            support_type="general",
            nutrition_focus=["Balanced nutrition"],
        )

        return card

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load recipe detail: {e}")