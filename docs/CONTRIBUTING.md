# Contributing to WhatsFuse

Thank you for your interest in contributing to WhatsFuse! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive. We're building this together! 🤝

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/whatsfuse.git
cd whatsfuse
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Guidelines

### Read project.md First!

Before contributing, **please read [.cursor/rules/project.md](../.cursor/rules/project.md)** - it contains comprehensive development guidelines for the project.

### Key Principles

1. **Follow the Architecture**: Maintain the provider abstraction pattern
2. **Type Safety**: Use type hints everywhere
3. **Documentation**: Add docstrings to all public APIs
4. **Testing**: Write tests for new features
5. **Consistency**: Follow existing code style

### Code Style

We use:
- **Black** for formatting (100 char line length)
- **Ruff** for linting
- **Mypy** for type checking

```bash
# Format code
black whatsfuse/ tests/

# Lint code
ruff check whatsfuse/ tests/

# Type check
mypy whatsfuse/
```

## Adding a New Provider

To add a new WhatsApp API provider:

### 1. Create Provider Directory

```bash
mkdir -p whatsfuse/providers/new_provider
```

### 2. Create Files

Create these files in `whatsfuse/providers/new_provider/`:

- `__init__.py` - Export the client class
- `client.py` - Client implementation (inherit from BaseClient)
- `transformer.py` - Data transformation logic
- `schemas.py` - Provider-specific data models

### 3. Implement Client

```python
# whatsfuse/providers/new_provider/client.py

from typing import Optional, Union
from pathlib import Path

from whatsfuse.core.base_client import BaseClient
from whatsfuse.core.types import Message, Chat, Contact
from whatsfuse.core.config import Config


class NewProviderClient(BaseClient):
    """Client for New Provider."""
    
    def __init__(self, config: Config):
        super().__init__(config)
        # Initialize provider-specific stuff
        self.api_url = config.api_url
        self.api_key = config.api_key
    
    def send_text_message(
        self,
        chat_id: str,
        text: str,
        **kwargs
    ) -> Message:
        """Send text message via New Provider."""
        # Make API call
        response = self._make_api_call(...)
        
        # Transform to unified format
        return self._transform_message(response)
    
    # Implement all other abstract methods...
```

### 4. Implement Transformer

```python
# whatsfuse/providers/new_provider/transformer.py

from whatsfuse.core.types import Message, Chat, Contact


class NewProviderTransformer:
    """Transform data between New Provider and unified format."""
    
    @staticmethod
    def to_message(provider_data: dict) -> Message:
        """Convert provider message to unified Message."""
        return Message(
            id=provider_data["id"],
            chat_id=provider_data["chat_id"],
            text=provider_data.get("text"),
            timestamp=provider_data["timestamp"],
            from_me=provider_data.get("from_me", False),
            type="text",  # or detect from provider_data
        )
    
    @staticmethod
    def from_message(message: Message) -> dict:
        """Convert unified Message to provider format."""
        return {
            "chatId": message.chat_id,
            "message": message.text,
            # ... provider-specific fields
        }
```

### 5. Register Provider

Update `whatsfuse/main.py`:

```python
def _create_client(self) -> BaseClient:
    provider = self.config.provider.lower()
    
    # ... existing providers ...
    
    elif provider == "new_provider":
        from whatsfuse.providers.new_provider.client import NewProviderClient
        return NewProviderClient(self.config)
```

### 6. Add Documentation

Create `docs/providers/new_provider.md` with:
- Provider overview
- Installation/setup instructions
- Authentication guide
- Usage examples
- Provider-specific features
- Troubleshooting

### 7. Write Tests

Create `tests/test_providers/test_new_provider.py`:

```python
import pytest
from whatsfuse.providers.new_provider.client import NewProviderClient
from whatsfuse.core.config import Config


def test_send_text_message():
    config = Config(
        provider="new_provider",
        api_url="https://api.newprovider.com",
        api_key="test-key"
    )
    
    client = NewProviderClient(config)
    
    # Mock API call and test
    # ...
```

### 8. Add Example

Create `examples/new_provider_example.py`:

```python
"""Example usage of New Provider."""

from whatsfuse import WhatsFuse

client = WhatsFuse(
    provider="new_provider",
    api_url="https://api.newprovider.com",
    api_key="your-key"
)

message = client.send_text_message(
    chat_id="1234567890",
    text="Hello from New Provider!"
)

print(f"Message sent: {message.id}")
```

### 9. Update Lists

Update supported providers in:
- `README.md`
- `docs/index.md`
- `whatsfuse/__init__.py` (in `list_providers()`)

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=whatsfuse --cov-report=html

# Run specific test file
pytest tests/test_providers/test_waha.py

# Run specific test
pytest tests/test_providers/test_waha.py::test_send_text_message
```

## Documentation

### Building Docs

Documentation is in Markdown format in the `docs/` directory. To preview:

```bash
# Install mkdocs (optional)
pip install mkdocs mkdocs-material

# Serve docs locally
mkdocs serve

# Open http://localhost:8000
```

### Writing Docs

- Use clear, beginner-friendly language
- Include code examples
- Add screenshots where helpful
- Link to related pages

## Submitting Changes

### 1. Commit Your Changes

```bash
git add .
git commit -m "feat: add new provider support"
```

Use conventional commit messages:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `chore:` - Build/tooling changes

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template
5. Submit!

### PR Checklist

- [ ] Code follows project style (`.cursor/rules/project.md`)
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Docstrings added
- [ ] Run `python scripts/validate_api.py` (if API changed)
- [ ] Run `python scripts/generate_docs.py` (if API changed)
- [ ] CHANGELOG.md updated (if applicable)

## Getting Help

- 💬 [GitHub Discussions](https://github.com/yourusername/whatsfuse/discussions)
- 🐛 [GitHub Issues](https://github.com/yourusername/whatsfuse/issues)
- 📧 Email: support@whatsfuse.dev

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

Thank you for contributing to WhatsFuse! 🎉

