from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from users.forms import RegisterForm, LoginForm, SearchForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = request.form.get('email')
        print(email)
        return login()
    return render_template('register.html', form=form)


@users_blueprint.route('/login')
def login():
    form = LoginForm()

    return render_template('login.html', form=form)


@users_blueprint.route('/search')
def search():
    return render_template('search.html')
