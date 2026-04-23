
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import asyncio
import random

from ..services.mealdb_service import (
    search_meals_by_name, filter_meals_by_category,
    get_meal_by_id, get_random_meal, list_categories, format_meal_card
)

router = APIRouter(prefix="/api", tags=["api-integration"])


@router.get("/health")
async def api_health():
    return {"status": "ok", "services": {"mealdb": "TheMealDB", "backend": "FastAPI"}}


@router.get("/meals/search")
async def search_meals(q: str = Query(...), limit: int = 10):
    try:
        meals = await search_meals_by_name(q)
        return {"meals": meals[:limit], "total": len(meals[:limit])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meals/random")
async def random_meal():
    try:
        meal = await get_random_meal()
        return meal
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
async def meals_by_category(category: str = Query(...), limit: int = 12):
    try:
        meals = await filter_meals_by_category(category)
        return {"meals": meals[:limit], "total": len(meals[:limit])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meals/{meal_id}")
async def get_meal(meal_id: str):
    try:
        meal = await get_meal_by_id(meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal not found")
        return meal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommend")
async def get_recommendations(
    category: Optional[str] = None,
    high_iron: bool = False,
    high_calcium: bool = False,
    low_sugar: bool = False,
    high_protein: bool = False,
    high_fibre: bool = False,
    child_age: Optional[int] = None,
    limit: int = 6,
):
    try:
        search_terms = ["chicken", "pasta", "vegetable", "rice", "fish", "egg"]
        term = random.choice(search_terms)
        meals = await search_meals_by_name(term)

        recommendations = []
        for meal in meals[:limit]:
            if isinstance(meal, dict):
                recommendations.append(format_meal_card(meal))

        return {
            "recommendations": recommendations,
            "total": len(recommendations),
            "filters_applied": {
                "category": category,
                "child_age": child_age,
            },
            "data_sources": ["TheMealDB"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))