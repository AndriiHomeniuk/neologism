import time

from flask import render_template, flash, request
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from werkzeug.urls import url_parse

from app import app, db
from app.models import User
from forms import LoginForm, RegistrationForm
from script import process


@app.route('/')
def index():
    return render_template('index.html', title='Home Page')


@app.route('/search', methods=['POST'])
def search():
    time_one = time.clock()
    searching = request.form["text"]
    app.logger.info(searching)
    result = process(searching)
    timer = time.clock() - time_one
    app.logger.info(timer)
    if result:
        return render_template('index.html', result=', '.join(result))

    return render_template('index.html', result='Новотворів не знайдено.')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('cabinet.html')

    form = LoginForm()
    if form.validate_on_submit():
        app_user = User.query.filter_by(username=form.username.data).first()
        if app_user is None or not app_user.check_password(form.password.data):
            flash('Неправильно введені пароль або ім"я користувача. Перевірте дані.')
            return render_template('login.html', form=form)

        login_user(app_user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = 'index.html'
            return render_template(next_page)

    return render_template('login.html', title='Увійти', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/cabinet')
@login_required
def cabinet():
    return render_template('cabinet.html', user='User')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return render_template('cabinet.html')

    form = RegistrationForm()
    if form.validate_on_submit():
        app_user = User(username=form.username.data, email=form.email.data)
        app_user.set_password(form.password.data)
        db.session.add(app_user)
        db.session.commit()
        flash('Вітаємо, відтепер ви зареєстровані та можете користуватися сервісом на повну!')
        return render_template('cabinet.html', form=form)

    return render_template('registration.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    app_user = User.query.filter_by(username=username).first_or_404()
    return render_template('cabinet.html', user=app_user)
