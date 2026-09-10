"""
AI Explanations Router — LittleWell
Exposes "Why This Meal?" AI-powered endpoints using Groq LLaMA3.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.ai_explanation_service import generate_why_this_meal

router = APIRouter(prefix="/ai", tags=["AI Explanations"])

class MealExplanationRequest(BaseModel):
    meal_name: str
    child_age_band: str = "4-8"
    needs_support: list = []
    allergies: list = []
    is_seasonal: bool = False
    nutrition_highlights: dict = {}

@router.post("/why-this-meal")
async def why_this_meal(request: MealExplanationRequest):
    try:
        explanation = generate_why_this_meal(
            meal_name=request.meal_name,
            child_age_band=request.child_age_band,
            needs_support=request.needs_support,
            allergies=request.allergies,
            is_seasonal=request.is_seasonal,
            nutrition_highlights=request.nutrition_highlights,
        )
        return {
            "meal_name": request.meal_name,
            "explanation": explanation,
            "generated_by": "Groq LLaMA3"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/why-this-meal/batch")
async def why_this_meal_batch(meals: list[MealExplanationRequest]):
    results = []
    for meal in meals[:6]:
        try:
            explanation = generate_why_this_meal(
                meal_name=meal.meal_name,
                child_age_band=meal.child_age_band,
                needs_support=meal.needs_support,
                allergies=meal.allergies,
                is_seasonal=meal.is_seasonal,
                nutrition_highlights=meal.nutrition_highlights,
            )
            results.append({
                "meal_name": meal.meal_name,
                "explanation": explanation,
                "generated_by": "Groq LLaMA3"
            })
        except Exception:
            results.append({
                "meal_name": meal.meal_name,
                "explanation": f"A nutritious meal perfectly suited for children aged {meal.child_age_band} years.",
                "generated_by": "fallback"
            })
    return {"explanations": results, "total": len(results)}
