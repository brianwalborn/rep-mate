from fitness.database.database import get_connection
from fitness.models.equipment import Equipment
from fitness.models.exercise import Exercise
from fitness.models.muscle import Muscle
from flask import Blueprint, redirect, render_template, request

bp = Blueprint('exercises', __name__)

@bp.route('/exercises/<uuid:id>/edit', methods = ['GET', 'POST'])
def edit_exercise(id):
  if request.method.upper() == 'GET':
    muscles = []
    equipment = []

    database = get_connection()
    response = database.execute(f"SELECT * FROM exercises WHERE id = '{id}'").fetchone()
    mg_response = database.execute('SELECT * FROM muscles').fetchall()
    e_response = database.execute('SELECT * FROM equipment').fetchall()

    for row in mg_response:
      muscles.append(Muscle(row))

    for row in e_response:
      equipment.append(Equipment(row))

    exercise = Exercise(response)

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

      database = get_connection()
      database.execute(f"UPDATE exercises SET name = '{name}', description = '{description}', equipment = '{equipment}', muscle = '{muscle}' WHERE id = '{id}'")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/exercises")

@bp.route('/exercises')
def list_exercises():
  exercises: list[Exercise] = []
  database = get_connection()
  response = database.execute('SELECT * FROM exercises').fetchall()

  for row in response:
    exercises.append(Exercise(row))

  return render_template(
    'exercises.html',
    content_title = 'Exercises',
    exercises = sorted(exercises, key = lambda x: x.name)
  )

@bp.route('/exercises/new', methods = ['GET', 'POST'])
def add_exercise():
  if request.method.upper() == 'GET':
    muscles = []
    equipment = []
    database = get_connection()
    mg_response = database.execute('SELECT * FROM muscles').fetchall()
    e_response = database.execute('SELECT * FROM equipment').fetchall()

    for row in mg_response:
      muscles.append(Muscle(row))

    for row in e_response:
      equipment.append(Equipment(row))

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

      database = get_connection()
      database.execute(f"INSERT INTO exercises (name, description, muscle, equipment) VALUES ('{name}', '{description}', '{muscle}', '{equipment}')")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/exercises")

@bp.route('/exercises/<uuid:id>', methods = ['GET', 'POST'])
def view_exercise(id):
  if request.method.upper() == 'GET':
    database = get_connection()
    response = database.execute(f"SELECT * FROM exercises WHERE id = '{id}'").fetchone()

    exercise = Exercise(response)

    return render_template(
      'exercises_view.html',
      content_title = exercise.name,
      id = id,
      description = exercise.description,
      muscle = exercise.muscle.name,
      equipment = exercise.equipment.name,
      date_added = exercise.date_added
    )
  elif request.method.upper() == 'POST':
    try:
      database = get_connection()
      database.execute(f"DELETE FROM exercises WHERE id = '{id}'")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/exercises")

