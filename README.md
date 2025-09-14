# Flask To-Do App

A simple user/project/task management system built with Flask.

## Features

- User registration & login (Flask-Login)
- Project creation per user
- Task management per project
- Minimal, clear HTML UI

## Setup

1. Clone the repo and open in GitHub Codespaces (recommended).
2. Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3. Initialize the database in Python:
from app import db, create_app
app = create_app()
with app.app_context():
db.create_all()

4. Run the app:
5. Visit `http://localhost:5000` in your browser.

## Directory Structure

- `app/` - App code (models, routes, templates)
- `.venv/` - Virtual environment
- `requirements.txt`
- `README.md`
