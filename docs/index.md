# WhatsFuse Documentation

> A unified Python SDK for multiple WhatsApp API providers

## Welcome to WhatsFuse

WhatsFuse is a powerful Python library that provides a **unified interface** for interacting with multiple unofficial WhatsApp API providers. Just like [LiteLLM](https://github.com/BerriAI/litellm) does for Large Language Models, WhatsFuse makes it easy to switch between different WhatsApp API providers without changing your code.

## Why WhatsFuse?

### The Problem
Different WhatsApp API providers have different:
- API endpoints and request formats
- Authentication methods
- Response structures
- Feature sets and capabilities
- Rate limits and pricing

This makes it difficult to:
- Switch providers when you find a better option
- Compare providers without rewriting your code
- Build applications that work with multiple providers

### The Solution
WhatsFuse provides:
- ✅ **Single Unified API** - One consistent interface for all providers
- ✅ **Easy Provider Switching** - Change providers with one line of code
- ✅ **Type Safety** - Full Python type hints for better IDE support
- ✅ **Async Support** - Built for modern async Python applications
- ✅ **Comprehensive Error Handling** - Consistent error types across providers
- ✅ **Rich Documentation** - Detailed guides and examples for every feature

## Quick Example

```python
from whatsfuse import WhatsFuse

# Initialize with WAHA provider
client = WhatsFuse(
    provider="waha",
    api_url="https://your-waha-instance.com",
    api_key="your-api-key"
)

# Send a message
message = client.send_text_message(
    chat_id="1234567890@c.us",
    text="Hello from WhatsFuse! 👋"
)

print(f"Message sent! ID: {message.id}")

# Switch to Green API with one line
client_green = WhatsFuse(
    provider="green_api",
    instance_id="your-instance",
    api_token="your-token"
)

# Same method works with different provider!
message = client_green.send_text_message(
    chat_id="1234567890",
    text="Hello from Green API! 🚀"
)
```

## Supported Providers

| Provider | Status | Authentication | Documentation |
|----------|--------|----------------|---------------|
| [WAHA](https://waha.devlike.pro) | ✅ Supported | API Key | [Guide](providers/waha.md) |
| [Green API](https://green-api.com) | ✅ Supported | Instance ID + Token | [Guide](providers/green_api.md) |
| More providers | 🚧 Coming Soon | - | - |

Want to add a provider? Check out our [Provider Development Guide](api-reference/creating-providers.md).

## Key Features

### 📤 Message Sending
- Text messages with formatting
- Images with captions
- Documents and files
- Audio and voice messages
- Video messages
- Location sharing
- Contacts
- Stickers

### 📥 Message Receiving
- Webhook support
- Message polling
- Real-time updates
- Message acknowledgments

### 💬 Chat Management
- List all chats
- Get chat history
- Mark messages as read
- Archive/unarchive chats
- Delete messages

### 👥 Contact Management
- Get contact list
- Get contact info
- Check if number is on WhatsApp
- Get profile picture

### 🔧 Advanced Features
- Session management
- QR code generation for login
- Group management
- Presence (online/offline) updates
- Typing indicators

## Getting Started

### Installation

```bash
pip install whatsfuse
```

### Basic Usage

1. **[Getting Started Guide](getting-started/installation.md)** - Install and set up WhatsFuse
2. **[Quick Start](getting-started/quickstart.md)** - Send your first message in 5 minutes
3. **[Configuration](getting-started/configuration.md)** - Learn about configuration options
4. **[Authentication](getting-started/authentication.md)** - Set up authentication for different providers

### Provider Guides

- **[WAHA Provider](providers/waha.md)** - Complete guide for WAHA
- **[Green API Provider](providers/green_api.md)** - Complete guide for Green API

### Examples

Check out the [examples directory](examples/) for:
- Sending different message types
- Handling webhooks
- Building chatbots
- Group management
- And more!

## Architecture

WhatsFuse follows a clean, modular architecture:

```
WhatsFuse Client (Your Code)
        ↓
Unified Interface (whatsfuse.main)
        ↓
Provider Abstraction (whatsfuse.core.base_client)
        ↓
Provider Implementations (whatsfuse.providers.*)
        ↓
HTTP Client (whatsfuse.utils.http)
        ↓
WhatsApp API Providers
```

Each provider is completely isolated, making it easy to:
- Add new providers
- Fix provider-specific issues
- Customize behavior per provider

## Provider Development

Want to add a new provider? Check out these resources:
- **[Parameter Mapping Guide](PARAMETER_MAPPING.md)** - How unified parameters map to provider APIs
- **[Contributing Guide](../CONTRIBUTING.md)** - Step-by-step guide to adding providers

## Contributing

We welcome contributions! See our [Contributing Guide](../CONTRIBUTING.md) for details on:
- Adding new providers
- Reporting bugs
- Suggesting features
- Submitting pull requests

## Support

- 📖 **Documentation**: You're reading it!
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/whatsfuse/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/whatsfuse/discussions)
- 📧 **Email**: support@whatsfuse.dev

## License

WhatsFuse is released under the MIT License. See [LICENSE](../LICENSE) for details.

## Acknowledgments

- Inspired by [LiteLLM](https://github.com/BerriAI/litellm)
- Built with ❤️ for the WhatsApp automation community
- Thanks to all WhatsApp API providers for their services

---

Ready to get started? Head over to the [Installation Guide](getting-started/installation.md)!

