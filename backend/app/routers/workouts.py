from app.auth.dependencies import get_current_user
from app.crud.workouts import create_workout, list_workouts, update_workout
from app.database import get_db
from app.models.exercise import Exercise
from app.models.workout import Workout
from app.schemas.workout import WorkoutCreate, WorkoutOut, WorkoutUpdate
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.get("", response_model=list[WorkoutOut])
def get_workouts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Order by date descending (newest first)
    workouts = db.query(Workout).filter(Workout.user_id == user.id).order_by(Workout.date.desc()).offset(skip).limit(limit).all()

    # Enrich workout exercises with muscle data
    for workout in workouts:
        for workout_ex in workout.exercises:
            exercise = db.query(Exercise).filter(Exercise.id == workout_ex.exercise_id).first()
            if exercise:
                workout_ex.muscles = exercise.muscles
            else:
                workout_ex.muscles = []

    return workouts

@router.post("", response_model=WorkoutOut)
def create(workout: WorkoutCreate, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return create_workout(db, workout, user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.put("/{workout_id}", response_model=WorkoutOut)
def update(workout_id: str, workout: WorkoutUpdate, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        updated = update_workout(db, workout_id, workout, user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not updated:
        raise HTTPException(status_code=404, detail="Workout not found")

    return updated

@router.delete("/{workout_id}")
def delete(workout_id: str, user = Depends(get_current_user), db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == user.id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    db.delete(workout)
    db.commit()
    return {"message": "Workout deleted successfully"}
