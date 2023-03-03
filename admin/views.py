from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app import db, requires_roles, User

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin-home.html')
