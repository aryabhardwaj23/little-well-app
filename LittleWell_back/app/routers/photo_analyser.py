from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from ..db import get_db
from .. import models
from ..auth_utils import get_current_user

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

# Important:
# auto_error=False means no token will NOT automatically return 401.
# This allows both logged-in and non-logged-in users to use photo analysis.
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False,
)


class PhotoAnalysisResponse(BaseModel):
    detected_foods: list
    nutrition_score: dict
    ai_feedback: str
    matched_foods: list
    child_profile: dict
    personalised_checks: dict
    mode: str


async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db),
):
    """
    Optional authentication helper.

    - If no token is provided, return None.
    - If token is provided and valid, return current user.
    - If token is invalid/expired, also return None instead of blocking quick analysis.
    """
    if not token:
        return None

    try:
        return await get_current_user(token=token, db=db)
    except Exception:
        return None


@router.post("/analyse", response_model=PhotoAnalysisResponse)
async def analyse_photo(
    file: UploadFile = File(...),

    # Optional profile-based mode
    child_id: Optional[int] = Form(None),

    # Quick analysis fallback mode
    child_age: int = Form(6),
    child_name: str = Form("your child"),

    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image_bytes = await file.read()

        if len(image_bytes) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image must be under 5MB")

        mode = "quick_age_only"

        # Default quick-analysis context.
        # Used when the user is not logged in or no child_id is provided.
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

        # Enhanced personalised mode:
        # only use profile if BOTH login token and child_id are present.
        if current_user is not None and child_id is not None:
            child = (
                db.query(models.UserChild)
                .filter(
                    models.UserChild.child_id == child_id,
                    models.UserChild.user_id == current_user.user_id,
                )
                .first()
            )

            if child:
                child_context = build_child_profile_context(db=db, child=child)
                child_age_for_scoring = age_band_to_age(child_context.get("age_band"))
                mode = "profile_personalised"
            else:
                # Token exists, but child does not belong to this user.
                # Do not expose profile data. Fall back to quick mode safely.
                mode = "quick_age_only"

        food_labels = detect_food_labels(image_bytes)

        matched_df = match_ausnut(food_labels)

        # AUSNUT-first scoring with child safety override and small visual adjustment.
        # Frontend does not need to change because the response shape stays compatible.
        nutrition_score = score_nutrition(
            matched_df=matched_df,
            child_age=child_age_for_scoring,
            food_labels=food_labels,
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
            mode=mode,
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
            "personalisation": "Optional child profile context",
            "child_safety": "Safety override for unsuitable child lunchbox items",
        },
    }