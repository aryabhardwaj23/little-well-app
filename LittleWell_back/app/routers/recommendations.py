"""
Recommendations Router — LittleWell
Integrates TheMealDB (real images) + AUSNUT (Australian nutrition data)
Author: Suryansh Sharma (ssha0314) — API Integration
Branch: feature/api-integration
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
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
import asyncio
from typing import Optional

router = APIRouter(prefix="/products/recommended", tags=["recommendations"])

STATUS_TO_CATEGORY = {
    "iron":      ["Chicken", "Lamb", "Seafood", "Beef"],
    "calcium":   ["Pasta", "Vegetarian", "Breakfast"],
    "vitamin_d": ["Seafood", "Breakfast"],
    "variety":   ["Vegan", "Vegetarian", "Pasta", "Side"],
}

CHILD_AGE_BAND_TO_CATEGORY = {
    "2-3":  ["Breakfast", "Vegetarian", "Pasta"],
    "4-8":  ["Chicken", "Pasta", "Vegetarian", "Seafood"],
    "9-13": ["Chicken", "Beef", "Seafood", "Pasta"],
    "14-18":["Beef", "Chicken", "Seafood", "Lamb"],
}


def get_nutrition_labels(nutrients: dict) -> list[str]:
    labels = []
    if nutrients.get("iron_mg", 0) >= 2.5:    labels.append("High Iron")
    if nutrients.get("calcium_mg", 0) >= 120:  labels.append("High Calcium")
    if nutrients.get("sugar_g", 0) <= 5:       labels.append("Low Sugar")
    if nutrients.get("protein_g", 0) >= 10:    labels.append("High Protein")
    if nutrients.get("fibre_g", 0) >= 3:       labels.append("Good source of Fibre")
    if nutrients.get("vitamin_c_mg", 0) >= 7:  labels.append("Contains Vitamin C")
    return labels


async def build_lunchbox_from_meal(meal, child_name=None, support_type="general", nutrition_focus=None):
    if nutrition_focus is None:
        nutrition_focus = ["Balanced nutrition"]

    card = format_meal_card(meal)

    nutrition_labels = []
    ausnut_nutrition = None
    if card["ingredients"]:
        main_ingredient = card["ingredients"][0]["ingredient"]
        ausnut_nutrition = get_food_by_name(main_ingredient)
        if ausnut_nutrition:
            nutrition_labels = get_nutrition_labels(ausnut_nutrition)

    items = []
    for ing in card["ingredients"][:4]:
        items.append({
            "name":    ing["ingredient"],
            "amount":  ing["measure"],
            "image":   ing["image"],
            "section": "ingredient",
        })

    return {
        "id":             card["id"],
        "childName":      child_name,
        "mealName":       card["name"],
        "mealImage":      card["image"],
        "category":       card["category"],
        "area":           card["area"],
        "items":          items,
        "nutritionFocus": nutrition_focus + nutrition_labels,
        "whyThisMeal":    f"{card['name']} provides {', '.join(nutrition_focus).lower()} and is suitable for children's lunchboxes.",
        "supportType":    support_type,
        "instructions":   card["instructions"],
        "tags":           card["tags"],
        "ausnutData":     ausnut_nutrition,
    }


@router.get("")
async def get_recommended_products(
    child_id: int,
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    child = db.query(models.UserChild).filter(models.UserChild.child_id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    needs_support = []
    if child.iron_status == "needs_support":       needs_support.append("iron")
    if child.calcium_status == "needs_support":    needs_support.append("calcium")
    if child.vitamin_d_status == "needs_support":  needs_support.append("vitamin_d")
    if child.variety_status == "needs_support":    needs_support.append("variety")

    if needs_support:
        categories = STATUS_TO_CATEGORY.get(needs_support[0], ["Chicken", "Vegetarian"])
    else:
        categories = CHILD_AGE_BAND_TO_CATEGORY.get(child.age_band, ["Chicken", "Pasta", "Vegetarian"])

    all_meals = []
    for cat in categories[:2]:
        meals = await filter_meals_by_category(cat)
        all_meals.extend(meals[:3])

    meal_ids = [m["idMeal"] for m in all_meals[:6]]
    tasks = [get_meal_by_id(mid) for mid in meal_ids]
    full_meals = await asyncio.gather(*tasks, return_exceptions=True)

    nutrition_focus = [f"{n.replace('_', ' ').title()} Support" for n in needs_support] or ["Balanced nutrition"]

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
        "lunchboxes":   lunchboxes,
        "child":        {"name": child.child_name, "age_band": child.age_band},
        "dataSource":   "TheMealDB + AUSNUT 2011-13 FSANZ",
    }


@router.get("/family")
async def get_family_recommended_products(
    child_ids: str = Query(...),
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    ids = [int(x) for x in child_ids.split(",") if x.strip()]
    children = db.query(models.UserChild).filter(models.UserChild.child_id.in_(ids)).all()
    if not children:
        raise HTTPException(status_code=404, detail="No children found")

    combined_support = set()
    names = []
    for child in children:
        names.append(child.child_name)
        if child.iron_status == "needs_support":      combined_support.add("iron")
        if child.calcium_status == "needs_support":   combined_support.add("calcium")
        if child.vitamin_d_status == "needs_support": combined_support.add("vitamin_d")
        if child.variety_status == "needs_support":   combined_support.add("variety")

    all_meals = []
    for cat in ["Chicken", "Pasta", "Vegetarian"][:2]:
        meals = await filter_meals_by_category(cat)
        all_meals.extend(meals[:3])

    meal_ids = [m["idMeal"] for m in all_meals[:6]]
    full_meals = await asyncio.gather(*[get_meal_by_id(mid) for mid in meal_ids], return_exceptions=True)

    nutrition_focus = [f"{n.replace('_', ' ').title()} Support" for n in combined_support] or ["Balanced nutrition"]

    lunchboxes = []
    for meal in full_meals:
        if not isinstance(meal, dict):
            continue
        card = await build_lunchbox_from_meal(
            meal=meal,
            child_name=" + ".join(names),
            support_type="general",
            nutrition_focus=nutrition_focus,
        )
        lunchboxes.append(card)

    return {"needsSupport": list(combined_support), "lunchboxes": lunchboxes, "children": names}


@router.get("/quick")
async def get_quick_recommended_products(
    ageGroup: str,
    allergies: str = "",
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    allergy_list = [a.strip() for a in allergies.split(",") if a.strip()]
    categories = CHILD_AGE_BAND_TO_CATEGORY.get(ageGroup, ["Chicken", "Vegetarian", "Pasta"])

    all_meals = []
    for cat in categories[:2]:
        meals = await filter_meals_by_category(cat)
        all_meals.extend(meals[:3])

    meal_ids = [m["idMeal"] for m in all_meals[:6]]
    full_meals = await asyncio.gather(*[get_meal_by_id(mid) for mid in meal_ids], return_exceptions=True)

    lunchboxes = []
    for meal in full_meals:
        if not isinstance(meal, dict):
            continue
        card = await build_lunchbox_from_meal(meal=meal, child_name=None, support_type="general", nutrition_focus=["Balanced nutrition"])
        lunchboxes.append(card)

    return {"needsSupport": [], "lunchboxes": lunchboxes, "quickInput": {"ageGroup": ageGroup, "allergies": allergy_list}}


@router.get("/meals/search")
async def search_meals(q: str = Query(...), limit: int = Query(10, ge=1, le=50)):
    try:
        meals = await search_meals_by_name(q)
        full_meals = await asyncio.gather(*[get_meal_by_id(m["idMeal"]) for m in meals[:limit]], return_exceptions=True)
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
        foods = filter_by_nutrition(high_iron=high_iron, high_calcium=high_calcium, low_sugar=low_sugar, high_protein=high_protein, high_fibre=high_fibre, limit=limit)
        for food in foods:
            food["labels"] = get_nutrition_labels(food)
        return {"foods": foods, "total": len(foods), "data_source": "AUSNUT 2011-13 (FSANZ, CC BY 4.0)"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def api_health():
    return {"status": "ok", "services": {"mealdb": "TheMealDB — free, no key needed", "ausnut": "AUSNUT 2011-13 FSANZ CC BY 4.0", "backend": "FastAPI + SQLAlchemy + MySQL"}}
