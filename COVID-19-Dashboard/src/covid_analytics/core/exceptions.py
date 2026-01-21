"""Custom exceptions for COVID Analytics"""


class CovidAnalyticsError(Exception):
    """Base exception for all COVID Analytics errors"""
    pass


class DataLoadError(CovidAnalyticsError):
    """Raised when data loading fails"""
    pass


class DataValidationError(CovidAnalyticsError):
    """Raised when data validation fails"""
    pass


class DataProcessingError(CovidAnalyticsError):
    """Raised when data processing fails"""
    pass


class ConfigurationError(CovidAnalyticsError):
    """Raised when configuration is invalid"""
    pass


class APIError(CovidAnalyticsError):
    """Raised when external API calls fail"""
    pass


class CacheError(CovidAnalyticsError):
    """Raised when cache operations fail"""
    pass
