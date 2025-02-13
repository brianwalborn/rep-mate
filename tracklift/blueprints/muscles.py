from flask import Blueprint, redirect, render_template, request
from tracklift.models.muscle import Muscle

bp = Blueprint('muscles', __name__)

@bp.route('/muscles/<uuid:id>/edit', methods = ['GET', 'POST'])
def edit_muscle(id):
  if request.method.upper() == 'GET':
    muscle = Muscle(id = id).get()

    return render_template(
      'muscles_edit.html',
      content_title = 'Edit Muscle',
      muscle = muscle
    )
  elif request.method.upper() == 'POST':
    try:
      name = request.form['name']

      Muscle(id = id, name = name).update()
    except Exception as e:
      print(e)
    finally:
      return redirect("/muscles")

@bp.route('/muscles')
def list_muscles():
  muscles = Muscle().get_all()

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

      Muscle(name = name).add()
    except Exception as e:
      print(e)
    finally:
      return redirect("/muscles")

@bp.route('/muscles/<uuid:id>', methods = ['GET', 'POST'])
def view_muscle(id):
  if request.method.upper() == 'GET':
    muscle = Muscle(id = id).get()

    return render_template(
      'muscles_view.html',
      content_title = muscle.name,
      id = id
    )
  elif request.method.upper() == 'POST':
    try:
      Muscle(id = id).delete()
    except Exception as e:
      print(e)
    finally:
      return redirect("/muscles")

