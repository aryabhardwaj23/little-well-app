from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..auth_utils import get_current_user
from .. import models
from ..services.knowledge_service import (
    get_user_children_with_serves,
    get_food_group_guide,
    get_additive_awareness_guide,
)

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/serves/children")
def read_children_serves(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return {
        "children": get_user_children_with_serves(
            db=db,
            user_id=current_user.user_id,
        )
    }


@router.get("/food-groups")
def read_food_group_guide(
    db: Session = Depends(get_db),
):
    return {
        "food_groups": get_food_group_guide(db)
    }


@router.get("/additive-awareness")
def read_additive_awareness(
    db: Session = Depends(get_db),
):
    return get_additive_awareness_guide(db)


@router.get("/additive-heatmap")
def read_additive_heatmap(
    db: Session = Depends(get_db),
):
    return get_additive_awareness_guide(db)