import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_get_books_returns_empty_list(client):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.get_json() == {"books": []}


def test_post_books_creates_book(client):
    response = client.post(
        "/books",
        json={
            "title": "The Hobbit",
            "author": "J. R. R. Tolkien",
            "price": 12.5,
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "title": "The Hobbit",
        "author": "J. R. R. Tolkien",
        "price": 12.5,
    }


def test_get_book_returns_book_by_id(client):
    created = client.post(
        "/books",
        json={"title": "1984", "author": "George Orwell", "price": 9.99},
    ).get_json()

    response = client.get(f"/books/{created['id']}")

    assert response.status_code == 200
    assert response.get_json() == created


def test_get_book_returns_not_found_for_unknown_id(client):
    response = client.get("/books/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}


def test_post_books_rejects_missing_fields(client):
    response = client.post(
        "/books",
        json={"title": "The Hobbit", "price": 12.5},
    )

    assert response.status_code == 400
    assert response.get_json()["missing_fields"] == ["author"]


def test_post_books_rejects_invalid_price(client):
    response = client.post(
        "/books",
        json={"title": "The Hobbit", "author": "J. R. R. Tolkien", "price": -1},
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Price must be a non-negative number"
    }
