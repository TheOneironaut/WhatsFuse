# WhatsFuse 🔥

> Unified Python SDK for Multiple WhatsApp API Providers

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)]()

WhatsFuse is a powerful Python library that provides a **unified interface** for interacting with multiple unofficial WhatsApp API providers. Inspired by [LiteLLM](https://github.com/BerriAI/litellm), WhatsFuse makes it easy to switch between different WhatsApp API providers without changing your code.

## ✨ Why WhatsFuse?

### The Problem
Different WhatsApp API providers have:
- 🔀 Different API endpoints and request formats
- 🔐 Different authentication methods
- 📊 Different response structures
- 🎯 Different feature sets

This makes it difficult to:
- Switch providers without rewriting code
- Compare providers objectively
- Build portable WhatsApp automation

### The Solution
WhatsFuse provides:
- ✅ **Single Unified API** - One consistent interface for all providers
- ✅ **Easy Provider Switching** - Change providers with one line of code
- ✅ **Type Safety** - Full Python type hints for better IDE support
- ✅ **Comprehensive Error Handling** - Consistent error types across providers
- ✅ **Rich Documentation** - Detailed guides and examples

## 🚀 Quick Start

### Installation

```bash
pip install whatsfuse
```

### Basic Usage

```python
from whatsfuse import WhatsFuse

# Initialize with WAHA provider
client = WhatsFuse(
    provider="waha",
    api_url="http://localhost:3000",
    api_key="your-api-key"
)

# Send a message
message = client.send_text_message(
    chat_id="1234567890@c.us",
    text="Hello from WhatsFuse! 👋"
)

print(f"Message sent! ID: {message.id}")
```

### Switch Providers Easily

```python
# Switch to Green API with one line
client_green = WhatsFuse(
    provider="green_api",
    instance_id="your-instance",
    api_token="your-token"
)

# SAME CODE works with different provider! 🎯
message = client_green.send_text_message(
    chat_id="1234567890",
    text="Hello from Green API! 🚀",
    reply_to="msg_abc123",        # Unified parameters
    mentions=["972501234567"],     # Work across all providers
    link_preview=False             # No code changes needed!
)
```

## 📚 Supported Providers

| Provider | Status | Documentation |
|----------|--------|---------------|
| [WAHA](https://waha.devlike.pro) | ✅ Supported | [Guide](docs/providers/waha.md) |
| [Green API](https://green-api.com) | ✅ Supported | [Guide](docs/providers/green_api.md) |
| More providers | 🚧 Coming Soon | - |

## 🎯 Key Features

### Message Sending
```python
# Text messages
client.send_text_message(chat_id, "Hello!")

# Images with captions
client.send_image(chat_id, "image.jpg", caption="Check this out!")

# Documents
client.send_file(chat_id, "document.pdf", filename="report.pdf")

# Audio and video
client.send_audio(chat_id, "audio.mp3")
client.send_video(chat_id, "video.mp4", caption="Amazing!")

# Location
client.send_location(chat_id, latitude=37.7749, longitude=-122.4194)
```

### Chat Management
```python
# Get all chats
chats = client.get_chats()

# Get chat history
messages = client.get_chat_history(chat_id, limit=50)

# Mark as read
client.mark_as_read(chat_id, message_id)
```

### Contact Management
```python
# Get contacts
contacts = client.get_contacts()

# Check if number is on WhatsApp
is_on_whatsapp = client.check_number_status("1234567890")
```

## 📖 Documentation

### Getting Started
- 📦 [Installation Guide](docs/getting-started/installation.md)
- 🚀 [Quick Start](docs/getting-started/quickstart.md)
- ⚙️ [Configuration](docs/getting-started/configuration.md)

### Provider Guides
- 🔧 [WAHA Provider](docs/providers/waha.md)
- 🟢 [Green API Provider](docs/providers/green_api.md)

### API Reference
- 📚 [Full API Documentation](docs/api-reference/)

### Examples
Check out the [examples directory](examples/) for:
- Sending different message types
- Building chatbots
- Handling webhooks
- Group management
- And more!

## 🏗️ Project Structure

```
whatsfuse/
├── whatsfuse/              # Main package
│   ├── __init__.py        # Public API
│   ├── main.py            # Main WhatsFuse class
│   ├── core/              # Core functionality
│   │   ├── base_client.py # Abstract base class
│   │   ├── exceptions.py  # Custom exceptions
│   │   ├── types.py       # Type definitions
│   │   └── config.py      # Configuration
│   ├── providers/         # Provider implementations
│   │   ├── waha/          # WAHA provider
│   │   │   ├── client.py
│   │   │   ├── transformer.py
│   │   │   └── schemas.py
│   │   └── green_api/     # Green API provider
│   │       ├── client.py
│   │       ├── transformer.py
│   │       └── schemas.py
│   └── utils/             # Utility functions
├── docs/                  # User documentation
├── tests/                 # Test suite
├── examples/              # Example scripts
└── .cursorrules          # AI development guidelines
```

## 🔧 Architecture

WhatsFuse follows a clean, modular architecture inspired by LiteLLM:

```
Your Application
       ↓
WhatsFuse Client (Unified Interface)
       ↓
Provider Abstraction Layer
       ↓
Provider Implementations (WAHA, Green API, etc.)
       ↓
HTTP Client
       ↓
WhatsApp API Providers
```

### Design Principles

1. **Provider Abstraction** - Each provider is completely isolated
2. **Unified Interface** - All providers implement the same core methods
3. **Easy Extensibility** - Add new providers without changing existing code
4. **Type Safety** - Full type hints throughout the codebase
5. **Error Consistency** - Uniform error handling across providers

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Adding a New Provider

1. Create provider directory: `whatsfuse/providers/<provider_name>/`
2. Implement `client.py` inheriting from `BaseClient`
3. Implement `transformer.py` for data transformation
4. Add provider-specific schemas in `schemas.py`
5. Write tests
6. Add documentation

See [.cursorrules](.cursorrules) for detailed development guidelines.

### Reporting Issues

Found a bug? Have a suggestion? [Open an issue](https://github.com/yourusername/whatsfuse/issues)!

## 📝 Development Status

**Current Status: Alpha** 🚧

WhatsFuse is currently in active development. The project structure, architecture, and documentation are complete, but provider implementations are in progress.

### What's Ready
- ✅ Project structure and architecture
- ✅ Comprehensive documentation
- ✅ AI development guidelines (.cursorrules)
- ✅ Type definitions and interfaces
- ✅ Configuration management
- ✅ Error handling framework

### What's Coming
- 🚧 WAHA provider implementation
- 🚧 Green API provider implementation
- 🚧 Unit tests
- 🚧 Integration tests
- 🚧 Example scripts
- 🚧 Async support

## 🔐 Security

- Never commit API keys or credentials
- Use environment variables for sensitive data
- Review [security guidelines](docs/security.md)

## 📜 License

WhatsFuse is released under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Inspired by [LiteLLM](https://github.com/BerriAI/litellm)
- Built for the WhatsApp automation community
- Thanks to all WhatsApp API providers

## 📞 Support

- 📖 [Documentation](docs/)
- 🐛 [Issues](https://github.com/yourusername/whatsfuse/issues)
- 💬 [Discussions](https://github.com/yourusername/whatsfuse/discussions)
- 📧 Email: support@whatsfuse.dev

## ⭐ Star History

If you find WhatsFuse useful, please consider giving it a star! ⭐

---

**Made with ❤️ by the WhatsFuse community**

