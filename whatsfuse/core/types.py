"""Type definitions and data models for WhatsFuse."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal, Any


@dataclass
class Message:
    """Unified message object across all providers."""
    
    id: str
    chat_id: str
    text: Optional[str] = None
    timestamp: float = 0.0
    from_me: bool = False
    sender: Optional[str] = None
    type: Literal[
        "text", "image", "video", "audio", "document",
        "location", "contact", "sticker", "voice", "unknown"
    ] = "text"
    caption: Optional[str] = None
    media_url: Optional[str] = None
    mime_type: Optional[str] = None
    filename: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: Optional[str] = None
    quoted_message_id: Optional[str] = None
    is_forwarded: bool = False
    is_starred: bool = False
    metadata: dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Chat:
    """Unified chat object across all providers."""
    
    id: str
    name: str
    is_group: bool = False
    is_archived: bool = False
    is_muted: bool = False
    last_message: Optional[str] = None
    last_message_timestamp: Optional[float] = None
    unread_count: int = 0
    profile_pic_url: Optional[str] = None
    metadata: dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Contact:
    """Unified contact object across all providers."""
    
    id: str
    phone: str
    name: Optional[str] = None
    short_name: Optional[str] = None
    is_business: bool = False
    is_enterprise: bool = False
    profile_pic_url: Optional[str] = None
    status: Optional[str] = None
    metadata: dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Group:
    """Unified group object across all providers."""
    
    id: str
    name: str
    owner: Optional[str] = None
    creation_timestamp: Optional[float] = None
    participants: list[str] = None
    admins: list[str] = None
    description: Optional[str] = None
    profile_pic_url: Optional[str] = None
    metadata: dict[str, Any] = None
    
    def __post_init__(self):
        if self.participants is None:
            self.participants = []
        if self.admins is None:
            self.admins = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Session:
    """Unified session object (primarily for WAHA)."""
    
    name: str
    state: Literal[
        "READY", "STARTING", "SCAN_QR_CODE", "WORKING",
        "FAILED", "STOPPED"
    ]
    authenticated: bool = False
    qr_code: Optional[str] = None
    phone_number: Optional[str] = None
    metadata: dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class MessageReceipt:
    """Message delivery receipt information."""
    
    message_id: str
    chat_id: str
    sent: bool = False
    delivered: bool = False
    read: bool = False
    played: bool = False
    timestamp: Optional[float] = None


@dataclass
class ProviderConfig:
    """Configuration for a specific provider."""
    
    provider: str
    credentials: dict[str, Any]
    api_url: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    session: str = "default"
    extra: dict[str, Any] = None
    
    def __post_init__(self):
        if self.extra is None:
            self.extra = {}


@dataclass
class WebhookEvent:
    """Webhook event data."""
    
    event_type: str
    timestamp: float
    data: dict[str, Any]
    provider: str
    session: Optional[str] = None

