from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import psycopg,psycopg2

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:081205@localhost:5432/todo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    checked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Todo {self.name}>"

# Home route to display todos
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        todo_name = request.form.get("todo_name")
        if todo_name:
            new_todo = Todo(name=todo_name)
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for("home"))

    # Fetch all todos from the database
    items = Todo.query.all()
    return render_template("index.html", items=items)

# Route to update the 'checked' status of a todo
@app.route("/check/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.checked = not todo.checked  # Toggle the checked state
    db.session.commit()
    return redirect(url_for("home"))

# Route to delete a todo
@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))
with app.app_context():
    db.create_all()     


if __name__ == "__main__": 
    app.run(debug=True)
   
