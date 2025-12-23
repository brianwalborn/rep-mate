from app.database import get_db
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("", response_model=list[ExerciseOut])
def list_exercises(db: Session = Depends(get_db)):
    return db.query(Exercise).order_by(Exercise.name).all()

@router.post("", response_model=ExerciseOut)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db)
):
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.patch("/{exercise_id}/archive", response_model=ExerciseOut)
def archive_exercise(
    exercise_id: str,
    db: Session = Depends(get_db)
):
    exercise = db.query(Exercise).get(exercise_id)

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    exercise.archived = True
    db.commit()
    db.refresh(exercise)

    return exercise

@router.put("/{exercise_id}", response_model=ExerciseOut)
def update_exercise(
    exercise_id: str,
    exercise_data: ExerciseCreate,
    db: Session = Depends(get_db)
):
    exercise = db.query(Exercise).get(exercise_id)

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Update exercise fields
    for key, value in exercise_data.dict().items():
        setattr(exercise, key, value)

    db.commit()
    db.refresh(exercise)

    return exercise

@router.delete("/{exercise_id}")
def delete_exercise(
    exercise_id: str,
    db: Session = Depends(get_db)
):
    exercise = db.query(Exercise).get(exercise_id)

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db.delete(exercise)
    db.commit()

    return {"message": "Exercise deleted successfully"}

