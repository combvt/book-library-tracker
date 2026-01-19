# Book Library Tracker
A FastAPI-based application for managing a personal book library, supporting
both SQL and JSON storage backends, Google Books API integration, and a CLI
for browsing and searching books.

## Features

- Search books using the Google Books API
- Add books to a personal library
- View stored books and detailed information
- Remove books from the library

---

- Support for both SQLite & JSON storage backends
- Ability to choose storage type when using the CLI
- Persistent storage across sessions

---

- Interactive command-line interface for searching and managing books
- Detailed book view within the CLI
- Option to switch between searching and browsing the library

---

- REST API built with FastAPI (SQL storage)
- CRUD operations for managing books
- Search, random book, and library statistics endpoints
- Automatic API documentation via Swagger UI

---

- Request & response validation using Pydantic
- Structured error handling for invalid requests

---

- Automated tests for storage layer, API endpoints, and Google Books client
- Mocked external API calls in tests

## Tech stack
- Python - core language
- FastAPI - REST API framework
- SQLite / JSON - data storage
- Google Books API - external book data source
- Pydantic - request/response validation
- Requests - HTTP client
- Pytest - automated testing

## Project Structure
```text
├── src/
│   ├── api_app.py        # FastAPI application
│   ├── main.py           # CLI entrypoint
│   ├── library.py        # Core library logic
│   ├── models.py         # Domain models
│   ├── schemas.py        # Pydantic API schemas
│   ├── google_api_client.py
│   ├── utils.py
│   ├── text_utils.py
│   ├── db.py
│   ├── config.py
│   ├── storage/
│   │   ├── storage_base.py
│   │   ├── json_storage.py
│   │   └── sql_storage.py
│   └── exceptions.py
├── tests/                # Pytest test suite
├── requirements.txt
├── .env.example
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Setup
#### Prerequisites
- Python 3.11+
- Git (optional, for cloning the repository)
- Google Books API key required for full functionality

#### Clone the repo
- `git clone https://github.com/combvt/book-library-tracker.git`
- `cd book-library-tracker`

#### Create & activate a virtual environment
From the project root directory:
- Windows

```bash
python -m venv .venv

.venv\Scripts\Activate.ps1
```
If script execution is disabled, you may need to adjust PowerShell execution policy.

- Linux / macOS
```bash
python3 -m venv .venv

source .venv/bin/activate
```
Deactivate the virtual environment using `deactivate`


#### Install dependencies

Make sure `pip` is up to date:

```bash
python -m pip install --upgrade pip
```
Install the project dependencies
```bash
pip install -r requirements.txt
```


## Environment variables
This project uses environment variables, stored in a `.env` file.

Create your `.env` file via:

```bash
cp .env.example .env
```
The `.env` file defines the following variables:
- `API_KEY` - required, Google Books API key
- `LIBRARY_PATH` - optional, defaults to `book_library.json`
- `DB_PATH` - optional, defaults to `books.db`

Only `API_KEY` is required in order for the application to run.

## How to run

#### Run the CLI
- Run the application from the project root directory via:
```bash
python -m src.main
```
- You will be prompted to choose a storage backend (`json` or `sql`)
- Search for books using the Google Books API or browse your existing library
- When browsing the library, you can view detailed information about a book or remove it from the library

#### Run the API
- Host your local server via:
```bash
uvicorn src.api_app:app --reload
```
- The API will be available at `http://127.0.0.1:8000`
- Interactive API documentation is available via Swagger UI at `http://127.0.0.1:8000/docs`
- The API uses the SQL storage backend only

## API endpoints overview
- All endpoints are available via Swagger UI at `/docs`.
- API uses SQL storage only.

#### Library endpoints
- `GET /books` — list all books
- `GET /books?q=...` — search within stored library (title/author/description)
- `GET /books/{sql_index}` — fetch a single book by SQL id
- `DELETE /books/{sql_index}` — delete a book by SQL id
- `PUT /books/{sql_index}` — update fields on a stored book

#### Google Books integration
- `GET /search/google?q=...&results=...` — search via Google Books API (does not store)
- `POST /books/from-google/{book_id}` — save book by Google ID

#### Utility endpoints
- `GET /books/random` — fetch a random book from library
- `GET /books/stats` — library statistics (total books, unique authors, page stats, earliest/latest added)

#### Minimal notes
- `results` is limited (1-20)
- Update endpoint accepts partial fields (only provided fields are updated)
- Common status codes (200/201/204, 404, 409)

## Data model notes

#### Book 
- Core domain model representing a book fetched from Google Books
- Stored fields include title, author, publication date, page count, categories, description, ISBN and Google Books ID

#### SQL metadata
- When using SQL storage, books are assigned an auto-increment SQL ID
- A `created_at` timestamp is automatically stored when the book is added

#### Storage differences
- JSON storage persists only the core book fields without additional metadata
- SQL storage supports additional metadata and statistical queries

#### API schemas (Pydantic)
- Request and response models are defined using Pydantic
- These models control validation and API responses but are not used internally by the CLI

## Tests
- Run the test suite using `pytest`
- Tests cover SQL storage logic, mocked Google Books API calls, and REST API endpoints

## Common issues / troubleshooting
- Missing API KEY → create `.env` and set `API_KEY`  

- If using SQLite: DB file location controlled by `DB_PATH`

- If JSON file corrupted/invalid → app treats it as empty (your JSON storage returns [] )

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for a history of feature additions and the evolution of the project over time.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Notes
- This project was built to practice backend fundamentals such as API design,
data persistence, external API integration, and testing.

