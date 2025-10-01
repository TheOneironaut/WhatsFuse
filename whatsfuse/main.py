"""Main entry point for WhatsFuse - unified WhatsApp API interface."""

from typing import Optional, Union, Any
from pathlib import Path

from whatsfuse.core.base_client import BaseClient
from whatsfuse.core.config import Config
from whatsfuse.core.types import Message, Chat, Contact, Group, Session
from whatsfuse.core.exceptions import (
    UnsupportedProviderError,
    ConfigurationError,
)


class WhatsFuse:
    """Unified WhatsApp API client.
    
    This is the main entry point for WhatsFuse. It provides a consistent
    interface across different WhatsApp API providers.
    
    Example:
        >>> from whatsfuse import WhatsFuse
        >>> 
        >>> # Initialize with WAHA
        >>> client = WhatsFuse(
        ...     provider="waha",
        ...     api_url="http://localhost:3000",
        ...     api_key="your-api-key"
        ... )
        >>> 
        >>> # Send a message
        >>> message = client.send_text_message(
        ...     chat_id="1234567890@c.us",
        ...     text="Hello from WhatsFuse!"
        ... )
        >>> 
        >>> # Switch to Green API
        >>> client_green = WhatsFuse(
        ...     provider="green_api",
        ...     instance_id="your-instance",
        ...     api_token="your-token"
        ... )
        >>> 
        >>> # Same method, different provider
        >>> message = client_green.send_text_message(
        ...     chat_id="1234567890",
        ...     text="Hello from Green API!"
        ... )
    """
    
    def __init__(
        self,
        provider: str,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        instance_id: Optional[str] = None,
        api_token: Optional[str] = None,
        session: str = "default",
        timeout: int = 30,
        max_retries: int = 3,
        **kwargs
    ):
        """Initialize WhatsFuse client.
        
        Args:
            provider: Provider name ("waha", "green_api")
            api_url: API URL (required for WAHA)
            api_key: API key (required for WAHA)
            instance_id: Instance ID (required for Green API)
            api_token: API token (required for Green API)
            session: Session name (for WAHA, default: "default")
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            **kwargs: Additional provider-specific parameters
        
        Raises:
            UnsupportedProviderError: If provider is not supported
            ConfigurationError: If required configuration is missing
        """
        # Create configuration
        self.config = Config(
            provider=provider,
            api_url=api_url,
            api_key=api_key,
            instance_id=instance_id,
            api_token=api_token,
            session=session,
            timeout=timeout,
            max_retries=max_retries,
            extra=kwargs,
        )
        
        # Validate configuration
        try:
            self.config.validate()
        except ValueError as e:
            raise ConfigurationError(str(e))
        
        # Initialize provider-specific client
        self._client = self._create_client()
    
    def _create_client(self) -> BaseClient:
        """Create provider-specific client.
        
        Returns:
            Provider client instance
        
        Raises:
            UnsupportedProviderError: If provider is not supported
        """
        provider = self.config.provider.lower()
        
        if provider == "waha":
            from whatsfuse.providers.waha.client import WAHAClient
            return WAHAClient(self.config)
        
        elif provider == "green_api":
            from whatsfuse.providers.green_api.client import GreenAPIClient
            return GreenAPIClient(self.config)
        
        else:
            raise UnsupportedProviderError(
                f"Provider '{provider}' is not supported. "
                f"Supported providers: waha, green_api"
            )
    
    @classmethod
    def from_env(cls) -> "WhatsFuse":
        """Create WhatsFuse client from environment variables.
        
        Environment variables:
            WHATSFUSE_PROVIDER: Provider name
            WHATSFUSE_API_URL: API URL (for WAHA)
            WHATSFUSE_API_KEY: API key (for WAHA)
            GREEN_API_INSTANCE_ID: Instance ID (for Green API)
            GREEN_API_API_TOKEN: API token (for Green API)
            WHATSFUSE_SESSION: Session name
        
        Returns:
            WhatsFuse instance
        
        Example:
            >>> from whatsfuse import WhatsFuse
            >>> client = WhatsFuse.from_env()
        """
        config = Config.from_env()
        
        return cls(
            provider=config.provider,
            api_url=config.api_url,
            api_key=config.api_key,
            instance_id=config.instance_id,
            api_token=config.api_token,
            session=config.session,
            timeout=config.timeout,
            max_retries=config.max_retries,
        )
    
    # Delegate all methods to the underlying provider client
    
    def send_text_message(
        self,
        chat_id: str,
        text: str,
        reply_to: Optional[str] = None,
        mentions: Optional[list[str]] = None,
        link_preview: bool = True,
        **kwargs
    ) -> Message:
        """Send a text message.
        
        Args:
            chat_id: The unique identifier for the chat
            text: The message text to send
            reply_to: Optional message ID to reply to (if supported)
            mentions: Optional list of phone numbers to mention (if supported)
            link_preview: Whether to show link preview (default: True)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Message object containing the sent message details
        
        Example:
            >>> message = client.send_text_message(
            ...     chat_id="1234567890@c.us",
            ...     text="Hello, World!",
            ...     reply_to="msg_abc123",
            ...     mentions=["972501234567"],
            ...     link_preview=False
            ... )
            >>> print(f"Message sent! ID: {message.id}")
        """
        return self._client.send_text_message(
            chat_id, text, reply_to, mentions, link_preview, **kwargs
        )
    
    def send_image(
        self,
        chat_id: str,
        image: Union[str, bytes, Path],
        caption: Optional[str] = None,
        reply_to: Optional[str] = None,
        filename: Optional[str] = None,
        **kwargs
    ) -> Message:
        """Send an image message.
        
        Args:
            chat_id: The unique identifier for the chat
            image: Image URL, file path, or bytes
            caption: Optional caption for the image
            reply_to: Optional message ID to reply to (if supported)
            filename: Optional custom filename for the image
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Message object
        """
        return self._client.send_image(
            chat_id, image, caption, reply_to, filename, **kwargs
        )
    
    def send_file(
        self,
        chat_id: str,
        file: Union[str, bytes, Path],
        filename: Optional[str] = None,
        caption: Optional[str] = None,
        reply_to: Optional[str] = None,
        **kwargs
    ) -> Message:
        """Send a file/document message.
        
        Args:
            chat_id: The unique identifier for the chat
            file: File URL, file path, or bytes
            filename: Optional custom filename
            caption: Optional caption for the file
            reply_to: Optional message ID to reply to (if supported)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Message object
        """
        return self._client.send_file(
            chat_id, file, filename, caption, reply_to, **kwargs
        )
    
    def send_audio(
        self,
        chat_id: str,
        audio: Union[str, bytes, Path],
        reply_to: Optional[str] = None,
        **kwargs
    ) -> Message:
        """Send an audio message.
        
        Args:
            chat_id: The unique identifier for the chat
            audio: Audio URL, file path, or bytes
            reply_to: Optional message ID to reply to (if supported)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Message object
        """
        return self._client.send_audio(chat_id, audio, reply_to, **kwargs)
    
    def send_video(
        self,
        chat_id: str,
        video: Union[str, bytes, Path],
        caption: Optional[str] = None,
        reply_to: Optional[str] = None,
        **kwargs
    ) -> Message:
        """Send a video message.
        
        Args:
            chat_id: The unique identifier for the chat
            video: Video URL, file path, or bytes
            caption: Optional caption for the video
            reply_to: Optional message ID to reply to (if supported)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Message object
        """
        return self._client.send_video(
            chat_id, video, caption, reply_to, **kwargs
        )
    
    def send_location(
        self,
        chat_id: str,
        latitude: float,
        longitude: float,
        name: Optional[str] = None,
        address: Optional[str] = None,
        reply_to: Optional[str] = None,
        **kwargs
    ) -> Message:
        """Send a location message.
        
        Args:
            chat_id: The unique identifier for the chat
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            name: Optional location name
            address: Optional location address
            reply_to: Optional message ID to reply to (if supported)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Message object
        """
        return self._client.send_location(
            chat_id, latitude, longitude, name, address, reply_to, **kwargs
        )
    
    def get_chats(self, limit: Optional[int] = None, **kwargs) -> list[Chat]:
        """Get list of chats.
        
        Args:
            limit: Maximum number of chats to return
            **kwargs: Additional provider-specific parameters
        
        Returns:
            List of Chat objects
        """
        return self._client.get_chats(limit, **kwargs)
    
    def get_chat_history(
        self,
        chat_id: str,
        limit: int = 50,
        **kwargs
    ) -> list[Message]:
        """Get message history for a specific chat.
        
        Args:
            chat_id: The unique identifier for the chat
            limit: Maximum number of messages to return
            **kwargs: Additional provider-specific parameters
        
        Returns:
            List of Message objects
        """
        return self._client.get_chat_history(chat_id, limit, **kwargs)
    
    def mark_as_read(
        self,
        chat_id: str,
        message_id: Optional[str] = None,
        **kwargs
    ) -> bool:
        """Mark message(s) as read.
        
        Args:
            chat_id: The unique identifier for the chat
            message_id: Optional specific message ID to mark as read
            **kwargs: Additional provider-specific parameters
        
        Returns:
            True if successful
        """
        return self._client.mark_as_read(chat_id, message_id, **kwargs)
    
    def get_contacts(self, **kwargs) -> list[Contact]:
        """Get list of contacts.
        
        Args:
            **kwargs: Additional provider-specific parameters
        
        Returns:
            List of Contact objects
        """
        return self._client.get_contacts(**kwargs)
    
    def get_contact_info(self, contact_id: str, **kwargs) -> Contact:
        """Get information about a specific contact.
        
        Args:
            contact_id: The unique identifier for the contact
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Contact object
        """
        return self._client.get_contact_info(contact_id, **kwargs)
    
    def check_number_status(self, phone_number: str, **kwargs) -> bool:
        """Check if a phone number is registered on WhatsApp.
        
        Args:
            phone_number: Phone number to check
            **kwargs: Additional provider-specific parameters
        
        Returns:
            True if number is on WhatsApp, False otherwise
        """
        return self._client.check_number_status(phone_number, **kwargs)
    
    # Session management (for providers that support it)
    
    def create_session(self, name: str, **kwargs) -> Session:
        """Create a new session (if supported by provider).
        
        Args:
            name: Session name
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Session object
        """
        return self._client.create_session(name, **kwargs)
    
    def get_sessions(self, **kwargs) -> list[Session]:
        """Get list of sessions (if supported by provider).
        
        Args:
            **kwargs: Additional provider-specific parameters
        
        Returns:
            List of Session objects
        """
        return self._client.get_sessions(**kwargs)
    
    # Context manager support
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def close(self):
        """Close client and cleanup resources."""
        self._client.close()


# Async version placeholder
class AsyncWhatsFuse:
    """Async version of WhatsFuse client.
    
    This is a placeholder for the async implementation.
    Full async support will be added in a future version.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize async client."""
        raise NotImplementedError(
            "Async support is not yet implemented. "
            "Use the synchronous WhatsFuse class for now."
        )

