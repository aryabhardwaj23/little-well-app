"""
AUSNUT Local Dataset Service — LittleWell

Reads the AUSNUT CSV file locally.
Place the CSV file at: app/data/ausnut_2011_13.csv
"""

import os
import re
from difflib import get_close_matches
from functools import lru_cache
from typing import Optional

import pandas as pd


AUSNUT_PATH = os.path.join(os.path.dirname(__file__), "../data/ausnut_2011_13.csv")

# AUSNUT column name mapping to friendly names
AUSNUT_COLUMNS = {
    "Food Name": "food_name",
    "Energy, with dietary fibre (kJ)": "energy_kj",
    "Protein (g)": "protein_g",
    "Total fat (g)": "fat_g",
    "Available carbohydrates (g)": "carbs_g",
    "Total sugars (g)": "sugar_g",
    "Dietary fibre (g)": "fibre_g",
    "Calcium (Ca) (mg)": "calcium_mg",
    "Iron (Fe) (mg)": "iron_mg",
    "Sodium (Na) (mg)": "sodium_mg",
    "Vitamin C (mg)": "vitamin_c_mg",
    "Zinc (Zn) (mg)": "zinc_mg",
}

NUMERIC_COLS = [
    "protein_g",
    "fat_g",
    "carbs_g",
    "sugar_g",
    "fibre_g",
    "calcium_mg",
    "iron_mg",
    "sodium_mg",
    "vitamin_c_mg",
    "zinc_mg",
    "calories_kcal",
]


@lru_cache(maxsize=1)
def load_ausnut() -> pd.DataFrame:
    """
    Load and cache AUSNUT dataset on first call.
    Cached so it's only read from disk once per app lifetime.
    """
    if not os.path.exists(AUSNUT_PATH):
        raise FileNotFoundError(
            f"AUSNUT CSV not found at {AUSNUT_PATH}. "
            "Please place the CSV file in app/data/ausnut_2011_13.csv"
        )

    df = pd.read_csv(AUSNUT_PATH, encoding="latin-1")

    # Rename only columns that exist in this file
    rename_map = {k: v for k, v in AUSNUT_COLUMNS.items() if k in df.columns}
    df = df.rename(columns=rename_map)

    # Convert kJ to kcal
    if "energy_kj" in df.columns:
        df["calories_kcal"] = (pd.to_numeric(df["energy_kj"], errors="coerce") / 4.184).round(1)

    # Fill NaN with 0 for numeric columns
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Safe food name cleanup
    if "food_name" in df.columns:
        df["food_name"] = df["food_name"].fillna("").astype(str).str.strip()

    # Build normalized search column once
    if "food_name" in df.columns and "_normalized_food_name" not in df.columns:
        df["_normalized_food_name"] = df["food_name"].apply(normalize_food_name)

    return df


def normalize_food_name(text: str) -> str:
    """
    Normalize ingredient text for matching against AUSNUT food names.
    Used to improve matching between MealDB ingredient names and AUSNUT names.
    """
    if not text:
        return ""

    text = text.lower().strip()

    # Common ingredient replacements from MealDB-style names to simpler food terms
    replacements = {
        "prawns": "prawn",
        "shrimp": "prawn",
        "jumbo shrimp": "prawn",
        "king prawns": "prawn",
        "mixed beef cuts": "beef",
        "beef cuts": "beef",
        "minced beef": "beef",
        "ground beef": "beef",
        "red onions": "onion",
        "brown onions": "onion",
        "spring onions": "onion",
        "onions": "onion",
        "garlic clove": "garlic",
        "garlic cloves": "garlic",
        "cloves garlic": "garlic",
        "chicken breasts": "chicken",
        "chicken breast": "chicken",
        "chicken thighs": "chicken",
        "beef mince": "beef",
        "plain flour": "flour",
        "all purpose flour": "flour",
        "all-purpose flour": "flour",
        "caster sugar": "sugar",
        "icing sugar": "sugar",
        "olive oil": "oil",
        "vegetable oil": "oil",
        "red capsicum": "capsicum",
        "green capsicum": "capsicum",
        "bell peppers": "capsicum",
        "bell pepper": "capsicum",
        "potatoes": "potato",
        "tomatoes": "tomato",
        "eggs": "egg",
        "peas": "pea",
        "carrots": "carrot",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove common descriptive words that reduce match quality
    stop_words = {
        "fresh", "dried", "chopped", "sliced", "minced", "ground", "large", "small",
        "medium", "raw", "cooked", "skinless", "boneless", "lean", "extra", "virgin",
        "red", "green", "yellow", "black", "white", "whole", "plain", "all", "purpose",
        "cut", "cuts", "to", "taste", "optional", "for", "serving", "tbsp", "tsp",
        "cup", "cups", "kg", "g", "ml", "oz", "lb"
    }

    parts = [p for p in text.split() if p not in stop_words]
    normalized = " ".join(parts).strip()

    # Singularize simple plurals
    if normalized.endswith("s") and len(normalized) > 3:
        normalized = normalized[:-1]

    return normalized


def search_ausnut(query: str, limit: int = 20) -> list[dict]:
    """Search AUSNUT by food name (case-insensitive partial match)."""
    df = load_ausnut()

    if "food_name" not in df.columns or not query:
        return []

    mask = df["food_name"].str.contains(query, case=False, na=False)
    results = df[mask].head(limit)
    return results.to_dict(orient="records")


def filter_by_nutrition(
    high_iron: bool = False,
    high_calcium: bool = False,
    low_sugar: bool = False,
    high_protein: bool = False,
    high_fibre: bool = False,
    max_calories: Optional[float] = None,
    limit: int = 20,
) -> list[dict]:
    """
    Filter AUSNUT foods by nutritional criteria.
    """
    df = load_ausnut()

    if high_iron and "iron_mg" in df.columns:
        df = df[df["iron_mg"] >= 2.5]

    if high_calcium and "calcium_mg" in df.columns:
        df = df[df["calcium_mg"] >= 120]

    if low_sugar and "sugar_g" in df.columns:
        df = df[df["sugar_g"] <= 5]

    if high_protein and "protein_g" in df.columns:
        df = df[df["protein_g"] >= 10]

    if high_fibre and "fibre_g" in df.columns:
        df = df[df["fibre_g"] >= 3]

    if max_calories is not None and "calories_kcal" in df.columns:
        df = df[df["calories_kcal"] <= max_calories]

    return df.head(limit).to_dict(orient="records")


def get_food_by_name(food_name: str) -> Optional[dict]:
    """Get exact nutrition data for a food name from AUSNUT."""
    df = load_ausnut()

    if "food_name" not in df.columns or not food_name:
        return None

    match = df[df["food_name"].str.lower() == food_name.lower()]
    if match.empty:
        return None

    return match.iloc[0].to_dict()


def get_food_by_name_contains(food_name: str) -> Optional[dict]:
    """
    Try a simple contains match after normalization.
    Useful when exact food name matching fails.
    """
    df = load_ausnut()

    if "_normalized_food_name" not in df.columns or not food_name:
        return None

    normalized_query = normalize_food_name(food_name)
    if not normalized_query:
        return None

    # AUSNUT row contains query
    contains_match = df[
        df["_normalized_food_name"].str.contains(normalized_query, case=False, na=False)
    ]
    if not contains_match.empty:
        return contains_match.iloc[0].to_dict()

    # Query contains AUSNUT row
    reverse_match = df[
        df["_normalized_food_name"].apply(
            lambda x: x in normalized_query if isinstance(x, str) and x else False
        )
    ]
    if not reverse_match.empty:
        # Prefer longer normalized food names because they are often more specific
        reverse_match = reverse_match.copy()
        reverse_match["_match_len"] = reverse_match["_normalized_food_name"].str.len()
        reverse_match = reverse_match.sort_values("_match_len", ascending=False)
        return reverse_match.iloc[0].to_dict()

    return None


def get_food_by_name_fuzzy(food_name: str) -> Optional[dict]:
    """
    Try to match a MealDB ingredient name to AUSNUT using:
    1) exact match
    2) normalized exact match
    3) contains match
    4) difflib close match

    This is best for integrating MealDB ingredients with AUSNUT.
    """
    df = load_ausnut()

    if "food_name" not in df.columns or not food_name:
        return None

    # 1) Exact match
    exact = get_food_by_name(food_name)
    if exact:
        return exact

    normalized_query = normalize_food_name(food_name)
    if not normalized_query:
        return None

    # 2) Normalized exact match
    if "_normalized_food_name" in df.columns:
        normalized_exact = df[df["_normalized_food_name"] == normalized_query]
        if not normalized_exact.empty:
            return normalized_exact.iloc[0].to_dict()

    # 3) Contains match
    contains = get_food_by_name_contains(food_name)
    if contains:
        return contains

    # 4) Close match
    if "_normalized_food_name" in df.columns:
        choices = df["_normalized_food_name"].dropna().astype(str).unique().tolist()
        close = get_close_matches(normalized_query, choices, n=1, cutoff=0.75)

        if close:
            fuzzy_match = df[df["_normalized_food_name"] == close[0]]
            if not fuzzy_match.empty:
                return fuzzy_match.iloc[0].to_dict()

    return None