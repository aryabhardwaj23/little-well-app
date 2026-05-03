from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


# ── Supported age bands ───────────────────────────────────────────────────────

ALLOWED_CHILD_AGE_BANDS = {
    "5-6 years",
    "7-9 years",
    "10-12 years",
}


# ── Child schemas ─────────────────────────────────────────────────────────────

class ChildBase(BaseModel):
    child_name: str
    age_band: str
    band_id: Optional[int] = None

    iron_status: int = 0
    calcium_status: int = 0
    vitamin_d_status: int = 0
    variety_status: int = 0

    restriction_id: Optional[int] = None

    @field_validator("age_band")
    @classmethod
    def validate_age_band(cls, value: str):
        if value not in ALLOWED_CHILD_AGE_BANDS:
            raise ValueError(
                "LittleWell currently supports children aged 5-12 only. "
                "Allowed age bands: 5-6 years, 7-9 years, 10-12 years."
            )
        return value


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

    restriction_id: Optional[int] = None
    restriction_code: Optional[str] = None
    restriction_name: Optional[str] = None

    allergies: List[int] = Field(default_factory=list)

    class Config:
        from_attributes = True


# ── Recommendation schemas ────────────────────────────────────────────────────

class RecommendationItem(BaseModel):
    reference_food_id: Optional[int] = None
    name: str
    amount: str
    image: Optional[str] = None
    section: str


class LunchboxCard(BaseModel):
    id: str
    reference_food_id: Optional[int] = None
    source: Optional[str] = None
    title: Optional[str] = None
    heroImage: Optional[str] = None
    childName: Optional[str] = None
    items: List[RecommendationItem]
    nutritionFocus: List[str]
    whyThisMeal: str
    supportType: str


class RecommendationResponse(BaseModel):
    needsSupport: List[str]
    lunchboxes: List[LunchboxCard]


# ── Weekly plan schemas ───────────────────────────────────────────────────────

class WeeklyPlanLunchboxItem(BaseModel):
    reference_food_id: Optional[int] = None
    name: str
    amount: Optional[str] = None
    section: Optional[str] = None


class WeeklyPlanMealCreate(BaseModel):
    reference_food_id: Optional[int] = None
    cook_day: str
    cover_days: Optional[str] = None
    meal_title: str
    lunchbox_items: List[WeeklyPlanLunchboxItem] = Field(default_factory=list)

    servings: Optional[float] = None
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
    lunchbox_items: List[WeeklyPlanLunchboxItem] = Field(default_factory=list)

    servings: Optional[float] = None
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
    restriction_id: Optional[int] = None

    class Config:
        from_attributes = True


class WeeklyPlanResponse(BaseModel):
    plan_id: int
    user_id: int
    plan_name: str
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


# ── Auth schemas ──────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse