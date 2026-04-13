from sqlalchemy.orm import Session
from . import models, schemas


def get_children(db: Session):
    return db.query(models.UserChild).all()


def get_child_by_id(db: Session, child_id: int):
    return db.query(models.UserChild).filter(models.UserChild.child_id == child_id).first()


def create_child(db: Session, child: schemas.ChildCreate):

    new_user = models.UserSearch()
    db.add(new_user)
    db.flush()  

    db_child = models.UserChild(
        user_id=new_user.user_id,
        child_name=child.child_name,
        age_band=child.age_band,
        band_id=child.band_id,
        iron_status=child.iron_status,
        calcium_status=child.calcium_status,
        vitamin_d_status=child.vitamin_d_status,
        variety_status=child.variety_status,
        religious_needs=child.religious_needs,
    )
    db.add(db_child)
    db.flush() 

    for allergen_id in child.allergies:
        db_link = models.UserSearchAllergen(
            user_id=new_user.user_id,
            child_id=db_child.child_id,
            allergen_id=allergen_id,
        )
        db.add(db_link)

    db.commit()
    db.refresh(db_child)
    return db_child


def update_child(db: Session, child_id: int, child: schemas.ChildUpdate):
    db_child = get_child_by_id(db, child_id)
    if not db_child:
        return None

    db_child.user_id = child.user_id
    db_child.child_name = child.child_name
    db_child.age_band = child.age_band
    db_child.band_id = child.band_id
    db_child.iron_status = child.iron_status
    db_child.calcium_status = child.calcium_status
    db_child.vitamin_d_status = child.vitamin_d_status
    db_child.variety_status = child.variety_status
    db_child.religious_needs = child.religious_needs

    db.commit()
    db.refresh(db_child)
    return db_child