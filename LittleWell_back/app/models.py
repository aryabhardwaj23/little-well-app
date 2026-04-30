from sqlalchemy import Column, Integer, String, Text, DateTime, Date, func, ForeignKey
from sqlalchemy.orm import relationship

from .db import Base


class UserSearch(Base):
    __tablename__ = "user_search"

    user_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class UserChild(Base):
    __tablename__ = "user_child"

    child_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    child_name = Column(String(100), nullable=False)
    age_band = Column(String(50), nullable=False)
    band_id = Column(Integer, nullable=True)

    iron_status = Column(Integer, default=0)
    calcium_status = Column(Integer, default=0)
    vitamin_d_status = Column(Integer, default=0)
    variety_status = Column(Integer, default=0)

    religious_needs = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class UserSearchAllergen(Base):
    __tablename__ = "user_search_allergen"

    user_id = Column(Integer, primary_key=True)
    child_id = Column(Integer, primary_key=True)
    allergen_id = Column(Integer, primary_key=True)


class PackagedProduct(Base):
    __tablename__ = "packaged_products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    ingredients_list = Column(Text, nullable=True)
    serving_size = Column(String(100), nullable=True)

    has_added_sugar = Column(Integer, default=0)
    has_added_preservatives = Column(Integer, default=0)
    has_food_color = Column(Integer, default=0)

    sugar_detected_count = Column(Integer, default=0)
    preservative_detected_count = Column(Integer, default=0)
    color_detected_count = Column(Integer, default=0)

    is_vegan = Column(Integer, default=0)
    is_vegetarian = Column(Integer, default=0)
    is_non_vegan = Column(Integer, default=1)

    palm_oil_status = Column(String(50), nullable=True)


class ProductFlag(Base):
    __tablename__ = "product_flag"

    flag_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    flag_type = Column(String(100), nullable=True)
    detected_count = Column(Integer, default=0)
    severity = Column(String(50), nullable=True)
    rationale = Column(Text, nullable=True)


class ProductAllergen(Base):
    __tablename__ = "product_allergen"

    allergen_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    allergen_name = Column(String(100), nullable=True)
    canonical_allergen = Column(String(100), nullable=True)


class SeasonalProduce(Base):
    __tablename__ = "seasonal_produce"

    produce_name = Column(String(255), primary_key=True)
    produce_type = Column(String(100), nullable=True)
    season_id = Column(Integer, nullable=False)
    season_status = Column(String(100), nullable=True)


class Season(Base):
    __tablename__ = "seasons"

    season_id = Column(Integer, primary_key=True, index=True)
    season = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)


class WeeklyPlan(Base):
    __tablename__ = "weekly_plan"

    plan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)

    plan_name = Column(String(150), nullable=False)
    plan_type = Column(String(50), default="weekly")

    cook_frequency = Column(Integer, nullable=False)
    variety_preference = Column(String(50), nullable=True)
    meal_style = Column(String(50), nullable=True)

    season_id = Column(Integer, nullable=True)
    status = Column(String(30), default="active")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    children = relationship(
        "WeeklyPlanChild",
        cascade="all, delete-orphan",
        back_populates="plan",
    )

    meals = relationship(
        "WeeklyPlanMeal",
        cascade="all, delete-orphan",
        back_populates="plan",
    )


class WeeklyPlanChild(Base):
    __tablename__ = "weekly_plan_child"

    plan_child_id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("weekly_plan.plan_id"), nullable=False)
    child_id = Column(Integer, ForeignKey("user_child.child_id"), nullable=False)

    plan = relationship("WeeklyPlan", back_populates="children")


class WeeklyPlanMeal(Base):
    __tablename__ = "weekly_plan_meal"

    meal_id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("weekly_plan.plan_id"), nullable=False)

    reference_food_id = Column(Integer, nullable=True)

    cook_day = Column(String(50), nullable=False)
    cover_days = Column(String(100), nullable=True)

    meal_title = Column(String(150), nullable=False)

    servings = Column(Integer, nullable=True)
    prep_time_minutes = Column(Integer, nullable=True)

    nutrition_tags = Column(String(255), nullable=True)
    seasonal_note = Column(Text, nullable=True)
    storage_tip = Column(Text, nullable=True)

    recipe_id = Column(Integer, nullable=True)
    image_url = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    plan = relationship("WeeklyPlan", back_populates="meals")