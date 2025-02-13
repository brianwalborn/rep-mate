from flask import Blueprint, redirect, render_template, request
from tracklift.models.equipment import Equipment
from tracklift.models.exercise import Exercise
from tracklift.models.muscle import Muscle

bp = Blueprint('exercises', __name__)

@bp.route('/exercises/<uuid:id>/edit', methods = ['GET', 'POST'])
def edit_exercise(id):
  if request.method.upper() == 'GET':
    muscles = Muscle().get_all()
    equipment = Equipment().get_all()
    exercise = Exercise(id = id).get()

    return render_template(
        'exercises_edit.html',
        content_title = "Edit Exercise",
        exercise = exercise,
        equipment = equipment,
        muscles = muscles
      )
  elif request.method.upper() == 'POST':
    try:
      name = request.form['name']
      description = request.form['description']
      equipment = request.form['equipment']
      muscle = request.form['muscle']

      Exercise(id = id, name = name, description = description, equipment_id = equipment, muscle_id = muscle).update()
    except Exception as e:
      print(e)
    finally:
      return redirect("/exercises")

@bp.route('/exercises')
def list_exercises():
  exercises = Exercise().get_all()

  return render_template(
    'exercises.html',
    content_title = 'Exercises',
    exercises = sorted(exercises, key = lambda x: x.name)
  )

@bp.route('/exercises/new', methods = ['GET', 'POST'])
def add_exercise():
  if request.method.upper() == 'GET':
    muscles = Muscle().get_all()
    equipment = Equipment().get_all()

    return render_template(
      'exercises_new.html',
      content_title = 'Add Exercise',
      equipment = equipment,
      muscles = muscles
    )
  elif request.method.upper() == 'POST':
    try:
      name = request.form['name']
      description = request.form['description']
      equipment = request.form['equipment']
      muscle = request.form['muscle']

      Exercise(name = name, description = description, equipment_id = equipment, muscle_id = muscle).add()
    except Exception as e:
      print(e)
    finally:
      return redirect("/exercises")

@bp.route('/exercises/<uuid:id>', methods = ['GET', 'POST'])
def view_exercise(id):
  if request.method.upper() == 'GET':
    exercise = Exercise(id = id).get()

    return render_template(
      'exercises_view.html',
      content_title = exercise.name,
      id = id,
      description = exercise.description,
      muscle = Muscle(id = exercise.muscle_id).get().name,
      equipment = Equipment(id = exercise.equipment_id).get().name,
      date_added = exercise.date_added
    )
  elif request.method.upper() == 'POST':
    try:
      Exercise(id = id).delete()
    except Exception as e:
      print(e)
    finally:
      return redirect("/exercises")

