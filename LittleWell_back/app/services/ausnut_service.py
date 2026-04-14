"""
AUSNUT 2011-13 Local Dataset Service — LittleWell
Australian Food and Nutrient Database — FSANZ, CC BY 4.0
Download: https://www.foodstandards.gov.au/science-data/monitoringnutrients/ausnut/ausnutdatafiles

This service reads the AUSNUT CSV file locally — no API call needed.
Place the CSV file at: data/ausnut_2011_13.csv
"""
import pandas as pd
import os
from typing import Optional
from functools import lru_cache

AUSNUT_PATH = os.path.join(os.path.dirname(__file__), "../data/ausnut_2011_13.csv")

# AUSNUT column name mapping to friendly names
AUSNUT_COLUMNS = {
    "Food Name":                        "food_name",
    "Energy, with dietary fibre (kJ)":  "energy_kj",
    "Protein (g)":                      "protein_g",
    "Total fat (g)":                    "fat_g",
    "Available carbohydrates (g)":      "carbs_g",
    "Total sugars (g)":                 "sugar_g",
    "Dietary fibre (g)":                "fibre_g",
    "Calcium (Ca) (mg)":                "calcium_mg",
    "Iron (Fe) (mg)":                   "iron_mg",
    "Sodium (Na) (mg)":                 "sodium_mg",
    "Vitamin C (mg)":                   "vitamin_c_mg",
    "Zinc (Zn) (mg)":                   "zinc_mg",
}


@lru_cache(maxsize=1)
def load_ausnut() -> pd.DataFrame:
    """
    Load and cache AUSNUT dataset on first call.
    Cached so it's only read from disk once per app lifetime.
    """
    if not os.path.exists(AUSNUT_PATH):
        raise FileNotFoundError(
            f"AUSNUT CSV not found at {AUSNUT_PATH}. "
            "Download from: https://www.foodstandards.gov.au/science-data/"
            "monitoringnutrients/ausnut/ausnutdatafiles"
        )

    df = pd.read_csv(AUSNUT_PATH, encoding="latin-1")

    # Rename only columns that exist in this file
    rename_map = {k: v for k, v in AUSNUT_COLUMNS.items() if k in df.columns}
    df = df.rename(columns=rename_map)

    # Convert kJ to kcal (1 kcal = 4.184 kJ)
    if "energy_kj" in df.columns:
        df["calories_kcal"] = (df["energy_kj"] / 4.184).round(1)

    # Fill NaN with 0 for numeric columns
    numeric_cols = ["protein_g","fat_g","carbs_g","sugar_g","fibre_g",
                    "calcium_mg","iron_mg","sodium_mg","vitamin_c_mg","zinc_mg","calories_kcal"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def search_ausnut(query: str, limit: int = 20) -> list[dict]:
    """Search AUSNUT by food name (case-insensitive partial match)."""
    df = load_ausnut()
    if "food_name" not in df.columns:
        return []
    mask    = df["food_name"].str.contains(query, case=False, na=False)
    results = df[mask].head(limit)
    return results.to_dict(orient="records")


def filter_by_nutrition(
    high_iron:     bool = False,
    high_calcium:  bool = False,
    low_sugar:     bool = False,
    high_protein:  bool = False,
    high_fibre:    bool = False,
    max_calories:  Optional[float] = None,
    limit:         int = 20,
) -> list[dict]:
    """
    Filter AUSNUT foods by nutritional criteria.
    Used by LittleWell meal filter feature — maps to Australian Dietary Guidelines.
    """
    df = load_ausnut()

    if high_iron     and "iron_mg"      in df.columns: df = df[df["iron_mg"]      >= 2.5]
    if high_calcium  and "calcium_mg"   in df.columns: df = df[df["calcium_mg"]   >= 120]
    if low_sugar     and "sugar_g"      in df.columns: df = df[df["sugar_g"]      <= 5]
    if high_protein  and "protein_g"    in df.columns: df = df[df["protein_g"]    >= 10]
    if high_fibre    and "fibre_g"      in df.columns: df = df[df["fibre_g"]      >= 3]
    if max_calories  and "calories_kcal"in df.columns: df = df[df["calories_kcal"]<= max_calories]

    return df.head(limit).to_dict(orient="records")


def get_food_by_name(food_name: str) -> Optional[dict]:
    """Get exact nutrition data for a food name from AUSNUT."""
    df = load_ausnut()
    if "food_name" not in df.columns:
        return None
    match = df[df["food_name"].str.lower() == food_name.lower()]
    if match.empty:
        return None
    return match.iloc[0].to_dict()
