from pydantic import BaseModel
from typing import List, Optional


class ChildBase(BaseModel):
    child_name: str
    age_band: str
    band_id: Optional[int] = None
    iron_status: str = "normal"
    calcium_status: str = "normal"
    vitamin_d_status: str = "normal"
    variety_status: str = "normal"
    religious_needs: Optional[str] = ""


class ChildCreate(ChildBase):
    allergies: List[int] = []


class ChildUpdate(ChildBase):
    user_id: int
    allergies: List[int] = []


class ChildResponse(BaseModel):
    child_id: int
    user_id: int
    child_name: str
    age_band: str
    band_id: Optional[int] = None
    iron_status: str
    calcium_status: str
    vitamin_d_status: str
    variety_status: str
    religious_needs: Optional[str] = ""
    allergies: List[int] = []

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