from datetime import timedelta
from app.models.set import Set, WorkoutExercise
from app.models.workout import Workout
from sqlalchemy.orm import Session

def _minutes_between(start_time, end_time) -> int:
    elapsed_seconds = max((end_time - start_time).total_seconds(), 0)
    return int((elapsed_seconds + 59) // 60)

def create_workout(db: Session, payload, user_id: str):
    start_time = payload.start_time or payload.date
    if payload.end_time:
        end_time = payload.end_time
    else:
        end_time = start_time + timedelta(minutes=payload.duration or 0)

    if end_time < start_time:
        raise ValueError("End time cannot be before start time")

    workout = Workout(
        user_id=user_id,
        date=start_time,
        start_time=start_time,
        end_time=end_time,
        duration=_minutes_between(start_time, end_time)
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
                    completed=s.completed,
                    unit=s.unit
                )
            )

    db.commit()
    db.refresh(workout)
    return workout

def update_workout(db: Session, workout_id: str, payload, user_id: str):
    workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == user_id).first()
    if not workout:
        return None

    start_time = payload.start_time or workout.start_time or payload.date or workout.date
    end_time = payload.end_time or workout.end_time

    if end_time is None:
        if payload.duration is not None:
            end_time = start_time + timedelta(minutes=payload.duration)
        else:
            end_time = start_time + timedelta(minutes=workout.duration or 0)

    if end_time < start_time:
        raise ValueError("End time cannot be before start time")

    workout.date = start_time
    workout.start_time = start_time
    workout.end_time = end_time
    workout.duration = _minutes_between(start_time, end_time)

    db.commit()
    db.refresh(workout)
    return workout

def list_workouts(db: Session):
    return db.query(Workout).all()
