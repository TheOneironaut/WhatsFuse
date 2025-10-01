# WhatsFuse Architecture

This document provides a visual overview of the WhatsFuse architecture.

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              Your Application                       │
│                                                     │
│  from whatsfuse import WhatsFuse                    │
│  client = WhatsFuse(provider="waha", ...)          │
│  message = client.send_text_message(...)           │
│                                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     │ Uses unified API
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│         WhatsFuse Client (whatsfuse/main.py)        │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  - Provider selection & instantiation       │   │
│  │  - Configuration management                 │   │
│  │  - Method delegation to provider clients    │   │
│  │  - Uniform error handling                   │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     │ Delegates to
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│     BaseClient (whatsfuse/core/base_client.py)      │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  Abstract Base Class                        │   │
│  │  - Defines interface contract               │   │
│  │  - Abstract methods all providers must      │   │
│  │    implement                                │   │
│  │  - Common utilities (context manager, etc.) │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────┬───────────────────┬───────────────────┘
              │                   │
              │ Implemented by    │ Implemented by
              │                   │
              ▼                   ▼
┌─────────────────────┐   ┌─────────────────────┐
│                     │   │                     │
│   WAHA Client       │   │  Green API Client   │
│   (providers/waha)  │   │ (providers/green_api│
│                     │   │                     │
│  ┌───────────────┐  │   │  ┌───────────────┐  │
│  │ client.py     │  │   │  │ client.py     │  │
│  │ - API calls   │  │   │  │ - API calls   │  │
│  │ - Auth        │  │   │  │ - Auth        │  │
│  │ - Sessions    │  │   │  │ - Instance    │  │
│  └───────────────┘  │   │  └───────────────┘  │
│  ┌───────────────┐  │   │  ┌───────────────┐  │
│  │transformer.py │  │   │  │transformer.py │  │
│  │ - Format      │  │   │  │ - Format      │  │
│  │   conversion  │  │   │  │   conversion  │  │
│  └───────────────┘  │   │  └───────────────┘  │
│                     │   │                     │
└──────────┬──────────┘   └──────────┬──────────┘
           │                         │
           │ Makes HTTP requests     │ Makes HTTP requests
           │                         │
           ▼                         ▼
┌──────────────────────────────────────────────┐
│                                              │
│        HTTP Client Layer (httpx)             │
│                                              │
│  - Connection pooling                        │
│  - Retry logic                               │
│  - Timeout handling                          │
│  - Request/Response processing               │
│                                              │
└─────────────────┬────────────────────────────┘
                  │
                  │ HTTP requests
                  │
                  ▼
┌─────────────────────────────────────────────┐
│                                             │
│        WhatsApp API Providers               │
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │              │      │                 │ │
│  │ WAHA Server  │      │ Green API Cloud │ │
│  │              │      │                 │ │
│  └──────────────┘      └─────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
```

## Data Flow

### Sending a Message

```
User Code
    │
    │ client.send_text_message("123", "Hello")
    ▼
WhatsFuse Client (main.py)
    │
    │ Validates input
    │ Routes to provider client
    ▼
Provider Client (providers/waha/client.py)
    │
    │ Formats request for provider API
    ▼
Transformer (providers/waha/transformer.py)
    │
    │ Converts unified format → provider format
    ▼
HTTP Client
    │
    │ POST /api/sendText
    ▼
WAHA Server
    │
    │ Sends via WhatsApp
    ▼
WhatsApp Network
    │
    │ Response
    ▼
Provider Client
    │
    │ Receives response
    ▼
Transformer
    │
    │ Converts provider format → unified format
    ▼
WhatsFuse Client
    │
    │ Returns Message object
    ▼
User Code
```

## Module Relationships

```
whatsfuse/
│
├── __init__.py ──────────┐
│   (Public API)          │ Exports
│                         │
├── main.py ──────────────┼─────────┐
│   (WhatsFuse class)     │         │ Uses
│                         │         │
├── core/                 │         │
│   ├── base_client.py ◄──┤         │
│   │   (Abstract interface)        │
│   │                               │
│   ├── types.py ◄──────────────────┤
│   │   (Message, Chat, etc.)       │
│   │                               │
│   ├── exceptions.py ◄─────────────┤
│   │   (Error hierarchy)           │
│   │                               │
│   └── config.py ◄─────────────────┤
│       (Configuration)             │
│                                   │
├── providers/                      │
│   ├── waha/                       │
│   │   ├── client.py ◄─────────────┤
│   │   │   (Implements BaseClient) │
│   │   │                           │
│   │   ├── transformer.py          │
│   │   │   (Data conversion)       │
│   │   │                           │
│   │   └── schemas.py              │
│   │       (WAHA-specific types)   │
│   │                               │
│   └── green_api/                  │
│       ├── client.py ◄─────────────┘
│       │   (Implements BaseClient)
│       │
│       ├── transformer.py
│       │   (Data conversion)
│       │
│       └── schemas.py
│           (Green API types)
│
└── utils/
    ├── http.py
    │   (HTTP utilities)
    │
    ├── validators.py
    │   (Input validation)
    │
    └── logger.py
        (Logging config)
```

## Component Responsibilities

### 1. WhatsFuse Client (`main.py`)

**Responsibilities:**
- Provider selection and instantiation
- Configuration management
- Method delegation
- Unified error handling

**Does NOT:**
- Make direct API calls
- Handle provider-specific logic
- Transform data

### 2. BaseClient (`core/base_client.py`)

**Responsibilities:**
- Define interface contract
- Provide common utilities
- Context manager support

**Does NOT:**
- Implement provider-specific logic
- Make API calls
- Handle configuration

### 3. Provider Clients (`providers/*/client.py`)

**Responsibilities:**
- Implement BaseClient interface
- Make provider-specific API calls
- Handle authentication
- Use transformers for data conversion

**Does NOT:**
- Expose provider-specific details to user
- Handle provider selection
- Manage global configuration

### 4. Transformers (`providers/*/transformer.py`)

**Responsibilities:**
- Convert provider format to unified format
- Convert unified format to provider format
- Handle missing fields gracefully

**Does NOT:**
- Make API calls
- Handle business logic
- Manage state

### 5. Types (`core/types.py`)

**Responsibilities:**
- Define unified data models
- Provide type safety
- Support IDE autocomplete

**Does NOT:**
- Contain business logic
- Make API calls
- Handle validation (that's for validators)

## Design Patterns

### 1. Abstract Factory Pattern

```python
class WhatsFuse:
    def _create_client(self) -> BaseClient:
        if provider == "waha":
            return WAHAClient(config)
        elif provider == "green_api":
            return GreenAPIClient(config)
```

Creates the appropriate provider client based on configuration.

### 2. Adapter Pattern

```python
class WAHAClient(BaseClient):
    def send_text_message(self, chat_id, text):
        # Adapts WAHA API to unified interface
        waha_response = self._call_waha_api(...)
        return self.transformer.to_message(waha_response)
```

Adapts provider-specific APIs to the unified interface.

### 3. Strategy Pattern

Different providers implement different strategies for the same operations:

```python
# Same method, different implementation
waha_client.send_text_message(...)  # → WAHA strategy
green_client.send_text_message(...) # → Green API strategy
```

### 4. Facade Pattern

`WhatsFuse` class provides a simple facade over complex provider implementations:

```python
# Complex provider-specific code hidden behind simple interface
client = WhatsFuse(provider="waha", ...)
message = client.send_text_message(chat_id, text)
```

## Key Interfaces

### BaseClient Interface

```python
class BaseClient(ABC):
    # Message Operations
    @abstractmethod
    def send_text_message(chat_id: str, text: str) -> Message
    
    @abstractmethod
    def send_image(chat_id: str, image: Union[str, bytes]) -> Message
    
    # Chat Operations
    @abstractmethod
    def get_chats(limit: Optional[int]) -> list[Chat]
    
    @abstractmethod
    def get_chat_history(chat_id: str, limit: int) -> list[Message]
    
    # Contact Operations
    @abstractmethod
    def get_contacts() -> list[Contact]
    
    @abstractmethod
    def check_number_status(phone: str) -> bool
```

### Transformer Interface

```python
class ProviderTransformer:
    @staticmethod
    def to_message(provider_data: dict) -> Message:
        """Provider format → Unified format"""
        
    @staticmethod
    def from_message(message: Message) -> dict:
        """Unified format → Provider format"""
    
    @staticmethod
    def to_chat(provider_data: dict) -> Chat:
        """Provider format → Unified format"""
```

## Error Flow

```
User Code
    │
    │ client.send_text_message(...)
    ▼
WhatsFuse Client
    │
    │ Validates and delegates
    ▼
Provider Client
    │
    │ Makes API call
    │
    ▼ Error occurs
    │
    │ Provider-specific error
    │ (e.g., WAHA returns 401)
    ▼
Provider Client catches error
    │
    │ Transform to WhatsFuse exception
    │ raise AuthenticationError("Invalid API key", provider="waha")
    ▼
WhatsFuse Client
    │
    │ Re-raises (or adds context)
    ▼
User Code
    │
    │ try/except WhatsFuseError
    │ Handle gracefully
```

## Configuration Flow

```
1. User creates WhatsFuse instance
        │
        ▼
2. Config object created
        │
        ├─► From explicit params (highest priority)
        ├─► From environment variables
        └─► From defaults (lowest priority)
        │
        ▼
3. Config validated
        │
        ├─► Check required fields
        ├─► Validate provider-specific requirements
        └─► Raise ConfigurationError if invalid
        │
        ▼
4. Provider client created
        │
        └─► Uses validated config
```

## Extension Points

### Adding a New Provider

1. Create `providers/new_provider/` directory
2. Implement `client.py` (inherit BaseClient)
3. Implement `transformer.py` (data conversion)
4. Create `schemas.py` (provider-specific types)
5. Register in `main.py._create_client()`
6. Add tests
7. Add documentation

### Adding a New Method

1. Add abstract method to `BaseClient`
2. Implement in all provider clients
3. Add to `WhatsFuse` class in `main.py`
4. Update type definitions if needed
5. Add tests
6. Update documentation

## Testing Architecture

```
tests/
│
├── test_core/
│   ├── test_config.py      # Config validation
│   ├── test_types.py       # Type definitions
│   └── test_exceptions.py  # Exception hierarchy
│
├── test_providers/
│   ├── test_waha.py        # WAHA client (mocked)
│   └── test_green_api.py   # Green API client (mocked)
│
└── integration/
    └── test_integration.py # Real API tests (optional)
```

**Testing Strategy:**
- **Unit tests**: Mock HTTP calls, test logic
- **Integration tests**: Real API calls (require credentials)
- **Type tests**: Use mypy for static analysis

---

This architecture ensures:
- ✅ **Loose coupling** - Components are independent
- ✅ **High cohesion** - Each component has a clear purpose
- ✅ **Extensibility** - Easy to add new providers
- ✅ **Testability** - Easy to mock and test
- ✅ **Maintainability** - Clear structure and responsibilities

