from app.models.set import Set, WorkoutExercise
from app.models.workout import Workout
from sqlalchemy.orm import Session

def create_workout(db: Session, payload, user_id: str):
    workout = Workout(
        user_id=user_id,
        date=payload.date,  # Keep the full datetime
        duration=payload.duration
    )
    db.add(workout)
    db.flush()

    for ex in payload.exercises:
        workout_ex = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=ex.exercise_id,
            exercise_name=ex.name,  # Changed from exercise_name to name
            equipment=ex.equipment,
            notes=ex.notes  # Add notes field
        )
        db.add(workout_ex)
        db.flush()

        for s in ex.sets:
            db.add(
                Set(
                    workout_exercise_id=workout_ex.id,
                    weight=s.weight,
                    reps=s.reps,
                    completed=s.completed
                )
            )

    db.commit()
    db.refresh(workout)
    return workout

def list_workouts(db: Session):
    return db.query(Workout).all()
