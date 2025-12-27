from app.database import get_db
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentOut, EquipmentUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/equipment", tags=["Equipment"])

@router.get("", response_model=list[EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    """Get all equipment"""
    return db.query(Equipment).filter(Equipment.archived == False).order_by(Equipment.name).all()

@router.post("", response_model=EquipmentOut)
def create_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db)
):
    """Create new equipment"""
    # Check if equipment with same name already exists
    existing = db.query(Equipment).filter(Equipment.name == equipment.name).first()
    if existing:
        # If it's archived, unarchive it
        if existing.archived:
            existing.archived = False
            db.commit()
            db.refresh(existing)
            return existing
        else:
            raise HTTPException(status_code=400, detail="Equipment with this name already exists")

    db_equipment = Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

@router.put("/{equipment_id}", response_model=EquipmentOut)
def update_equipment(
    equipment_id: str,
    equipment: EquipmentUpdate,
    db: Session = Depends(get_db)
):
    """Update equipment"""
    db_equipment = db.query(Equipment).get(equipment_id)

    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    # Check for name conflicts
    existing = db.query(Equipment).filter(
        Equipment.name == equipment.name,
        Equipment.id != equipment_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Equipment with this name already exists")

    db_equipment.name = equipment.name
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

@router.delete("/{equipment_id}")
def delete_equipment(
    equipment_id: str,
    db: Session = Depends(get_db)
):
    """Delete (archive) equipment"""
    db_equipment = db.query(Equipment).get(equipment_id)

    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    db_equipment.archived = True
    db.commit()
    return {"message": "Equipment deleted successfully"}
