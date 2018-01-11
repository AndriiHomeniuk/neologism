from flask import Flask, render_template, flash, redirect
from config import Config
from forms import LoginForm

app = Flask(__name__)
app.debug = True
app.config.from_object(Config)


@app.route('/')
def index():
    username = 'User'
    return render_template('index.html', user = username)


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
    return render_template('about.html', user = username)


if __name__ == '__main__':
    app.run()