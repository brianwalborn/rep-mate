from fitness.database.database import get_connection
from fitness.models.exercise import Exercise
from fitness.models.set import Set
from fitness.models.workout import Workout
from fitness.models.workout_exercise import WorkoutExercise
from flask import Blueprint, redirect, render_template, request
import uuid

bp = Blueprint('workouts', __name__)

@bp.route('/workouts')
def list_workouts():
  workouts = []
  database = get_connection()
  response = database.execute('SELECT * FROM workouts').fetchall()

  for row in response:
    workouts.append(Workout(row))

  return render_template(
    'workouts.html',
    content_title = 'Workouts',
    workouts = workouts,
    new_workout_id = uuid.uuid4()
  )

@bp.route('/workouts/new/<uuid:id>', methods = ['GET', 'POST'])
def new_workout(id):
  database = get_connection()
  context = 'exercises'
  workout_exercise_id = ''

  if request.method.upper() == 'GET':
    database.execute(f"INSERT INTO workouts (id, name) VALUES ('{id}', '{id}')")
    database.commit()
  elif request.method.upper() == 'POST':
    if request.form['submit'] == 'Add Exercise':
      exercise = request.form['exercise']
      notes = request.form['notes']
      database.execute(f"INSERT INTO workout_exercises (workout_id, exercise_id, notes) VALUES ('{id}', '{exercise}', '{notes}')")
      database.commit()
      context = 'sets'
      workout_exercise_id = database.execute(f"SELECT id FROM workout_exercises WHERE workout_id = '{id}' AND exercise_id = '{exercise}'").fetchone()[0]
    elif request.form['submit'] == 'Add Set':
      woe_id = request.form['workout_exercise_id']
      weight = request.form['weight']
      reps = request.form['repetitions']
      database.execute(f"INSERT INTO sets (workout_exercise_id, repetitions, weight) VALUES ('{woe_id}', '{reps}', '{weight}')")
      database.commit()
      context = 'sets'
      workout_exercise_id = woe_id
    elif request.form['submit'] == 'Finish Exercise':
      woe_id = request.form['workout_exercise_id']
      weight = request.form['weight']
      reps = request.form['repetitions']
      if weight and reps:
        database.execute(f"INSERT INTO sets (workout_exercise_id, repetitions, weight) VALUES ('{woe_id}', '{reps}', '{weight}')")
        database.commit()

  exercises = []
  workout_exercises: list[WorkoutExercise] = []
  sets = []
  wo_exercises = database.execute(f"SELECT * FROM workout_exercises where workout_id = '{id}'").fetchall()
  r_exercises = database.execute('SELECT * FROM exercises').fetchall()

  for row in wo_exercises:
    workout_exercises.append(WorkoutExercise(row))

  for row in r_exercises:
    exercises.append(Exercise(row))

  for exercise in workout_exercises:
    response = database.execute(f"SELECT * FROM sets WHERE workout_exercise_id = '{exercise.id}'").fetchall()

    for row in response:
      sets.append(Set(row))

  return render_template(
    'workouts_new.html',
    content_title = 'Workout',
    workout_exercises = workout_exercises,
    exercises = exercises,
    sets = sets,
    context = context,
    workout_exercise_id = workout_exercise_id
  )

@bp.route('/workouts/<uuid:id>', methods = ['GET', 'POST'])
def view_workout(id):
  if request.method.upper() == 'GET':
    database = get_connection()
    exercises = []
    workout_exercises: list[WorkoutExercise] = []
    sets = []
    wo_exercises = database.execute(f"SELECT * FROM workout_exercises where workout_id = '{id}'").fetchall()
    r_exercises = database.execute('SELECT * FROM exercises').fetchall()

    workout = Workout(id = id)

    for row in wo_exercises:
      workout_exercises.append(WorkoutExercise(row))

    for row in r_exercises:
      exercises.append(Exercise(row))

    for exercise in workout_exercises:
      response = database.execute(f"SELECT * FROM sets WHERE workout_exercise_id = '{exercise.id}'").fetchall()

      for row in response:
        sets.append(Set(row))

    return render_template(
      'workouts_view.html',
      content_title = f'{workout.date_added}',
      workout_exercises = workout_exercises,
      exercises = exercises,
      sets = sets
    )
  elif request.method.upper() == 'POST':
    try:
      database = get_connection()
      workout_exercises = database.execute(f"SELECT * FROM workout_exercises WHERE workout_id = '{id}'").fetchall()

      for row in workout_exercises:
        exercise = WorkoutExercise(row)

        database.execute(f"DELETE FROM sets WHERE workout_exercise_id = '{exercise.id}'")

      database.execute(f"DELETE FROM workout_exercises WHERE workout_id = '{id}'")
      database.execute(f"DELETE FROM workouts WHERE id = '{id}'")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/workouts")
