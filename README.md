# Customer API Service

A simple CRUD API for managing customer information using FastAPI.

## Features

- Create, Read, Update, and Delete customers
- Field validation
- Email uniqueness validation
- RESTful API design
- SQLite database storage

## Customer Model (As given in the requirements document)

| Attribute    | Type   | Constraints   | Notes                  |
|--------------|--------|---------------|------------------------|
| Id           | UUID   | PK            |                        |
| First Name   | String | Required      |                        |
| Middle Name  | String | Optional      | Null is acceptable     |
| Last Name    | String | Required      |                        |
| Email Address| String | Unique        |                        |
| Phone Number | String |               | Can be composite       |

## Project Structure

```
├── api/                # API routes
│   ├── app.py          # Main FastAPI application
│   └── customer_routes.py  # Customer endpoints
├── models/             # Data models
│   ├── customer.py     # Pydantic models
│   └── db_models.py    # SQLAlchemy ORM models
├── services/           # Business logic
│   ├── customer_service.py  # Customer operations
│   └── database.py     # Database connection
├── app.py             # Application entry point
└── requirements.txt   # Dependencies
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## API Endpoints

- `GET /customers/` - List all customers
- `POST /customers/` - Create a new customer
- `GET /customers/{id}` - Get a specific customer
- `PUT /customers/{id}` - Update a customer
- `DELETE /customers/{id}` - Delete a customer

## Documentation

API documentation is available at `/docs` when the server is running.

## Running the API

Start the server with the following command:

```bash
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, documentation will be available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /`: Welcome message
- `POST /customers/`: Create a new customer
- `GET /customers/`: List all customers
- `GET /customers/{customer_id}`: Get a specific customer
- `PUT /customers/{customer_id}`: Update a customer
- `DELETE /customers/{customer_id}`: Delete a customer

## Testing

The API includes unit tests that use FastAPI's TestClient and an in-memory SQLite database to test the endpoints without requiring a running server.

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run a specific test file
python -m unittest tests/test_customer_api.py
```

### Test Structure

Tests are designed to be self-contained, with each test method setting up its own test environment including:

- In-memory SQLite database
- Database tables created fresh for each test
- FastAPI dependency overrides for database sessions

This approach ensures tests are isolated and can be run in any order without dependencies between test cases.