from __future__ import annotations

from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)
    books: list[dict[str, str | int | float]] = []
    next_id = 1

    @app.get("/")
    def api_status():
        return jsonify(
            {
                "message": "Online Bookstore API",
                "endpoints": {
                    "get_books": "GET /books",
                    "get_book": "GET /books/<id>",
                    "add_book": "POST /books",
                },
            }
        )

    @app.get("/books")
    def get_books():
        return jsonify({"books": books})

    @app.get("/books/<int:book_id>")
    def get_book(book_id: int):
        book = next((item for item in books if item["id"] == book_id), None)
        if book is None:
            return jsonify({"error": "Book not found"}), 404
        return jsonify(book)

    @app.post("/books")
    def add_book():
        nonlocal next_id

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400

        required_text_fields = ("title", "author")
        missing_fields = [
            field
            for field in required_text_fields
            if not isinstance(payload.get(field), str) or not payload[field].strip()
        ]
        if missing_fields:
            return (
                jsonify(
                    {
                        "error": "Title and author are required",
                        "missing_fields": missing_fields,
                    }
                ),
                400,
            )

        price = payload.get("price")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            return jsonify({"error": "Price must be a non-negative number"}), 400

        book = {
            "id": next_id,
            "title": payload["title"].strip(),
            "author": payload["author"].strip(),
            "price": round(float(price), 2),
        }
        books.append(book)
        next_id += 1
        return jsonify(book), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
