#!/usr/bin/env python3
"""
Quick start script for the Research Assistant API server.
"""
import uvicorn
from config.settings import settings
from config.logging_config import setup_logging


def main():
    """Run the API server."""
    # Setup logging
    setup_logging(
        log_level=settings.LOG_LEVEL,
        log_file=settings.LOGS_DIR / "api.log",
        log_format="text" if settings.DEBUG else "json",
        json_logs=(settings.ENVIRONMENT == "production")
    )
    
    # Print startup banner
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║     🚀 {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}                      
║     Environment: {settings.ENVIRONMENT}                                   
║     LLM: {settings.LLM_PROVIDER} ({settings.LLM_MODEL_NAME})                      
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Run server
    uvicorn.run(
        "api.app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        workers=settings.API_WORKERS if not settings.DEBUG else 1,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=settings.DEBUG
    )


if __name__ == "__main__":
    main()