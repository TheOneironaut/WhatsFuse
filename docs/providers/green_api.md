# Green API Provider Guide

Complete guide for using WhatsFuse with [Green API](https://green-api.com/).

## What is Green API?

Green API is a cloud-based WhatsApp Business API that provides easy integration without the need for self-hosting. It offers a managed service with good reliability and various pricing tiers.

### Key Features
- ✅ Cloud-hosted (no setup needed)
- ✅ Easy to get started
- ✅ Free tier available
- ✅ Multiple instances support
- ✅ Webhook support
- ✅ Media handling
- ✅ REST API
- ✅ Good documentation

## Getting Started

### Step 1: Create Account

1. Go to [green-api.com](https://green-api.com)
2. Click "Sign Up" or "Get Started"
3. Complete registration
4. Verify your email

### Step 2: Create Instance

1. Log in to your dashboard
2. Click "Create Instance"
3. Choose a pricing plan (Free tier available)
4. Note your **Instance ID** and **API Token**

### Step 3: Connect WhatsApp

1. Go to your instance dashboard
2. Click "Connect WhatsApp"
3. Scan the QR code with your WhatsApp
4. Wait for status to show "Authorized"

## Authentication

Green API uses Instance ID + API Token authentication:

```python
from whatsfuse import WhatsFuse

client = WhatsFuse(
    provider="green_api",
    instance_id="1234567890",
    api_token="your-api-token-here"
)
```

### Using Environment Variables

```bash
# .env
WHATSFUSE_PROVIDER=green_api
GREEN_API_INSTANCE_ID=1234567890
GREEN_API_API_TOKEN=your-api-token-here
```

```python
from whatsfuse import WhatsFuse

client = WhatsFuse.from_env()
```

## Instance Management

### Get Instance State

```python
state = client.get_state()

print(f"Status: {state.state_instance}")
# authorized, notAuthorized, blocked, sleepMode, etc.
```

### Get Instance Settings

```python
settings = client.get_settings()

print(f"Webhooks enabled: {settings.webhooks_enabled}")
print(f"Incoming webhook: {settings.incoming_webhook_url}")
```

### Update Instance Settings

```python
client.update_settings(
    webhooks_enabled=True,
    incoming_webhook_url="https://your-server.com/webhook",
    outgoing_webhook_url="https://your-server.com/webhook-outgoing"
)
```

### Reboot Instance

```python
# Reboot the instance (useful if having issues)
client.reboot_instance()
```

### Logout

```python
# Logout from WhatsApp (will require QR scan again)
client.logout()
```

## Sending Messages

### Text Message

```python
message = client.send_text_message(
    chat_id="1234567890@c.us",  # Or just "1234567890"
    text="Hello from Green API! 👋"
)

print(f"Message sent: {message.id}")
```

### Text with Formatting

```python
message = client.send_text_message(
    chat_id="1234567890",
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
    chat_id="1234567890",
    image="https://example.com/image.jpg",
    caption="Check this out! 📸"
)

# From local file
message = client.send_image(
    chat_id="1234567890",
    image="/path/to/local/image.jpg",
    caption="Local image"
)
```

### Document/File

```python
message = client.send_file(
    chat_id="1234567890",
    file="https://example.com/document.pdf",  # URL
    filename="report.pdf"
)

# Or from local file
message = client.send_file(
    chat_id="1234567890",
    file="/path/to/document.pdf",
    filename="report.pdf"
)
```

### Audio

```python
message = client.send_audio(
    chat_id="1234567890",
    audio="https://example.com/audio.mp3"
)

# Voice message (audio plays inline)
message = client.send_audio(
    chat_id="1234567890",
    audio="/path/to/voice.ogg",
    as_voice=True  # Sends as voice message
)
```

### Video

```python
message = client.send_video(
    chat_id="1234567890",
    video="https://example.com/video.mp4",
    caption="Check this video!"
)
```

### Location

```python
message = client.send_location(
    chat_id="1234567890",
    latitude=37.7749,
    longitude=-122.4194,
    name="San Francisco",
    address="San Francisco, CA, USA"
)
```

### Contact

```python
message = client.send_contact(
    chat_id="1234567890",
    contact={
        "phoneContact": 9876543210,
        "firstName": "John",
        "lastName": "Doe",
        "company": "ACME Inc"
    }
)
```

### Link with Preview

```python
message = client.send_link(
    chat_id="1234567890",
    url="https://example.com",
    title="Example Website",
    description="Check out this website",
    image="https://example.com/preview.jpg"
)
```

## Receiving Messages

### Using Webhooks (Recommended)

Configure webhooks in your instance settings:

```python
client.update_settings(
    webhooks_enabled=True,
    incoming_webhook_url="https://your-server.com/webhook"
)
```

Handle webhooks in your server:

```python
from flask import Flask, request
from whatsfuse import WhatsFuse

app = Flask(__name__)
client = WhatsFuse(provider="green_api", instance_id="...", api_token="...")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Green API webhook structure
    if data['typeWebhook'] == 'incomingMessageReceived':
        message_data = data['messageData']
        sender = message_data['sender']  # Phone number
        message_type = message_data['typeMessage']
        
        if message_type == 'textMessage':
            text = message_data['textMessageData']['textMessage']
            
            # Echo the message back
            client.send_text_message(
                chat_id=sender,
                text=f"You said: {text}"
            )
    
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(port=5000)
```

### Polling Messages

```python
import time

# Get last incoming messages
while True:
    messages = client.receive_notification()
    
    if messages:
        for message in messages:
            if message.type == 'incomingMessageReceived':
                print(f"New message: {message.text}")
                
                # Delete the notification after processing
                client.delete_notification(message.receipt_id)
    
    time.sleep(5)
```

## Chat Management

### Get Chats

```python
chats = client.get_chats()

for chat in chats:
    print(f"{chat.name} - ID: {chat.id}")
```

### Get Chat History

```python
messages = client.get_chat_history(
    chat_id="1234567890@c.us",
    count=100
)

for msg in messages:
    print(f"[{msg.timestamp}] {msg.sender}: {msg.text}")
```

### Get Last Messages

```python
# Get last incoming messages
messages = client.get_last_incoming_messages(minutes=60)

for msg in messages:
    print(f"From {msg.sender}: {msg.text}")
```

### Clear Messages Queue

```python
# Clear all messages in queue
client.clear_messages_queue()
```

## Contact Management

### Get Contacts

```python
contacts = client.get_contacts()

for contact in contacts:
    print(f"{contact.name}: {contact.id}")
```

### Get Contact Info

```python
contact = client.get_contact_info(contact_id="1234567890@c.us")

print(f"Name: {contact.name}")
print(f"Phone: {contact.wa_id}")
```

### Check WhatsApp

```python
# Check if number is on WhatsApp
result = client.check_whatsapp("1234567890")

if result.exists:
    print(f"✅ Number is on WhatsApp")
    print(f"WhatsApp ID: {result.chat_id}")
else:
    print("❌ Number not on WhatsApp")
```

### Get Avatar

```python
# Get profile picture URL
avatar = client.get_avatar(chat_id="1234567890@c.us")

print(f"Profile picture: {avatar.url}")
```

## Group Management

### Create Group

```python
group = client.create_group(
    group_name="My Group",
    chat_ids=["1234567890@c.us", "0987654321@c.us"]
)

print(f"Group created: {group.chat_id}")
```

### Update Group Name

```python
client.update_group_name(
    group_id="123456789@g.us",
    group_name="New Group Name"
)
```

### Get Group Data

```python
group = client.get_group_data(group_id="123456789@g.us")

print(f"Name: {group.group_name}")
print(f"Owner: {group.owner}")
print(f"Participants: {len(group.participants)}")

for participant in group.participants:
    print(f"  - {participant.id}: {participant.name}")
```

### Add Group Participant

```python
client.add_group_participant(
    group_id="123456789@g.us",
    participant_chat_id="1234567890@c.us"
)
```

### Remove Group Participant

```python
client.remove_group_participant(
    group_id="123456789@g.us",
    participant_chat_id="1234567890@c.us"
)
```

### Set Group Admin

```python
client.set_group_admin(
    group_id="123456789@g.us",
    participant_chat_id="1234567890@c.us"
)
```

### Remove Group Admin

```python
client.remove_group_admin(
    group_id="123456789@g.us",
    participant_chat_id="1234567890@c.us"
)
```

### Set Group Picture

```python
client.set_group_picture(
    group_id="123456789@g.us",
    file="https://example.com/group-pic.jpg"
)
```

### Leave Group

```python
client.leave_group(group_id="123456789@g.us")
```

## Read Receipts & Presence

### Mark as Read

```python
# Mark chat as read (Green API specific)
client.read_chat(chat_id="1234567890@c.us")
```

### Set Presence

```python
# Show as online
client.set_presence(presence="online")

# Show as offline
client.set_presence(presence="offline")
```

## File Operations

### Upload File

```python
# Upload file to Green API servers
uploaded = client.upload_file(file_path="/path/to/file.pdf")

print(f"File URL: {uploaded.url}")

# Use the URL to send
client.send_file(
    chat_id="1234567890",
    file=uploaded.url,
    filename="document.pdf"
)
```

### Download File

```python
# Download media from message
media = client.download_file(
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)

# Save to file
with open("downloaded_file.jpg", "wb") as f:
    f.write(media)
```

## Queue Management

### Show Messages Queue

```python
# Get messages in queue
queue = client.show_messages_queue()

print(f"Messages in queue: {len(queue)}")
```

### Clear Queue

```python
# Clear all messages
client.clear_messages_queue()
```

## Account Management

### Get Account Info

```python
# Get QR code (if not authorized)
qr = client.get_qr_code()

if qr.exists:
    print(f"Scan QR: {qr.message}")
else:
    print("Already authorized")
```

### Get Account Settings

```python
settings = client.get_settings()

print(f"Webhooks: {settings.webhooks_enabled}")
print(f"Mark incoming as read: {settings.mark_incoming_messages_readed}")
```

### Update Settings

```python
client.update_settings(
    webhooks_enabled=True,
    incoming_webhook_url="https://your-server.com/webhook",
    mark_incoming_messages_readed=False,
    keep_online_status=True
)
```

## Error Handling

Handle Green API-specific errors:

```python
from whatsfuse import (
    WhatsFuseError,
    AuthenticationError,
    InstanceNotAuthorizedError,
    RateLimitError
)

try:
    message = client.send_text_message("123", "Hello")
except InstanceNotAuthorizedError:
    print("❌ Instance not authorized - scan QR code")
except AuthenticationError:
    print("❌ Invalid credentials")
except RateLimitError as e:
    print(f"❌ Rate limited: {e}")
except WhatsFuseError as e:
    print(f"❌ Error: {e}")
```

## Rate Limits

Green API has rate limits based on your plan:

- **Free Plan**: Lower rate limits
- **Paid Plans**: Higher rate limits

Best practices:
```python
import time

# Add delays between bulk sends
for recipient in recipients:
    client.send_text_message(recipient, "Hello!")
    time.sleep(1)  # Wait 1 second between messages
```

## Best Practices

1. **Use Webhooks**: More reliable than polling
2. **Check Instance State**: Verify authorization before sending
3. **Handle Errors**: Always wrap calls in try-except
4. **Respect Rate Limits**: Add delays between bulk operations
5. **Clear Queue**: Regularly clear notification queue to avoid overflow
6. **Monitor Usage**: Check your usage in the dashboard
7. **Secure Credentials**: Never commit API tokens

## Configuration Options

### Timeouts

```python
client = WhatsFuse(
    provider="green_api",
    instance_id="123",
    api_token="token",
    timeout=30,  # Request timeout in seconds
    connect_timeout=10
)
```

### Retry Logic

```python
client = WhatsFuse(
    provider="green_api",
    instance_id="123",
    api_token="token",
    max_retries=3,
    retry_delay=2
)
```

## Troubleshooting

### Instance Not Authorized

**Solution**: Scan QR code again
```python
qr = client.get_qr_code()
print("Scan this QR code with WhatsApp")
```

### Webhooks Not Working

1. Check webhook URL is accessible from internet
2. Ensure HTTPS (HTTP might not work)
3. Verify webhooks are enabled in settings
4. Check webhook logs in Green API dashboard

### Messages Not Sending

1. Check instance state: `client.get_state()`
2. Verify recipient number format
3. Check rate limits
4. Review error messages

### Rate Limit Errors

Wait and retry:
```python
import time

try:
    client.send_text_message("123", "Hello")
except RateLimitError:
    print("Rate limited, waiting...")
    time.sleep(60)
    client.send_text_message("123", "Hello")
```

## Pricing & Plans

Green API offers several plans:

- **Free Tier**: Limited messages, good for testing
- **Basic**: More messages and features
- **Business**: Higher limits and priority support
- **Enterprise**: Custom limits and SLA

Check [green-api.com/pricing](https://green-api.com/en/pricing.html) for current pricing.

## Resources

- 📖 [Green API Documentation](https://green-api.com/en/docs/)
- 🌐 [Green API Website](https://green-api.com)
- 🎮 [Green API Console](https://console.green-api.com)
- 💬 [Support](https://green-api.com/en/contacts.html)

## Need Help?

- 🐛 [Report WhatsFuse issues](https://github.com/yourusername/whatsfuse/issues)
- 💬 [WhatsFuse Discussions](https://github.com/yourusername/whatsfuse/discussions)
- 📧 Email: support@whatsfuse.dev

