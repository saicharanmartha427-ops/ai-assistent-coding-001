import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_get_students_returns_empty_list(client):
    response = client.get("/students")

    assert response.status_code == 200
    assert response.get_json() == {"students": []}


def test_root_returns_api_information(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Student Management API"


def test_post_students_creates_student(client):
    response = client.post(
        "/students",
        json={
            "name": "Asha Sharma",
            "email": "asha@example.com",
            "course": "Computer Science",
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "name": "Asha Sharma",
        "email": "asha@example.com",
        "course": "Computer Science",
    }

    list_response = client.get("/students")
    assert list_response.get_json()["students"] == [response.get_json()]


def test_post_students_rejects_missing_fields(client):
    response = client.post(
        "/students",
        json={"name": "Asha Sharma", "email": "asha@example.com"},
    )

    assert response.status_code == 400
    assert response.get_json()["missing_fields"] == ["course"]


def test_post_students_rejects_duplicate_email_case_insensitively(client):
    student = {
        "name": "Asha Sharma",
        "email": "asha@example.com",
        "course": "Computer Science",
    }
    client.post("/students", json=student)

    response = client.post(
        "/students",
        json={**student, "name": "Another Student", "email": "ASHA@example.com"},
    )

    assert response.status_code == 409
    assert response.get_json() == {
        "error": "A student with this email already exists"
    }


def test_post_students_rejects_non_json_body(client):
    response = client.post("/students", data="not json")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Request body must be a JSON object"
