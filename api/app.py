"""
FastAPI application factory and configuration.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from config.settings import settings
from config.logging_config import setup_logging
from src.core.exceptions import ResearchAssistantError
from api.middleware import RequestLoggingMiddleware, MetricsMiddleware
from api.routers import research, documents, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    setup_logging(
        log_level=settings.LOG_LEVEL,
        log_format=settings.LOG_FORMAT,
        json_logs=(settings.ENVIRONMENT == "production")
    )
    
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Initialize any connections or models here
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    # Cleanup connections


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    # Create FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="Intelligent Research Assistant with LangChain, LangGraph, and LangSmith",
        docs_url="/api/docs" if settings.DEBUG else None,
        redoc_url="/api/redoc" if settings.DEBUG else None,
        openapi_url="/api/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Response-Time"]
    )
    
    # Add custom middleware
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(MetricsMiddleware)
    
    # Register exception handlers
    @app.exception_handler(ResearchAssistantError)
    async def handle_app_error(request: Request, exc: ResearchAssistantError):
        """Handle application-specific errors."""
        logger.error(f"Application error: {exc.message}")
        return JSONResponse(
            status_code=400,
            content=exc.to_dict()
        )
    
    @app.exception_handler(ValueError)
    async def handle_validation_error(request: Request, exc: ValueError):
        """Handle validation errors."""
        logger.warning(f"Validation error: {exc}")
        return JSONResponse(
            status_code=422,
            content={
                "error": "VALIDATION_ERROR",
                "message": str(exc)
            }
        )
    
    @app.exception_handler(Exception)
    async def handle_general_error(request: Request, exc: Exception):
        """Handle unexpected errors."""
        logger.exception("Unhandled exception")
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_ERROR",
                "message": "An unexpected error occurred" if not settings.DEBUG else str(exc)
            }
        )
    
    # Include routers
    app.include_router(
        health.router,
        prefix="/api/v1",
        tags=["Health"]
    )
    app.include_router(
        research.router,
        prefix="/api/v1/research",
        tags=["Research"]
    )
    app.include_router(
        documents.router,
        prefix="/api/v1/documents",
        tags=["Documents"]
    )
    
    logger.info("Application configured successfully")
    return app


# Create application instance
app = create_app()