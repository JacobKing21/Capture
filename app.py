from flask import Flask, render_template
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from users.views import users_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureKey'
app.register_blueprint(users_blueprint)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
