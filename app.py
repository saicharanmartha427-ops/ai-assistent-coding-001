from __future__ import annotations

from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)
    students: list[dict[str, str | int]] = []
    next_id = 1

    @app.get("/")
    def api_status():
        return jsonify(
            {
                "message": "Student Management API",
                "endpoints": {
                    "get_students": "GET /students",
                    "add_student": "POST /students",
                },
            }
        )

    @app.get("/students")
    def get_students():
        return jsonify({"students": students})

    @app.post("/students")
    def add_student():
        nonlocal next_id

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400

        required_fields = ("name", "email", "course")
        missing_fields = [
            field
            for field in required_fields
            if not isinstance(payload.get(field), str) or not payload[field].strip()
        ]
        if missing_fields:
            return (
                jsonify(
                    {
                        "error": "Fields name, email, and course are required",
                        "missing_fields": missing_fields,
                    }
                ),
                400,
            )

        email = payload["email"].strip().lower()
        if any(student["email"] == email for student in students):
            return jsonify({"error": "A student with this email already exists"}), 409

        student = {
            "id": next_id,
            "name": payload["name"].strip(),
            "email": email,
            "course": payload["course"].strip(),
        }
        students.append(student)
        next_id += 1
        return jsonify(student), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
