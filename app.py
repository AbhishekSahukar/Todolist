from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_migrate import Migrate
import psycopg, psycopg2
import secrets
secret_key = secrets.token_hex(32)
print(secret_key)


app = Flask(__name__)


app.secret_key = '9eb55fdc43b12894b2e95c1d49d8b44bc171402a6ff32e7b4b747a5c6f3e8efe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:081205@localhost:5432/todo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '7f8b5892bd224d41b7577911fb4cf499c13335d442fad2443b5615a19a2e8d7a'

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    checked = db.Column(db.Boolean, default=False)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            return render_template("signup.html", error="Email already exists")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return render_template("login.html", error="Invalid email or password")

        # Store the username in the session
        session['user_id'] = user.id
        session['username'] = user.username  # Save the username, not email
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@jwt_required(optional=True)
def home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for("login"))

    if request.method == "POST":
        todo_name = request.form.get("todo_name")
        if todo_name:
            new_todo = Todo(name=todo_name, user_id=user_id)
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for("home"))

    items = Todo.query.filter_by(user_id=user_id).all()
    return render_template("index.html", items=items, username=session.get('username'))


@app.route("/check_todo/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    user_id = session.get('user_id')
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    todo.checked = not todo.checked
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete_todo/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    user_id = session.get('user_id')
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))






with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
