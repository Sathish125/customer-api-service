import logging
import os
from fastapi import FastAPI
from services.database import init_db
from api.customer_routes import router as customer_router

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("customer-api")

app = FastAPI(title="Customer API Service")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Customer API Service")
    init_db()
    logger.info("Database initialized successfully")

# Root endpoint
@app.get("/")
def read_root():
    logger.debug("Root endpoint accessed")
    return {"message": "Welcome to Customer API Service"}

# Health check endpoint
@app.get("/health")
def health_check():
    logger.debug("Health check endpoint accessed")
    return {"status": "healthy", "service": "customer-api"}

# Include routers
app.include_router(customer_router, prefix="/customers", tags=["customers"])
