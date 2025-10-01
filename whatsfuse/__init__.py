"""
WhatsFuse - Unified WhatsApp API Interface

A Python SDK that provides a single, consistent interface for multiple
WhatsApp API providers, inspired by LiteLLM.
"""

__version__ = "0.1.0"

from whatsfuse.main import WhatsFuse, AsyncWhatsFuse
from whatsfuse.core.exceptions import (
    WhatsFuseError,
    ProviderError,
    AuthenticationError,
    RateLimitError,
    InvalidRequestError,
    NetworkError,
    SessionNotFoundError,
    MessageNotSentError,
    InstanceNotAuthorizedError,
)
from whatsfuse.core.types import (
    Message,
    Chat,
    Contact,
    Group,
    Session,
)

__all__ = [
    # Main classes
    "WhatsFuse",
    "AsyncWhatsFuse",
    # Exceptions
    "WhatsFuseError",
    "ProviderError",
    "AuthenticationError",
    "RateLimitError",
    "InvalidRequestError",
    "NetworkError",
    "SessionNotFoundError",
    "MessageNotSentError",
    "InstanceNotAuthorizedError",
    # Types
    "Message",
    "Chat",
    "Contact",
    "Group",
    "Session",
]


def list_providers() -> list[str]:
    """List all supported providers.
    
    Returns:
        List of provider names
    """
    return ["waha", "green_api"]


def get_version() -> str:
    """Get WhatsFuse version.
    
    Returns:
        Version string
    """
    return __version__

