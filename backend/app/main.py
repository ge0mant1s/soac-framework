
"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import engine, Base
from .routes import auth_routes, device_routes, rule_routes, dashboard_routes, \
    incident_routes, operational_model_routes, detection_routes, event_routes
from .config import settings
from .operational_models.model_loader import get_model_loader
from .services.event_ingestion import event_ingestion_service
from datetime import datetime
import logging
import asyncio
import os

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

# Configure CORS - supports Railway deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Only add HSTS in production
    if settings.ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

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
app.include_router(event_routes.router, prefix="/api/v1")

# Background task for event collection
background_task = None

# Startup event
@app.on_event("startup")
async def startup_event():
    """Load operational models and start background tasks on startup"""
    global background_task
    
    try:
        logger.info("Loading operational models...")
        model_loader = get_model_loader()
        models = model_loader.get_all_models()
        logger.info(f"Loaded {len(models)} operational models: {list(models.keys())}")
    except Exception as e:
        logger.error(f"Error loading operational models: {str(e)}")
    
    # Start background event collection if enabled
    enable_background_collection = os.getenv("ENABLE_BACKGROUND_COLLECTION", "true").lower() == "true"
    
    if enable_background_collection:
        try:
            logger.info("Starting background event collection task...")
            background_task = asyncio.create_task(event_ingestion_service.start_background_collection())
            logger.info("Background event collection started")
        except Exception as e:
            logger.error(f"Error starting background event collection: {str(e)}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Stop background tasks on shutdown"""
    global background_task
    
    try:
        logger.info("Stopping background tasks...")
        event_ingestion_service.stop()
        
        if background_task:
            background_task.cancel()
            try:
                await background_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Background tasks stopped")
    except Exception as e:
        logger.error(f"Error stopping background tasks: {str(e)}")

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
    """Health check endpoint for Railway and monitoring"""
    from .database import SessionLocal
    
    status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT,
        "version": "3.0.0"
    }
    
    # Check database connectivity
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        status["database"] = "connected"
    except Exception as e:
        status["status"] = "unhealthy"
        status["database"] = "disconnected"
        status["error"] = str(e)
        logger.error(f"Health check failed: {str(e)}")
    
    return status
