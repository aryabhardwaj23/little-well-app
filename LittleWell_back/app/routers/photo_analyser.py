from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from ..db import get_db
from ..auth_utils import get_current_user
from .. import models

from ..services.photo_analyser_service import (
    detect_food_labels,
    match_ausnut,
    score_nutrition,
    generate_ai_feedback,
    build_child_profile_context,
    generate_personalised_checks,
    age_band_to_age,
)

router = APIRouter(prefix="/photo", tags=["Photo Analyser"])


class PhotoAnalysisResponse(BaseModel):
    detected_foods: list
    nutrition_score: dict
    ai_feedback: str
    matched_foods: list
    child_profile: dict
    personalised_checks: dict


@router.post("/analyse", response_model=PhotoAnalysisResponse)
async def analyse_photo(
    file: UploadFile = File(...),

    # New profile-based mode
    child_id: Optional[int] = Form(None),

    # Backward-compatible fallback mode
    child_age: int = Form(6),
    child_name: str = Form("your child"),

    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image_bytes = await file.read()

        if len(image_bytes) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image must be under 5MB")

        child_context = None

        # Preferred mode: use saved child profile
        if child_id is not None:
            child = (
                db.query(models.UserChild)
                .filter(
                    models.UserChild.child_id == child_id,
                    models.UserChild.user_id == current_user.user_id,
                )
                .first()
            )

            if not child:
                raise HTTPException(status_code=404, detail="Child profile not found")

            child_context = build_child_profile_context(db=db, child=child)
            child_age_for_scoring = age_band_to_age(child_context.get("age_band"))
        else:
            # Fallback mode for old frontend
            child_context = {
                "child_id": None,
                "child_name": child_name or "your child",
                "age_band": f"{child_age} years old",
                "child_age": child_age,
                "allergens": [],
                "dietary_restriction": None,
                "dietary_restrictions": [],
                "nutrition_focus": [],
            }
            child_age_for_scoring = child_age

        food_labels = detect_food_labels(image_bytes)

        matched_df = match_ausnut(food_labels)

        nutrition_score = score_nutrition(
            matched_df=matched_df,
            child_age=child_age_for_scoring,
        )

        personalised_checks = generate_personalised_checks(
            food_labels=food_labels,
            child_context=child_context,
        )

        ai_feedback = generate_ai_feedback(
            food_labels=food_labels,
            nutrition_score=nutrition_score,
            child_context=child_context,
            personalised_checks=personalised_checks,
        )

        matched_foods = []
        if not matched_df.empty:
            try:
                matched_foods = matched_df.iloc[:, 1].dropna().astype(str).tolist()
            except Exception:
                matched_foods = []

        return PhotoAnalysisResponse(
            detected_foods=food_labels,
            nutrition_score=nutrition_score,
            ai_feedback=ai_feedback,
            matched_foods=matched_foods,
            child_profile=child_context,
            personalised_checks=personalised_checks,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/health")
def photo_health():
    return {
        "status": "ok",
        "services": {
            "image_recognition": "Groq vision model",
            "nutrition_data": "AUSNUT",
            "ai_explanation": "Groq LLaMA",
            "personalisation": "Child profile context",
        },
    }