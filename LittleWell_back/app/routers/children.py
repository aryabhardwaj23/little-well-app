from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/children", tags=["children"])


@router.get("", response_model=list[schemas.ChildResponse])
def read_children(db: Session = Depends(get_db)):
    children = crud.get_children(db)
    result = []

    for child in children:
        allergies = crud.get_child_allergen_ids(db, child.child_id)

        result.append(
            schemas.ChildResponse(
                child_id=child.child_id,
                user_id=child.user_id,
                child_name=child.child_name,
                age_band=child.age_band,
                band_id=child.band_id,
                iron_status=child.iron_status,
                calcium_status=child.calcium_status,
                vitamin_d_status=child.vitamin_d_status,
                variety_status=child.variety_status,
                religious_needs=child.religious_needs or "",
                allergies=allergies,
            )
        )

    return result


@router.get("/{child_id}", response_model=schemas.ChildResponse)
def read_child(child_id: int, db: Session = Depends(get_db)):
    child = crud.get_child_by_id(db, child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    allergies = crud.get_child_allergen_ids(db, child.child_id)

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
        religious_needs=child.religious_needs or "",
        allergies=allergies,
    )


@router.post("", response_model=schemas.ChildResponse)
def create_child(child: schemas.ChildCreate, db: Session = Depends(get_db)):
    new_child = crud.create_child(db, child)

    return schemas.ChildResponse(
        child_id=new_child.child_id,
        user_id=new_child.user_id,
        child_name=new_child.child_name,
        age_band=new_child.age_band,
        band_id=new_child.band_id,
        iron_status=new_child.iron_status,
        calcium_status=new_child.calcium_status,
        vitamin_d_status=new_child.vitamin_d_status,
        variety_status=new_child.variety_status,
        religious_needs=new_child.religious_needs or "",
        allergies=crud.get_child_allergen_ids(db, new_child.child_id),
    )


@router.put("/{child_id}", response_model=schemas.ChildResponse)
def update_child(child_id: int, child: schemas.ChildUpdate, db: Session = Depends(get_db)):
    updated_child = crud.update_child(db, child_id, child)
    if not updated_child:
        raise HTTPException(status_code=404, detail="Child not found")

    return schemas.ChildResponse(
        child_id=updated_child.child_id,
        user_id=updated_child.user_id,
        child_name=updated_child.child_name,
        age_band=updated_child.age_band,
        band_id=updated_child.band_id,
        iron_status=updated_child.iron_status,
        calcium_status=updated_child.calcium_status,
        vitamin_d_status=updated_child.vitamin_d_status,
        variety_status=updated_child.variety_status,
        religious_needs=updated_child.religious_needs or "",
        allergies=crud.get_child_allergen_ids(db, updated_child.child_id),
    )

@router.delete("/{child_id}")
def delete_child(child_id: int, db: Session = Depends(get_db)):
    deleted_child = crud.delete_child(db, child_id)
    if not deleted_child:
        raise HTTPException(status_code=404, detail="Child not found")

    return {"message": "Child deleted successfully", "child_id": child_id}