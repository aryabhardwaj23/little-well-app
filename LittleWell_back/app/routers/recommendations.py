from datetime import date
import random
import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..db import get_db
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
    get_food_by_name,
)

router = APIRouter(prefix="/products/recommended", tags=["recommendations"])


# Config / mappings

STATUS_TO_CATEGORY = {
    "iron": ["Chicken", "Lamb", "Seafood", "Beef"],
    "calcium": ["Pasta", "Vegetarian", "Breakfast"],
    "vitamin_d": ["Seafood", "Breakfast"],
    "variety": ["Vegan", "Vegetarian", "Pasta", "Side"],
}

CHILD_AGE_BAND_TO_CATEGORY = {
    "0-3 years": ["Breakfast", "Vegetarian", "Pasta"],
    "3-6 years": ["Chicken", "Pasta", "Vegetarian", "Seafood"],
    "6-9 years": ["Chicken", "Beef", "Seafood", "Pasta"],
    "9-12 years": ["Beef", "Chicken", "Seafood", "Lamb"],
    "12+ years": ["Beef", "Chicken", "Seafood", "Lamb"],
    # Backward compatibility
    "2-3": ["Breakfast", "Vegetarian", "Pasta"],
    "4-8": ["Chicken", "Pasta", "Vegetarian", "Seafood"],
    "9-13": ["Chicken", "Beef", "Seafood", "Pasta"],
    "14-18": ["Beef", "Chicken", "Seafood", "Lamb"],
}


# Core helpers

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


def product_text(product) -> str:
    parts = [
        product.name or "",
        product.brand or "",
        product.category or "",
        product.ingredients_list or "",
    ]
    return " ".join(parts).lower()


def is_valid_product_name(name: Optional[str]) -> bool:
    if not name:
        return False
    cleaned = name.strip()
    if len(cleaned) < 3:
        return False
    if cleaned.lower() in {"a", "n/a", "unknown", "test"}:
        return False
    return True


def score_product_for_slot(product, slot: str, needs: list[str]) -> int:
    text = product_text(product)
    score = 0

    # General quality
    if int(product.has_added_preservatives or 0) == 0:
        score += 1
    if int(product.has_added_sugar or 0) == 0:
        score += 1
    if int(product.has_food_color or 0) == 0:
        score += 1

    # Slot heuristics
    if slot == "protein":
        keywords = [
            "protein", "peanut butter", "nut butter", "tofu", "beans",
            "lentil", "chickpea", "yogurt", "milk", "cheese", "egg"
        ]
        if any(k in text for k in keywords):
            score += 6

    elif slot == "carbs":
        keywords = [
            "bread", "rice", "oat", "cracker", "cereal", "wrap",
            "pasta", "grain", "wholegrain", "whole grain"
        ]
        if any(k in text for k in keywords):
            score += 6

    # Nutrition support
    if "iron" in needs:
        iron_keywords = ["iron", "protein", "beans", "lentil", "chickpea", "peanut butter"]
        if any(k in text for k in iron_keywords):
            score += 3

    if "calcium" in needs:
        calcium_keywords = ["calcium", "milk", "cheese", "yogurt"]
        if any(k in text for k in calcium_keywords):
            score += 3

    if "vitamin_d" in needs:
        vitamin_d_keywords = ["vitamin d", "fortified", "milk", "egg"]
        if any(k in text for k in vitamin_d_keywords):
            score += 2

    if "variety" in needs:
        if int(product.has_added_preservatives or 0) == 0:
            score += 2
        if int(product.has_food_color or 0) == 0:
            score += 2

    return score


def get_child_allergen_ids(db: Session, child_id: int) -> list[int]:
    rows = (
        db.query(models.UserSearchAllergen)
        .filter(models.UserSearchAllergen.child_id == child_id)
        .all()
    )
    return [int(row.allergen_id) for row in rows]


def get_blocked_product_ids_by_allergens(db: Session, allergen_ids: list[int]) -> set[int]:
    if not allergen_ids:
        return set()

    rows = (
        db.query(models.ProductAllergen)
        .filter(models.ProductAllergen.allergen_id.in_(allergen_ids))
        .all()
    )
    return {int(row.product_id) for row in rows}


def get_candidate_products(db: Session, blocked_product_ids: set[int]) -> list:
    query = db.query(models.PackagedProduct)

    if blocked_product_ids:
        query = query.filter(~models.PackagedProduct.product_id.in_(blocked_product_ids))

    products = query.limit(300).all()

    cleaned = []
    for p in products:
        if not is_valid_product_name(p.name):
            continue
        cleaned.append(p)

    return cleaned


def get_seasonal_items(db: Session, seasonal: bool = True):
    current_season = get_current_season_name()
    query = db.query(models.SeasonalProduce)

    if seasonal:
        season_row = (
            db.query(models.Season)
            .filter(func.lower(models.Season.season) == current_season)
            .first()
        )
        if season_row:
            query = query.filter(models.SeasonalProduce.season_id == season_row.season_id)

    rows = query.limit(200).all()

    fruits = []
    veggies = []

    for row in rows:
        ptype = (row.produce_type or "").lower()
        name = row.produce_name or ""

        if not is_valid_product_name(name):
            continue

        if "fruit" in ptype:
            fruits.append(name)
        elif "veg" in ptype or "vegetable" in ptype:
            veggies.append(name)

    return fruits, veggies


def fallback_fruits():
    return ["Gala Apple", "Banana", "Pear", "Mandarin"]


def fallback_veggies():
    return ["Carrot Sticks", "Cucumber", "Buk Choy", "Baby Broccoli"]


def make_item(name: str, amount: str, section: str, image: Optional[str] = None):
    return {
        "name": name,
        "amount": amount,
        "image": image,  # no placeholder; frontend decides whether to render
        "section": section,
    }


def build_lunchbox(
    child_name: Optional[str],
    lunchbox_id: str,
    index: int,
    protein_product,
    carb_product,
    fruit_name: str,
    veg_name: str,
    needs: list[str],
):
    support_type = needs[0] if needs else "general"

    items = []

    if protein_product:
        items.append(
            make_item(
                name=protein_product.name,
                amount=protein_product.serving_size or "1 serving",
                section="protein",
                image=None,
            )
        )

    if carb_product:
        items.append(
            make_item(
                name=carb_product.name,
                amount=carb_product.serving_size or "1 serving",
                section="carbs",
                image=None,
            )
        )

    items.append(make_item(name=fruit_name, amount="1 serving", section="fruit", image=None))
    items.append(make_item(name=veg_name, amount="1 serving", section="veggies", image=None))

    return {
        "id": lunchbox_id,
        "source": "database",
        "title": f"Lunchbox Option {index}",
        "heroImage": None,
        "childName": child_name,
        "items": items,
        "nutritionFocus": focus_labels(needs),
        "whyThisMeal": "This lunchbox combines a protein item, a carbohydrate item, and seasonal fruit and vegetables filtered by the child's needs.",
        "supportType": support_type,
    }


def get_randomised_candidates(products: list, slot: str, needs: list[str], top_n: int = 20) -> list:
    ranked = sorted(
        products,
        key=lambda p: score_product_for_slot(p, slot, needs),
        reverse=True,
    )
    shortlisted = ranked[:top_n]
    random.shuffle(shortlisted)
    return shortlisted


def pick_next_unused(candidates: list, used_ids: set[int]):
    for p in candidates:
        pid = int(p.product_id)
        if pid not in used_ids:
            used_ids.add(pid)
            return p
    return None


def generate_lunchboxes_for_child(db: Session, child, seasonal: bool = True, max_boxes: int = 3):
    needs = get_needs_support(child)
    allergen_ids = get_child_allergen_ids(db, child.child_id)
    blocked_product_ids = get_blocked_product_ids_by_allergens(db, allergen_ids)

    products = get_candidate_products(db, blocked_product_ids)
    fruits, veggies = get_seasonal_items(db, seasonal=seasonal)

    if not fruits:
        fruits = fallback_fruits()
    if not veggies:
        veggies = fallback_veggies()

    lunchboxes = []
    used_ids = set()

    protein_candidates = get_randomised_candidates(products, "protein", needs, top_n=20)
    carb_candidates = get_randomised_candidates(products, "carbs", needs, top_n=20)

    for i in range(max_boxes):
        protein_product = pick_next_unused(protein_candidates, used_ids)
        carb_product = pick_next_unused(carb_candidates, used_ids)

        if not protein_product and not carb_product:
            break

        fruit_name = random.choice(fruits)
        veg_name = random.choice(veggies)

        lunchboxes.append(
            build_lunchbox(
                child_name=child.child_name,
                lunchbox_id=f"{child.child_id}-box-{i + 1}",
                index=i + 1,
                protein_product=protein_product,
                carb_product=carb_product,
                fruit_name=fruit_name,
                veg_name=veg_name,
                needs=needs,
            )
        )

    return {
        "needsSupport": needs,
        "lunchboxes": lunchboxes,
    }


# MealDB + AUSNUT helpers

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


async def build_lunchbox_from_meal(meal, child_name=None, support_type="general", nutrition_focus=None):
    if nutrition_focus is None:
        nutrition_focus = ["Balanced nutrition"]

    card = format_meal_card(meal)

    nutrition_labels = []
    ausnut_nutrition = None

    if card.get("ingredients"):
        main_ingredient = card["ingredients"][0]["ingredient"]
        ausnut_nutrition = get_food_by_name(main_ingredient)
        if ausnut_nutrition:
            nutrition_labels = get_nutrition_labels(ausnut_nutrition)

    items = []
    for ing in card.get("ingredients", [])[:4]:
        items.append({
            "name": ing["ingredient"],
            "amount": ing["measure"],
            "image": ing.get("image"),
            "section": "ingredient",
        })

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
        "nutritionFocus": nutrition_focus + nutrition_labels,
        "whyThisMeal": f"{card.get('name', 'This meal')} provides {', '.join(nutrition_focus).lower()} and is suitable for children's lunchboxes.",
        "supportType": support_type,
        "instructions": card.get("instructions"),
        "tags": card.get("tags"),
        "ausnutData": ausnut_nutrition,
    }


# Main database routes

@router.get("")
def get_recommended_products(
    child_id: int,
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    child = db.query(models.UserChild).filter(models.UserChild.child_id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    return generate_lunchboxes_for_child(
        db=db,
        child=child,
        seasonal=seasonal,
        max_boxes=3,
    )


@router.get("/family")
def get_family_recommended_products(
    child_ids: str = Query(...),
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    ids = [int(x) for x in child_ids.split(",") if x.strip()]
    children = db.query(models.UserChild).filter(models.UserChild.child_id.in_(ids)).all()

    if not children:
        raise HTTPException(status_code=404, detail="No children found")

    class FamilyChild:
        pass

    family = FamilyChild()
    family.child_id = ids[0]
    family.child_name = " + ".join([c.child_name for c in children])
    family.iron_status = 1 if any(int(c.iron_status or 0) == 1 for c in children) else 0
    family.calcium_status = 1 if any(int(c.calcium_status or 0) == 1 for c in children) else 0
    family.vitamin_d_status = 1 if any(int(c.vitamin_d_status or 0) == 1 for c in children) else 0
    family.variety_status = 1 if any(int(c.variety_status or 0) == 1 for c in children) else 0

    return generate_lunchboxes_for_child(
        db=db,
        child=family,
        seasonal=seasonal,
        max_boxes=3,
    )


@router.get("/quick")
def get_quick_recommended_products(
    ageGroup: str,
    allergies: str = "",
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    allergy_list = [a.strip() for a in allergies.split(",") if a.strip()]

    fruits, veggies = get_seasonal_items(db, seasonal=seasonal)
    if not fruits:
        fruits = fallback_fruits()
    if not veggies:
        veggies = fallback_veggies()

    products = get_candidate_products(db, blocked_product_ids=set())

    protein_candidates = get_randomised_candidates(products, "protein", [], top_n=20)
    carb_candidates = get_randomised_candidates(products, "carbs", [], top_n=20)

    lunchboxes = []
    used_ids = set()

    for i in range(3):
        protein_product = pick_next_unused(protein_candidates, used_ids)
        carb_product = pick_next_unused(carb_candidates, used_ids)

        if not protein_product and not carb_product:
            break

        fruit_name = random.choice(fruits)
        veg_name = random.choice(veggies)

        lunchboxes.append(
            build_lunchbox(
                child_name=None,
                lunchbox_id=f"quick-box-{i + 1}",
                index=i + 1,
                protein_product=protein_product,
                carb_product=carb_product,
                fruit_name=fruit_name,
                veg_name=veg_name,
                needs=[],
            )
        )

    return {
        "needsSupport": [],
        "lunchboxes": lunchboxes,
        "quickInput": {
            "ageGroup": ageGroup,
            "allergies": allergy_list,
            "seasonal": seasonal,
        },
    }


# MealDB + AUSNUT enhancement routes

@router.get("/meals/search")
async def search_meals(q: str = Query(...), limit: int = Query(10, ge=1, le=50)):
    try:
        meals = await search_meals_by_name(q)
        full_meals = await asyncio.gather(
            *[get_meal_by_id(m["idMeal"]) for m in meals[:limit]],
            return_exceptions=True,
        )
        return {"meals": [format_meal_card(m) for m in full_meals if isinstance(m, dict)]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meals/random")
async def random_meal():
    try:
        meal = await get_random_meal()
        if not meal:
            raise HTTPException(status_code=404, detail="No meal found")
        return format_meal_card(meal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meals/categories")
async def meal_categories():
    try:
        return {"categories": await list_categories()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mealdb/child")
async def get_child_meal_recommendations(
    child_id: int,
    db: Session = Depends(get_db),
):
    """
    Enhancement endpoint:
    returns recipe-style lunchbox suggestions using MealDB + AUSNUT.
    Does not replace the main database-driven /products/recommended endpoint.
    """
    child = db.query(models.UserChild).filter(models.UserChild.child_id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    needs_support = get_needs_support(child)

    if needs_support:
        categories = STATUS_TO_CATEGORY.get(needs_support[0], ["Chicken", "Vegetarian"])
    else:
        categories = CHILD_AGE_BAND_TO_CATEGORY.get(child.age_band, ["Chicken", "Pasta", "Vegetarian"])

    all_meals = []
    for cat in categories[:2]:
        meals = await filter_meals_by_category(cat)
        all_meals.extend(meals[:3])

    meal_ids = [m["idMeal"] for m in all_meals[:6]]
    full_meals = await asyncio.gather(
        *[get_meal_by_id(mid) for mid in meal_ids],
        return_exceptions=True,
    )

    nutrition_focus = focus_labels(needs_support)

    lunchboxes = []
    for meal in full_meals:
        if not isinstance(meal, dict):
            continue

        card = await build_lunchbox_from_meal(
            meal=meal,
            child_name=child.child_name,
            support_type=needs_support[0] if needs_support else "general",
            nutrition_focus=nutrition_focus,
        )
        lunchboxes.append(card)

    return {
        "needsSupport": needs_support,
        "lunchboxes": lunchboxes,
        "child": {"name": child.child_name, "age_band": child.age_band},
        "dataSource": "TheMealDB + AUSNUT 2011-13 FSANZ",
    }


@router.get("/health")
async def api_health():
    return {
        "status": "ok",
        "services": {
            "mealdb": "TheMealDB",
            "ausnut": "AUSNUT",
            "backend": "FastAPI + SQLAlchemy + MySQL",
        },
    }