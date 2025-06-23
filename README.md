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
customer-api-service/
├── api/                    # API layer
│   ├── __init__.py
│   ├── app.py             # FastAPI application setup
│   └── customer_routes.py # Customer endpoints
├── models/                # Data models
│   ├── __init__.py
│   ├── customer.py        # Pydantic schemas
│   └── db_models.py       # SQLAlchemy ORM models
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── customer_service.py # Customer CRUD operations
│   └── database.py        # Database configuration
├── tests/                 # Test suite
│   ├── __init__.py
│   └── test_customer_api.py # API tests
├── data/                  # Database files (auto-created)
├── app.py                 # Application entry point
├── requirements.txt       # Python dependencies
└── README.md             # current file
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

The API includes comprehensive unit tests using pytest and FastAPI's TestClient. Tests use a separate SQLite database file to ensure isolation from production data.

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/test_customer_api.py -v

# Run with code coverage (at 75% now)
python -m pytest tests/ --cov=api --cov=services --cov=models
```

### Test Features

- **Separate Test Database**: Uses `test_customers.db` (automatically created and cleaned up)
- **Real API Testing**: Tests actual HTTP endpoints using FastAPI TestClient
- **Data Isolation**: Each test starts with a clean database state
- **Production Code Testing**: Tests the actual API code, not mock implementations