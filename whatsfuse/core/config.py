"""Configuration management for WhatsFuse."""

import os
from typing import Optional, Any
from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration for WhatsFuse client."""
    
    # Provider settings
    provider: str
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    
    # Green API specific
    instance_id: Optional[str] = None
    api_token: Optional[str] = None
    
    # Session settings (WAHA)
    session: str = "default"
    
    # HTTP settings
    timeout: int = 30
    connect_timeout: int = 10
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Logging
    log_level: str = "INFO"
    
    # Extra provider-specific config
    extra: dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables.
        
        Environment variables:
            WHATSFUSE_PROVIDER: Provider name
            WHATSFUSE_API_URL: API URL (for WAHA)
            WHATSFUSE_API_KEY: API key (for WAHA)
            GREEN_API_INSTANCE_ID: Instance ID (for Green API)
            GREEN_API_API_TOKEN: API token (for Green API)
            WHATSFUSE_SESSION: Session name (default: "default")
            WHATSFUSE_LOG_LEVEL: Log level (default: "INFO")
        
        Returns:
            Config instance
        """
        provider = os.getenv("WHATSFUSE_PROVIDER", "waha")
        
        config = cls(
            provider=provider,
            api_url=os.getenv("WHATSFUSE_API_URL"),
            api_key=os.getenv("WHATSFUSE_API_KEY"),
            instance_id=os.getenv("GREEN_API_INSTANCE_ID"),
            api_token=os.getenv("GREEN_API_API_TOKEN"),
            session=os.getenv("WHATSFUSE_SESSION", "default"),
            log_level=os.getenv("WHATSFUSE_LOG_LEVEL", "INFO"),
        )
        
        return config
    
    def validate(self) -> None:
        """Validate configuration.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.provider:
            raise ValueError("Provider is required")
        
        if self.provider == "waha":
            if not self.api_url:
                raise ValueError("API URL is required for WAHA provider")
            if not self.api_key:
                raise ValueError("API key is required for WAHA provider")
        
        elif self.provider == "green_api":
            if not self.instance_id:
                raise ValueError("Instance ID is required for Green API provider")
            if not self.api_token:
                raise ValueError("API token is required for Green API provider")
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def get_provider_config(self) -> dict[str, Any]:
        """Get provider-specific configuration.
        
        Returns:
            Dictionary of provider configuration
        """
        if self.provider == "waha":
            return {
                "api_url": self.api_url,
                "api_key": self.api_key,
                "session": self.session,
            }
        elif self.provider == "green_api":
            return {
                "instance_id": self.instance_id,
                "api_token": self.api_token,
            }
        return {}

