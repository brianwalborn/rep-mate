from flask import Blueprint, redirect, render_template, request
from tracklift.models.equipment import Equipment

bp = Blueprint('equipment', __name__)

@bp.route('/equipment/<uuid:id>/edit', methods = ['GET', 'POST'])
def edit_equipment(id):
  if request.method.upper() == 'GET':
    equipment = Equipment(id = id).get()

    return render_template(
      'equipment_edit.html',
      content_title = 'Edit Equipment',
      equipment = equipment
    )
  elif request.method.upper() == 'POST':
    try:
      name = request.form['name']

      Equipment(id = id, name = name).update()
    except Exception as e:
      print(e)
    finally:
      return redirect("/equipment")

@bp.route('/equipment')
def list_equipment():
  equipment = Equipment().get_all()

  return render_template(
    'equipment.html',
    content_title = 'Equipment',
    equipment = sorted(equipment, key = lambda x: x.name)
  )

@bp.route('/equipment/new', methods = ['GET', 'POST'])
def add_equipment():
  if request.method.upper() == 'GET':
    return render_template(
      'equipment_new.html',
      content_title = 'Add Equipment'
    )
  elif request.method.upper() == 'POST':
    try:
      name = request.form['name']

      Equipment(name = name).add()
    except Exception as e:
      print(e)
    finally:
      return redirect("/equipment")

@bp.route('/equipment/<uuid:id>', methods = ['GET', 'POST'])
def view_equipment(id):
  if request.method.upper() == 'GET':
    equipment = Equipment(id = id).get()

    return render_template(
      'equipment_view.html',
      content_title = equipment.name,
      id = id
    )
  elif request.method.upper() == 'POST':
    try:
      Equipment(id = id).delete()
    except Exception as e:
      print(e)
    finally:
      return redirect("/equipment")

