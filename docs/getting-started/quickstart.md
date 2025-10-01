# Quick Start

Send your first WhatsApp message in 5 minutes! 🚀

## Prerequisites

- WhatsFuse installed ([Installation Guide](installation.md))
- Access to a WhatsApp API provider (WAHA or Green API)
- Provider credentials configured

## Your First Message

### Step 1: Initialize the Client

```python
from whatsfuse import WhatsFuse

# Using WAHA
client = WhatsFuse(
    provider="waha",
    api_url="http://localhost:3000",
    api_key="your-api-key"
)

# Or using Green API
client = WhatsFuse(
    provider="green_api",
    instance_id="your-instance",
    api_token="your-token"
)
```

### Step 2: Send a Text Message

```python
message = client.send_text_message(
    chat_id="1234567890@c.us",  # WhatsApp ID format
    text="Hello from WhatsFuse! 👋"
)

print(f"✅ Message sent!")
print(f"Message ID: {message.id}")
print(f"Timestamp: {message.timestamp}")
```

### Step 3: Send an Image

```python
message = client.send_image(
    chat_id="1234567890@c.us",
    image="https://example.com/image.jpg",  # URL or local path
    caption="Check out this image! 📸"
)

print(f"✅ Image sent! ID: {message.id}")
```

## Common Use Cases

### Sending Different Message Types

```python
# Text with formatting
client.send_text_message(
    chat_id="1234567890@c.us",
    text="*Bold* _italic_ ~strikethrough~ ```code```"
)

# Document/File
client.send_file(
    chat_id="1234567890@c.us",
    file="/path/to/document.pdf",
    filename="report.pdf"
)

# Audio
client.send_audio(
    chat_id="1234567890@c.us",
    audio="/path/to/audio.mp3"
)

# Video
client.send_video(
    chat_id="1234567890@c.us",
    video="/path/to/video.mp4",
    caption="Check this out!"
)

# Location
client.send_location(
    chat_id="1234567890@c.us",
    latitude=37.7749,
    longitude=-122.4194,
    name="San Francisco"
)
```

### Getting Chat Information

```python
# Get all chats
chats = client.get_chats()
for chat in chats:
    print(f"{chat.name}: {chat.last_message}")

# Get messages from a specific chat
messages = client.get_chat_history(
    chat_id="1234567890@c.us",
    limit=50
)

for msg in messages:
    print(f"{msg.sender}: {msg.text}")
```

### Working with Contacts

```python
# Get all contacts
contacts = client.get_contacts()
for contact in contacts:
    print(f"{contact.name}: {contact.phone}")

# Check if number is on WhatsApp
is_registered = client.check_number_status("1234567890")
print(f"Number is on WhatsApp: {is_registered}")
```

### Mark Messages as Read

```python
# Mark a message as read
client.mark_as_read(
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)
```

## Complete Example: Simple Chatbot

Here's a simple echo bot that responds to messages:

```python
from whatsfuse import WhatsFuse
import time

# Initialize client
client = WhatsFuse(
    provider="waha",
    api_url="http://localhost:3000",
    api_key="your-api-key"
)

print("🤖 Bot started! Listening for messages...")

# Get the last message timestamp to avoid processing old messages
last_timestamp = time.time()

while True:
    try:
        # Get recent messages
        chats = client.get_chats(limit=10)
        
        for chat in chats:
            # Get recent messages from this chat
            messages = client.get_chat_history(
                chat_id=chat.id,
                limit=5
            )
            
            for message in messages:
                # Skip old messages
                if message.timestamp <= last_timestamp:
                    continue
                
                # Skip messages from us
                if message.from_me:
                    continue
                
                # Update timestamp
                last_timestamp = message.timestamp
                
                # Echo the message back
                if message.text:
                    client.send_text_message(
                        chat_id=chat.id,
                        text=f"You said: {message.text}"
                    )
                    print(f"📨 Replied to {chat.name}")
        
        # Wait before checking again
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped!")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(10)
```

## Using Async/Await

WhatsFuse supports async operations for better performance:

```python
import asyncio
from whatsfuse import AsyncWhatsFuse

async def main():
    # Initialize async client
    client = AsyncWhatsFuse(
        provider="waha",
        api_url="http://localhost:3000",
        api_key="your-api-key"
    )
    
    # Send message asynchronously
    message = await client.send_text_message(
        chat_id="1234567890@c.us",
        text="Hello async world! ⚡"
    )
    
    print(f"Message sent: {message.id}")
    
    # Close the client
    await client.close()

# Run the async function
asyncio.run(main())
```

## Using Context Manager

For automatic resource cleanup:

```python
from whatsfuse import WhatsFuse

with WhatsFuse(provider="waha", api_url="...", api_key="...") as client:
    message = client.send_text_message(
        chat_id="1234567890@c.us",
        text="This is clean! ✨"
    )
# Client automatically closed after with block
```

## Switching Providers

The beauty of WhatsFuse is how easy it is to switch providers:

```python
# Start with WAHA
client_waha = WhatsFuse(provider="waha", api_url="...", api_key="...")

# Switch to Green API (same methods work!)
client_green = WhatsFuse(provider="green_api", instance_id="...", api_token="...")

# Both use the exact same API
message1 = client_waha.send_text_message("123@c.us", "From WAHA")
message2 = client_green.send_text_message("123", "From Green API")
```

## Error Handling

Always handle errors gracefully:

```python
from whatsfuse import WhatsFuse, WhatsFuseError, RateLimitError

client = WhatsFuse(provider="waha", api_url="...", api_key="...")

try:
    message = client.send_text_message("invalid_id", "Test")
except RateLimitError:
    print("⏰ Rate limit hit, waiting...")
    time.sleep(60)
except WhatsFuseError as e:
    print(f"❌ Error: {e}")
```

## Next Steps

Now that you've sent your first message, explore more:

- 📚 [Configuration Guide](configuration.md) - Learn all configuration options
- 🔐 [Authentication Guide](authentication.md) - Secure your credentials
- 📖 [API Reference](../api-reference/) - Explore all available methods
- 💡 [Examples](../examples/) - See more complex use cases
- 🔧 [Provider Guides](../providers/) - Provider-specific features

## Tips for Success

1. **Always use environment variables** for credentials
2. **Implement error handling** for production code
3. **Use async** for better performance with many requests
4. **Test with a test number** before sending to real users
5. **Check rate limits** of your chosen provider
6. **Use logging** to debug issues

## Common Issues

### Wrong Chat ID Format

Different providers use different chat ID formats:
- WAHA: `1234567890@c.us` (with suffix)
- Green API: `1234567890` (without suffix)

WhatsFuse normalizes this, but check your provider's docs.

### Messages Not Sending

1. Check that your WhatsApp session is active
2. Verify the recipient number is on WhatsApp
3. Ensure your API credentials are valid
4. Check for rate limiting

### Rate Limiting

If you're sending many messages:
```python
import time

for recipient in recipients:
    client.send_text_message(recipient, "Hello!")
    time.sleep(1)  # Wait 1 second between messages
```

## Need Help?

- 🐛 [Report issues on GitHub](https://github.com/yourusername/whatsfuse/issues)
- 💬 [Ask questions in discussions](https://github.com/yourusername/whatsfuse/discussions)
- 📧 Email: support@whatsfuse.dev

Happy messaging! 🎉

