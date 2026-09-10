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
        WITH cleaned_products AS (
            SELECT
                product_id,
                name,
                brand,
                category,
                category_map,
                has_added_sugar,
                has_added_preservatives,
                has_food_color,
                sugar_detected_count,
                preservative_detected_count,
                color_detected_count,

                CASE
                    /* Exclude unsuitable non-lunchbox / non-food records */
                    WHEN LOWER(COALESCE(category_map, category, '')) LIKE '%dietary supplement%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%supplement%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%vitamin%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%bodybuilding%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%protein powder%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%protein shake%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%medication%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%non food%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%open beauty facts%'
                    THEN NULL

                    /* Alcohol is not suitable for a children lunchbox guide */
                    WHEN LOWER(COALESCE(category_map, category, '')) LIKE '%alcohol%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%beer%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%wine%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%cider%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%whisky%'
                      OR LOWER(COALESCE(category_map, category, '')) LIKE '%lagers%'
                    THEN NULL

                    /* Use existing cleaned category if it is already useful */
                    WHEN category_map IS NOT NULL
                      AND category_map <> ''
                      AND category_map <> 'Other'
                    THEN category_map

                    /* Sweet snacks / confectionery */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%candy%'
                      OR LOWER(COALESCE(category, '')) LIKE '%candies%'
                      OR LOWER(COALESCE(category, '')) LIKE '%bonbon%'
                      OR LOWER(COALESCE(category, '')) LIKE '%gummi%'
                      OR LOWER(COALESCE(category, '')) LIKE '%gummy%'
                      OR LOWER(COALESCE(category, '')) LIKE '%lollipop%'
                      OR LOWER(COALESCE(category, '')) LIKE '%chocolate%'
                      OR LOWER(COALESCE(category, '')) LIKE '%confection%'
                      OR LOWER(COALESCE(category, '')) LIKE '%marshmallow%'
                      OR LOWER(COALESCE(category, '')) LIKE '%sweet snack%'
                      OR LOWER(COALESCE(category, '')) LIKE '%dessert%'
                      OR LOWER(COALESCE(category, '')) LIKE '%pudding%'
                      OR LOWER(COALESCE(category, '')) LIKE '%jelly%'
                      OR LOWER(COALESCE(category, '')) LIKE '%lamington%'
                      OR LOWER(COALESCE(category, '')) LIKE '%ice pop%'
                      OR LOWER(COALESCE(category, '')) LIKE '%protein bar%'
                      OR LOWER(COALESCE(category, '')) LIKE '%health bar%'
                      OR LOWER(COALESCE(category, '')) LIKE '%energy bar%'
                      OR LOWER(COALESCE(category, '')) LIKE '%bars%'
                    THEN 'Sweet Snacks & Confectionery'

                    /* Biscuits / cookies / cakes */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%biscuit%'
                      OR LOWER(COALESCE(category, '')) LIKE '%cookie%'
                      OR LOWER(COALESCE(category, '')) LIKE '%cake%'
                      OR LOWER(COALESCE(category, '')) LIKE '%brownie%'
                      OR LOWER(COALESCE(category, '')) LIKE '%waffle%'
                      OR LOWER(COALESCE(category, '')) LIKE '%pastr%'
                      OR LOWER(COALESCE(category, '')) LIKE '%croissant%'
                      OR LOWER(COALESCE(category, '')) LIKE '%doughnut%'
                    THEN 'Biscuits, Cookies & Cakes'

                    /* Beverages */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%beverage%'
                      OR LOWER(COALESCE(category, '')) LIKE '%drink%'
                      OR LOWER(COALESCE(category, '')) LIKE '%water%'
                      OR LOWER(COALESCE(category, '')) LIKE '%cola%'
                      OR LOWER(COALESCE(category, '')) LIKE '%soda%'
                      OR LOWER(COALESCE(category, '')) LIKE '%juice%'
                      OR LOWER(COALESCE(category, '')) LIKE '%tea%'
                      OR LOWER(COALESCE(category, '')) LIKE '%coffee%'
                      OR LOWER(COALESCE(category, '')) LIKE '%kombucha%'
                      OR LOWER(COALESCE(category, '')) LIKE '%coconut water%'
                      OR LOWER(COALESCE(category, '')) LIKE '%chai%'
                      OR LOWER(COALESCE(category, '')) LIKE '%cappuccino%'
                      OR LOWER(COALESCE(category, '')) LIKE '%electrolyte%'
                    THEN 'Beverages'

                    /* Frozen and ready meals */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%readymeal%'
                      OR LOWER(COALESCE(category, '')) LIKE '%ready meal%'
                      OR LOWER(COALESCE(category, '')) LIKE '%microwave%'
                      OR LOWER(COALESCE(category, '')) LIKE '%meal%'
                      OR LOWER(COALESCE(category, '')) LIKE '%dumpling%'
                      OR LOWER(COALESCE(category, '')) LIKE '%ravioli%'
                      OR LOWER(COALESCE(category, '')) LIKE '%spring roll%'
                      OR LOWER(COALESCE(category, '')) LIKE '%sandwich%'
                      OR LOWER(COALESCE(category, '')) LIKE '%sushi%'
                      OR LOWER(COALESCE(category, '')) LIKE '%pizza%'
                      OR LOWER(COALESCE(category, '')) LIKE '%lasagna%'
                      OR LOWER(COALESCE(category, '')) LIKE '%hash brown%'
                      OR LOWER(COALESCE(category, '')) LIKE '%recipe base%'
                    THEN 'Frozen & Ready Meals'

                    /* Condiments / sauces / spreads */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%condiment%'
                      OR LOWER(COALESCE(category, '')) LIKE '%sauce%'
                      OR LOWER(COALESCE(category, '')) LIKE '%spread%'
                      OR LOWER(COALESCE(category, '')) LIKE '%spice%'
                      OR LOWER(COALESCE(category, '')) LIKE '%salt%'
                      OR LOWER(COALESCE(category, '')) LIKE '%sweetener%'
                      OR LOWER(COALESCE(category, '')) LIKE '%sugar%'
                      OR LOWER(COALESCE(category, '')) LIKE '%broth%'
                      OR LOWER(COALESCE(category, '')) LIKE '%seasoning%'
                      OR LOWER(COALESCE(category, '')) LIKE '%garlic%'
                      OR LOWER(COALESCE(category, '')) LIKE '%ginger%'
                      OR LOWER(COALESCE(category, '')) LIKE '%paprika%'
                      OR LOWER(COALESCE(category, '')) LIKE '%vanilla extract%'
                      OR LOWER(COALESCE(category, '')) LIKE '%jelly cup%'
                      OR LOWER(COALESCE(category, '')) LIKE '%mint jelly%'
                      OR LOWER(COALESCE(category, '')) LIKE '%tahini%'
                    THEN 'Condiments, Sauces & Spreads'

                    /* Dairy and eggs */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%dair%'
                      OR LOWER(COALESCE(category, '')) LIKE '%lait%'
                      OR LOWER(COALESCE(category, '')) LIKE '%fromage%'
                      OR LOWER(COALESCE(category, '')) LIKE '%cheese%'
                      OR LOWER(COALESCE(category, '')) LIKE '%milk%'
                      OR LOWER(COALESCE(category, '')) LIKE '%yogurt%'
                      OR LOWER(COALESCE(category, '')) LIKE '%yoghurt%'
                      OR LOWER(COALESCE(category, '')) LIKE '%cream%'
                      OR LOWER(COALESCE(category, '')) LIKE '%butter%'
                      OR LOWER(COALESCE(category, '')) LIKE '%egg%'
                      OR LOWER(COALESCE(category, '')) LIKE '%camembert%'
                    THEN 'Dairy & Eggs'

                    /* Breakfast cereals */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%breakfast%'
                      OR LOWER(COALESCE(category, '')) LIKE '%cereal%'
                      OR LOWER(COALESCE(category, '')) LIKE '%corn-flake%'
                      OR LOWER(COALESCE(category, '')) LIKE '%muesli%'
                      OR LOWER(COALESCE(category, '')) LIKE '%musli%'
                      OR LOWER(COALESCE(category, '')) LIKE '%porridge%'
                      OR LOWER(COALESCE(category, '')) LIKE '%oat%'
                    THEN 'Breakfast Cereals'

                    /* Salty snacks */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%salty snack%'
                      OR LOWER(COALESCE(category, '')) LIKE '%chips%'
                      OR LOWER(COALESCE(category, '')) LIKE '%crisps%'
                      OR LOWER(COALESCE(category, '')) LIKE '%crackers%'
                      OR LOWER(COALESCE(category, '')) LIKE '%popcorn%'
                      OR LOWER(COALESCE(category, '')) LIKE '%pea puffs%'
                      OR LOWER(COALESCE(category, '')) LIKE '%salty roasted peas%'
                    THEN 'Salty Snacks'

                    /* Bread and bakery */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%bread%'
                      OR LOWER(COALESCE(category, '')) LIKE '%bakery%'
                      OR LOWER(COALESCE(category, '')) LIKE '%wrap%'
                      OR LOWER(COALESCE(category, '')) LIKE '%naan%'
                      OR LOWER(COALESCE(category, '')) LIKE '%roti%'
                      OR LOWER(COALESCE(category, '')) LIKE '%taco shell%'
                    THEN 'Bread & Bakery'

                    /* Meat, fish, poultry */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%meat%'
                      OR LOWER(COALESCE(category, '')) LIKE '%chicken%'
                      OR LOWER(COALESCE(category, '')) LIKE '%fish%'
                      OR LOWER(COALESCE(category, '')) LIKE '%tuna%'
                      OR LOWER(COALESCE(category, '')) LIKE '%salmon%'
                      OR LOWER(COALESCE(category, '')) LIKE '%mackerel%'
                      OR LOWER(COALESCE(category, '')) LIKE '%bacon%'
                      OR LOWER(COALESCE(category, '')) LIKE '%pepperoni%'
                      OR LOWER(COALESCE(category, '')) LIKE '%pâté%'
                      OR LOWER(COALESCE(category, '')) LIKE '%beef%'
                    THEN 'Meat, Fish & Poultry'

                    /* Fruits and vegetables */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%fruit%'
                      OR LOWER(COALESCE(category, '')) LIKE '%vegetable%'
                      OR LOWER(COALESCE(category, '')) LIKE '%salad%'
                      OR LOWER(COALESCE(category, '')) LIKE '%tomato%'
                      OR LOWER(COALESCE(category, '')) LIKE '%beetroot%'
                      OR LOWER(COALESCE(category, '')) LIKE '%corn%'
                      OR LOWER(COALESCE(category, '')) LIKE '%carrot%'
                      OR LOWER(COALESCE(category, '')) LIKE '%cherries%'
                      OR LOWER(COALESCE(category, '')) LIKE '%apricot%'
                      OR LOWER(COALESCE(category, '')) LIKE '%olives%'
                      OR LOWER(COALESCE(category, '')) LIKE '%kalamata%'
                      OR LOWER(COALESCE(category, '')) LIKE '%capers%'
                      OR LOWER(COALESCE(category, '')) LIKE '%pickled%'
                    THEN 'Fruits & Vegetables'

                    /* Legumes and plant proteins */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%legume%'
                      OR LOWER(COALESCE(category, '')) LIKE '%bean%'
                      OR LOWER(COALESCE(category, '')) LIKE '%chickpea%'
                      OR LOWER(COALESCE(category, '')) LIKE '%lentil%'
                      OR LOWER(COALESCE(category, '')) LIKE '%tofu%'
                      OR LOWER(COALESCE(category, '')) LIKE '%falafel%'
                      OR LOWER(COALESCE(category, '')) LIKE '%plant protein%'
                      OR LOWER(COALESCE(category, '')) LIKE '%meat analogue%'
                      OR LOWER(COALESCE(category, '')) LIKE '%vegetarian ground%'
                    THEN 'Legumes & Plant Proteins'

                    /* Grains, pasta, rice */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%pasta%'
                      OR LOWER(COALESCE(category, '')) LIKE '%rice%'
                      OR LOWER(COALESCE(category, '')) LIKE '%quinoa%'
                      OR LOWER(COALESCE(category, '')) LIKE '%noodle%'
                      OR LOWER(COALESCE(category, '')) LIKE '%spaghetti%'
                      OR LOWER(COALESCE(category, '')) LIKE '%penne%'
                      OR LOWER(COALESCE(category, '')) LIKE '%gnocchi%'
                    THEN 'Grains, Pasta & Rice'

                    /* Oils and fats */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%oil%'
                      OR LOWER(COALESCE(category, '')) LIKE '%margarine%'
                      OR LOWER(COALESCE(category, '')) LIKE '%fat%'
                    THEN 'Oils & Fats'

                    /* Baby foods */
                    WHEN LOWER(COALESCE(category, '')) LIKE '%baby%'
                      OR LOWER(COALESCE(category, '')) LIKE '%toddler%'
                      OR LOWER(COALESCE(category, '')) LIKE '%aliments pour bébé%'
                    THEN 'Baby & Toddler Foods'

                    ELSE NULL
                END AS cleaned_category

            FROM packaged_products_enriched
        )

        SELECT
            cleaned_category AS category,
            COUNT(*) AS total_products,

            SUM(CASE WHEN has_added_sugar = 1 THEN 1 ELSE 0 END) AS added_sugar_count,
            SUM(CASE WHEN has_added_preservatives = 1 THEN 1 ELSE 0 END) AS preservatives_count,
            SUM(CASE WHEN has_food_color = 1 THEN 1 ELSE 0 END) AS food_color_count,

            SUM(COALESCE(sugar_detected_count, 0)) AS sugar_detected_total,
            SUM(COALESCE(preservative_detected_count, 0)) AS preservative_detected_total,
            SUM(COALESCE(color_detected_count, 0)) AS color_detected_total

        FROM cleaned_products

        WHERE cleaned_category IS NOT NULL
          AND cleaned_category <> ''
          AND cleaned_category <> 'Other'

        GROUP BY cleaned_category

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
            "It means this category may need closer label checking when choosing lunchbox items. "
            "Records such as supplements, alcohol, and unclear non-food products are excluded "
            "from this children-focused guide."
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