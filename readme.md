# Flask Todo App with Login, JWT & PostgreSQL

A full-stack Todo application built with Flask, PostgreSQL, and JWT authentication. Users can register, log in, and manage their personal todo items in a secure and elegant way.


##  Features

- User authentication (Sign up & login)
- JWT-protected route support
- Passwords hashed using `werkzeug.security`
- Session-based login persistence
- Todo create, check/uncheck, delete
- PostgreSQL database using SQLAlchemy ORM
- `.env` file support for secure config


## Tech Stack

| Layer         | Technology               |

| Backend       | Python 3.10, Flask 3.x   |
| Database      | PostgreSQL               |
| ORM           | SQLAlchemy               |
| Auth          | Flask-JWT-Extended       |
| Secrets       | python-dotenv            |
| Migrations    | Flask-Migrate            |
| Templates     | HTML + Jinja2            |

##  Setup Instructions

### 1️ Clone the Repo

bash
git clone https://github.com/YOUR_USERNAME/flask-todo-app.git
cd flask-todo-app

### 2️ Create a Virtual Environment

python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

### 3 Install Dependencies

pip install -r requirements.txt

### 4 Set Up PostgreSQL

Make sure PostgreSQL is running.
CREATE DATABASE todo_db;

### 5️ Configure Environment Variables

#.env
SECRET_KEY=your_flask_secret
SQLALCHEMY_DATABASE_URI=postgresql://postgres:your_password@localhost:5432/todo_db
JWT_SECRET_KEY=your_jwt_secret

### 6️ Run the App

python app.py

### Screenshhots ###

### Login Page
![Login Page](assets/Login.png)

### Adding todo 
![Add todo](assets/Addtodo.png)

### Added todo
![Added todo](assets/Addedtodo.png)

### Checked todo
![Add todo](assets/Checkedtodo.png)

License
MIT © Abhishek Sahukar

This app was built as part of a portfolio project to learn Flask, SQLAlchemy, and web deployment. Feel free to fork, improve, and share!