from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Project, Task

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Redirect unconditionally to login page, or consider redirecting logged-in users to dashboard
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects)

@main_bp.route('/project/create', methods=['POST'])
@login_required
def create_project():
    name = request.form['name']
    new_project = Project(name=name, user_id=current_user.id)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main_bp.route('/project/<int:project_id>')
@login_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
    tasks = Task.query.filter_by(project_id=project.id).all()
    return render_template('project.html', project=project, tasks=tasks)

@main_bp.route('/task/add/<int:project_id>', methods=['POST'])
@login_required
def add_task(project_id):
    title = request.form['title']
    new_task = Task(title=title, project_id=project_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('main.view_project', project_id=project_id))
