from sqlalchemy import Column, Integer, String, Text
from .db import Base


class UserChild(Base):
    __tablename__ = "user_child"

    child_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    child_name = Column(String(100), nullable=False)
    age_band = Column(String(50), nullable=False)
    band_id = Column(Integer, nullable=True)

    iron_status = Column(String(50), default="normal")
    calcium_status = Column(String(50), default="normal")
    vitamin_d_status = Column(String(50), default="normal")
    variety_status = Column(String(50), default="normal")

    religious_needs = Column(String(100), nullable=True)


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

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    parent_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)