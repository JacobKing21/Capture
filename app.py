import sqlite3
from flask import Flask, render_template
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ctf.db'


db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'users.login'


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    # User information
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=False, default='user')

    # User auth information
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # User constructor
    def __init__(self, role, email, password):
        self.role = role
        self.email = email
        # Generating password hash
        self.password = generate_password_hash(password)


class Product(db.Model):

    __tablename__ = 'Product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


def init_db():
    """Initialization of the database tables
    """
    db.drop_all()
    db.create_all()


def create_entries():
    admin = User(role='admin', email='john@gmail.com', password='securepass123')
    user = User(role='user', email='jsmith@email.com', password='password123')
    product1 = Product(name='Hoodie', price=30, quantity=5)
    product2 = Product(name='Jeans', price=25, quantity=6)
    product3 = Product(name='Socks', price=2, quantity=4)
    product4 = Product(name='Trainers', price=40.99, quantity=10)
    product5 = Product(name='Cowboy Boots', price=25, quantity=15)
    product6 = Product(name='T-Shirt', price=10, quantity=66)
    product7 = Product(name='Shirt', price=13, quantity=30)
    product8 = Product(name='Top Hat', price=15.50, quantity=0)
    db.session.add(admin)
    db.session.add(user)
    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    db.session.add(product5)
    db.session.add(product6)
    db.session.add(product7)
    db.session.add(product8)

    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    """Getting the user id from login manager to determine which user is logged in"""
    return User.query.get(int(user_id))


from users.views import users_blueprint
app.register_blueprint(users_blueprint)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
