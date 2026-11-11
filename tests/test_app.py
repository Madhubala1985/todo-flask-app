import pytest

from app import create_app, db
from app.models import Task


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    yield app
    with app.app_context():
        db.drop_all()


def register_and_login(client, username, password="pw12345"):
    client.post("/register", data={"username": username, "password": password})
    return client.post("/login", data={"username": username, "password": password})


def test_register_login_and_create_project(app):
    client = app.test_client()
    resp = register_and_login(client, "alice")
    assert resp.status_code == 302 and "/dashboard" in resp.headers["Location"]
    client.post("/project/create", data={"name": "Thesis"})
    assert b"Thesis" in client.get("/dashboard").data


def test_wrong_password_is_rejected(app):
    client = app.test_client()
    register_and_login(client, "alice")
    client.get("/logout")
    resp = client.post("/login", data={"username": "alice", "password": "nope"})
    assert "/login" in resp.headers["Location"]


def test_dashboard_requires_login(app):
    resp = app.test_client().get("/dashboard")
    assert resp.status_code == 302 and "/login" in resp.headers["Location"]


def test_add_and_toggle_task(app):
    client = app.test_client()
    register_and_login(client, "alice")
    client.post("/project/create", data={"name": "P"})
    client.post("/task/add/1", data={"title": "write tests"})
    client.post("/task/1/toggle")
    with app.app_context():
        assert db.session.get(Task, 1).complete is True


def test_users_cannot_touch_other_users_projects(app):
    alice, bob = app.test_client(), app.test_client()
    register_and_login(alice, "alice")
    alice.post("/project/create", data={"name": "Private"})
    alice.post("/task/add/1", data={"title": "secret"})

    register_and_login(bob, "bob")
    assert bob.get("/project/1").status_code == 404
    assert bob.post("/task/add/1", data={"title": "intrusion"}).status_code == 404
    assert bob.post("/task/1/toggle").status_code == 404
    with app.app_context():
        assert Task.query.count() == 1
        assert db.session.get(Task, 1).complete is False
