from fitness.database.database import get_connection
from fitness.models.equipment import Equipment
from flask import Blueprint, redirect, render_template, request

bp = Blueprint('equipment', __name__)

@bp.route('/equipment/<uuid:id>/edit', methods = ['GET', 'POST'])
def edit_equipment(id):
  if request.method.upper() == 'GET':
    database = get_connection()
    response = database.execute(f"SELECT * FROM equipment WHERE id = '{id}'").fetchone()

    equipment = Equipment(response)

    return render_template(
      'equipment_edit.html',
      content_title = 'Edit Equipment',
      equipment = equipment
    )
  elif request.method.upper() == 'POST':
    try:
      name = request.form['name']

      database = get_connection()
      database.execute(f"UPDATE equipment SET name = '{name}' WHERE id = '{id}'")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/equipment")

@bp.route('/equipment')
def list_equipment():
  equipment: list[Equipment] = []
  database = get_connection()
  response = database.execute('SELECT * FROM equipment').fetchall()

  for row in response:
    equipment.append(Equipment(row))

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

      database = get_connection()
      database.execute(f"INSERT INTO equipment (name) VALUES ('{name}')")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/equipment")

@bp.route('/equipment/<uuid:id>', methods = ['GET', 'POST'])
def view_equipment(id):
  if request.method.upper() == 'GET':
    database = get_connection()
    response = database.execute(f"SELECT * FROM equipment WHERE id = '{id}'").fetchone()

    equipment = Equipment(response)

    return render_template(
      'equipment_view.html',
      content_title = equipment.name,
      id = id
    )
  elif request.method.upper() == 'POST':
    try:
      database = get_connection()
      database.execute(f"DELETE FROM equipment WHERE id = '{id}'")
      database.commit()
    except Exception as e:
      print(e)
    finally:
      return redirect("/equipment")

