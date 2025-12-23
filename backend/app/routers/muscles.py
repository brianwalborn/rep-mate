from app.database import get_db
from app.models.muscle import Muscle
from app.schemas.muscle import MuscleCreate, MuscleOut, MuscleUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/muscles", tags=["Muscles"])

@router.get("", response_model=list[MuscleOut])
def list_muscles(db: Session = Depends(get_db)):
    """Get all muscles"""
    return db.query(Muscle).filter(Muscle.archived == False).all()

@router.post("", response_model=MuscleOut)
def create_muscle(
    muscle: MuscleCreate,
    db: Session = Depends(get_db)
):
    """Create a new muscle"""
    # Check if muscle with same name already exists
    existing = db.query(Muscle).filter(Muscle.name == muscle.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Muscle with this name already exists")

    db_muscle = Muscle(**muscle.dict())
    db.add(db_muscle)
    db.commit()
    db.refresh(db_muscle)
    return db_muscle

@router.put("/{muscle_id}", response_model=MuscleOut)
def update_muscle(
    muscle_id: str,
    muscle: MuscleUpdate,
    db: Session = Depends(get_db)
):
    """Update a muscle"""
    db_muscle = db.query(Muscle).filter(Muscle.id == muscle_id).first()

    if not db_muscle:
        raise HTTPException(status_code=404, detail="Muscle not found")

    # Check if another muscle with the same name exists
    existing = db.query(Muscle).filter(
        Muscle.name == muscle.name,
        Muscle.id != muscle_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Muscle with this name already exists")

    db_muscle.name = muscle.name
    db.commit()
    db.refresh(db_muscle)
    return db_muscle

@router.delete("/{muscle_id}")
def delete_muscle(
    muscle_id: str,
    db: Session = Depends(get_db)
):
    """Delete a muscle (soft delete by archiving)"""
    db_muscle = db.query(Muscle).filter(Muscle.id == muscle_id).first()

    if not db_muscle:
        raise HTTPException(status_code=404, detail="Muscle not found")

    db_muscle.archived = True
    db.commit()

    return {"message": "Muscle deleted successfully"}
