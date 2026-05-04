from sqlalchemy.orm import Session
from . import models, schemas


ALLOWED_CHILD_AGE_BANDS = {
    "5-6 years",
    "7-9 years",
    "10-12 years",
}


def validate_child_age_band(age_band: str):
    if age_band not in ALLOWED_CHILD_AGE_BANDS:
        raise ValueError(
            "LittleWell currently supports children aged 5-12 only. "
            "Allowed age bands: 5-6 years, 7-9 years, 10-12 years."
        )


def get_children(db: Session, user_id: int):
    return (
        db.query(models.UserChild)
        .filter(models.UserChild.user_id == user_id)
        .all()
    )


def get_child_by_id(db: Session, child_id: int, user_id: int):
    return (
        db.query(models.UserChild)
        .filter(
            models.UserChild.child_id == child_id,
            models.UserChild.user_id == user_id,
        )
        .first()
    )


def get_child_allergen_ids(db: Session, child_id: int, user_id: int):
    rows = (
        db.query(models.UserSearchAllergen)
        .filter(
            models.UserSearchAllergen.child_id == child_id,
            models.UserSearchAllergen.user_id == user_id,
        )
        .all()
    )

    return [row.allergen_id for row in rows]


def replace_child_allergens(
    db: Session,
    child_id: int,
    user_id: int,
    allergen_ids: list[int],
):
    db.query(models.UserSearchAllergen).filter(
        models.UserSearchAllergen.child_id == child_id,
        models.UserSearchAllergen.user_id == user_id,
    ).delete()

    for allergen_id in allergen_ids:
        db.add(
            models.UserSearchAllergen(
                user_id=user_id,
                child_id=child_id,
                allergen_id=allergen_id,
            )
        )


def create_child(db: Session, child: schemas.ChildCreate, user_id: int):
    validate_child_age_band(child.age_band)

    db_child = models.UserChild(
        user_id=user_id,
        child_name=child.child_name,
        age_band=child.age_band,
        band_id=child.band_id,
        iron_status=child.iron_status,
        calcium_status=child.calcium_status,
        vitamin_d_status=child.vitamin_d_status,
        variety_status=child.variety_status,
        restriction_id=child.restriction_id,
    )

    db.add(db_child)
    db.flush()

    for allergen_id in child.allergies:
        db.add(
            models.UserSearchAllergen(
                user_id=user_id,
                child_id=db_child.child_id,
                allergen_id=allergen_id,
            )
        )

    db.commit()
    db.refresh(db_child)
    return db_child


def update_child(
    db: Session,
    child_id: int,
    child: schemas.ChildUpdate,
    user_id: int,
):
    validate_child_age_band(child.age_band)

    db_child = get_child_by_id(db, child_id, user_id)

    if not db_child:
        return None

    db_child.child_name = child.child_name
    db_child.age_band = child.age_band
    db_child.band_id = child.band_id
    db_child.iron_status = child.iron_status
    db_child.calcium_status = child.calcium_status
    db_child.vitamin_d_status = child.vitamin_d_status
    db_child.variety_status = child.variety_status
    db_child.restriction_id = child.restriction_id

    replace_child_allergens(
        db=db,
        child_id=db_child.child_id,
        user_id=user_id,
        allergen_ids=child.allergies,
    )

    db.commit()
    db.refresh(db_child)
    return db_child


def delete_child(db: Session, child_id: int, user_id: int):
    db_child = get_child_by_id(db, child_id, user_id)

    if not db_child:
        return None

    db.query(models.UserSearchAllergen).filter(
        models.UserSearchAllergen.child_id == child_id,
        models.UserSearchAllergen.user_id == user_id,
    ).delete()

    db.delete(db_child)
    db.commit()

    return db_child