from sqlalchemy import text
from sqlalchemy.orm import Session


AGE_BAND_TO_AGE = {
    "5-6 years": 5,
    "7-9 years": 7,
    "10-12 years": 10,
}


def get_heat_level(percent: int) -> str:
    if percent > 60:
        return "warning"
    if percent >= 41:
        return "high"
    if percent >= 21:
        return "medium"
    return "low"


def get_label_priority(risk_score: float) -> str:
    if risk_score >= 60:
        return "High label-check priority"
    if risk_score >= 35:
        return "Moderate label-check priority"
    if risk_score > 0:
        return "Low label-check priority"
    return "No major additive signal"


def build_category_tip(
    category: str,
    added_sugar_percent: int,
    preservatives_percent: int,
    colours_percent: int,
) -> str:
    highest_value = max(
        added_sugar_percent,
        preservatives_percent,
        colours_percent,
    )

    if highest_value == added_sugar_percent and added_sugar_percent >= 40:
        return (
            f"{category} may need closer sugar label checking. "
            "Compare similar products and look for lower added sugar options."
        )

    if highest_value == preservatives_percent and preservatives_percent >= 40:
        return (
            f"{category} may need closer preservative checking. "
            "Look at the ingredient list and compare simpler options when possible."
        )

    if highest_value == colours_percent and colours_percent >= 40:
        return (
            f"{category} may need closer artificial colour checking. "
            "Check ingredient lists for colour additives or colour codes."
        )

    return (
        f"{category} shows a lower additive signal in the available records, "
        "but it is still useful to compare labels when buying packaged foods."
    )


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
                "lookup_age": None,
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

        total_daily_target = sum(
            item["recommended_serves"] for item in serve_items
        )

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
                "description": build_food_group_description(code),
                "parent_tip": build_food_group_tip(code),
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


def build_food_group_description(group_code: str) -> str:
    code = str(group_code).lower()

    if "vegetable" in code or "veg" in code:
        return "Vegetables support fibre, vitamins, and everyday balanced eating."

    if "fruit" in code:
        return "Fruit provides vitamins, fibre, and natural sweetness."

    if "grain" in code or "cereal" in code:
        return "Grain foods provide energy for school and play."

    if "protein" in code or "meat" in code or "egg" in code or "legume" in code:
        return "Protein foods support growth, repair, and fullness."

    if "dairy" in code or "milk" in code or "cheese" in code:
        return "Dairy foods support calcium intake for bones and teeth."

    return "This food group can contribute to a balanced lunchbox when chosen carefully."


def build_food_group_tip(group_code: str) -> str:
    code = str(group_code).lower()

    if "vegetable" in code or "veg" in code:
        return "Try adding colourful vegetables in small portions to make lunchboxes easier to accept."

    if "fruit" in code:
        return "Whole fruit is usually a better everyday choice than fruit juice."

    if "grain" in code or "cereal" in code:
        return "Choose wholegrain options when possible for extra fibre."

    if "protein" in code or "meat" in code or "egg" in code or "legume" in code:
        return "Use simple lunchbox proteins such as egg, chicken, beans, tuna, tofu, or yoghurt."

    if "dairy" in code or "milk" in code or "cheese" in code:
        return "Milk, yoghurt, and cheese can help children meet calcium needs."

    return "Compare options and choose foods that fit your child’s needs and preferences."


def get_additive_awareness_guide(db: Session):
    sql = text("""
        SELECT
            COALESCE(NULLIF(category_map, ''), NULLIF(category, ''), 'Other') AS category,
            COUNT(*) AS total_products,

            SUM(CASE WHEN has_added_sugar = 1 THEN 1 ELSE 0 END) AS added_sugar_count,
            SUM(CASE WHEN has_added_preservatives = 1 THEN 1 ELSE 0 END) AS preservatives_count,
            SUM(CASE WHEN has_food_color = 1 THEN 1 ELSE 0 END) AS food_color_count,

            SUM(COALESCE(sugar_detected_count, 0)) AS sugar_detected_total,
            SUM(COALESCE(preservative_detected_count, 0)) AS preservative_detected_total,
            SUM(COALESCE(color_detected_count, 0)) AS color_detected_total

        FROM packaged_products_enriched

        WHERE COALESCE(NULLIF(category_map, ''), NULLIF(category, '')) IS NOT NULL

        GROUP BY COALESCE(NULLIF(category_map, ''), NULLIF(category, ''), 'Other')

        HAVING COUNT(*) >= 3

        ORDER BY
            (
                SUM(CASE WHEN has_added_sugar = 1 THEN 1 ELSE 0 END) * 0.4
                + SUM(CASE WHEN has_added_preservatives = 1 THEN 1 ELSE 0 END) * 0.3
                + SUM(CASE WHEN has_food_color = 1 THEN 1 ELSE 0 END) * 0.3
            ) DESC,
            total_products DESC

        LIMIT 12
    """)

    rows = db.execute(sql).mappings().all()

    heatmap = []

    for row in rows:
        total = int(row["total_products"] or 1)

        added_sugar_count = int(row["added_sugar_count"] or 0)
        preservatives_count = int(row["preservatives_count"] or 0)
        food_color_count = int(row["food_color_count"] or 0)

        added_sugar_percent = round(added_sugar_count / total * 100)
        preservatives_percent = round(preservatives_count / total * 100)
        artificial_colours_percent = round(food_color_count / total * 100)

        risk_score = round(
            added_sugar_percent * 0.4
            + preservatives_percent * 0.3
            + artificial_colours_percent * 0.3,
            1,
        )

        category = row["category"]

        heatmap.append({
            "category": category,
            "total_products": total,
            "risk_score": risk_score,
            "label_priority": get_label_priority(risk_score),
            "parent_tip": build_category_tip(
                category=category,
                added_sugar_percent=added_sugar_percent,
                preservatives_percent=preservatives_percent,
                colours_percent=artificial_colours_percent,
            ),
            "added_sugar": {
                "count": added_sugar_count,
                "detected_total": int(row["sugar_detected_total"] or 0),
                "percent": added_sugar_percent,
                "level": get_heat_level(added_sugar_percent),
            },
            "preservatives": {
                "count": preservatives_count,
                "detected_total": int(row["preservative_detected_total"] or 0),
                "percent": preservatives_percent,
                "level": get_heat_level(preservatives_percent),
            },
            "artificial_colours": {
                "count": food_color_count,
                "detected_total": int(row["color_detected_total"] or 0),
                "percent": artificial_colours_percent,
                "level": get_heat_level(artificial_colours_percent),
            },
        })

    summary = build_additive_summary(heatmap)

    return {
        "title": "Additive Awareness Guide",
        "description": (
            "This guide helps parents identify packaged food categories that may need "
            "closer label checking. It summarises how often added sugar, preservatives, "
            "and artificial colours appear in available packaged product records."
        ),
        "disclaimer": (
            "A higher percentage does not mean every product in the category is unhealthy. "
            "It means this category may need closer label checking when choosing lunchbox items."
        ),
        "how_to_read": [
            {
                "level": "low",
                "label": "0–20%",
                "meaning": "Lower prevalence in the available product records.",
            },
            {
                "level": "medium",
                "label": "21–40%",
                "meaning": "Worth checking labels, especially for regular purchases.",
            },
            {
                "level": "high",
                "label": "41–60%",
                "meaning": "Compare products carefully before choosing.",
            },
            {
                "level": "warning",
                "label": "Above 60%",
                "meaning": "This category often contains this additive type in the available records.",
            },
        ],
        "parent_tips": [
            "Compare similar products instead of relying only on front-of-pack claims.",
            "Check the ingredient list for sugar, syrup, preservatives, colours, or additive codes.",
            "Choose simpler ingredient lists where possible.",
            "Use this as a label-checking guide, not as medical advice.",
        ],
        "summary": summary,
        "heatmap": heatmap,
    }


def build_additive_summary(heatmap: list[dict]):
    if not heatmap:
        return {
            "highest_added_sugar": None,
            "highest_preservatives": None,
            "highest_artificial_colours": None,
            "highest_overall_priority": None,
        }

    highest_added_sugar = max(
        heatmap,
        key=lambda item: item["added_sugar"]["percent"],
    )

    highest_preservatives = max(
        heatmap,
        key=lambda item: item["preservatives"]["percent"],
    )

    highest_artificial_colours = max(
        heatmap,
        key=lambda item: item["artificial_colours"]["percent"],
    )

    highest_overall_priority = max(
        heatmap,
        key=lambda item: item["risk_score"],
    )

    return {
        "highest_added_sugar": {
            "category": highest_added_sugar["category"],
            "percent": highest_added_sugar["added_sugar"]["percent"],
            "total_products": highest_added_sugar["total_products"],
        },
        "highest_preservatives": {
            "category": highest_preservatives["category"],
            "percent": highest_preservatives["preservatives"]["percent"],
            "total_products": highest_preservatives["total_products"],
        },
        "highest_artificial_colours": {
            "category": highest_artificial_colours["category"],
            "percent": highest_artificial_colours["artificial_colours"]["percent"],
            "total_products": highest_artificial_colours["total_products"],
        },
        "highest_overall_priority": {
            "category": highest_overall_priority["category"],
            "risk_score": highest_overall_priority["risk_score"],
            "label_priority": highest_overall_priority["label_priority"],
            "total_products": highest_overall_priority["total_products"],
        },
    }