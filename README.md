# Flask Task Manager

A small multi-user project and task manager built with Flask. Users register, log in, create projects, and
add tasks they can tick off. Each user sees and changes only their own data.

![python](https://img.shields.io/badge/python-3.12-blue) ![flask](https://img.shields.io/badge/flask-3.1-black)

## Features
- Registration and login with hashed passwords (Werkzeug) and session handling (Flask-Login)
- Projects per user, tasks per project, mark tasks done or undo
- Ownership checks on every project and task route: another user's data returns 404
- Application factory pattern, blueprints, SQLAlchemy models, configuration from environment variables
- pytest suite covering authentication, task flow and cross-user access

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="change-me"          # optional in development
python run.py                          # http://localhost:5000
```
The SQLite database is created automatically on first run. Set `DATABASE_URL` to use another database.

## Tests
```bash
pytest
```

## Structure
```
app/
  __init__.py      application factory, database and login setup
  models.py        User, Project, Task
  routes/auth.py   register, login, logout
  routes/main.py   dashboard, projects, tasks (with ownership checks)
  templates/       Jinja2 templates
tests/             pytest suite
run.py             development entry point
```
