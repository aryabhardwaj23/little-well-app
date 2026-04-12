from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models
from typing import List

router = APIRouter(prefix="/products/recommended", tags=["recommendations"])


def build_lunchbox_from_product(product, child_name=None, support_type="general", nutrition_focus=None):
    if nutrition_focus is None:
        nutrition_focus = ["Balanced nutrition"]

    return {
        "id": str(product.product_id),
        "childName": child_name,
        "items": [
            {
                "name": product.name,
                "amount": product.serving_size or "1 serving",
                "image": "https://via.placeholder.com/300",
                "section": "protein",
            }
        ],
        "nutritionFocus": nutrition_focus,
        "whyThisMeal": f"{product.name} was selected based on the current nutrition and filtering rules.",
        "supportType": support_type,
    }


@router.get("")
def get_recommended_products(
    child_id: int,
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    child = db.query(models.UserChild).filter(models.UserChild.child_id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    query = db.query(models.PackagedProduct)

    if child.variety_status == "needs_support":
        query = query.filter(models.PackagedProduct.has_added_preservatives == 0)

    products = query.limit(6).all()

    needs_support = []
    if child.iron_status == "needs_support":
        needs_support.append("iron")
    if child.calcium_status == "needs_support":
        needs_support.append("calcium")
    if child.vitamin_d_status == "needs_support":
        needs_support.append("vitamin_d")
    if child.variety_status == "needs_support":
        needs_support.append("variety")

    lunchboxes = [
        build_lunchbox_from_product(
            product=p,
            child_name=child.child_name,
            support_type="general" if not needs_support else needs_support[0],
            nutrition_focus=[f"{n.replace('_', ' ').title()} Support" for n in needs_support] or ["Balanced nutrition"],
        )
        for p in products
    ]

    return {
        "needsSupport": needs_support,
        "lunchboxes": lunchboxes,
    }


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

    query = db.query(models.PackagedProduct).limit(6)
    products = query.all()

    combined_support = set()
    names = []

    for child in children:
        names.append(child.child_name)
        if child.iron_status == "needs_support":
            combined_support.add("iron")
        if child.calcium_status == "needs_support":
            combined_support.add("calcium")
        if child.vitamin_d_status == "needs_support":
            combined_support.add("vitamin_d")
        if child.variety_status == "needs_support":
            combined_support.add("variety")

    lunchboxes = [
        build_lunchbox_from_product(
            product=p,
            child_name=" + ".join(names),
            support_type="general",
            nutrition_focus=[f"{n.replace('_', ' ').title()} Support" for n in combined_support] or ["Balanced nutrition"],
        )
        for p in products
    ]

    return {
        "needsSupport": list(combined_support),
        "lunchboxes": lunchboxes,
    }


@router.get("/quick")
def get_quick_recommended_products(
    ageGroup: str,
    allergies: str = "",
    seasonal: bool = True,
    db: Session = Depends(get_db),
):
    allergy_list = [a.strip() for a in allergies.split(",") if a.strip()]

    query = db.query(models.PackagedProduct)


    products = query.limit(6).all()

    lunchboxes = [
        build_lunchbox_from_product(
            product=p,
            child_name=None,
            support_type="general",
            nutrition_focus=["Balanced nutrition"],
        )
        for p in products
    ]

    return {
        "needsSupport": [],
        "lunchboxes": lunchboxes,
        "quickInput": {
            "ageGroup": ageGroup,
            "allergies": allergy_list,
            "seasonal": seasonal,
        },
    }