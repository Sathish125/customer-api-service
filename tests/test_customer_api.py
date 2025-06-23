import unittest
import os
import sys
from fastapi.testclient import TestClient

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Override database URL for testing
import services.database
services.database.SQLALCHEMY_DATABASE_URL = "sqlite:///./data/test_customers.db"
services.database.engine = services.database.create_engine(
    services.database.SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
services.database.SessionLocal = services.database.sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=services.database.engine
)

from api.app import app
from services.database import Base, engine, SessionLocal
from models.db_models import Customer

class TestCustomerAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create tables once for all tests
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
    
    @classmethod
    def tearDownClass(cls):
        # Clean up after all tests
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("data/test_customers.db"):
            os.remove("data/test_customers.db")
    
    def setUp(self):
        # Clear data before each test
        db = SessionLocal()
        db.query(Customer).delete()
        db.commit()
        db.close()
    
    def test_create_customer(self):
        """Test creating a new customer"""
        customer_data = {
            "first_name": "Sathish",
            "last_name": "Poorna",
            "email": "sathishtest@gmail.com",
            "phone_number": "555-555-5555"
        }
        response = self.client.post("/customers/", json=customer_data)
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
            "email": "sathishtest2@gmail.com",
            "phone_number": "555-555-5555"
        }
        create_response = self.client.post("/customers/", json=customer_data)
        self.assertEqual(create_response.status_code, 201)
        customer_id = create_response.json()["id"]
        
        response = self.client.get(f"/customers/{customer_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], "Sathish")
        self.assertEqual(data["last_name"], "Poorna")
        self.assertEqual(data["email"], "sathishtest2@gmail.com")
        self.assertEqual(data["phone_number"], "555-555-5555")
        self.assertEqual(data["id"], customer_id)

if __name__ == "__main__":
    unittest.main()
