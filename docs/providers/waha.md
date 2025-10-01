# WAHA Provider Guide

Complete guide for using WhatsFuse with [WAHA (WhatsApp HTTP API)](https://waha.devlike.pro/).

## What is WAHA?

WAHA is a self-hosted WhatsApp HTTP API that allows you to send and receive WhatsApp messages via HTTP requests. It's open-source, feature-rich, and gives you complete control over your WhatsApp automation.

### Key Features
- ✅ Self-hosted (full control)
- ✅ Multiple sessions support
- ✅ Webhook support
- ✅ Media handling (images, videos, documents)
- ✅ Group management
- ✅ QR code generation
- ✅ Docker support
- ✅ Free and open-source

## Installation & Setup

### Option 1: Docker (Recommended)

```bash
# Pull the latest image
docker pull devlikeapro/waha

# Run WAHA
docker run -it -p 3000:3000 devlikeapro/waha

# Or with environment variables
docker run -it \
  -p 3000:3000 \
  -e WAHA_API_KEY=your-secure-api-key \
  devlikeapro/waha
```

### Option 2: Docker Compose

```yaml
# docker-compose.yml
version: '3'
services:
  waha:
    image: devlikeapro/waha
    ports:
      - "3000:3000"
    environment:
      - WAHA_API_KEY=your-secure-api-key
    volumes:
      - ./waha-data:/app/.waha
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

### Option 3: Manual Installation

See [WAHA installation docs](https://waha.devlike.pro/docs/install-update/) for manual installation steps.

## Authentication

WAHA uses API key authentication:

```python
from whatsfuse import WhatsFuse

client = WhatsFuse(
    provider="waha",
    api_url="http://localhost:3000",
    api_key="your-api-key"
)
```

### Using Environment Variables

```bash
# .env
WHATSFUSE_PROVIDER=waha
WHATSFUSE_API_URL=http://localhost:3000
WHATSFUSE_API_KEY=your-api-key
```

```python
from whatsfuse import WhatsFuse

client = WhatsFuse.from_env()
```

## Session Management

WAHA supports multiple WhatsApp sessions (different phone numbers).

### Create a Session

```python
# Create a new session
session = client.create_session(
    name="default",
    config={
        "webhooks": {
            "url": "https://your-webhook-url.com/webhook",
            "events": ["message"]
        }
    }
)

print(f"Session created: {session.name}")
```

### Get QR Code for Login

```python
# Get QR code to scan with WhatsApp
qr_code = client.get_qr_code(session="default")

# qr_code is a base64 encoded PNG image
# Display it or save it
with open("qr.png", "wb") as f:
    f.write(qr_code.decode_base64())

print("Scan the QR code with WhatsApp!")
```

### Check Session Status

```python
# Get session status
status = client.get_session_status(session="default")

print(f"Status: {status.state}")  # READY, STARTING, SCAN_QR_CODE, etc.
print(f"Authenticated: {status.authenticated}")
```

### List All Sessions

```python
# Get all sessions
sessions = client.get_sessions()

for session in sessions:
    print(f"{session.name}: {session.state}")
```

### Stop/Delete Session

```python
# Stop a session
client.stop_session(session="default")

# Delete a session completely
client.delete_session(session="default")
```

## Sending Messages

### Text Message

```python
message = client.send_text_message(
    chat_id="1234567890@c.us",
    text="Hello from WAHA! 👋",
    session="default"  # Optional, defaults to "default"
)

print(f"Message sent: {message.id}")
```

### Text with Formatting

```python
message = client.send_text_message(
    chat_id="1234567890@c.us",
    text="""
*Bold text*
_Italic text_
~Strikethrough~
```monospace```
"""
)
```

### Image

```python
# From URL
message = client.send_image(
    chat_id="1234567890@c.us",
    image="https://example.com/image.jpg",
    caption="Check this out! 📸"
)

# From local file
message = client.send_image(
    chat_id="1234567890@c.us",
    image="/path/to/local/image.jpg",
    caption="Local image"
)

# From bytes
with open("image.jpg", "rb") as f:
    image_bytes = f.read()
    
message = client.send_image(
    chat_id="1234567890@c.us",
    image=image_bytes,
    caption="Image from bytes"
)
```

### Document/File

```python
message = client.send_file(
    chat_id="1234567890@c.us",
    file="/path/to/document.pdf",
    filename="report.pdf",  # Optional custom filename
    caption="Here's the report"
)
```

### Audio

```python
message = client.send_audio(
    chat_id="1234567890@c.us",
    audio="/path/to/audio.mp3"
)
```

### Video

```python
message = client.send_video(
    chat_id="1234567890@c.us",
    video="/path/to/video.mp4",
    caption="Check this video!"
)
```

### Location

```python
message = client.send_location(
    chat_id="1234567890@c.us",
    latitude=37.7749,
    longitude=-122.4194,
    name="San Francisco",
    address="San Francisco, CA, USA"
)
```

### Contact

```python
message = client.send_contact(
    chat_id="1234567890@c.us",
    contact_id="9876543210@c.us"
)
```

### Reply to Message

```python
message = client.send_text_message(
    chat_id="1234567890@c.us",
    text="This is a reply",
    reply_to="message_id_to_reply_to"
)
```

### Buttons (WAHA Plus feature)

```python
message = client.send_buttons(
    chat_id="1234567890@c.us",
    text="Choose an option:",
    buttons=[
        {"id": "1", "text": "Option 1"},
        {"id": "2", "text": "Option 2"},
        {"id": "3", "text": "Option 3"}
    ]
)
```

## Receiving Messages

### Using Webhooks (Recommended)

Configure webhooks when creating a session:

```python
client.create_session(
    name="default",
    config={
        "webhooks": {
            "url": "https://your-server.com/webhook",
            "events": ["message", "message.ack", "state.change"]
        }
    }
)
```

Handle webhooks in your server:

```python
from flask import Flask, request
from whatsfuse import WhatsFuse

app = Flask(__name__)
client = WhatsFuse(provider="waha", api_url="...", api_key="...")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    if data['event'] == 'message':
        message = data['payload']
        chat_id = message['from']
        text = message.get('body', '')
        
        # Echo the message back
        if text and not message.get('fromMe'):
            client.send_text_message(
                chat_id=chat_id,
                text=f"You said: {text}"
            )
    
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(port=5000)
```

### Polling Messages

```python
import time

last_timestamp = time.time()

while True:
    # Get recent messages
    chats = client.get_chats(limit=10)
    
    for chat in chats:
        messages = client.get_chat_history(
            chat_id=chat.id,
            limit=10
        )
        
        for message in messages:
            if message.timestamp > last_timestamp and not message.from_me:
                print(f"New message from {chat.name}: {message.text}")
                last_timestamp = message.timestamp
    
    time.sleep(5)
```

## Chat Management

### Get All Chats

```python
chats = client.get_chats(limit=50, session="default")

for chat in chats:
    print(f"{chat.name} - Last message: {chat.last_message}")
```

### Get Chat History

```python
messages = client.get_chat_history(
    chat_id="1234567890@c.us",
    limit=100
)

for msg in messages:
    print(f"[{msg.timestamp}] {msg.sender}: {msg.text}")
```

### Mark as Read

```python
client.mark_as_read(
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)
```

### Archive/Unarchive Chat

```python
# Archive
client.archive_chat(chat_id="1234567890@c.us")

# Unarchive
client.unarchive_chat(chat_id="1234567890@c.us")
```

### Delete Message

```python
client.delete_message(
    chat_id="1234567890@c.us",
    message_id="message_id_here",
    for_everyone=True  # Delete for everyone (within time limit)
)
```

## Contact Management

### Get All Contacts

```python
contacts = client.get_contacts()

for contact in contacts:
    print(f"{contact.name}: {contact.phone}")
```

### Get Contact Info

```python
contact = client.get_contact_info(contact_id="1234567890@c.us")

print(f"Name: {contact.name}")
print(f"Phone: {contact.phone}")
print(f"Is business: {contact.is_business}")
```

### Check if Number is on WhatsApp

```python
is_registered = client.check_number_status("1234567890")

if is_registered:
    print("✅ Number is on WhatsApp")
else:
    print("❌ Number is not on WhatsApp")
```

### Get Profile Picture

```python
profile_pic = client.get_profile_picture(contact_id="1234567890@c.us")

# profile_pic is a URL or base64 image
print(f"Profile picture: {profile_pic}")
```

## Group Management

### Create Group

```python
group = client.create_group(
    name="My Group",
    participants=["1234567890@c.us", "0987654321@c.us"]
)

print(f"Group created: {group.id}")
```

### Get Group Info

```python
group = client.get_group_info(group_id="123456789@g.us")

print(f"Name: {group.name}")
print(f"Participants: {len(group.participants)}")
```

### Add/Remove Participants

```python
# Add participants
client.add_group_participants(
    group_id="123456789@g.us",
    participants=["1234567890@c.us"]
)

# Remove participants
client.remove_group_participants(
    group_id="123456789@g.us",
    participants=["1234567890@c.us"]
)
```

### Leave Group

```python
client.leave_group(group_id="123456789@g.us")
```

## Presence & Typing

### Set Presence

```python
# Set as online
client.set_presence(chat_id="1234567890@c.us", presence="available")

# Set as offline
client.set_presence(chat_id="1234567890@c.us", presence="unavailable")
```

### Send Typing Indicator

```python
# Start typing
client.send_typing(chat_id="1234567890@c.us", typing=True)

# Stop typing
client.send_typing(chat_id="1234567890@c.us", typing=False)
```

## Error Handling

Handle WAHA-specific errors:

```python
from whatsfuse import (
    WhatsFuseError,
    AuthenticationError,
    SessionNotFoundError,
    MessageNotSentError
)

try:
    message = client.send_text_message("123@c.us", "Hello")
except AuthenticationError:
    print("❌ Invalid API key")
except SessionNotFoundError:
    print("❌ Session not found - create one first")
except MessageNotSentError as e:
    print(f"❌ Message failed: {e}")
except WhatsFuseError as e:
    print(f"❌ Error: {e}")
```

## Advanced Features

### Download Media

```python
# Download media from a message
media = client.download_media(
    message_id="message_id_here",
    chat_id="1234567890@c.us"
)

# Save to file
with open("downloaded_media.jpg", "wb") as f:
    f.write(media)
```

### Get Message Info

```python
info = client.get_message_info(
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)

print(f"Delivered: {info.delivered}")
print(f"Read: {info.read}")
print(f"Played: {info.played}")
```

### Star/Unstar Message

```python
# Star a message
client.star_message(
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)

# Unstar a message
client.unstar_message(
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)
```

## Configuration Options

### Timeouts

```python
client = WhatsFuse(
    provider="waha",
    api_url="http://localhost:3000",
    api_key="your-api-key",
    timeout=30,  # Request timeout in seconds
    connect_timeout=10  # Connection timeout
)
```

### Retry Logic

```python
client = WhatsFuse(
    provider="waha",
    api_url="http://localhost:3000",
    api_key="your-api-key",
    max_retries=3,  # Number of retries
    retry_delay=1  # Delay between retries (seconds)
)
```

### Session Name

```python
# Use a custom session name
client.send_text_message(
    chat_id="1234567890@c.us",
    text="Hello",
    session="my-custom-session"
)
```

## Best Practices

1. **Keep WAHA Updated**: Regularly update to get new features and bug fixes
   ```bash
   docker pull devlikeapro/waha
   ```

2. **Use HTTPS**: In production, run WAHA behind a reverse proxy with SSL
   
3. **Secure Your API Key**: Never commit API keys, use environment variables

4. **Monitor Sessions**: Regularly check session status and reconnect if needed
   
5. **Handle Webhooks**: Use webhooks instead of polling for better performance

6. **Backup Sessions**: Back up the `.waha` folder to preserve sessions
   
7. **Rate Limiting**: Respect WhatsApp's rate limits to avoid bans

## Troubleshooting

### QR Code Not Scanning

- Ensure your phone has internet connection
- Make sure you're using the latest WhatsApp version
- Try deleting and recreating the session

### Session Disconnecting

- Check if phone is connected to internet
- Ensure phone battery saver isn't killing WhatsApp
- Check WAHA logs for errors

### Messages Not Sending

- Verify session is in READY state
- Check if recipient number is correct
- Ensure you're not rate limited

### Docker Issues

```bash
# Check logs
docker logs <container-id>

# Restart container
docker restart <container-id>

# Remove and recreate
docker-compose down && docker-compose up -d
```

## Resources

- 📖 [WAHA Official Documentation](https://waha.devlike.pro/docs)
- 🐛 [WAHA GitHub Issues](https://github.com/devlikeapro/waha/issues)
- 💬 [WAHA Discord Community](https://discord.gg/waha)
- 📚 [WAHA API Reference](https://waha.devlike.pro/docs/swagger/)

## Need Help?

- 🐛 [Report WhatsFuse issues](https://github.com/yourusername/whatsfuse/issues)
- 💬 [WhatsFuse Discussions](https://github.com/yourusername/whatsfuse/discussions)
- 📧 Email: support@whatsfuse.dev

