"""
Main FastAPI application for Gemma Chatbot
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from backend.api.routes import router
from backend.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="A simple conversational chatbot powered by Google Gemma-3-1B-IT",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["chatbot"])


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to Gemma Chatbot API",
        "version": settings.API_VERSION,
        "model": settings.MODEL_NAME,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    logger.info("🚀 Starting Gemma Chatbot API...")
    logger.info(f"📦 Model: {settings.MODEL_NAME}")
    logger.info(f"🌡️  Temperature: {settings.TEMPERATURE}")
    logger.info(f"📝 Max Tokens: {settings.MAX_TOKENS}")
    logger.info("✅ API is ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    logger.info("👋 Shutting down Gemma Chatbot API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )