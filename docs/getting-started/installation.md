# Installation

Get WhatsFuse up and running in minutes.

## Requirements

- Python 3.10 or higher
- pip (Python package manager)
- Access to at least one WhatsApp API provider (WAHA, Green API, etc.)

## Install via pip

```bash
pip install whatsfuse
```

### Install from source

For the latest development version:

```bash
git clone https://github.com/yourusername/whatsfuse.git
cd whatsfuse
pip install -e .
```

## Verify Installation

Check that WhatsFuse is installed correctly:

```python
import whatsfuse

print(whatsfuse.__version__)
print("Supported providers:", whatsfuse.list_providers())
```

Expected output:
```
0.1.0
Supported providers: ['waha', 'green_api']
```

## Provider Setup

WhatsFuse requires credentials for at least one WhatsApp API provider. Follow the guide for your chosen provider:

### WAHA Setup

1. **Deploy WAHA instance**
   - Self-hosted: Follow [WAHA installation guide](https://waha.devlike.pro/docs/install-update/)
   - Docker: `docker run -it -p 3000:3000 devlikeapro/waha`
   - Cloud: Use any cloud provider (AWS, GCP, Azure, etc.)

2. **Get your API URL and Key**
   - Default URL: `http://localhost:3000`
   - API key is configured during WAHA setup

3. **Test connection**
   ```python
   from whatsfuse import WhatsFuse
   
   client = WhatsFuse(
       provider="waha",
       api_url="http://localhost:3000",
       api_key="your-api-key"
   )
   
   # Check if connection works
   sessions = client.get_sessions()
   print(f"Connected! Found {len(sessions)} sessions")
   ```

See the complete [WAHA Provider Guide](../providers/waha.md) for detailed setup.

### Green API Setup

1. **Create account**
   - Sign up at [Green API](https://green-api.com)
   - Choose a plan (free tier available)

2. **Create instance**
   - Go to dashboard
   - Click "Create Instance"
   - Note your Instance ID and API Token

3. **Test connection**
   ```python
   from whatsfuse import WhatsFuse
   
   client = WhatsFuse(
       provider="green_api",
       instance_id="your-instance-id",
       api_token="your-api-token"
   )
   
   # Check if connection works
   state = client.get_state()
   print(f"Connected! State: {state}")
   ```

See the complete [Green API Provider Guide](../providers/green_api.md) for detailed setup.

## Environment Variables

For security, use environment variables for credentials:

```bash
# .env file
WHATSFUSE_PROVIDER=waha
WHATSFUSE_API_URL=http://localhost:3000
WHATSFUSE_API_KEY=your-api-key
```

Then in your code:

```python
from whatsfuse import WhatsFuse
import os

client = WhatsFuse(
    provider=os.getenv("WHATSFUSE_PROVIDER"),
    api_url=os.getenv("WHATSFUSE_API_URL"),
    api_key=os.getenv("WHATSFUSE_API_KEY")
)
```

Or use the built-in config loading:

```python
from whatsfuse import WhatsFuse

# Automatically loads from environment variables
client = WhatsFuse.from_env()
```

## Development Installation

If you're contributing to WhatsFuse:

```bash
# Clone the repository
git clone https://github.com/yourusername/whatsfuse.git
cd whatsfuse

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
pytest
```

## Optional Dependencies

WhatsFuse has optional dependencies for specific features:

```bash
# Async support (recommended)
pip install whatsfuse[async]

# Image processing
pip install whatsfuse[images]

# All optional dependencies
pip install whatsfuse[all]
```

## Troubleshooting

### Import Error

**Problem**: `ModuleNotFoundError: No module named 'whatsfuse'`

**Solution**:
```bash
# Ensure pip installed successfully
pip install --upgrade whatsfuse

# Check if it's in your Python path
python -c "import sys; print(sys.path)"
```

### Connection Error

**Problem**: `ConnectionError: Failed to connect to provider API`

**Solutions**:
1. Check your API URL is correct and accessible
2. Verify your API credentials
3. Ensure no firewall is blocking the connection
4. For WAHA: Check the instance is running (`docker ps`)

### Version Conflicts

**Problem**: Dependency version conflicts

**Solution**:
```bash
# Use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install whatsfuse
```

## Next Steps

- 📚 [Quick Start Guide](quickstart.md) - Send your first message
- 🔧 [Configuration Guide](configuration.md) - Learn all configuration options
- 🔐 [Authentication Guide](authentication.md) - Set up authentication properly
- 📖 [API Reference](../api-reference/) - Explore all available methods

## Need Help?

- 🐛 Found a bug? [Report it on GitHub](https://github.com/yourusername/whatsfuse/issues)
- 💬 Questions? [Join our discussions](https://github.com/yourusername/whatsfuse/discussions)
- 📧 Email: support@whatsfuse.dev

