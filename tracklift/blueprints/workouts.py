from flask import Blueprint, redirect, render_template, request
from tracklift.models.exercise import Exercise
from tracklift.models.set import Set
from tracklift.models.workout import Workout
from tracklift.models.workout_exercise import WorkoutExercise
import uuid

bp = Blueprint('workouts', __name__)

@bp.route('/workouts')
def list_workouts():
  workouts = Workout().get_all()

  return render_template(
    'workouts.html',
    content_title = 'Workouts',
    workouts = workouts,
    new_workout_id = uuid.uuid4()
  )

@bp.route('/workouts/new/<uuid:id>', methods = ['GET', 'POST'])
def new_workout(id):
  context = 'exercises'
  workout_exercise_id = ''

  if request.method.upper() == 'GET':
    Workout(id = id, name = id).add()
  elif request.method.upper() == 'POST':
    if request.form['submit'] == 'Add Exercise':
      exercise = request.form['exercise']
      notes = request.form['notes']
      WorkoutExercise(workout_id = id, exercise_id = exercise, notes = notes).add()
      context = 'sets'
      workout_exercise_id = WorkoutExercise(workout_id = id, exercise_id = exercise).get().id
    elif request.form['submit'] == 'Add Set':
      woe_id = request.form['workout_exercise_id']
      weight = request.form['weight']
      reps = request.form['repetitions']
      Set(workout_exercise_id = woe_id, repetitions = reps, weight = weight).add()
      context = 'sets'
      workout_exercise_id = woe_id
    elif request.form['submit'] == 'Finish Exercise':
      woe_id = request.form['workout_exercise_id']
      weight = request.form['weight']
      reps = request.form['repetitions']
      if weight and reps:
        Set(workout_exercise_id = woe_id, repetitions = reps, weight = weight).add()

  exercises = Exercise().get_all()
  workout_exercises = WorkoutExercise(workout_id = id).get_all()
  sets = []

  for workout_exercise in workout_exercises:
    response = Set(workout_exercise_id = workout_exercise.id).get_all()

    for value in response:
      sets.append(value)

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
    exercises = Exercise().get_all()
    workout_exercises = WorkoutExercise(workout_id = id).get_all()
    sets = []

    workout = Workout(id = id).get()

    for exercise in workout_exercises:
      response = Set(workout_exercise_id = exercise.id).get_all()

      for value in response:
        sets.append(value)

    return render_template(
      'workouts_view.html',
      content_title = f'{workout.date_added}',
      workout_exercises = workout_exercises,
      exercises = exercises,
      sets = sets
    )
  elif request.method.upper() == 'POST':
    try:
      workout_exercises = WorkoutExercise(workout_id = id).get_all()

      for ex in workout_exercises:
        Set(workout_exercise_id = ex.id).delete()

      WorkoutExercise(workout_id = id).delete()
      Workout(id = id).delete()
    except Exception as e:
      print(e)
    finally:
      return redirect("/workouts")
