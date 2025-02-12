from fitness.database.database import get_connection
from fitness.models.muscle import Muscle
from flask import Blueprint, redirect, render_template, request

bp = Blueprint('muscles', __name__)

@bp.route('/muscles/<uuid:id>/edit', methods = ['GET', 'POST'])
def edit_muscle(id):
  if request.method.upper() == 'GET':
    database = get_connection()
    response = database.execute(f"SELECT * FROM muscles WHERE id = '{id}'").fetchone()

    muscle = Muscle(response)

    return render_template(
      'muscles_edit.html',
      content_title = 'Edit Muscle',
      muscle = muscle
    )
  elif request.method.upper() == 'POST':
    try:
      name = request.form['name']

      database = get_connection()
      database.execute(f"UPDATE muscles SET name = '{name}' WHERE id = '{id}'")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/muscles")

@bp.route('/muscles')
def list_muscles():
  muscles: list[Muscle] = []
  database = get_connection()
  response = database.execute('SELECT * FROM muscles').fetchall()

  for row in response:
    muscles.append(Muscle(row))

  return render_template(
    'muscles.html',
    content_title = 'Muscles',
    muscles = sorted(muscles, key = lambda x: x.name)
  )

@bp.route('/muscles/new', methods = ['GET', 'POST'])
def add_muscle():
  if request.method.upper() == 'GET':
    return render_template(
      'muscles_new.html',
      content_title = 'Add Muscle'
    )
  elif request.method.upper() == 'POST':
    try:
      name = request.form['name']

      database = get_connection()
      database.execute(f"INSERT INTO muscles (name) VALUES ('{name}')")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/muscles")

@bp.route('/muscles/<uuid:id>', methods = ['GET', 'POST'])
def view_muscle(id):
  if request.method.upper() == 'GET':
    database = get_connection()
    response = database.execute(f"SELECT * FROM muscles WHERE id = '{id}'").fetchone()

    muscle = Muscle(response)

    return render_template(
      'muscles_view.html',
      content_title = muscle.name,
      id = id
    )
  elif request.method.upper() == 'POST':
    try:
      database = get_connection()
      database.execute(f"DELETE FROM muscles WHERE id = '{id}'")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/muscles")

