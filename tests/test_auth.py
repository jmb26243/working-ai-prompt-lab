
import pytest

from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_registration_success(client, app):
    response = client.post("/register", data={
        "username": "teststudent",
        "email": "test@example.com",
        "password": "TestPassword123"
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(email="test@example.com").first()

        assert user is not None
        assert user.username == "teststudent"
        assert user.password_hash != "TestPassword123"
        assert user.check_password("TestPassword123")


def test_duplicate_email_rejected(client, app):
    with app.app_context():
        user = User(
            username="student1",
            email="duplicate@example.com"
        )
        user.set_password("Password123")
        db.session.add(user)
        db.session.commit()

    response = client.post("/register", data={
        "username": "student2",
        "email": "duplicate@example.com",
        "password": "AnotherPassword123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"already exists" in response.data

    with app.app_context():
        assert User.query.filter_by(
            email="duplicate@example.com"
        ).count() == 1


def test_login_success(client, app):
    with app.app_context():
        user = User(
            username="loginstudent",
            email="login@example.com"
        )
        user.set_password("CorrectPassword123")
        db.session.add(user)
        db.session.commit()

    response = client.post("/login", data={
        "email": "login@example.com",
        "password": "CorrectPassword123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome," in response.data
    assert b"loginstudent" in response.data


def test_login_wrong_password_rejected(client, app):
    with app.app_context():
        user = User(
            username="wrongpasswordstudent",
            email="wrong@example.com"
        )
        user.set_password("CorrectPassword123")
        db.session.add(user)
        db.session.commit()

    response = client.post("/login", data={
        "email": "wrong@example.com",
        "password": "IncorrectPassword123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid email or password." in response.data
    assert b"Welcome, wrongpasswordstudent!" not in response.data

def test_logout_success(client, app):
    with app.app_context():
        user = User(
            username="logoutstudent",
            email="logout@example.com"
        )
        user.set_password("Password123")
        db.session.add(user)
        db.session.commit()

    # Sign in first
    client.post("/login", data={
        "email": "logout@example.com",
        "password": "Password123"
    })

    # Sign out
    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"You have been signed out." in response.data

    # Verify protected page is no longer accessible
    response = client.get("/experiments/new")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
