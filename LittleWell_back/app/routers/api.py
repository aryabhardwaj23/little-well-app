from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import asyncio

from ..services.mealdb_service import (
    search_meals_by_name, filter_meals_by_category,
    get_meal_by_id, get_random_meal, list_categories, format_meal_card
)
from ..services.ausnut_service import (
    filter_by_nutrition, get_food_by_name
)
from ..services.nutrition_service import (
    get_nutrition_labels, get_child_percentage
)

router = APIRouter(prefix="/api", tags=["api-integration"])


@router.get("/health")
async def health():
    return {"status": "ok", "service": "LittleWell API", "version": "1.0.0"}


@router.get("/meals/search")
async def search_meals(
    q: str = Query(...),
    limit: int = Query(10, ge=1, le=50)
):
    try:
        meals = await search_meals_by_name(q)
        detailed = []
        for meal in meals[:limit]:
            full = await get_meal_by_id(meal["idMeal"])
            if full:
                detailed.append(format_meal_card(full))
        return {"meals": detailed, "total": len(detailed)}
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
        categories = await list_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meals/filter/category")
async def filter_by_category(
    category: str = Query(...),
    limit: int = Query(12, ge=1, le=50)
):
    try:
        meals = await filter_meals_by_category(category)
        tasks = [get_meal_by_id(m["idMeal"]) for m in meals[:limit]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        enriched = [format_meal_card(r) for r in results if isinstance(r, dict)]
        return {"meals": enriched, "total": len(enriched), "category": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meals/{meal_id}")
async def get_meal(meal_id: str):
    try:
        meal = await get_meal_by_id(meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail=f"Meal {meal_id} not found")
        return format_meal_card(meal)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nutrition/ausnut")
async def ausnut_filter(
    high_iron:    bool = Query(False),
    high_calcium: bool = Query(False),
    low_sugar:    bool = Query(False),
    high_protein: bool = Query(False),
    high_fibre:   bool = Query(False),
    max_calories: Optional[float] = Query(None),
    limit:        int = Query(20, ge=1, le=100)
):
    try:
        foods = filter_by_nutrition(
            high_iron=high_iron, high_calcium=high_calcium,
            low_sugar=low_sugar, high_protein=high_protein,
            high_fibre=high_fibre, max_calories=max_calories, limit=limit
        )
        for food in foods:
            food["labels"] = get_nutrition_labels(food)
        return {"foods": foods, "total": len(foods), "data_source": "AUSNUT 2011-13 FSANZ CC BY 4.0"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommend")
async def recommend_meals(
    category:     Optional[str]  = Query(None),
    high_iron:    bool = Query(False),
    high_calcium: bool = Query(False),
    low_sugar:    bool = Query(False),
    high_protein: bool = Query(False),
    high_fibre:   bool = Query(False),
    child_age:    Optional[int]  = Query(None),
    limit:        int = Query(6, ge=1, le=20)
):
    try:
        if category:
            meal_list = await filter_meals_by_category(category)
        else:
            child_categories = ["Chicken", "Pasta", "Vegetarian", "Seafood"]
            meal_list = []
            for cat in child_categories:
                meals = await filter_meals_by_category(cat)
                meal_list.extend(meals[:3])

        meal_ids   = [m["idMeal"] for m in meal_list[:limit * 2]]
        tasks      = [get_meal_by_id(mid) for mid in meal_ids]
        full_meals = await asyncio.gather(*tasks, return_exceptions=True)

        any_filter = any([high_iron, high_calcium, low_sugar, high_protein, high_fibre])
        recommendations = []

        for meal in full_meals:
            if not isinstance(meal, dict):
                continue
            card            = format_meal_card(meal)
            nutrition_match = None

            if card["ingredients"]:
                main_ingredient = card["ingredients"][0]["ingredient"]
                nutrition_match = get_food_by_name(main_ingredient)

            if nutrition_match:
                nutrients = {k: v for k, v in nutrition_match.items()
                             if k in ["calories_kcal","protein_g","fat_g","carbs_g",
                                      "sugar_g","fibre_g","calcium_mg","iron_mg",
                                      "sodium_mg","vitamin_c_mg","zinc_mg"]}
                card["nutrition"]        = nutrients
                card["nutrition_labels"] = get_nutrition_labels(nutrients)
                card["child_pct"]        = get_child_percentage(nutrients)

                if any_filter:
                    passes = True
                    if high_iron    and nutrients.get("iron_mg",    0) < 2.5:  passes = False
                    if high_calcium and nutrients.get("calcium_mg", 0) < 120:  passes = False
                    if low_sugar    and nutrients.get("sugar_g",    0) > 5:    passes = False
                    if high_protein and nutrients.get("protein_g",  0) < 10:   passes = False
                    if high_fibre   and nutrients.get("fibre_g",    0) < 3:    passes = False
                    if not passes:
                        continue
            else:
                card["nutrition"]        = None
                card["nutrition_labels"] = []
                card["child_pct"]        = None

            if child_age:
                card["age_appropriate"] = 5 <= child_age <= 12

            recommendations.append(card)
            if len(recommendations) >= limit:
                break

        if not recommendations and any_filter:
            for meal in full_meals[:limit]:
                if isinstance(meal, dict):
                    recommendations.append(format_meal_card(meal))

        return {
            "recommendations": recommendations,
            "total":           len(recommendations),
            "filters_applied": {
                "category": category, "high_iron": high_iron,
                "high_calcium": high_calcium, "low_sugar": low_sugar,
                "high_protein": high_protein, "high_fibre": high_fibre,
                "child_age": child_age,
            },
            "data_sources": ["TheMealDB", "AUSNUT 2011-13 FSANZ CC BY 4.0"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
