"""Pytest configuration and fixtures."""

import pytest
from whatsfuse.core.config import Config


@pytest.fixture
def waha_config():
    """WAHA configuration fixture."""
    return Config(
        provider="waha",
        api_url="http://localhost:3000",
        api_key="test-api-key",
        session="test-session"
    )


@pytest.fixture
def green_api_config():
    """Green API configuration fixture."""
    return Config(
        provider="green_api",
        instance_id="1234567890",
        api_token="test-api-token"
    )


@pytest.fixture
def mock_message():
    """Mock message data."""
    from whatsfuse.core.types import Message
    
    return Message(
        id="msg_123",
        chat_id="1234567890@c.us",
        text="Test message",
        timestamp=1234567890.0,
        from_me=True,
        sender="me@c.us",
        type="text"
    )


@pytest.fixture
def mock_chat():
    """Mock chat data."""
    from whatsfuse.core.types import Chat
    
    return Chat(
        id="1234567890@c.us",
        name="Test Chat",
        is_group=False,
        last_message="Hello",
        unread_count=0
    )

