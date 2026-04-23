from pydantic import BaseModel, Field
from typing import List, Optional


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