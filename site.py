from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    username = 'User'
    return render_template('index.html', user = username)


@app.route('/login')
def login():
    pass


@app.route('/signup')
def signUp():
    pass


if __name__ == '__main__':
    app.run()