<<<<<<< HEAD
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
   
=======
from flask import Flask, render_template, url_for, request, redirect
import random

app = Flask(__name__)
todos = [
    {
        'id': 1,
        'name': 'Write SQL',
        'checked': False,
    },
    {
        'id': 2,
        'name': 'Write Python',
        'checked': False,
    },
]
   
 

@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def home():
    if (request.method == "POST"):
       todo_Name = (request.form["todo_name"])
       cur_id = random.randint(1,1000)
       todos.append({
          'id': cur_id,
          'name': todo_Name,
          'checked':False

       })
       return redirect(url_for("home"))
    return render_template("index.html", items=todos)
@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['checked'] = not todo['checked']
            break
    return redirect(url_for("home"))
    
@app.route("/delete/<int:todo_id>",methods =["POST"])
def delete_todo(todo_id):
    global todos
    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)
    return redirect(url_for("home"))        
   
      

   
if __name__ == "__main__":
  app.run(debug=True)
>>>>>>> 9a8ac78c74adb32a810bf35c4eb4c6b4af6c6ebf
