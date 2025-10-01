# WhatsFuse Design Document

> Comprehensive design blueprint for WhatsFuse - A unified WhatsApp API interface

## Table of Contents

1. [Project Overview](#project-overview)
2. [Inspiration](#inspiration)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Core Components](#core-components)
6. [Provider System](#provider-system)
7. [Type System](#type-system)
8. [Configuration](#configuration)
9. [Error Handling](#error-handling)
10. [Development Guidelines](#development-guidelines)
11. [Implementation Roadmap](#implementation-roadmap)
12. [API Design](#api-design)

## Project Overview

**WhatsFuse** is a unified Python SDK for multiple WhatsApp API providers, inspired by LiteLLM's approach to unifying different LLM providers.

### Goals

1. **Unified Interface**: Single, consistent API across all WhatsApp providers
2. **Easy Provider Switching**: Change providers with minimal code changes
3. **Type Safety**: Full Python type hints for better development experience
4. **Extensibility**: Easy to add new providers
5. **Production Ready**: Comprehensive error handling, logging, and testing

### Non-Goals

- Official WhatsApp Business API (we focus on unofficial APIs)
- Message encryption/security (handled by providers)
- Message storage/database (left to the application)

## Inspiration

### LiteLLM Pattern

WhatsFuse is inspired by [LiteLLM](https://github.com/BerriAI/litellm), which provides a unified interface for different LLM providers:

```python
# LiteLLM example
import litellm

# OpenAI
response = litellm.completion(model="gpt-3.5-turbo", messages=[...])

# Anthropic
response = litellm.completion(model="claude-2", messages=[...])

# Same interface, different providers!
```

### WhatsFuse Approach

We apply the same pattern to WhatsApp APIs:

```python
# WhatsFuse example
from whatsfuse import WhatsFuse

# WAHA
client = WhatsFuse(provider="waha", api_url="...", api_key="...")
message = client.send_text_message(chat_id, text)

# Green API
client = WhatsFuse(provider="green_api", instance_id="...", api_token="...")
message = client.send_text_message(chat_id, text)

# Same interface, different providers!
```

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────┐
│        User Application                 │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     WhatsFuse Client (main.py)          │
│  - Unified interface                    │
│  - Provider selection                   │
│  - Configuration management             │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  BaseClient (base_client.py)            │
│  - Abstract methods                     │
│  - Interface contract                   │
└─────────────┬───────────────────────────┘
              │
       ┌──────┴──────┬──────────────┐
       ▼             ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│  WAHA    │  │ Green    │  │ Future   │
│  Client  │  │ API      │  │ Provider │
│          │  │ Client   │  │          │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│Transformer│  │Transformer│  │Transformer│
│          │  │          │  │          │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     ▼             ▼             ▼
┌──────────────────────────────────────┐
│       HTTP Client (httpx)            │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│    WhatsApp API Providers            │
└──────────────────────────────────────┘
```

### Layer Responsibilities

1. **User Application Layer**
   - Uses WhatsFuse client
   - Business logic
   - Application-specific error handling

2. **Unified Interface Layer** (`main.py`)
   - Provider-agnostic API
   - Provider instantiation
   - Configuration loading
   - Method delegation

3. **Abstraction Layer** (`base_client.py`)
   - Defines interface contract
   - Common utilities
   - Context manager support

4. **Provider Layer** (`providers/*/client.py`)
   - Provider-specific implementation
   - API endpoint handling
   - Authentication

5. **Transformation Layer** (`providers/*/transformer.py`)
   - Data format conversion
   - Provider format → Unified format
   - Unified format → Provider format

6. **HTTP Layer** (`utils/http.py`)
   - HTTP request/response handling
   - Connection pooling
   - Retry logic

## Project Structure

### Directory Layout

```
whatsfuse/
├── .cursorrules              # AI development guidelines (CRITICAL!)
├── .gitignore
├── .python-version
├── README.md                 # Project overview
├── LICENSE
├── pyproject.toml           # Package configuration
│
├── whatsfuse/               # Main package
│   ├── __init__.py         # Public API exports
│   ├── main.py             # WhatsFuse and AsyncWhatsFuse classes
│   │
│   ├── core/               # Core functionality
│   │   ├── __init__.py
│   │   ├── base_client.py  # Abstract base class
│   │   ├── exceptions.py   # Custom exceptions
│   │   ├── types.py        # Type definitions (Message, Chat, etc.)
│   │   └── config.py       # Configuration management
│   │
│   ├── providers/          # Provider implementations
│   │   ├── __init__.py
│   │   ├── waha/
│   │   │   ├── __init__.py
│   │   │   ├── client.py       # WAHA client implementation
│   │   │   ├── transformer.py  # Data transformation
│   │   │   └── schemas.py      # WAHA-specific schemas
│   │   └── green_api/
│   │       ├── __init__.py
│   │       ├── client.py       # Green API client implementation
│   │       ├── transformer.py  # Data transformation
│   │       └── schemas.py      # Green API-specific schemas
│   │
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── http.py         # HTTP client utilities
│       ├── validators.py   # Input validation
│       └── logger.py       # Logging configuration
│
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures
│   ├── test_core/
│   │   ├── test_config.py
│   │   ├── test_types.py
│   │   └── test_exceptions.py
│   ├── test_providers/
│   │   ├── test_waha.py
│   │   └── test_green_api.py
│   └── integration/
│       └── test_integration.py
│
├── docs/                   # User documentation
│   ├── index.md           # Documentation home
│   ├── DESIGN.md          # This file
│   │
│   ├── getting-started/
│   │   ├── installation.md
│   │   ├── quickstart.md
│   │   ├── configuration.md
│   │   └── authentication.md
│   │
│   ├── providers/
│   │   ├── waha.md
│   │   └── green_api.md
│   │
│   ├── api-reference/
│   │   ├── client.md
│   │   ├── messages.md
│   │   ├── chats.md
│   │   ├── contacts.md
│   │   └── creating-providers.md
│   │
│   └── examples/
│       ├── sending-messages.md
│       ├── chatbots.md
│       ├── webhooks.md
│       └── groups.md
│
└── examples/               # Example scripts
    ├── basic_usage.py
    ├── send_messages.py
    ├── receive_messages.py
    ├── chatbot.py
    └── webhook_handler.py
```

### File Purposes

#### Core Files

- **`whatsfuse/__init__.py`**: Public API, exports main classes and types
- **`whatsfuse/main.py`**: `WhatsFuse` class, main entry point
- **`whatsfuse/core/base_client.py`**: Abstract base class for all providers
- **`whatsfuse/core/types.py`**: Unified type definitions (Message, Chat, etc.)
- **`whatsfuse/core/exceptions.py`**: Custom exception hierarchy
- **`whatsfuse/core/config.py`**: Configuration management and validation

#### Provider Files

- **`providers/*/client.py`**: Provider-specific client implementation
- **`providers/*/transformer.py`**: Data transformation logic
- **`providers/*/schemas.py`**: Provider-specific data models

#### Configuration Files

- **`.cursorrules`**: AI development guidelines (VERY IMPORTANT!)
- **`pyproject.toml`**: Package metadata and dependencies
- **`.gitignore`**: Git ignore patterns

## Core Components

### 1. BaseClient (Abstract Base Class)

All providers must implement:

```python
class BaseClient(ABC):
    # Message sending
    @abstractmethod
    def send_text_message(chat_id, text, **kwargs) -> Message
    
    @abstractmethod
    def send_image(chat_id, image, caption, **kwargs) -> Message
    
    @abstractmethod
    def send_file(chat_id, file, filename, caption, **kwargs) -> Message
    
    @abstractmethod
    def send_audio(chat_id, audio, **kwargs) -> Message
    
    @abstractmethod
    def send_video(chat_id, video, caption, **kwargs) -> Message
    
    @abstractmethod
    def send_location(chat_id, lat, lon, name, address, **kwargs) -> Message
    
    # Chat management
    @abstractmethod
    def get_chats(limit, **kwargs) -> list[Chat]
    
    @abstractmethod
    def get_chat_history(chat_id, limit, **kwargs) -> list[Message]
    
    @abstractmethod
    def mark_as_read(chat_id, message_id, **kwargs) -> bool
    
    # Contact management
    @abstractmethod
    def get_contacts(**kwargs) -> list[Contact]
    
    @abstractmethod
    def get_contact_info(contact_id, **kwargs) -> Contact
    
    @abstractmethod
    def check_number_status(phone_number, **kwargs) -> bool
```

### 2. Type System

Unified data models:

```python
@dataclass
class Message:
    id: str
    chat_id: str
    text: Optional[str]
    timestamp: float
    from_me: bool
    sender: Optional[str]
    type: Literal["text", "image", "video", ...]
    # ... more fields

@dataclass
class Chat:
    id: str
    name: str
    is_group: bool
    last_message: Optional[str]
    # ... more fields

@dataclass
class Contact:
    id: str
    phone: str
    name: Optional[str]
    # ... more fields
```

### 3. Configuration System

```python
@dataclass
class Config:
    provider: str
    api_url: Optional[str]
    api_key: Optional[str]
    instance_id: Optional[str]
    api_token: Optional[str]
    session: str = "default"
    timeout: int = 30
    max_retries: int = 3
    
    @classmethod
    def from_env(cls) -> "Config":
        # Load from environment variables
        pass
    
    def validate(self) -> None:
        # Validate configuration
        pass
```

## Provider System

### Provider Implementation Pattern

Each provider follows this pattern:

1. **Client Class** (`client.py`)
   - Inherits from `BaseClient`
   - Implements all abstract methods
   - Handles provider-specific authentication
   - Makes HTTP requests to provider API

2. **Transformer Class** (`transformer.py`)
   - Converts provider format to unified format
   - Converts unified format to provider format
   - Handles missing fields gracefully

3. **Schemas** (`schemas.py`)
   - Provider-specific data models
   - Request/response schemas

### Adding a New Provider

To add a new provider:

```python
# 1. Create directory
whatsfuse/providers/new_provider/

# 2. Implement client
class NewProviderClient(BaseClient):
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_url = config.api_url
        # Initialize provider-specific stuff
    
    def send_text_message(self, chat_id, text, **kwargs):
        # Make API call
        response = self._make_request(...)
        # Transform response
        return self.transformer.to_message(response)

# 3. Implement transformer
class NewProviderTransformer:
    @staticmethod
    def to_message(provider_data: dict) -> Message:
        return Message(
            id=provider_data["messageId"],
            chat_id=provider_data["chatId"],
            # ... transform fields
        )

# 4. Register in main.py
if provider == "new_provider":
    from whatsfuse.providers.new_provider import NewProviderClient
    return NewProviderClient(config)
```

## Type System

### Core Types

All types use `@dataclass` for simplicity and type safety:

```python
from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class Message:
    """Unified message representation"""
    id: str
    chat_id: str
    text: Optional[str] = None
    timestamp: float = 0.0
    from_me: bool = False
    type: Literal["text", "image", "video", ...] = "text"
    metadata: dict = field(default_factory=dict)

@dataclass
class Chat:
    """Unified chat representation"""
    id: str
    name: str
    is_group: bool = False
    unread_count: int = 0
    metadata: dict = field(default_factory=dict)
```

### Design Decisions

1. **Dataclasses over Pydantic**: Simpler, no extra dependency for core types
2. **Optional fields**: Handle differences between providers gracefully
3. **Metadata dict**: Store provider-specific data without polluting main fields
4. **Type hints**: Full type safety and IDE support

## Configuration

### Configuration Sources (Priority Order)

1. **Explicit parameters** to `WhatsFuse()`
2. **Environment variables**
3. **Default values**

### Environment Variables

```bash
# Provider selection
WHATSFUSE_PROVIDER=waha

# WAHA config
WHATSFUSE_API_URL=http://localhost:3000
WHATSFUSE_API_KEY=your-api-key
WHATSFUSE_SESSION=default

# Green API config
GREEN_API_INSTANCE_ID=1234567890
GREEN_API_API_TOKEN=your-api-token

# Common config
WHATSFUSE_LOG_LEVEL=INFO
```

### Usage Patterns

```python
# Pattern 1: Explicit configuration
client = WhatsFuse(
    provider="waha",
    api_url="http://localhost:3000",
    api_key="key"
)

# Pattern 2: From environment
client = WhatsFuse.from_env()

# Pattern 3: Mixed
client = WhatsFuse(
    provider="waha",  # explicit
    api_key=os.getenv("API_KEY")  # env var
)
```

## Error Handling

### Exception Hierarchy

```
WhatsFuseError (base)
├── ProviderError
├── AuthenticationError
├── RateLimitError
├── InvalidRequestError
├── NetworkError
├── SessionNotFoundError (WAHA)
├── MessageNotSentError
├── InstanceNotAuthorizedError (Green API)
├── ConfigurationError
├── UnsupportedProviderError
└── TransformationError
```

### Error Handling Pattern

```python
from whatsfuse import WhatsFuse, WhatsFuseError, RateLimitError

try:
    message = client.send_text_message(chat_id, text)
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except WhatsFuseError as e:
    print(f"Error from {e.provider}: {e.message}")
```

## Development Guidelines

### Coding Standards

See `.cursorrules` for comprehensive guidelines. Key points:

1. **Python 3.10+** features
2. **Type hints** on all functions
3. **Docstrings** (Google style) on all public APIs
4. **PEP 8** style with 100 char line length
5. **Testing** with minimum 80% coverage

### Testing Strategy

1. **Unit Tests**: Test individual components with mocks
2. **Integration Tests**: Test with real APIs (optional, requires credentials)
3. **Type Checking**: Use `mypy` for static type analysis
4. **Linting**: Use `black` + `ruff` for code quality

### Documentation Strategy

1. **User Docs** (`docs/`): For end users
   - Getting started guides
   - Provider-specific guides
   - API reference
   - Examples

2. **Code Docs**: For developers
   - Inline comments for complex logic
   - Docstrings for all public APIs
   - Type hints for clarity

3. **AI Docs** (`.cursorrules`): For AI assistants
   - Project structure
   - Coding standards
   - Development workflow

## Implementation Roadmap

### Phase 1: Foundation (DONE ✅)
- [x] Project structure
- [x] Core types and interfaces
- [x] Configuration system
- [x] Exception hierarchy
- [x] Documentation structure
- [x] `.cursorrules` for AI development

### Phase 2: WAHA Provider (IN PROGRESS 🚧)
- [ ] HTTP client utilities
- [ ] WAHA client implementation
- [ ] WAHA transformer
- [ ] Unit tests
- [ ] Integration tests
- [ ] Examples

### Phase 3: Green API Provider (PLANNED 📋)
- [ ] Green API client implementation
- [ ] Green API transformer
- [ ] Unit tests
- [ ] Integration tests
- [ ] Examples

### Phase 4: Polish & Release (PLANNED 📋)
- [ ] Comprehensive testing
- [ ] Performance optimization
- [ ] Documentation review
- [ ] Example applications
- [ ] PyPI package
- [ ] CI/CD setup

### Future Phases
- [ ] Async support (`AsyncWhatsFuse`)
- [ ] Additional providers
- [ ] Webhook helpers
- [ ] Message queue support
- [ ] Advanced features (buttons, lists, etc.)

## API Design

### Design Principles

1. **Consistency**: Same method names and signatures across providers
2. **Simplicity**: Easy to use for common cases
3. **Flexibility**: Support provider-specific features via `**kwargs`
4. **Type Safety**: Full type hints for IDE support
5. **Error Clarity**: Clear, actionable error messages

### Method Naming Convention

- **send_***: Send messages (send_text_message, send_image, etc.)
- **get_***: Retrieve data (get_chats, get_contacts, etc.)
- **check_***: Boolean checks (check_number_status, etc.)
- **create_***: Create resources (create_session, create_group, etc.)
- **delete_***: Delete resources (delete_message, etc.)
- **update_***: Update resources (update_profile, etc.)

### Return Types

- **Single object**: Return the object directly
  ```python
  message: Message = client.send_text_message(...)
  ```

- **Multiple objects**: Return list
  ```python
  chats: list[Chat] = client.get_chats()
  ```

- **Success/failure**: Return bool
  ```python
  success: bool = client.mark_as_read(...)
  ```

---

## Summary

WhatsFuse provides a **clean, unified interface** for multiple WhatsApp API providers, inspired by LiteLLM's architecture. The project is designed to be:

1. **Easy to use**: Simple API, clear documentation
2. **Easy to extend**: Add new providers easily
3. **Type-safe**: Full Python type hints
4. **Well-documented**: Comprehensive docs for users and developers
5. **AI-friendly**: Detailed `.cursorrules` for AI development

The foundation is complete. Now it's time to implement the providers! 🚀

