from fastapi import FastAPI
from services.database import init_db
from api.customer_routes import router as customer_router

app = FastAPI(title="Customer API Service")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Customer API Service"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "customer-api"}

# Include routers
app.include_router(customer_router, prefix="/customers", tags=["customers"])
