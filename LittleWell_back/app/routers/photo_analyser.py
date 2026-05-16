from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from ..services.photo_analyser_service import detect_food_labels, match_ausnut, score_nutrition, generate_ai_feedback

router = APIRouter(prefix="/photo", tags=["Photo Analyser"])

class PhotoAnalysisResponse(BaseModel):
    detected_foods: list
    nutrition_score: dict
    ai_feedback: str
    matched_foods: list

@router.post("/analyse", response_model=PhotoAnalysisResponse)
async def analyse_photo(
    file: UploadFile = File(...),
    child_age: int = Form(6),
    child_name: str = Form("your child"),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    try:
        image_bytes = await file.read()
        if len(image_bytes) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image must be under 5MB")
        food_labels     = detect_food_labels(image_bytes)
        matched_df      = match_ausnut(food_labels)
        nutrition_score = score_nutrition(matched_df, child_age)
        ai_feedback     = generate_ai_feedback(food_labels, nutrition_score, child_age, child_name)
        matched_foods   = matched_df.iloc[:, 0].tolist() if not matched_df.empty else []
        return PhotoAnalysisResponse(detected_foods=food_labels, nutrition_score=nutrition_score, ai_feedback=ai_feedback, matched_foods=matched_foods)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/health")
def photo_health():
    return {"status": "ok"}
