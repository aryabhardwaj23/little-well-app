from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..db import get_db
from ..auth_utils import get_current_user
from ..models import (
    User,
    UserChild,
    WeeklyPlan,
    WeeklyPlanChild,
    WeeklyPlanMeal,
)
from ..schemas import (
    WeeklyPlanCreate,
    WeeklyPlanResponse,
    WeeklyPlanGenerateRequest,
    WeeklyPlanGenerateResponse,
)
from ..routers.recommendations import generate_lunchboxes_for_child
from ..services.mealdb_service import find_best_recipe_for_lunchbox

router = APIRouter(prefix="/weekly-plans", tags=["weekly-plans"])


def normalize_cook_frequency(value) -> int:
    if value is None:
        return 2

    if isinstance(value, int):
        return value

    text = str(value).strip().lower()

    mapping = {
        "once": 1,
        "1": 1,

        "twice": 2,
        "two": 2,
        "2": 2,
        "2 times": 2,
        "2 times per week": 2,

        "three_times": 3,
        "three": 3,
        "3": 3,
        "3 times": 3,
        "3 times per week": 3,

        "daily": 5,
        "five": 5,
        "5": 5,
        "5 times": 5,
        "5 times per week": 5,
    }

    return mapping.get(text, 2)


def cook_frequency_to_db_value(value: int) -> str:
    mapping = {
        1: "once",
        2: "twice",
        3: "three_times",
        5: "daily",
    }

    return mapping.get(value, "twice")


def variety_to_db_value(value) -> str:
    if not value:
        return "medium"

    text = str(value).strip().lower()

    mapping = {
        "keep it simple": "low",
        "simple": "low",
        "low": "low",

        "balanced": "medium",
        "medium": "medium",

        "more variety": "high",
        "high": "high",
    }

    return mapping.get(text, "medium")


def meal_style_to_db_value(value) -> str:
    if not value:
        return "mixed"

    text = str(value).strip().lower()

    mapping = {
        "quick & simple": "traditional",
        "quick and simple": "traditional",
        "simple": "traditional",
        "traditional": "traditional",

        "mix of simple and varied": "mixed",
        "mixed": "mixed",

        "asian": "asian",
        "mediterranean": "mediterranean",
        "vegetarian": "vegetarian",
    }

    return mapping.get(text, "mixed")


def cook_day_to_db_value(value) -> str:
    if not value:
        return "Monday"

    text = str(value).strip()
    text = text.replace("Cook on ", "").strip()

    valid_days = {
        "monday": "Monday",
        "tuesday": "Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
        "sunday": "Sunday",
    }

    return valid_days.get(text.lower(), "Monday")


def pydantic_to_dict(item):
    """
    Supports both Pydantic v1 and v2.
    v2 uses model_dump(), v1 uses dict().
    """
    if hasattr(item, "model_dump"):
        return item.model_dump()

    return item.dict()


def get_cover_text(frequency: int, index: int) -> str:
    covers = {
        2: ["Monday to Wednesday", "Thursday to Friday"],
        3: ["Monday to Tuesday", "Wednesday to Thursday", "Friday"],
        5: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    }

    cover_list = covers.get(frequency, ["Selected days"])

    if index < len(cover_list):
        return cover_list[index]

    return "Selected days"


def get_cook_title(frequency: int, index: int) -> str:
    titles = {
        2: ["Cook on Sunday", "Cook on Wednesday"],
        3: ["Cook on Sunday", "Cook on Tuesday", "Cook on Thursday"],
        5: [
            "Cook on Monday",
            "Cook on Tuesday",
            "Cook on Wednesday",
            "Cook on Thursday",
            "Cook on Friday",
        ],
    }

    title_list = titles.get(frequency, [f"Cook Session {index + 1}"])

    if index < len(title_list):
        return title_list[index]

    return f"Cook Session {index + 1}"


def get_prep_time(frequency: int, index: int) -> str:
    """
    Return varied prep time text for UI.
    This prevents every generated batch from showing the same prep value.
    """
    if frequency == 5:
        times = ["20 mins", "22 mins", "18 mins", "25 mins", "20 mins"]
    elif frequency == 3:
        times = ["30 mins", "35 mins", "28 mins"]
    else:
        times = ["40 mins", "35 mins"]

    return times[index % len(times)]


def get_storage_tip(frequency: int, index: int) -> str:
    """
    Return varied storage tips for UI.
    This prevents every generated batch from showing the same storage message.
    """
    if frequency == 5:
        tips = [
            "Prepare fresh and keep chilled until lunch.",
            "Store in an airtight container and keep cold with an ice pack.",
            "Pack wet ingredients separately to keep the lunchbox fresh.",
            "Refrigerate overnight and avoid leaving it at room temperature.",
            "Use a sealed lunchbox and eat within the school day.",
        ]
    elif frequency == 3:
        tips = [
            "Cook in batch, portion safely, and store in the fridge.",
            "Keep refrigerated and use within two school days.",
            "Store sauce or dressing separately to avoid soggy food.",
        ]
    else:
        tips = [
            "Batch cook, portion safely, and refrigerate.",
            "Use airtight containers and reheat only when needed.",
        ]

    return tips[index % len(tips)]


def get_season_name_from_id(season_id: int | None) -> str:
    mapping = {
        1: "Spring",
        2: "Summer",
        3: "Autumn",
        4: "Winter",
    }

    return mapping.get(season_id, "Seasonal")


def build_plan_response(db: Session, plan: WeeklyPlan, user_id: int) -> dict:
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
            .filter(
                UserChild.child_id.in_(child_ids),
                UserChild.user_id == user_id,
            )
            .all()
        )

        child_info_map = {
            child.child_id: child
            for child in child_rows
        }

        children = [
            {
                "child_id": child_id,
                "child_name": (
                    child_info_map[child_id].child_name
                    if child_id in child_info_map
                    else f"Child #{child_id}"
                ),
                "restriction_id": (
                    child_info_map[child_id].restriction_id
                    if child_id in child_info_map
                    else None
                ),
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
        "cook_frequency": normalize_cook_frequency(plan.cook_frequency),
        "variety_preference": plan.variety_preference,
        "meal_style": plan.meal_style,
        "season_id": plan.season_id,
        "status": plan.status,
        "created_at": plan.created_at,
        "updated_at": plan.updated_at,
        "children": children,
        "meals": meals,
    }


@router.post("/generate", response_model=WeeklyPlanGenerateResponse)
async def generate_weekly_plan(
    payload: WeeklyPlanGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.user_id

    if not payload.child_ids:
        raise HTTPException(
            status_code=400,
            detail="At least one child must be selected.",
        )

    frequency = normalize_cook_frequency(payload.cook_frequency)

    if frequency not in {2, 3, 5}:
        raise HTTPException(
            status_code=400,
            detail="cook_frequency must be 2, 3, or 5.",
        )

    children = (
        db.query(UserChild)
        .filter(
            UserChild.child_id.in_(payload.child_ids),
            UserChild.user_id == user_id,
        )
        .all()
    )

    found_child_ids = {child.child_id for child in children}

    missing_child_ids = [
        child_id
        for child_id in payload.child_ids
        if child_id not in found_child_ids
    ]

    if missing_child_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Child profile(s) not found or not owned by this user: {missing_child_ids}",
        )

    if not children:
        raise HTTPException(
            status_code=404,
            detail="No children found.",
        )

    all_lunchboxes = []

    if len(children) == 1:
        result = generate_lunchboxes_for_child(
            db=db,
            child=children[0],
            seasonal=payload.seasonal,
            max_boxes=frequency,
            user_id=user_id,
        )

        all_lunchboxes = result.get("lunchboxes", [])

    else:
        class FamilyChild:
            pass

        family = FamilyChild()
        family.child_id = children[0].child_id
        family.child_name = " + ".join([child.child_name for child in children])
        family.age_band = children[0].age_band

        family.iron_status = (
            1
            if any(int(child.iron_status or 0) == 1 for child in children)
            else 0
        )

        family.calcium_status = (
            1
            if any(int(child.calcium_status or 0) == 1 for child in children)
            else 0
        )

        family.vitamin_d_status = (
            1
            if any(int(child.vitamin_d_status or 0) == 1 for child in children)
            else 0
        )

        family.variety_status = (
            1
            if any(int(child.variety_status or 0) == 1 for child in children)
            else 0
        )

        family.restriction_id = children[0].restriction_id

        result = generate_lunchboxes_for_child(
            db=db,
            child=family,
            seasonal=payload.seasonal,
            max_boxes=frequency,
            user_id=user_id,
        )

        all_lunchboxes = result.get("lunchboxes", [])

    if not all_lunchboxes:
        raise HTTPException(
            status_code=500,
            detail="Could not generate lunchbox recommendations.",
        )

    used_recipe_ids = set()
    batches = []
    season_name = get_season_name_from_id(payload.season_id)

    for index in range(frequency):
        lunchbox = all_lunchboxes[index % len(all_lunchboxes)]

        recipe = await find_best_recipe_for_lunchbox(
            lunchbox=lunchbox,
            used_recipe_ids=used_recipe_ids,
        )

        if recipe.get("id"):
            used_recipe_ids.add(str(recipe["id"]))

        batches.append(
            {
                "id": f"batch-{index + 1}",
                "cookDay": get_cook_title(frequency, index),
                "coverDays": get_cover_text(frequency, index),
                "prepTime": get_prep_time(frequency, index),
                "seasonalNote": f"{season_name} ingredients are prioritised where available.",
                "storageTip": get_storage_tip(frequency, index),
                "lunchbox": lunchbox,
                "recipe": recipe,
            }
        )

    return {
        "child_ids": payload.child_ids,
        "cook_frequency": frequency,
        "season_id": payload.season_id,
        "batches": batches,
    }


@router.post("", response_model=WeeklyPlanResponse)
def create_weekly_plan(
    payload: WeeklyPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.user_id

    if not payload.child_ids:
        raise HTTPException(
            status_code=400,
            detail="At least one child must be selected.",
        )

    valid_children = (
        db.query(UserChild)
        .filter(
            UserChild.child_id.in_(payload.child_ids),
            UserChild.user_id == user_id,
        )
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
            detail=f"Child profile(s) not found or not owned by this user: {missing_child_ids}",
        )

    plan = WeeklyPlan(
        user_id=user_id,
        plan_name=payload.plan_name,
        cook_frequency=cook_frequency_to_db_value(payload.cook_frequency),
        variety_preference=variety_to_db_value(payload.variety_preference),
        meal_style=meal_style_to_db_value(payload.meal_style),
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
                cook_day=cook_day_to_db_value(meal.cook_day),
                cover_days=meal.cover_days,
                meal_title=meal.meal_title,

                lunchbox_items=[
                    pydantic_to_dict(item)
                    for item in meal.lunchbox_items
                ] if meal.lunchbox_items else [],

                servings=meal.servings or 1,
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

    return build_plan_response(db, plan, user_id)


@router.get("", response_model=list[WeeklyPlanResponse])
def get_weekly_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.user_id

    plans = (
        db.query(WeeklyPlan)
        .filter(WeeklyPlan.user_id == user_id)
        .order_by(desc(WeeklyPlan.created_at))
        .all()
    )

    return [build_plan_response(db, plan, user_id) for plan in plans]


@router.get("/{plan_id}", response_model=WeeklyPlanResponse)
def get_weekly_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.user_id

    plan = (
        db.query(WeeklyPlan)
        .filter(
            WeeklyPlan.plan_id == plan_id,
            WeeklyPlan.user_id == user_id,
        )
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Weekly plan not found.",
        )

    return build_plan_response(db, plan, user_id)


@router.delete("/{plan_id}", status_code=204)
def delete_weekly_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.user_id

    plan = (
        db.query(WeeklyPlan)
        .filter(
            WeeklyPlan.plan_id == plan_id,
            WeeklyPlan.user_id == user_id,
        )
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
def duplicate_weekly_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.user_id

    old_plan = (
        db.query(WeeklyPlan)
        .filter(
            WeeklyPlan.plan_id == plan_id,
            WeeklyPlan.user_id == user_id,
        )
        .first()
    )

    if not old_plan:
        raise HTTPException(
            status_code=404,
            detail="Weekly plan not found.",
        )

    new_plan = WeeklyPlan(
        user_id=user_id,
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
        child_belongs_to_user = (
            db.query(UserChild)
            .filter(
                UserChild.child_id == child.child_id,
                UserChild.user_id == user_id,
            )
            .first()
        )

        if child_belongs_to_user:
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

                lunchbox_items=meal.lunchbox_items or [],

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

    return build_plan_response(db, new_plan, user_id)