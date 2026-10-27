# Online Bookstore REST API

A Flask REST API for viewing and adding books to an in-memory bookstore
inventory. Data resets when the application restarts.

## Setup and run

From this directory:

```powershell
py -m pip install -r requirements.txt
py app.py
```

The API runs at `http://127.0.0.1:5000`.

## Endpoints

### GET `/books`

Returns all books:

```json
{
  "books": [
    {
      "id": 1,
      "title": "The Hobbit",
      "author": "J. R. R. Tolkien",
      "price": 12.5
    }
  ]
}
```

### GET `/books/<id>`

Returns one book by numeric ID. For example:

```text
GET http://127.0.0.1:5000/books/1
```

Returns `404 Not Found` when the ID does not exist.

### POST `/books`

Adds a book. Send a JSON object containing `title`, `author`, and a
non-negative numeric `price`:

```json
{
  "title": "The Hobbit",
  "author": "J. R. R. Tolkien",
  "price": 12.50
}
```

The successful response is `201 Created` and includes the generated book ID.
Invalid JSON, missing fields, or an invalid price return `400 Bad Request`.

## Postman or browser verification

1. Run `py app.py`.
2. Open `http://127.0.0.1:5000/books` in a browser. Initially it returns
   `{"books":[]}`.
3. In Postman, create a `POST` request to
   `http://127.0.0.1:5000/books`.
4. Select **Body > raw > JSON** and send the sample JSON above.
5. Verify the `201` response and note the generated `id`.
6. Open `http://127.0.0.1:5000/books/<id>` in a browser or Postman.
7. Open `http://127.0.0.1:5000/books` again and verify the book appears.

PowerShell example:

```powershell
$body = @{
    title = "The Hobbit"
    author = "J. R. R. Tolkien"
    price = 12.50
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/books" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

## Test cases

Run the automated tests:

```powershell
py -m pytest -q
```

| # | Request | Expected result |
|---|---|---|
| 1 | `GET /books` with no books | `200`, with an empty `books` array |
| 2 | Valid `POST /books` | `201`, with the created book and generated `id` |
| 3 | `GET /books/1` after adding book 1 | `200`, with the matching book details |
| 4 | `GET /books/999` | `404`, with `Book not found` |
| 5 | POST without `author` | `400`, with `missing_fields` |
| 6 | POST with a negative price | `400`, with a price validation error |
