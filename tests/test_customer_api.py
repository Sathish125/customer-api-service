import unittest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.app import app
from models.db_models import Base, Customer
from services.database import get_db

class TestCustomerAPI(unittest.TestCase):
    def setUp(self):
        # Create a test database in memory
        self.engine = create_engine("sqlite:///:memory:")
        self.TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create all tables in the test database
        Base.metadata.create_all(bind=self.engine)
        
        # Override the get_db dependency (to use the test database)
        def override_get_db():
            db = self.TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()
        
        app.dependency_overrides[get_db] = override_get_db
        
        # Create a test client
        self.client = TestClient(app)
    
    def tearDown(self):
        # Clean up after each test
        Base.metadata.drop_all(bind=self.engine)
        # Remove the dependency override
        app.dependency_overrides.clear()
    
    def test_create_customer(self):
        """Test creating a new customer"""

        customer_data = {
            "first_name": "Sathish",
            "last_name": "Poorna",
            "email": "sathishtest@gmail.com",
            "phone_number": "555-555-5555"
        }
        
        # Send POST request to create customer
        response = self.client.post("/customers/", json=customer_data)
        
        # Check response
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["first_name"], customer_data["first_name"])
        self.assertEqual(data["last_name"], customer_data["last_name"])
        self.assertEqual(data["email"], customer_data["email"])
        self.assertEqual(data["phone_number"], customer_data["phone_number"])
        self.assertIsNotNone(data["id"])
        
    def test_read_customer(self):
        """Test reading a customer"""

        customer_data = {
            "first_name": "Sathish",
            "last_name": "Poorna",
            "email": "sathishtest@gmail.com",
            "phone_number": "555-555-5555"
        }
        
        # Create the customer
        create_response = self.client.post("/customers/", json=customer_data)
        self.assertEqual(create_response.status_code, 201)
        customer_id = create_response.json()["id"]
        
        # Send GET request to read the customer
        response = self.client.get("/customers/{}".format(customer_id))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], "Sathish")
        self.assertEqual(data["last_name"], "Poorna")
        self.assertEqual(data["email"], "sathishtest@gmail.com")
        self.assertEqual(data["phone_number"], "555-555-5555")
        self.assertEqual(data["id"], customer_id)


if __name__ == "__main__":
    unittest.main()
