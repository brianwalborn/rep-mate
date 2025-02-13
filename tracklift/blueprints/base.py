from flask import Blueprint, redirect, url_for

bp = Blueprint('base', __name__)

@bp.route('/')
@bp.route('/home')
def index():
  return redirect(url_for('workouts.list_workouts'))
