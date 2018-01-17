from flask import Flask, render_template, flash, redirect, request
from config import Config
from forms import LoginForm
from script import process
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.debug = True
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models


@app.route('/')
def index():
    username = 'User'
    return render_template('index.html', user=username)


@app.route('/search', methods=['POST'])
def search():
    searching = request.form["text"]
    app.logger.info(searching)
    result = process(searching)
    return render_template('index.html', result=", ".join(result))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title='Увійти', form=form)


@app.route('/about')
def about():
    username = 'User'
    return render_template('about.html', user=username)


@app.route('/cabinet')
def cabinet():
    username = 'User'
    return render_template('cabinet.html', user=username)


@app.route('/registration')
def registration():
    username = 'User'
    return render_template('registration.html', user=username)


if __name__ == '__main__':
    app.run()
