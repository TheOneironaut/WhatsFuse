"""Custom exceptions for WhatsFuse."""


class WhatsFuseError(Exception):
    """Base exception for all WhatsFuse errors."""
    
    def __init__(self, message: str, provider: str | None = None):
        self.message = message
        self.provider = provider
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.provider:
            return f"[{self.provider}] {self.message}"
        return self.message


class ProviderError(WhatsFuseError):
    """Exception for provider-specific errors."""
    pass


class AuthenticationError(WhatsFuseError):
    """Exception for authentication failures."""
    pass


class RateLimitError(WhatsFuseError):
    """Exception for rate limit errors."""
    
    def __init__(
        self,
        message: str,
        provider: str | None = None,
        retry_after: int | None = None
    ):
        self.retry_after = retry_after
        super().__init__(message, provider)


class InvalidRequestError(WhatsFuseError):
    """Exception for invalid request parameters."""
    pass


class NetworkError(WhatsFuseError):
    """Exception for network-related errors."""
    pass


class SessionNotFoundError(WhatsFuseError):
    """Exception for session not found errors (WAHA-specific)."""
    pass


class MessageNotSentError(WhatsFuseError):
    """Exception for message sending failures."""
    pass


class InstanceNotAuthorizedError(WhatsFuseError):
    """Exception for unauthorized instance errors (Green API-specific)."""
    pass


class ConfigurationError(WhatsFuseError):
    """Exception for configuration errors."""
    pass


class UnsupportedProviderError(WhatsFuseError):
    """Exception for unsupported provider."""
    pass


class TransformationError(WhatsFuseError):
    """Exception for data transformation errors."""
    pass

