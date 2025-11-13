
"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import engine, Base
from .routes import auth_routes, device_routes, rule_routes, dashboard_routes, \
    incident_routes, operational_model_routes, detection_routes
from .config import settings
from .operational_models.model_loader import get_model_loader
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="SOaC Framework API",
    description="Security Operations as Code Framework - Phase 3B: Detection Engine & Operational Models",
    version="3.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Include routers
app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(device_routes.router, prefix="/api/v1")
app.include_router(rule_routes.router, prefix="/api/v1")
app.include_router(dashboard_routes.router, prefix="/api/v1")
app.include_router(incident_routes.router, prefix="/api/v1")
app.include_router(operational_model_routes.router, prefix="/api/v1")
app.include_router(detection_routes.router, prefix="/api/v1")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Load operational models on startup"""
    try:
        logger.info("Loading operational models...")
        model_loader = get_model_loader()
        models = model_loader.get_all_models()
        logger.info(f"Loaded {len(models)} operational models: {list(models.keys())}")
    except Exception as e:
        logger.error(f"Error loading operational models: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "SOaC Framework API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/api/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
