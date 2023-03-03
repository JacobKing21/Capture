import sqlite3
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app import User, db
from users.forms import RegisterForm, LoginForm, SearchForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already in use', 'error')
            return render_template('register.html', form=form)

        new_user = User(role='user',
                        email=form.email.data,
                        password=form.password.data)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            flash('Please check your login details and try again')

            return render_template('login.html', form=form)

        login_user(user)

        return redirect(url_for('users.search'))
    return render_template('login.html', form=form)


@users_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    list1 = []
    if form.validate_on_submit():
        name = request.form.get('name')
        conn = sqlite3.connect('C:/Users/jacob/PycharmProjects/Capture/instance/ctf.db')
        c = conn.cursor()
        sql = c.execute("SELECT * FROM Product WHERE name LIKE '%s'" % name)
        res = sql.fetchall()

        list1 = []
        list2 = []
        list3 = []

        print(res)
        for i in res:
            list1.append(i[1])
            list2.append(i[2])
            list2.append(i[3])
        return render_template('search.html', count=len(list1), name=name, form=form,
                               result1=list1, result2=list2, result3=list3)

    return render_template('search.html', form=form, count=len(list1))


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
