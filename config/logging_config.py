"""
Structured logging configuration using loguru.
"""
import sys
import logging
from pathlib import Path
from typing import Optional
from loguru import logger


class InterceptHandler(logging.Handler):
    """Intercept standard logging and route to loguru."""
    
    def emit(self, record: logging.LogRecord):
        """Emit a log record."""
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    log_format: str = "text",
    json_logs: bool = False
) -> logger:
    """
    Configure application logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        log_format: Format type ("text" or "json")
        json_logs: Whether to use JSON formatting
    
    Returns:
        Configured logger instance
    """
    logger.remove()
    
    if json_logs or log_format == "json":
        logger.add(
            sys.stdout,
            format="{message}",
            level=log_level,
            serialize=True,
            backtrace=True,
            diagnose=True if log_level == "DEBUG" else False,
        )
    else:
        logger.add(
            sys.stdout,
            colorize=True,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            ),
            level=log_level,
            backtrace=True,
            diagnose=True if log_level == "DEBUG" else False,
        )
    
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            str(log_file),
            rotation="500 MB",
            retention="30 days",
            compression="zip",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
                   "{name}:{function}:{line} | {message}",
            level=log_level,
            backtrace=True,
        )
    
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    for logger_name in ["uvicorn", "uvicorn.error", "fastapi"]:
        logging.getLogger(logger_name).handlers = [InterceptHandler()]
    
    return logger


def get_logger(name: str) -> logger:
    """Get a logger instance for a specific module."""
    return logger.bind(name=name)