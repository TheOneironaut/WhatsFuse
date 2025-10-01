"""Base client interface that all providers must implement.

UNIFIED INTERFACE PHILOSOPHY:
-----------------------------
This base client defines a FIXED, UNIFIED API inspired by WAHA's design.
All providers (WAHA, Green API, etc.) MUST implement the SAME interface
with the SAME parameters.

Key principles:
1. Users write code ONCE - it works with ALL providers
2. Parameters are UNIFIED and EXPLICIT (not hidden in **kwargs)
3. Each provider TRANSLATES unified parameters to its specific API format
4. Unsupported features are handled gracefully (warnings/emulation/documentation)

Example:
    # Same code works with both WAHA and Green API!
    client.send_text_message(
        chat_id="123",
        text="Hello",
        reply_to="msg_456",      # WAHA uses 'reply_to', Green API uses 'quotedMessageId'
        mentions=["972501234567"],  # Unified parameter
        link_preview=False       # Unified parameter
    )
    
The provider implementation handles the translation internally.
"""

from abc import ABC, abstractmethod
from typing import Optional, Union, Any
from pathlib import Path

from whatsfuse.core.types import Message, Chat, Contact, Group, Session
from whatsfuse.core.config import Config


class BaseClient(ABC):
    """Abstract base class for all WhatsApp API provider clients.
    
    All provider implementations must inherit from this class and implement
    all abstract methods with the UNIFIED parameter interface.
    
    The interface is based on WAHA's API design, with providers translating
    their specific APIs to match this unified interface.
    """
    
    def __init__(self, config: Config):
        """Initialize the base client.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.provider_name = config.provider
    
    # Message Sending Methods
    
    @abstractmethod
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
        
        This method uses unified parameters that work across all providers.
        Each provider translates these to its specific API format.
        
        Args:
            chat_id: The unique identifier for the chat
            text: The message text to send
            reply_to: Optional message ID to reply to (if supported)
            mentions: Optional list of phone numbers to mention (if supported)
            link_preview: Whether to show link preview (default: True)
            **kwargs: Additional provider-specific parameters (use sparingly)
        
        Returns:
            Message object containing the sent message details
        
        Raises:
            AuthenticationError: If API credentials are invalid
            InvalidRequestError: If chat_id or text is invalid
            MessageNotSentError: If message failed to send
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    # Chat Management Methods
    
    @abstractmethod
    def get_chats(
        self,
        limit: Optional[int] = None,
        **kwargs
    ) -> list[Chat]:
        """Get list of chats.
        
        Args:
            limit: Maximum number of chats to return
            **kwargs: Additional provider-specific parameters
        
        Returns:
            List of Chat objects
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    # Contact Management Methods
    
    @abstractmethod
    def get_contacts(self, **kwargs) -> list[Contact]:
        """Get list of contacts.
        
        Args:
            **kwargs: Additional provider-specific parameters
        
        Returns:
            List of Contact objects
        """
        pass
    
    @abstractmethod
    def get_contact_info(
        self,
        contact_id: str,
        **kwargs
    ) -> Contact:
        """Get information about a specific contact.
        
        Args:
            contact_id: The unique identifier for the contact
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Contact object
        """
        pass
    
    @abstractmethod
    def check_number_status(
        self,
        phone_number: str,
        **kwargs
    ) -> bool:
        """Check if a phone number is registered on WhatsApp.
        
        Args:
            phone_number: Phone number to check
            **kwargs: Additional provider-specific parameters
        
        Returns:
            True if number is on WhatsApp, False otherwise
        """
        pass
    
    # Session Management (optional - some providers may not support)
    
    def create_session(self, name: str, **kwargs) -> Session:
        """Create a new session (if supported by provider).
        
        Args:
            name: Session name
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Session object
        
        Raises:
            NotImplementedError: If provider doesn't support sessions
        """
        raise NotImplementedError(
            f"Session management not supported by {self.provider_name}"
        )
    
    def get_sessions(self, **kwargs) -> list[Session]:
        """Get list of sessions (if supported by provider).
        
        Args:
            **kwargs: Additional provider-specific parameters
        
        Returns:
            List of Session objects
        
        Raises:
            NotImplementedError: If provider doesn't support sessions
        """
        raise NotImplementedError(
            f"Session management not supported by {self.provider_name}"
        )
    
    # Utility Methods
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def close(self):
        """Close client and cleanup resources."""
        pass

