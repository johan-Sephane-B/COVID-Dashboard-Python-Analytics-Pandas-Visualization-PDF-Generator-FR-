"""
Structured logging using structlog.
Provides JSON logs for production and human-readable logs for development.
"""

import logging
import sys
from typing import Any, Dict

import structlog
from structlog.types import EventDict, Processor

from covid_analytics.core.config import get_settings


def add_app_context(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Add application context to log entries"""
    settings = get_settings()
    event_dict["app"] = settings.app_name
    event_dict["version"] = settings.app_version
    return event_dict


def setup_logging() -> None:
    """Configure structured logging"""
    settings = get_settings()
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )
    
    # Processors for structlog
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        add_app_context,
    ]
    
    # Add format-specific processors
    if settings.log_format == "json":
        processors.append(structlog.processors.format_exc_info)
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured structlog logger
    
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("data_loaded", rows=1000, columns=20)
    """
    return structlog.get_logger(name)


# Initialize logging on module import
setup_logging()
