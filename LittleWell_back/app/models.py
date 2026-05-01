from sqlalchemy import Column, Integer, String, Text, DateTime, Date, func, ForeignKey, Numeric
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

    child_name = Column(Text, nullable=True)
    age_band = Column(Text, nullable=True)
    band_id = Column(Integer, nullable=True)

    iron_status = Column(Integer, default=0)
    calcium_status = Column(Integer, default=0)
    vitamin_d_status = Column(Integer, default=0)
    variety_status = Column(Integer, default=0)

    # DB column: restriction_id int
    # Links to dietary_restriction.restriction_id
    restriction_id = Column(
        Integer,
        ForeignKey("dietary_restriction.restriction_id"),
        nullable=True,
    )

    created_at = Column(DateTime, server_default=func.now())

    restriction = relationship("DietaryRestriction")


class UserSearchAllergen(Base):
    __tablename__ = "user_search_allergen"

    user_id = Column(Integer, primary_key=True)
    child_id = Column(Integer, primary_key=True)
    allergen_id = Column(Integer, primary_key=True)


class AgeBand(Base):
    __tablename__ = "age_band"

    band_id = Column(Integer, primary_key=True, index=True)
    label = Column(Text, nullable=True)
    group_name = Column(Text, nullable=True)
    upper_age_limit = Column(Integer, nullable=True)
    lower_age_limit = Column(Integer, nullable=True)


class Allergen(Base):
    __tablename__ = "allergens"

    allergen_id = Column(Integer, primary_key=True, index=True)
    allergen_code = Column(Text, nullable=True)
    allergen_name = Column(Text, nullable=True)
    allergen_clean = Column(Text, nullable=True)
    canonical_allergen = Column(Text, nullable=True)


class DietaryRestriction(Base):
    __tablename__ = "dietary_restriction"

    restriction_id = Column(Integer, primary_key=True, index=True)
    restriction_code = Column(String(50), nullable=False, unique=True)
    restriction_name = Column(String(100), nullable=False)
    restriction_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    excludes_meat = Column(Integer, nullable=False, default=0)
    excludes_fish = Column(Integer, nullable=False, default=0)
    excludes_dairy = Column(Integer, nullable=False, default=0)
    excludes_egg = Column(Integer, nullable=False, default=0)
    excludes_pork = Column(Integer, nullable=False, default=0)
    excludes_shellfish = Column(Integer, nullable=False, default=0)
    excludes_gluten = Column(Integer, nullable=False, default=0)
    excludes_nuts = Column(Integer, nullable=False, default=0)

    is_active = Column(Integer, nullable=False, default=1)


class PackagedProduct(Base):
    __tablename__ = "packaged_products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=True)
    brand = Column(Text, nullable=True)
    category = Column(Text, nullable=True)
    ingredients_list = Column(Text, nullable=True)
    serving_size = Column(Text, nullable=True)

    has_added_sugar = Column(Integer, default=0)
    has_added_preservatives = Column(Integer, default=0)
    has_food_color = Column(Integer, default=0)

    sugar_detected_count = Column(Integer, default=0)
    preservative_detected_count = Column(Integer, default=0)
    color_detected_count = Column(Integer, default=0)

    is_vegan = Column(Integer, default=0)
    is_vegetarian = Column(Integer, default=0)
    is_non_vegan = Column(Integer, default=1)

    palm_oil_status = Column(Text, nullable=True)


class ProductFlag(Base):
    __tablename__ = "product_flag"

    flag_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    flag_type = Column(Text, nullable=True)
    detected_count = Column(Integer, default=0)
    severity = Column(Text, nullable=True)
    rationale = Column(Text, nullable=True)


class ProductAllergen(Base):
    __tablename__ = "product_allergen"

    # DB changed: id is now the row-level primary key
    id = Column(Integer, primary_key=True, index=True)

    allergen_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    allergen_name = Column(Text, nullable=True)
    canonical_allergen = Column(Text, nullable=True)


class ReferenceAllergen(Base):
    __tablename__ = "reference_allergen"

    product_allergen_id = Column(Integer, primary_key=True, index=True)
    reference_food_id = Column(Integer, nullable=False)
    allergen_id = Column(Integer, nullable=False)
    occurrence_type = Column(Text, nullable=True)
    matched_text = Column(Text, nullable=True)
    source_text = Column(Text, nullable=True)


class ReferenceFood(Base):
    __tablename__ = "reference_food"

    reference_food_id = Column(Integer, primary_key=True, index=True)
    food_group_id = Column(Integer, nullable=True)
    ausnut_food_id = Column(Text, nullable=True)
    food_name = Column(Text, nullable=True)
    is_raw = Column(Integer, nullable=True)
    adg_group_code = Column(Text, nullable=True)
    value = Column(Numeric(10, 2), nullable=True)

    is_vegan = Column(Integer, nullable=False, default=0)
    is_vegetarian = Column(Integer, nullable=False, default=0)
    is_gluten_free = Column(Integer, nullable=False, default=0)
    is_dairy_free = Column(Integer, nullable=False, default=0)
    is_egg_free = Column(Integer, nullable=False, default=0)
    is_nut_free = Column(Integer, nullable=False, default=0)
    is_halal = Column(Integer, nullable=False, default=0)
    is_kosher = Column(Integer, nullable=False, default=0)
    is_pork_free = Column(Integer, nullable=False, default=0)


class ReferenceFoodNutrient(Base):
    __tablename__ = "reference_food_nutrient"

    ref_food_nutrient_id = Column(Integer, primary_key=True, index=True)
    reference_food_id = Column(Integer, nullable=False)
    nutrient_code = Column(Text, nullable=True)
    amount_per_100g = Column(Numeric(10, 2), nullable=True)
    unit = Column(Text, nullable=True)


class SavedLunchbox(Base):
    __tablename__ = "saved_lunchbox"

    saved_lunchbox_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    child_id = Column(Integer, nullable=False)

    lunchbox_title = Column(String(150), nullable=False)

    protein_food_id = Column(Integer, nullable=True)
    vegetables_food_id = Column(Integer, nullable=True)
    grains_food_id = Column(Integer, nullable=True)
    fruit_food_id = Column(Integer, nullable=True)
    snack_food_id = Column(Integer, nullable=True)

    nutrition_tags = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class SeasonalProduce(Base):
    __tablename__ = "seasonal_produce"

    season_id = Column(Integer, primary_key=True)
    season_status = Column(Text, nullable=True)
    produce_name = Column(Text, primary_key=True)
    produce_type = Column(Text, nullable=True)


class Season(Base):
    __tablename__ = "seasons"

    season_id = Column(Integer, primary_key=True, index=True)
    season = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)


class WeeklyPlan(Base):
    __tablename__ = "weekly_plan"

    plan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)

    plan_name = Column(String(150), nullable=False)

    # DB enum: 'once', 'twice', 'three_times', 'daily'
    cook_frequency = Column(String(50), nullable=False)

    # DB enum: 'low', 'medium', 'high'
    variety_preference = Column(String(50), nullable=False)

    # DB enum: 'traditional', 'asian', 'mediterranean', 'vegetarian', 'mixed'
    meal_style = Column(String(50), nullable=False)

    season_id = Column(Integer, nullable=True)

    # DB enum: 'draft', 'active', 'completed', 'archived'
    status = Column(String(30), default="active", nullable=False)

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

    # DB enum: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
    cook_day = Column(String(20), nullable=False)

    cover_days = Column(String(100), nullable=True)

    # DB varchar(200)
    meal_title = Column(String(200), nullable=False)

    # DB decimal(4,1)
    servings = Column(Numeric(4, 1), nullable=False, default=1.0)

    prep_time_minutes = Column(Integer, nullable=True)

    # DB varchar(255)
    nutrition_tags = Column(String(255), nullable=True)
    seasonal_note = Column(String(255), nullable=True)
    storage_tip = Column(String(255), nullable=True)

    recipe_id = Column(Integer, nullable=True)

    # DB varchar(500)
    image_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    plan = relationship("WeeklyPlan", back_populates="meals")