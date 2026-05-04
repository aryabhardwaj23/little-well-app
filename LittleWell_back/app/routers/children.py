from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..auth_utils import get_current_user
from .. import crud, schemas, models


router = APIRouter(prefix="/children", tags=["children"])


def get_restriction_info(db: Session, restriction_id: int | None):
    if not restriction_id:
        return None

    return (
        db.query(models.DietaryRestriction)
        .filter(models.DietaryRestriction.restriction_id == restriction_id)
        .filter(models.DietaryRestriction.is_active == 1)
        .first()
    )


def build_child_response(
    db: Session,
    child,
    user_id: int,
) -> schemas.ChildResponse:
    allergies = crud.get_child_allergen_ids(
        db=db,
        child_id=child.child_id,
        user_id=user_id,
    )

    restriction = get_restriction_info(db, child.restriction_id)

    return schemas.ChildResponse(
        child_id=child.child_id,
        user_id=child.user_id,
        child_name=child.child_name,
        age_band=child.age_band,
        band_id=child.band_id,
        iron_status=child.iron_status,
        calcium_status=child.calcium_status,
        vitamin_d_status=child.vitamin_d_status,
        variety_status=child.variety_status,
        restriction_id=child.restriction_id,
        restriction_code=restriction.restriction_code if restriction else None,
        restriction_name=restriction.restriction_name if restriction else None,
        allergies=allergies,
    )


@router.get("", response_model=list[schemas.ChildResponse])
def read_children(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    children = crud.get_children(
        db=db,
        user_id=current_user.user_id,
    )

    return [
        build_child_response(
            db=db,
            child=child,
            user_id=current_user.user_id,
        )
        for child in children
    ]


@router.get("/{child_id}", response_model=schemas.ChildResponse)
def read_child(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    child = crud.get_child_by_id(
        db=db,
        child_id=child_id,
        user_id=current_user.user_id,
    )

    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    return build_child_response(
        db=db,
        child=child,
        user_id=current_user.user_id,
    )


@router.post("", response_model=schemas.ChildResponse)
def create_child(
    child: schemas.ChildCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_child = crud.create_child(
        db=db,
        child=child,
        user_id=current_user.user_id,
    )

    return build_child_response(
        db=db,
        child=new_child,
        user_id=current_user.user_id,
    )


@router.put("/{child_id}", response_model=schemas.ChildResponse)
def update_child(
    child_id: int,
    child: schemas.ChildUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    updated_child = crud.update_child(
        db=db,
        child_id=child_id,
        child=child,
        user_id=current_user.user_id,
    )

    if not updated_child:
        raise HTTPException(status_code=404, detail="Child not found")

    return build_child_response(
        db=db,
        child=updated_child,
        user_id=current_user.user_id,
    )


@router.delete("/{child_id}")
def delete_child(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    deleted_child = crud.delete_child(
        db=db,
        child_id=child_id,
        user_id=current_user.user_id,
    )

    if not deleted_child:
        raise HTTPException(status_code=404, detail="Child not found")

    return {
        "message": "Child deleted successfully",
        "child_id": child_id,
    }