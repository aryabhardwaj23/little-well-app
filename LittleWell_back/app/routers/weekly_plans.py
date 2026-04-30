from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..db import get_db
from ..models import (
    UserSearch,
    UserChild,
    WeeklyPlan,
    WeeklyPlanChild,
    WeeklyPlanMeal,
)
from ..schemas import WeeklyPlanCreate, WeeklyPlanResponse


router = APIRouter(prefix="/weekly-plans", tags=["weekly-plans"])


def get_or_create_demo_user(db: Session) -> int:
    user = db.query(UserSearch).order_by(UserSearch.user_id.asc()).first()

    if user:
        return user.user_id

    user = UserSearch()
    db.add(user)
    db.commit()
    db.refresh(user)

    return user.user_id


def build_plan_response(db: Session, plan: WeeklyPlan) -> dict:
    child_links = (
        db.query(WeeklyPlanChild)
        .filter(WeeklyPlanChild.plan_id == plan.plan_id)
        .all()
    )

    child_ids = [link.child_id for link in child_links]

    children = []

    if child_ids:
        child_rows = (
            db.query(UserChild)
            .filter(UserChild.child_id.in_(child_ids))
            .all()
        )

        child_name_map = {
            child.child_id: child.child_name
            for child in child_rows
        }

        children = [
            {
                "child_id": child_id,
                "child_name": child_name_map.get(child_id, f"Child #{child_id}"),
            }
            for child_id in child_ids
        ]

    meals = (
        db.query(WeeklyPlanMeal)
        .filter(WeeklyPlanMeal.plan_id == plan.plan_id)
        .order_by(WeeklyPlanMeal.meal_id.asc())
        .all()
    )

    return {
        "plan_id": plan.plan_id,
        "user_id": plan.user_id,
        "plan_name": plan.plan_name,
        "cook_frequency": plan.cook_frequency,
        "variety_preference": plan.variety_preference,
        "meal_style": plan.meal_style,
        "season_id": plan.season_id,
        "status": plan.status,
        "created_at": plan.created_at,
        "updated_at": plan.updated_at,
        "children": children,
        "meals": meals,
    }


@router.post("", response_model=WeeklyPlanResponse)
def create_weekly_plan(payload: WeeklyPlanCreate, db: Session = Depends(get_db)):
    user_id = get_or_create_demo_user(db)

    if not payload.child_ids:
        raise HTTPException(
            status_code=400,
            detail="At least one child must be selected.",
        )

    valid_children = (
        db.query(UserChild)
        .filter(UserChild.child_id.in_(payload.child_ids))
        .all()
    )

    valid_child_ids = {child.child_id for child in valid_children}

    missing_child_ids = [
        child_id
        for child_id in payload.child_ids
        if child_id not in valid_child_ids
    ]

    if missing_child_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Child profile(s) not found: {missing_child_ids}",
        )

    plan = WeeklyPlan(
        user_id=user_id,
        plan_name=payload.plan_name,
        cook_frequency=payload.cook_frequency,
        variety_preference=payload.variety_preference,
        meal_style=payload.meal_style,
        season_id=payload.season_id,
        status=payload.status or "active",
    )

    db.add(plan)
    db.flush()

    for child_id in payload.child_ids:
        db.add(
            WeeklyPlanChild(
                plan_id=plan.plan_id,
                child_id=child_id,
            )
        )

    for meal in payload.meals:
        db.add(
            WeeklyPlanMeal(
                plan_id=plan.plan_id,
                reference_food_id=meal.reference_food_id,
                cook_day=meal.cook_day,
                cover_days=meal.cover_days,
                meal_title=meal.meal_title,
                servings=meal.servings,
                prep_time_minutes=meal.prep_time_minutes,
                nutrition_tags=meal.nutrition_tags,
                seasonal_note=meal.seasonal_note,
                storage_tip=meal.storage_tip,
                recipe_id=meal.recipe_id,
                image_url=meal.image_url,
            )
        )

    db.commit()
    db.refresh(plan)

    return build_plan_response(db, plan)


@router.get("", response_model=list[WeeklyPlanResponse])
def get_weekly_plans(db: Session = Depends(get_db)):
    user_id = get_or_create_demo_user(db)

    plans = (
        db.query(WeeklyPlan)
        .filter(WeeklyPlan.user_id == user_id)
        .order_by(desc(WeeklyPlan.created_at))
        .all()
    )

    return [build_plan_response(db, plan) for plan in plans]


@router.get("/{plan_id}", response_model=WeeklyPlanResponse)
def get_weekly_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = (
        db.query(WeeklyPlan)
        .filter(WeeklyPlan.plan_id == plan_id)
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Weekly plan not found.",
        )

    return build_plan_response(db, plan)


@router.delete("/{plan_id}", status_code=204)
def delete_weekly_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = (
        db.query(WeeklyPlan)
        .filter(WeeklyPlan.plan_id == plan_id)
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Weekly plan not found.",
        )

    db.delete(plan)
    db.commit()

    return None


@router.post("/{plan_id}/duplicate", response_model=WeeklyPlanResponse)
def duplicate_weekly_plan(plan_id: int, db: Session = Depends(get_db)):
    old_plan = (
        db.query(WeeklyPlan)
        .filter(WeeklyPlan.plan_id == plan_id)
        .first()
    )

    if not old_plan:
        raise HTTPException(
            status_code=404,
            detail="Weekly plan not found.",
        )

    new_plan = WeeklyPlan(
        user_id=old_plan.user_id,
        plan_name=f"{old_plan.plan_name} Copy",
        cook_frequency=old_plan.cook_frequency,
        variety_preference=old_plan.variety_preference,
        meal_style=old_plan.meal_style,
        season_id=old_plan.season_id,
        status="active",
    )

    db.add(new_plan)
    db.flush()

    old_children = (
        db.query(WeeklyPlanChild)
        .filter(WeeklyPlanChild.plan_id == old_plan.plan_id)
        .all()
    )

    for child in old_children:
        db.add(
            WeeklyPlanChild(
                plan_id=new_plan.plan_id,
                child_id=child.child_id,
            )
        )

    old_meals = (
        db.query(WeeklyPlanMeal)
        .filter(WeeklyPlanMeal.plan_id == old_plan.plan_id)
        .order_by(WeeklyPlanMeal.meal_id.asc())
        .all()
    )

    for meal in old_meals:
        db.add(
            WeeklyPlanMeal(
                plan_id=new_plan.plan_id,
                reference_food_id=meal.reference_food_id,
                cook_day=meal.cook_day,
                cover_days=meal.cover_days,
                meal_title=meal.meal_title,
                servings=meal.servings,
                prep_time_minutes=meal.prep_time_minutes,
                nutrition_tags=meal.nutrition_tags,
                seasonal_note=meal.seasonal_note,
                storage_tip=meal.storage_tip,
                recipe_id=meal.recipe_id,
                image_url=meal.image_url,
            )
        )

    db.commit()
    db.refresh(new_plan)

    return build_plan_response(db, new_plan)