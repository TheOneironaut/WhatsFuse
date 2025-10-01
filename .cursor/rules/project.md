---
alwaysApply: true
---

# WhatsFuse Project Rules

## Project Overview
WhatsFuse is a unified interface for multiple unofficial WhatsApp API providers, inspired by LiteLLM's architecture. The goal is to provide a single, consistent API that abstracts away the differences between various WhatsApp API providers (WAHA, Green API, etc.).

## Core Principles

### 1. Architecture Philosophy
- **Provider Abstraction**: Each provider is encapsulated in its own module with a consistent interface
- **Unified API**: All providers must implement the same core methods defined in the base client
- **Easy Provider Switching**: Users should be able to switch providers with minimal code changes
- **Type Safety**: Use Python type hints throughout the codebase
- **Error Handling**: Consistent error handling across all providers with custom exceptions

### 2. Project Structure
```
whatsfuse/
├── whatsfuse/              # Main package
│   ├── __init__.py        # Public API exports
│   ├── main.py            # Main entry point and unified interface
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   ├── base_client.py     # Abstract base class for all providers
│   │   ├── exceptions.py      # Custom exception classes
│   │   ├── types.py           # Type definitions and data models
│   │   └── config.py          # Configuration management
│   ├── providers/         # Provider implementations
│   │   ├── __init__.py
│   │   ├── waha/
│   │   │   ├── __init__.py
│   │   │   ├── client.py      # WAHA client implementation
│   │   │   ├── transformer.py # Data transformation logic
│   │   │   └── schemas.py     # WAHA-specific schemas
│   │   └── green_api/
│   │       ├── __init__.py
│   │       ├── client.py      # Green API client implementation
│   │       ├── transformer.py # Data transformation logic
│   │       └── schemas.py     # Green API-specific schemas
│   └── utils/             # Utility functions
│       ├── __init__.py
│       ├── http.py        # HTTP client utilities
│       ├── validators.py  # Input validation helpers
│       └── logger.py      # Logging configuration
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── conftest.py       # Pytest fixtures
│   ├── test_core/
│   ├── test_providers/
│   └── integration/
├── docs/                  # User documentation
│   ├── index.md
│   ├── getting-started/
│   ├── providers/
│   ├── api-reference/
│   └── examples/
├── examples/              # Example scripts
├── .cursor/rules/         # Cursor rules
├── pyproject.toml
└── README.md
```

### 3. Coding Standards

#### Python Style
- Follow PEP 8 style guide
- Use Python 3.10+ features (structural pattern matching, type hints, etc.)
- Maximum line length: 100 characters
- Use docstrings for all public functions, classes, and modules (Google style)
- Use type hints for all function signatures

#### Naming Conventions
- Classes: `PascalCase` (e.g., `BaseClient`, `WAHAProvider`)
- Functions/Methods: `snake_case` (e.g., `send_message`, `get_chat_history`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TIMEOUT`, `MAX_RETRIES`)
- Private methods: prefix with `_` (e.g., `_transform_response`)
- Protected methods: prefix with `_` (e.g., `_validate_config`)

#### Import Organization
1. Standard library imports
2. Third-party imports
3. Local application imports
(Each group separated by a blank line, sorted alphabetically)

### 4. Provider Implementation Rules

#### Unified Interface Philosophy
**CRITICAL**: The API interface is UNIFIED and FIXED, inspired by WAHA's API design.
- All providers implement the SAME interface with the SAME parameters
- The interface is based on WAHA as the reference implementation
- Providers MUST translate/adapt their specific APIs to match this unified interface
- Users write code ONCE and it works with ALL providers without changes

#### Base Client Interface
All providers MUST implement these core methods with UNIFIED parameters:

**Message Sending:**
- `send_text_message(chat_id: str, text: str, reply_to: Optional[str] = None, mentions: Optional[List[str]] = None, link_preview: bool = True, **kwargs) -> Message`
- `send_image(chat_id: str, image: Union[str, bytes, Path], caption: Optional[str] = None, reply_to: Optional[str] = None, filename: Optional[str] = None, **kwargs) -> Message`
- `send_file(chat_id: str, file: Union[str, bytes, Path], filename: Optional[str] = None, caption: Optional[str] = None, reply_to: Optional[str] = None, **kwargs) -> Message`
- `send_audio(chat_id: str, audio: Union[str, bytes, Path], reply_to: Optional[str] = None, **kwargs) -> Message`
- `send_video(chat_id: str, video: Union[str, bytes, Path], caption: Optional[str] = None, reply_to: Optional[str] = None, **kwargs) -> Message`
- `send_location(chat_id: str, latitude: float, longitude: float, name: Optional[str] = None, address: Optional[str] = None, reply_to: Optional[str] = None, **kwargs) -> Message`

**Chat Management:**
- `get_chats(limit: Optional[int] = None, **kwargs) -> List[Chat]`
- `get_chat_history(chat_id: str, limit: int = 50, **kwargs) -> List[Message]`
- `mark_as_read(chat_id: str, message_id: Optional[str] = None, **kwargs) -> bool`

**Contact Management:**
- `get_contacts(**kwargs) -> List[Contact]`
- `get_contact_info(contact_id: str, **kwargs) -> Contact`
- `check_number_status(phone_number: str, **kwargs) -> bool`

**Note on `**kwargs`:**
- Used ONLY for truly provider-specific parameters that don't fit the unified model
- Should be minimized and well-documented
- Core parameters are explicit and shared across all providers

#### Provider-Specific Implementation
- Each provider client inherits from `BaseClient`
- Provider-specific logic goes in `client.py`
- **Data transformation** between provider format and unified format goes in `transformer.py`
- Provider-specific data models go in `schemas.py`
- **Never expose provider-specific implementation details to the user**

#### Translation Layer (Critical!)
Each provider MUST implement a translation layer that:
1. **Accepts unified parameters** (e.g., `reply_to`, `mentions`, `link_preview`)
2. **Translates to provider-specific format** (e.g., WAHA: `reply_to`, Green API: `quotedMessageId`)
3. **Handles unsupported features gracefully**:
   - Log a warning if feature not supported
   - Emulate if possible (e.g., mentions via text formatting)
   - Document feature support clearly
4. **Transforms responses back to unified format** using transformers

#### Data Transformation
- All provider responses MUST be transformed to unified format
- Transformer classes handle bidirectional transformation:
  - `to_unified(provider_data)`: Provider format → Unified format
  - `from_unified(unified_data)`: Unified format → Provider format
- Handle missing fields gracefully with sensible defaults

#### Feature Support Documentation
Each provider MUST document which unified features are supported:
- ✅ **Fully Supported**: Feature works as expected
- ⚠️ **Partial Support**: Feature emulated or has limitations
- ❌ **Not Supported**: Feature not available (logs warning)

Example:
```markdown
### WAHA Provider - Feature Support
- ✅ reply_to: Fully supported
- ✅ mentions: Fully supported
- ✅ link_preview: Fully supported

### Green API Provider - Feature Support
- ✅ reply_to: Fully supported (mapped to quotedMessageId)
- ⚠️ mentions: Partial support (added as text, not real mentions)
- ✅ link_preview: Fully supported
```

### 5. Error Handling

#### Custom Exceptions
- `WhatsFuseError`: Base exception class
- `ProviderError`: Provider-specific errors
- `AuthenticationError`: Authentication failures
- `RateLimitError`: Rate limit exceeded
- `InvalidRequestError`: Invalid request parameters
- `NetworkError`: Network-related errors

#### Error Handling Guidelines
- Always catch provider-specific errors and transform to WhatsFuse exceptions
- Include provider name in error messages for debugging
- Log errors before raising
- Provide helpful error messages with actionable information

### 6. Configuration Management

#### Environment Variables
- `WHATSFUSE_PROVIDER`: Default provider (e.g., "waha", "green_api")
- `WHATSFUSE_API_URL`: Provider API URL
- `WHATSFUSE_API_KEY`: Provider API key/token
- `WHATSFUSE_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

#### Config Priority (highest to lowest)
1. Explicit parameters passed to methods
2. Provider instance configuration
3. Environment variables
4. Default values

### 7. Testing Requirements

#### Unit Tests
- Test coverage minimum: 80%
- Mock all external API calls
- Test both success and failure paths
- Test data transformation logic thoroughly

#### Integration Tests
- Optional (requires actual API credentials)
- Separate from unit tests
- Document how to run with real credentials

#### Test Organization
- Mirror the source code structure in tests/
- Name test files: `test_<module_name>.py`
- Name test functions: `test_<functionality>_<scenario>`

### 8. Documentation Standards

#### User Documentation (docs/)
- Write in clear, beginner-friendly language
- Include practical examples for every feature
- Show code snippets with expected output
- Document common issues and troubleshooting

#### Code Documentation
- All public APIs must have docstrings
- Docstrings should include:
  - Brief description
  - Args with types
  - Returns with type
  - Raises (exceptions)
  - Example usage

Example:
```python
def send_text_message(
    self,
    chat_id: str,
    text: str,
    reply_to: Optional[str] = None,
    mentions: Optional[List[str]] = None,
    link_preview: bool = True,
    **kwargs
) -> Message:
    """Send a text message to a WhatsApp chat.
    
    This method uses UNIFIED parameters that work across all providers.
    Each provider translates these parameters to its specific API format.
    
    Args:
        chat_id: The unique identifier for the chat (phone number or group ID)
        text: The message text to send
        reply_to: Optional message ID to reply to (if supported by provider)
        mentions: Optional list of phone numbers to mention (if supported)
        link_preview: Whether to show link preview (default: True)
        **kwargs: Additional provider-specific parameters (use sparingly)
        
    Returns:
        Message object containing the sent message details
        
    Raises:
        AuthenticationError: If API credentials are invalid
        InvalidRequestError: If chat_id or text is invalid
        MessageNotSentError: If message failed to send
        
    Example:
        >>> # Same code works with ALL providers!
        >>> client = WhatsFuse(provider="waha", api_url="...", api_key="...")
        >>> message = client.send_text_message(
        ...     chat_id="1234567890",
        ...     text="Hello, World!",
        ...     reply_to="msg_abc123",
        ...     mentions=["972501234567"],
        ...     link_preview=False
        ... )
        >>> print(message.id)
        
        >>> # Switch provider - SAME CODE!
        >>> client = WhatsFuse(provider="green_api", instance_id="...", api_token="...")
        >>> message = client.send_text_message(
        ...     chat_id="1234567890",
        ...     text="Hello, World!",
        ...     reply_to="msg_abc123",  # Translated to quotedMessageId internally
        ...     mentions=["972501234567"],
        ...     link_preview=False
        ... )
    """
```

### 9. API Design Principles

#### Main Entry Point
- Primary interface: `WhatsFuse` class
- Simple initialization: `WhatsFuse(provider="waha", api_url="...", api_key="...")`
- Support context manager protocol for resource cleanup

#### Method Design
- Use clear, descriptive method names
- Prefer explicit parameters over magic values
- Support both positional and keyword arguments
- Return rich objects, not raw dictionaries
- Use dataclasses or Pydantic models for structured data

#### Backwards Compatibility
- Mark deprecated features with warnings
- Maintain deprecated features for at least 2 minor versions
- Document migration paths in deprecation warnings

### 10. Development Workflow

#### Adding a New Provider
1. Create provider directory in `whatsfuse/providers/<provider_name>/`
2. Implement `client.py` inheriting from `BaseClient`
3. Implement `transformer.py` for data transformation
4. Define provider-specific schemas in `schemas.py`
5. Add provider to `whatsfuse/providers/__init__.py`
6. Write unit tests
7. Add provider documentation in `docs/providers/<provider_name>.md`
8. Add example usage in `examples/<provider_name>_example.py`

#### Code Review Checklist
- [ ] Type hints present on all function signatures
- [ ] Docstrings present on all public APIs
- [ ] Error handling implemented correctly
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No breaking changes (or properly documented)

### 11. Dependencies Management

#### Core Dependencies
- `httpx`: Modern async HTTP client
- `pydantic`: Data validation and settings management
- `python-dotenv`: Environment variable management

#### Development Dependencies
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `pytest-asyncio`: Async test support
- `black`: Code formatting
- `ruff`: Fast Python linter
- `mypy`: Static type checking

#### Version Pinning
- Pin major and minor versions in pyproject.toml
- Allow patch version updates with `~=`
- Document breaking changes in dependency updates

### 12. Logging

#### Logging Guidelines
- Use Python's `logging` module
- Log at appropriate levels:
  - DEBUG: Detailed debugging information
  - INFO: General informational messages
  - WARNING: Warning messages
  - ERROR: Error messages
  - CRITICAL: Critical errors
- Include provider name in log messages
- Log all API requests and responses at DEBUG level
- Never log sensitive information (API keys, tokens, personal data)

### 13. Security Considerations

- Never commit API keys or secrets
- Use environment variables for sensitive configuration
- Validate all user inputs
- Sanitize data before logging
- Use HTTPS for all API communications
- Implement rate limiting where appropriate

### 14. Performance Guidelines

- Use async/await for I/O operations
- Implement connection pooling
- Cache frequently accessed data when appropriate
- Set reasonable timeouts for all HTTP requests
- Implement retry logic with exponential backoff

### 15. Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Run full test suite
4. Build documentation
5. Create git tag
6. Build and publish to PyPI
7. Create GitHub release with notes

## Adding New Functions or Parameters

**CRITICAL**: WhatsFuse uses a hybrid automation system for managing API methods and parameters.

### The Process

```
1. Edit api_spec.json (single source of truth)
   ↓
2. Update code manually (BaseClient, WhatsFuse, Providers)
   ↓
3. Run validation: python scripts/validate_api.py
   ↓
4. Generate docs: python scripts/generate_docs.py
   ↓
5. Commit all changes
```

### Step-by-Step Guide

#### Adding a New Method

1. **Update `api_spec.json`**:
   ```json
   {
     "methods": {
       "your_new_method": {
         "category": "messaging",
         "description": "Your method description",
         "returns": "Message",
         "status": "in_progress",
         "parameters": [
           {
             "name": "param_name",
             "type": "str",
             "required": true,
             "default": null,
             "description": "Parameter description"
           }
         ],
         "providers": {
           "waha": {
             "supported": true,
             "mapping": {"waha_param": "param_name"},
             "notes": "Implementation notes"
           }
         }
       }
     }
   }
   ```

2. **Update `BaseClient`** (`whatsfuse/core/base_client.py`):
   ```python
   @abstractmethod
   def your_new_method(self, param_name: str) -> Message:
       """Your method description."""
       pass
   ```

3. **Update `WhatsFuse`** (`whatsfuse/main.py`):
   ```python
   def your_new_method(self, param_name: str) -> Message:
       """Your method description."""
       return self._client.your_new_method(param_name)
   ```

4. **Update Each Provider** (`whatsfuse/providers/*/client.py`):
   ```python
   def your_new_method(self, param_name: str) -> Message:
       """Implementation for this provider."""
       # Translate parameters
       # Make API call
       # Return unified response
   ```

5. **Validate**:
   ```bash
   python scripts/validate_api.py  # Should pass ✅
   ```

6. **Generate Documentation**:
   ```bash
   python scripts/generate_docs.py  # Updates FEATURE_MATRIX.md
   ```

#### Adding a New Parameter to Existing Method

1. **Update `api_spec.json`**:
   - Add parameter to the method's `parameters` array
   - Update provider mappings in `providers` section

2. **Update `BaseClient`**: Add parameter to method signature

3. **Update `WhatsFuse`**: Add parameter to method signature

4. **Update All Providers**: Handle the new parameter

5. **Run validation and generate docs** (same as above)

### Validation System

The `validate_api.py` script checks:
- ✅ All methods in `api_spec.json` exist in `BaseClient`
- ✅ All parameters match between spec and code
- ✅ All providers implement required methods
- ❌ Fails if any inconsistency is found

### Documentation Generation

The `generate_docs.py` script automatically creates:
- `docs/FEATURE_MATRIX.md` - Complete feature and parameter documentation
- Provider mappings and support status
- Parameter tables with types and descriptions

### Important Notes

- **api_spec.json** is the single source of truth
- **Never skip validation** before committing
- **Always regenerate docs** after spec changes
- **Commit both spec and generated docs** together
- **Manual code implementation** gives you full flexibility

## AI Assistant Guidelines

When working on this project:
1. **Always** refer to this rules file for project standards
2. **Always** maintain the provider abstraction pattern
3. **Always** add type hints and docstrings
4. **Always** write or update tests for new features
5. **Always** update documentation when adding features
6. **Never** expose provider-specific implementation details in public API
7. **Never** commit credentials or sensitive data
8. **Before** adding new dependencies, consider if they're truly necessary
9. **Before** making breaking changes, discuss with the team
10. **Prefer** composition over inheritance where it makes sense
11. **When adding methods/parameters**: Follow the automation system process above

## Current Provider Status

### Supported Providers
1. **WAHA** (WhatsApp HTTP API)
   - Status: In Development
   - Base URL: https://waha.devlike.pro/docs
   - Auth Method: API Key

2. **Green API**
   - Status: Planned
   - Auth Method: Instance ID + API Token

### Provider Implementation Priority
1. WAHA (primary focus)
2. Green API
3. Future providers based on community needs
