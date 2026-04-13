from datetime import date
import random

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from .. import models

router = APIRouter(prefix="/products/recommended", tags=["recommendations"])


# ---------- helpers ----------

def get_current_season_name() -> str:
    month = date.today().month
    if month in [9, 10, 11]:
        return "spring"
    if month in [12, 1, 2]:
        return "summer"
    if month in [3, 4, 5]:
        return "autumn"
    return "winter"


def get_needs_support(child) -> list[str]:
    needs = []
    if int(child.iron_status or 0) == 1:
        needs.append("iron")
    if int(child.calcium_status or 0) == 1:
        needs.append("calcium")
    if int(child.vitamin_d_status or 0) == 1:
        needs.append("vitamin_d")
    if int(child.variety_status or 0) == 1:
        needs.append("variety")
    return needs


def focus_labels(needs: list[str]) -> list[str]:
    if not needs:
        return ["Balanced nutrition"]
    return [f"{n.replace('_', ' ').title()} Support" for n in needs]


def product_text(product) -> str:
    parts = [
        product.name or "",
        product.brand or "",
        product.category or "",
        product.ingredients_list or "",
    ]
    return " ".join(parts).lower()


def is_valid_product_name(name: str | None) -> bool:
    if not name:
        return False

    cleaned = name.strip()
    if len(cleaned) < 3:
        return False

    if cleaned.lower() in {"a", "n/a", "unknown", "test"}:
        return False

    return True


def score_product_for_slot(product, slot: str, needs: list[str]) -> int:
    text = product_text(product)
    score = 0

    # Generic quality filters
    if int(product.has_added_preservatives or 0) == 0:
        score += 1
    if int(product.has_added_sugar or 0) == 0:
        score += 1
    if int(product.has_food_color or 0) == 0:
        score += 1

    # Slot-based heuristics
    if slot == "protein":
        keywords = [
            "protein", "peanut butter", "nut butter", "tofu", "beans",
            "lentil", "chickpea", "yogurt", "milk", "cheese", "egg"
        ]
        if any(k in text for k in keywords):
            score += 6

    elif slot == "carbs":
        keywords = [
            "bread", "rice", "oat", "cracker", "cereal", "wrap",
            "pasta", "grain", "wholegrain", "whole grain"
        ]
        if any(k in text for k in keywords):
            score += 6

    # Nutrition support heuristics
    if "iron" in needs:
        iron_keywords = ["iron", "protein", "beans", "lentil", "chickpea", "peanut butter"]
        if any(k in text for k in iron_keywords):
            score += 3

    if "calcium" in needs:
        calcium_keywords = ["calcium", "milk", "cheese", "yogurt"]
        if any(k in text for k in calcium_keywords):
            score += 3

    if "vitamin_d" in needs:
        vitamin_d_keywords = ["vitamin d", "fortified", "milk", "egg"]
        if any(k in text for k in vitamin_d_keywords):
            score += 2

    if "variety" in needs:
        if int(product.has_added_preservatives or 0) == 0:
            score += 2
        if int(product.has_food_color or 0) == 0:
            score += 2

    return score


def get_child_allergen_ids(db: Session, child_id: int) -> list[int]:
    rows = (
        db.query(models.UserSearchAllergen)
        .filter(models.UserSearchAllergen.child_id == child_id)
        .all()
    )
    return [int(row.allergen_id) for row in rows]


def get_blocked_product_ids_by_allergens(db: Session, allergen_ids: list[int]) -> set[int]:
    if not allergen_ids:
        return set()

    rows = (
        db.query(models.ProductAllergen)
        .filter(models.ProductAllergen.allergen_id.in_(allergen_ids))
        .all()
    )
    return {int(row.product_id) for row in rows}


def get_candidate_products(db: Session, blocked_product_ids: set[int]) -> list:
    query = db.query(models.PackagedProduct)

    if blocked_product_ids:
        query = query.filter(~models.PackagedProduct.product_id.in_(blocked_product_ids))

    # 多取一点，方便随机
    products = query.limit(300).all()

    cleaned = []
    for p in products:
        if not is_valid_product_name(p.name):
            continue
        cleaned.append(p)

    return cleaned


def get_seasonal_items(db: Session, seasonal: bool = True):
    current_season = get_current_season_name()

    query = db.query(models.SeasonalProduce)

    if seasonal:
        season_row = (
            db.query(models.Season)
            .filter(func.lower(models.Season.season) == current_season)
            .first()
        )
        if season_row:
            query = query.filter(models.SeasonalProduce.season_id == season_row.season_id)

    rows = query.limit(200).all()

    fruits = []
    veggies = []

    for row in rows:
        ptype = (row.produce_type or "").lower()
        name = row.produce_name or ""

        if not is_valid_product_name(name):
            continue

        if "fruit" in ptype:
            fruits.append(name)
        elif "veg" in ptype or "vegetable" in ptype:
            veggies.append(name)

    return fruits, veggies


def fallback_fruits():
    return ["Gala Apple", "Banana", "Pear", "Mandarin"]


def fallback_veggies():
    return ["Carrot Sticks", "Cucumber", "Buk Choy", "Baby Broccoli"]


def make_item(name: str, amount: str, section: str):
    return {
        "name": name,
        "amount": amount,
        # 改成本地图，避免外部 placeholder 连接失败
        "image": "/placeholder-lunchbox.png",
        "section": section,
    }


def build_lunchbox(
    child_name: str | None,
    lunchbox_id: str,
    protein_product,
    carb_product,
    fruit_name: str,
    veg_name: str,
    needs: list[str],
):
    support_type = needs[0] if needs else "general"

    items = []

    if protein_product:
        items.append(
            make_item(
                name=protein_product.name,
                amount=protein_product.serving_size or "1 serving",
                section="protein",
            )
        )

    if carb_product:
        items.append(
            make_item(
                name=carb_product.name,
                amount=carb_product.serving_size or "1 serving",
                section="carbs",
            )
        )

    items.append(make_item(name=fruit_name, amount="1 serving", section="fruit"))
    items.append(make_item(name=veg_name, amount="1 serving", section="veggies"))

    return {
        "id": lunchbox_id,
        "childName": child_name,
        "items": items,
        "nutritionFocus": focus_labels(needs),
        "whyThisMeal": "This lunchbox combines a protein item, a carbohydrate item, and seasonal fruit and vegetables filtered by the child's needs.",
        "supportType": support_type,
    }


def get_randomised_candidates(products: list, slot: str, needs: list[str], top_n: int = 20) -> list:
    """
    先按分数排序，再从前 top_n 名里随机打乱。
    这样既不会完全乱推，也不会每次都一模一样。
    """
    ranked = sorted(
        products,
        key=lambda p: score_product_for_slot(p, slot, needs),
        reverse=True,
    )

    shortlisted = ranked[:top_n]
    random.shuffle(shortlisted)
    return shortlisted


def pick_next_unused(candidates: list, used_ids: set[int]):
    for p in candidates:
        pid = int(p.product_id)
        if pid not in used_ids:
            used_ids.add(pid)
            return p
    return None


def generate_lunchboxes_for_child(db: Session, child, seasonal: bool = True, max_boxes: int = 3):
    needs = get_needs_support(child)
    allergen_ids = get_child_allergen_ids(db, child.child_id)
    blocked_product_ids = get_blocked_product_ids_by_allergens(db, allergen_ids)

    products = get_candidate_products(db, blocked_product_ids)
    fruits, veggies = get_seasonal_items(db, seasonal=seasonal)

    if not fruits:
        fruits = fallback_fruits()
    if not veggies:
        veggies = fallback_veggies()

    lunchboxes = []
    used_ids = set()

    # 每次请求都重新随机一批候选
    protein_candidates = get_randomised_candidates(products, "protein", needs, top_n=20)
    carb_candidates = get_randomised_candidates(products, "carbs", needs, top_n=20)

    for i in range(max_boxes):
        protein_product = pick_next_unused(protein_candidates, used_ids)
        carb_product = pick_next_unused(carb_candidates, used_ids)

        if not protein_product and not carb_product:
            break

        fruit_name = random.choice(fruits)
        veg_name = random.choice(veggies)

        lunchboxes.append(
            build_lunchbox(
                child_name=child.child_name,
                lunchbox_id=f"{child.child_id}-box-{i + 1}",
                protein_product=protein_product,
                carb_product=carb_product,
                fruit_name=fruit_name,
                veg_name=veg_name,
                needs=needs,
            )
        )

    return {
        "needsSupport": needs,
        "lunchboxes": lunchboxes,
    }


# ---------- routes ----------

@router.get("")
def get_recommended_products(
    child_id: int,
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    child = db.query(models.UserChild).filter(models.UserChild.child_id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    return generate_lunchboxes_for_child(
        db=db,
        child=child,
        seasonal=seasonal,
        max_boxes=3,
    )


@router.get("/family")
def get_family_recommended_products(
    child_ids: str = Query(...),
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    ids = [int(x) for x in child_ids.split(",") if x.strip()]
    children = db.query(models.UserChild).filter(models.UserChild.child_id.in_(ids)).all()

    if not children:
        raise HTTPException(status_code=404, detail="No children found")

    # family mode: merge support flags
    class FamilyChild:
        pass

    family = FamilyChild()
    family.child_id = ids[0]
    family.child_name = " + ".join([c.child_name for c in children])
    family.iron_status = 1 if any(int(c.iron_status or 0) == 1 for c in children) else 0
    family.calcium_status = 1 if any(int(c.calcium_status or 0) == 1 for c in children) else 0
    family.vitamin_d_status = 1 if any(int(c.vitamin_d_status or 0) == 1 for c in children) else 0
    family.variety_status = 1 if any(int(c.variety_status or 0) == 1 for c in children) else 0

    return generate_lunchboxes_for_child(
        db=db,
        child=family,
        seasonal=seasonal,
        max_boxes=3,
    )


@router.get("/quick")
def get_quick_recommended_products(
    ageGroup: str,
    allergies: str = "",
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    allergy_list = [a.strip() for a in allergies.split(",") if a.strip()]

    fruits, veggies = get_seasonal_items(db, seasonal=seasonal)
    if not fruits:
        fruits = fallback_fruits()
    if not veggies:
        veggies = fallback_veggies()

    # quick mode 暂时不做 allergens -> product 过滤
    products = get_candidate_products(db, blocked_product_ids=set())

    protein_candidates = get_randomised_candidates(products, "protein", [], top_n=20)
    carb_candidates = get_randomised_candidates(products, "carbs", [], top_n=20)

    lunchboxes = []
    used_ids = set()

    for i in range(3):
        protein_product = pick_next_unused(protein_candidates, used_ids)
        carb_product = pick_next_unused(carb_candidates, used_ids)

        if not protein_product and not carb_product:
            break

        fruit_name = random.choice(fruits)
        veg_name = random.choice(veggies)

        lunchboxes.append(
            build_lunchbox(
                child_name=None,
                lunchbox_id=f"quick-box-{i + 1}",
                protein_product=protein_product,
                carb_product=carb_product,
                fruit_name=fruit_name,
                veg_name=veg_name,
                needs=[],
            )
        )

    return {
        "needsSupport": [],
        "lunchboxes": lunchboxes,
        "quickInput": {
            "ageGroup": ageGroup,
            "allergies": allergy_list,
            "seasonal": seasonal,
        },
    }