class AmidaError(Exception):
    """Base error for application-level failures."""


class TemplateNotFoundError(AmidaError):
    """Raised when a guild template is not found."""


class LastUsedNotFoundError(AmidaError):
    """Raised when user x guild last used template does not exist."""


class DuplicateTemplateTitleError(AmidaError):
    """Raised when template title duplicates in guild."""


class SaveFailedError(AmidaError):
    """Raised when create or upsert operations fail."""


class DrawFailedError(AmidaError):
    """Raised when draw operation cannot continue."""
