
import pytest

from app import create_app, db
from app.models import User, Experiment


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
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


@pytest.fixture
def logged_in_client(client, app):
    with app.app_context():
        user = User(
            username="experimentstudent",
            email="experiment@example.com"
        )
        user.set_password("Password123")
        db.session.add(user)
        db.session.commit()

    client.post("/login", data={
        "email": "experiment@example.com",
        "password": "Password123"
    })

    return client



def test_signed_in_user_can_save_experiment(logged_in_client, app):
    response = logged_in_client.post("/experiments/new", data={
        "title": "Testing a Prompt",
        "prompt": "Explain photosynthesis.",
        "ai_response": "Photosynthesis is how plants convert light into energy.",
        "relevance_score": "5",
        "clarity_score": "4",
        "completeness_score": "3",
        "notes": "The explanation was clear."
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Your experiment has been saved successfully!" in response.data

    with app.app_context():
        experiment = Experiment.query.first()

        assert experiment is not None
        assert experiment.title == "Testing a Prompt"
        assert experiment.relevance_score == 5
        assert experiment.clarity_score == 4
        assert experiment.completeness_score == 3
        assert experiment.rating == 4.0
        assert experiment.user.username == "experimentstudent"



def test_signed_out_user_cannot_create_experiment(client):
    response = client.get("/experiments/new")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_invalid_rating_is_rejected(logged_in_client, app):
    response = logged_in_client.post("/experiments/new", data={
        "title": "Invalid Rating Test",
        "prompt": "Test prompt",
        "ai_response": "Test response",
        "relevance_score": "6",
        "clarity_score": "4",
        "completeness_score": "5",
        "notes": "Testing invalid rating."
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Each evaluation score must be between 1 and 5." in response.data

    with app.app_context():
        assert Experiment.query.count() == 0


def test_missing_required_field_is_rejected(logged_in_client, app):
    response = logged_in_client.post("/experiments/new", data={
        "title": "",
        "prompt": "Test prompt",
        "ai_response": "Test response",
        "relevance_score": "4",
        "clarity_score": "4",
        "completeness_score": "4",
        "notes": ""
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Please complete the title, prompt, and AI response." in response.data

    with app.app_context():
        assert Experiment.query.count() == 0
