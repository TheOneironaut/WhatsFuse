# WhatsFuse 🚀

> **A unified Python SDK for multiple WhatsApp API providers**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

WhatsFuse provides a single, consistent interface for multiple WhatsApp API providers. Write your code once, switch providers with one line. Inspired by [LiteLLM](https://github.com/BerriAI/litellm).

## ✨ Features

- 🎯 **Unified Interface** - Same code works with all providers
- 🔄 **Easy Switching** - Change providers with one parameter
- 🛡️ **Type Safe** - Full Python type hints
- 📚 **Well Documented** - Comprehensive guides and examples
- 🧩 **Provider Agnostic** - Focus on your app, not provider APIs
- ⚡ **Modern Python** - Built with Python 3.10+ features

## 🎬 Quick Start

### Installation

```bash
pip install whatsfuse
```

### Basic Usage

```python
from whatsfuse import WhatsFuse

# Initialize with any provider
client = WhatsFuse(
    provider="waha",  # or "green_api"
    api_url="http://localhost:3000",
    api_key="your-api-key"
)

# Send a message
message = client.send_text_message(
    chat_id="1234567890@c.us",
    text="Hello from WhatsFuse! 👋"
)

print(f"Message sent: {message.id}")
```

### Switch Providers Instantly

```python
# Start with WAHA
client_waha = WhatsFuse(provider="waha", api_url="...", api_key="...")

# Switch to Green API - SAME CODE!
client_green = WhatsFuse(provider="green_api", instance_id="...", api_token="...")

# Both work identically! 🎯
message1 = client_waha.send_text_message("123@c.us", "Hello")
message2 = client_green.send_text_message("123@c.us", "Hello")
```

## 📋 Supported Providers

| Provider | Status | Type | Authentication |
|----------|--------|------|----------------|
| [WAHA](https://waha.devlike.pro) | ✅ Ready | Self-hosted | API Key |
| [Green API](https://green-api.com) | ✅ Ready | Cloud | Instance ID + Token |
| More providers | 🚧 Coming | - | - |

## 📖 Documentation

### Getting Started
- **[Installation Guide](docs/getting-started/installation.md)** - Setup and first steps
- **[Quick Start Tutorial](docs/getting-started/quickstart.md)** - Send your first message in 5 minutes

### Provider Guides
- **[WAHA Provider](docs/providers/waha.md)** - Complete WAHA setup and usage
- **[Green API Provider](docs/providers/green_api.md)** - Complete Green API setup and usage

### Development
- **[Project Overview](docs/development/project-overview.md)** - Architecture and design
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute
- **[Start Here](docs/development/start-here.md)** - Development setup
- **[Automation System](docs/development/automation-system.md)** - How we manage the API

### API Reference
- **[Feature Matrix](docs/FEATURE_MATRIX.md)** - Complete method and parameter reference
- **[Parameter Mapping](docs/PARAMETER_MAPPING.md)** - How unified parameters map to providers
- **[Architecture](docs/architecture.md)** - Visual architecture overview
- **[Design Document](docs/DESIGN.md)** - Detailed design decisions

## 🎯 Core Concepts

### Unified Interface

All providers implement the **same interface** with the **same parameters**:

```python
# Unified parameters work across ALL providers
client.send_text_message(
    chat_id="123",
    text="Hello",
    reply_to="msg_456",      # Unified parameter
    mentions=["972501234567"], # Unified parameter
    link_preview=False        # Unified parameter
)
```

Each provider translates these unified parameters to its specific API format internally.

### Provider Abstraction

```
Your Code (Unified)
       ↓
WhatsFuse Interface
       ↓
Provider Translation
       ↓
Provider API (WAHA/Green API/etc)
```

## 💡 Examples

### Send Different Message Types

```python
# Text message
client.send_text_message(chat_id="123@c.us", text="Hello!")

# Image with caption
client.send_image(
    chat_id="123@c.us",
    image="https://example.com/image.jpg",
    caption="Check this out!"
)

# Document
client.send_file(
    chat_id="123@c.us",
    file="/path/to/document.pdf",
    filename="report.pdf"
)

# Location
client.send_location(
    chat_id="123@c.us",
    latitude=37.7749,
    longitude=-122.4194,
    name="San Francisco"
)
```

### Receive Messages

```python
# Get chat history
messages = client.get_chat_history(
    chat_id="123@c.us",
    limit=50
)

for msg in messages:
    print(f"{msg.sender}: {msg.text}")
```

### Error Handling

```python
from whatsfuse import WhatsFuseError, AuthenticationError

try:
    message = client.send_text_message("123@c.us", "Hello")
except AuthenticationError:
    print("Invalid credentials")
except WhatsFuseError as e:
    print(f"Error: {e}")
```

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](docs/CONTRIBUTING.md) for:
- Adding new providers
- Reporting bugs
- Suggesting features
- Submitting pull requests

### Quick Dev Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/whatsfuse.git
cd whatsfuse

# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest
```

## 🔧 Development Tools

WhatsFuse uses a hybrid automation system for maintaining consistency:

```bash
# Validate API consistency
python scripts/validate_api.py

# Generate documentation
python scripts/generate_docs.py
```

See [Automation System](docs/development/automation-system.md) for details.

## 📊 Project Status

- ✅ **Core Architecture** - Complete
- ✅ **WAHA Provider** - Ready (placeholder implementation)
- ✅ **Green API Provider** - Ready (placeholder implementation)
- ✅ **Documentation** - Comprehensive
- 🚧 **Full Implementation** - In Progress
- 📋 **Additional Providers** - Planned

## 🎓 Architecture

WhatsFuse follows a clean, modular architecture:

```
┌─────────────────────────┐
│   Your Application      │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│  WhatsFuse Interface    │  ← Unified API
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
┌────────┐      ┌─────────┐
│  WAHA  │      │ Green   │  ← Provider Translation
│ Client │      │  API    │
└───┬────┘      └────┬────┘
    │                │
    ▼                ▼
  WAHA API      Green API
```

See [Architecture Docs](docs/architecture.md) for visual diagrams and detailed explanations.

## 📝 Philosophy

**Write Once, Run Anywhere**

```python
# Your code
def send_notification(client, phone, message):
    return client.send_text_message(phone, message)

# Works with ANY provider!
send_notification(waha_client, "123", "Hi")
send_notification(green_client, "123", "Hi")
```

## 🔗 Resources

- 📖 [Full Documentation](docs/index.md)
- 🐛 [Issue Tracker](https://github.com/yourusername/whatsfuse/issues)
- 💬 [Discussions](https://github.com/yourusername/whatsfuse/discussions)
- 📧 Email: support@whatsfuse.dev

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Inspired by [LiteLLM](https://github.com/BerriAI/litellm)
- Built with ❤️ for the WhatsApp automation community
- Thanks to all WhatsApp API providers

---

**Ready to start?** Check out our [Quick Start Guide](docs/getting-started/quickstart.md)!
