from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.models import Project, Task, db

main_bp = Blueprint("main", __name__)


def _own_project_or_404(project_id):
    """Return the project only if it belongs to the logged-in user."""
    project = db.get_or_404(Project, project_id)
    if project.user_id != current_user.id:
        abort(404)
    return project


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", projects=projects)


@main_bp.route("/project/create", methods=["POST"])
@login_required
def create_project():
    name = request.form.get("name", "").strip()
    if name:
        db.session.add(Project(name=name, user_id=current_user.id))
        db.session.commit()
    return redirect(url_for("main.dashboard"))


@main_bp.route("/project/<int:project_id>")
@login_required
def view_project(project_id):
    project = _own_project_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project.id).all()
    return render_template("project.html", project=project, tasks=tasks)


@main_bp.route("/task/add/<int:project_id>", methods=["POST"])
@login_required
def add_task(project_id):
    project = _own_project_or_404(project_id)
    title = request.form.get("title", "").strip()
    if title:
        db.session.add(Task(title=title, project_id=project.id))
        db.session.commit()
    return redirect(url_for("main.view_project", project_id=project.id))


@main_bp.route("/task/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = db.get_or_404(Task, task_id)
    _own_project_or_404(task.project_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for("main.view_project", project_id=task.project_id))
