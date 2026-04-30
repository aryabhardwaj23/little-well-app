from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChildBase(BaseModel):
    child_name: str
    age_band: str
    band_id: Optional[int] = None
    iron_status: int = 0
    calcium_status: int = 0
    vitamin_d_status: int = 0
    variety_status: int = 0
    religious_needs: Optional[str] = ""


class ChildCreate(ChildBase):
    allergies: List[int] = Field(default_factory=list)


class ChildUpdate(ChildBase):
    allergies: List[int] = Field(default_factory=list)


class ChildResponse(BaseModel):
    child_id: int
    user_id: int
    child_name: str
    age_band: str
    band_id: Optional[int] = None
    iron_status: int
    calcium_status: int
    vitamin_d_status: int
    variety_status: int
    religious_needs: Optional[str] = ""
    allergies: List[int] = Field(default_factory=list)

    class Config:
        from_attributes = True


class RecommendationItem(BaseModel):
    name: str
    amount: str
    image: str
    section: str


class LunchboxCard(BaseModel):
    id: str
    childName: Optional[str] = None
    items: List[RecommendationItem]
    nutritionFocus: List[str]
    whyThisMeal: str
    supportType: str


class RecommendationResponse(BaseModel):
    needsSupport: List[str]
    lunchboxes: List[LunchboxCard]

class WeeklyPlanMealCreate(BaseModel):
    reference_food_id: Optional[int] = None

    cook_day: str
    cover_days: Optional[str] = None
    meal_title: str

    servings: Optional[int] = None
    prep_time_minutes: Optional[int] = None

    nutrition_tags: Optional[str] = None
    seasonal_note: Optional[str] = None
    storage_tip: Optional[str] = None

    recipe_id: Optional[int] = None
    image_url: Optional[str] = None


class WeeklyPlanCreate(BaseModel):
    plan_name: str
    child_ids: List[int]

    cook_frequency: int
    variety_preference: Optional[str] = None
    meal_style: Optional[str] = None

    season_id: Optional[int] = None
    status: Optional[str] = "active"

    meals: List[WeeklyPlanMealCreate]


class WeeklyPlanMealResponse(BaseModel):
    meal_id: int
    plan_id: int

    reference_food_id: Optional[int] = None

    cook_day: str
    cover_days: Optional[str] = None
    meal_title: str

    servings: Optional[int] = None
    prep_time_minutes: Optional[int] = None

    nutrition_tags: Optional[str] = None
    seasonal_note: Optional[str] = None
    storage_tip: Optional[str] = None

    recipe_id: Optional[int] = None
    image_url: Optional[str] = None

    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WeeklyPlanChildResponse(BaseModel):
    child_id: int
    child_name: Optional[str] = None

    class Config:
        from_attributes = True


class WeeklyPlanResponse(BaseModel):
    plan_id: int
    user_id: int

    plan_name: str
    plan_type: Optional[str] = "weekly"

    cook_frequency: int
    variety_preference: Optional[str] = None
    meal_style: Optional[str] = None

    season_id: Optional[int] = None
    status: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    children: List[WeeklyPlanChildResponse] = []
    meals: List[WeeklyPlanMealResponse] = []

    class Config:
        from_attributes = True