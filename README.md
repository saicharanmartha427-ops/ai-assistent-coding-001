# Student Management REST API

A small Flask REST API for retrieving and registering student records.
Records are stored in memory, so they reset whenever the application restarts.

## Setup

From this directory, create and activate a virtual environment, then install
the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

## Run the API

```powershell
py app.py
```

The API is available at `http://127.0.0.1:5000`.

Opening `http://127.0.0.1:5000/` displays the available API endpoints.

## Endpoints

### GET `/students`

Returns all currently registered students:

```json
{
  "students": [
    {
      "id": 1,
      "name": "Asha Sharma",
      "email": "asha@example.com",
      "course": "Computer Science"
    }
  ]
}
```

### POST `/students`

Registers a student. The JSON body must include non-empty `name`, `email`, and
`course` fields:

```json
{
  "name": "Asha Sharma",
  "email": "asha@example.com",
  "course": "Computer Science"
}
```

Successful requests return `201 Created` and the new student, including its
generated `id`. A duplicate email returns `409 Conflict`; missing or invalid
input returns `400 Bad Request`.

## Browser/Postman verification

1. Start the server with `py app.py`.
2. Open `http://127.0.0.1:5000/students` in a browser. The initial response
   should be `{"students":[]}`.
3. In Postman, create a `POST` request to
   `http://127.0.0.1:5000/students`.
4. Select **Body > raw > JSON**, enter the sample body above, and send it.
   Verify the `201` response and generated `id`.
5. Open the GET URL again and verify the new student appears in the list.

## Test cases

Run the automated test cases with:

```powershell
py -m pytest -q
```

| # | Request | Expected result |
|---|---|---|
| 1 | `GET /students` before adding data | `200`, with an empty `students` array |
| 2 | Valid `POST /students` with all three fields | `201`, with the created student and an integer `id` |
| 3 | `GET /students` after a successful POST | `200`, with the new student in `students` |
| 4 | POST with a missing `course` field | `400`, with `missing_fields` containing `course` |
| 5 | POST with an email already registered | `409`, with a duplicate-email error |
| 6 | POST with a non-JSON body | `400`, with a request-body error |
