from sqlalchemy import text
from sqlalchemy.orm import Session


AGE_BAND_TO_AGE = {
    "5-6 years": 5,
    "7-9 years": 7,
    "10-12 years": 10,
}


FOOD_GROUP_EXAMPLES = {
    "Vegetables": {
        "description": "Vegetables support fibre, vitamins, and everyday balanced eating.",
        "parent_tip": "Try adding colourful vegetables in small portions to make lunchboxes easier to accept.",
    },
    "Fruit": {
        "description": "Fruit provides vitamins, fibre, and natural sweetness.",
        "parent_tip": "Whole fruit is usually a better everyday choice than fruit juice.",
    },
    "Grains": {
        "description": "Grain foods provide energy for school and play.",
        "parent_tip": "Choose wholegrain options when possible for extra fibre.",
    },
    "Protein": {
        "description": "Protein foods support growth, repair, and fullness.",
        "parent_tip": "Use simple lunchbox proteins such as egg, chicken, tuna, beans, tofu, or yoghurt.",
    },
    "Dairy": {
        "description": "Dairy foods support calcium intake for bones and teeth.",
        "parent_tip": "Milk, yoghurt, and cheese can help children meet calcium needs.",
    },
}


def get_user_children_with_serves(db: Session, user_id: int):
    children_sql = text("""
        SELECT
            child_id,
            child_name,
            age_band,
            band_id,
            restriction_id
        FROM user_child
        WHERE user_id = :user_id
        ORDER BY child_id DESC
    """)

    children = db.execute(children_sql, {"user_id": user_id}).mappings().all()

    result = []

    for child in children:
        age_band = child["age_band"]
        lookup_age = AGE_BAND_TO_AGE.get(age_band)

        if lookup_age is None:
            result.append({
                "child_id": child["child_id"],
                "child_name": child["child_name"],
                "age_band": age_band,
                "recommended_serves": [],
                "total_daily_target": None,
            })
            continue

        serves_sql = text("""
            SELECT
                food_group_name,
                adg_group_code,
                recommended_serves
            FROM age_band_serves
            WHERE age = :age
            ORDER BY
                CASE
                    WHEN food_group_name LIKE '%Vegetable%' THEN 1
                    WHEN food_group_name LIKE '%Fruit%' THEN 2
                    WHEN food_group_name LIKE '%Grain%' THEN 3
                    WHEN food_group_name LIKE '%Protein%' THEN 4
                    WHEN food_group_name LIKE '%Dairy%' THEN 5
                    ELSE 6
                END
        """)

        serves = db.execute(serves_sql, {"age": lookup_age}).mappings().all()

        serve_items = [
            {
                "food_group_name": row["food_group_name"],
                "adg_group_code": row["adg_group_code"],
                "recommended_serves": float(row["recommended_serves"]),
            }
            for row in serves
        ]

        total_daily_target = sum(item["recommended_serves"] for item in serve_items)

        result.append({
            "child_id": child["child_id"],
            "child_name": child["child_name"],
            "age_band": age_band,
            "lookup_age": lookup_age,
            "recommended_serves": serve_items,
            "total_daily_target": total_daily_target,
        })

    return result


def get_food_group_guide(db: Session):
    sql = text("""
        SELECT
            adg_group_code,
            food_name,
            is_vegan,
            is_vegetarian,
            is_gluten_free,
            is_dairy_free,
            is_egg_free,
            is_nut_free
        FROM reference_food
        WHERE adg_group_code IS NOT NULL
          AND food_name IS NOT NULL
        LIMIT 300
    """)

    rows = db.execute(sql).mappings().all()

    grouped = {}

    for row in rows:
        code = row["adg_group_code"] or "Other"

        if code not in grouped:
            grouped[code] = {
                "group_code": code,
                "description": "",
                "parent_tip": "",
                "examples": [],
            }

        if len(grouped[code]["examples"]) < 8:
            grouped[code]["examples"].append({
                "food_name": row["food_name"],
                "is_vegan": bool(row["is_vegan"]),
                "is_vegetarian": bool(row["is_vegetarian"]),
                "is_gluten_free": bool(row["is_gluten_free"]),
                "is_dairy_free": bool(row["is_dairy_free"]),
                "is_egg_free": bool(row["is_egg_free"]),
                "is_nut_free": bool(row["is_nut_free"]),
            })

    return list(grouped.values())


def get_additive_heatmap(db: Session):
    sql = text("""
        SELECT
            product_id,
            name,
            brand,
            category,
            has_added_sugar,
            has_added_preservatives,
            has_food_color,
            sugar_detected_count,
            preservative_detected_count,
            color_detected_count
        FROM packaged_products
        WHERE name IS NOT NULL
        ORDER BY
            COALESCE(sugar_detected_count, 0)
            + COALESCE(preservative_detected_count, 0)
            + COALESCE(color_detected_count, 0) DESC
        LIMIT 100
    """)

    rows = db.execute(sql).mappings().all()

    products = []

    for row in rows:
        sugar_count = row["sugar_detected_count"] or 0
        preservative_count = row["preservative_detected_count"] or 0
        color_count = row["color_detected_count"] or 0

        total_flags = sugar_count + preservative_count + color_count

        if total_flags >= 4:
            severity = "high"
        elif total_flags >= 2:
            severity = "medium"
        elif total_flags >= 1:
            severity = "low"
        else:
            severity = "none"

        products.append({
            "product_id": row["product_id"],
            "name": row["name"],
            "brand": row["brand"],
            "category": row["category"],
            "has_added_sugar": bool(row["has_added_sugar"]),
            "has_added_preservatives": bool(row["has_added_preservatives"]),
            "has_food_color": bool(row["has_food_color"]),
            "sugar_detected_count": sugar_count,
            "preservative_detected_count": preservative_count,
            "color_detected_count": color_count,
            "total_flags": total_flags,
            "severity": severity,
        })

    return products