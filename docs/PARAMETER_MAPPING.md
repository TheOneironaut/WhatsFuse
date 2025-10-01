# Parameter Mapping Guide

> How unified parameters map to provider-specific APIs

## Overview

WhatsFuse uses a **unified interface** based on WAHA's API design. Each provider translates these unified parameters to its specific API format internally.

This document shows how unified parameters map to each provider's native API.

## Core Principle

```
User Code (Unified)  →  Provider Translation  →  Provider API
     ↓                         ↓                      ↓
chat_id: "123"          WAHA: chatId="123"      WAHA API
reply_to: "msg_456"     WAHA: reply_to="..."   
mentions: [...]         WAHA: mentions=[...]    
                              ↓
                        Green API:              Green API
                        chatId="123@c.us"
                        quotedMessageId="..."
                        mentions=[...]
```

## Send Text Message

### Unified Interface
```python
client.send_text_message(
    chat_id: str,
    text: str,
    reply_to: Optional[str] = None,
    mentions: Optional[List[str]] = None,
    link_preview: bool = True,
)
```

### WAHA Provider Mapping
```python
# Unified → WAHA API
{
    "session": "default",
    "chatId": chat_id,           # Direct mapping
    "text": text,                # Direct mapping
    "reply_to": reply_to,        # Direct mapping (if provided)
    "mentions": mentions,        # Direct mapping (if provided)
    "linkPreview": link_preview  # Direct mapping
}
```
**Support**: ✅ All features fully supported

### Green API Provider Mapping
```python
# Unified → Green API
{
    "chatId": f"{chat_id}@c.us",        # Adds @c.us suffix
    "message": text,                     # 'message' not 'text'
    "quotedMessageId": reply_to,         # reply_to → quotedMessageId
    "mentions": [f"{m}@c.us" for m in mentions],  # Adds @c.us to each
    "linkPreview": link_preview          # Direct mapping
}
```
**Support**: 
- ✅ `reply_to`: Fully supported (mapped to `quotedMessageId`)
- ⚠️ `mentions`: Partial (format may differ)
- ✅ `link_preview`: Fully supported

## Send Image

### Unified Interface
```python
client.send_image(
    chat_id: str,
    image: Union[str, bytes, Path],
    caption: Optional[str] = None,
    reply_to: Optional[str] = None,
    filename: Optional[str] = None,
)
```

### WAHA Provider Mapping
```python
# Unified → WAHA API
{
    "session": "default",
    "chatId": chat_id,
    "file": {
        "url": image_url,          # If image is URL
        "mimetype": "image/jpeg",  # Auto-detected
        "filename": filename       # If provided
    },
    "caption": caption,            # If provided
    "reply_to": reply_to          # If provided
}
```

### Green API Provider Mapping
```python
# Unified → Green API
{
    "chatId": f"{chat_id}@c.us",
    "urlFile": image_url,          # If image is URL
    "fileName": filename,           # If provided
    "caption": caption,             # If provided
    "quotedMessageId": reply_to    # If provided
}
```

## Send File/Document

### Unified Interface
```python
client.send_file(
    chat_id: str,
    file: Union[str, bytes, Path],
    filename: Optional[str] = None,
    caption: Optional[str] = None,
    reply_to: Optional[str] = None,
)
```

### WAHA Provider Mapping
```python
# Unified → WAHA API
{
    "session": "default",
    "chatId": chat_id,
    "file": {
        "url": file_url,
        "mimetype": "application/pdf",  # Auto-detected
        "filename": filename
    },
    "caption": caption,
    "reply_to": reply_to
}
```

### Green API Provider Mapping
```python
# Unified → Green API
{
    "chatId": f"{chat_id}@c.us",
    "urlFile": file_url,
    "fileName": filename,
    "caption": caption,
    "quotedMessageId": reply_to
}
```

## Send Audio

### Unified Interface
```python
client.send_audio(
    chat_id: str,
    audio: Union[str, bytes, Path],
    reply_to: Optional[str] = None,
)
```

### WAHA Provider Mapping
```python
# Unified → WAHA API
{
    "session": "default",
    "chatId": chat_id,
    "file": {
        "url": audio_url,
        "mimetype": "audio/mpeg"
    },
    "reply_to": reply_to
}
```

### Green API Provider Mapping
```python
# Unified → Green API
{
    "chatId": f"{chat_id}@c.us",
    "urlFile": audio_url,
    "fileName": "audio.mp3",
    "quotedMessageId": reply_to
}
```

## Send Video

### Unified Interface
```python
client.send_video(
    chat_id: str,
    video: Union[str, bytes, Path],
    caption: Optional[str] = None,
    reply_to: Optional[str] = None,
)
```

### WAHA Provider Mapping
```python
# Unified → WAHA API
{
    "session": "default",
    "chatId": chat_id,
    "file": {
        "url": video_url,
        "mimetype": "video/mp4"
    },
    "caption": caption,
    "reply_to": reply_to
}
```

### Green API Provider Mapping
```python
# Unified → Green API
{
    "chatId": f"{chat_id}@c.us",
    "urlFile": video_url,
    "fileName": "video.mp4",
    "caption": caption,
    "quotedMessageId": reply_to
}
```

## Send Location

### Unified Interface
```python
client.send_location(
    chat_id: str,
    latitude: float,
    longitude: float,
    name: Optional[str] = None,
    address: Optional[str] = None,
    reply_to: Optional[str] = None,
)
```

### WAHA Provider Mapping
```python
# Unified → WAHA API
{
    "session": "default",
    "chatId": chat_id,
    "latitude": latitude,
    "longitude": longitude,
    "title": name,              # name → title
    "address": address,
    "reply_to": reply_to
}
```

### Green API Provider Mapping
```python
# Unified → Green API
{
    "chatId": f"{chat_id}@c.us",
    "latitude": latitude,
    "longitude": longitude,
    "nameLocation": name,        # name → nameLocation
    "address": address,
    "quotedMessageId": reply_to
}
```

## Chat ID Format

### Unified Format
```python
chat_id = "1234567890"  # Just the number
```

### WAHA Format
```python
# Individual chats
chatId = "1234567890@c.us"

# Group chats
chatId = "123456789-987654321@g.us"
```

### Green API Format
```python
# Individual chats
chatId = "1234567890@c.us"

# Group chats  
chatId = "123456789-987654321@g.us"
```

**Translation**: Most providers require the `@c.us` suffix, which is added automatically.

## Feature Support Matrix

| Feature | WAHA | Green API | Notes |
|---------|------|-----------|-------|
| `chat_id` | ✅ | ✅ | Auto-adds @c.us |
| `reply_to` | ✅ | ✅ | Maps to quotedMessageId |
| `mentions` | ✅ | ⚠️ | Green API: limited support |
| `link_preview` | ✅ | ✅ | Direct mapping |
| `caption` | ✅ | ✅ | Direct mapping |
| `filename` | ✅ | ✅ | Maps to fileName |

Legend:
- ✅ Fully supported
- ⚠️ Partial support (may have limitations)
- ❌ Not supported

## Adding a New Provider

When implementing a new provider, follow these steps:

### 1. Identify Parameter Mappings

Create a mapping document for your provider:
```python
PARAMETER_MAPPING = {
    # Unified → Provider
    "chat_id": "conversation_id",
    "text": "messageText",
    "reply_to": "inReplyTo",
    "mentions": "taggedUsers",
    # ... etc
}
```

### 2. Implement Translation Methods

```python
class MyProviderClient(BaseClient):
    def _translate_chat_id(self, chat_id: str) -> str:
        """Translate unified chat_id to provider format."""
        return f"{chat_id}@provider.com"
    
    def _translate_reply_to(self, reply_to: Optional[str]) -> dict:
        """Translate reply_to parameter."""
        if reply_to:
            return {"inReplyTo": reply_to}
        return {}
    
    def send_text_message(
        self,
        chat_id: str,
        text: str,
        reply_to: Optional[str] = None,
        mentions: Optional[list[str]] = None,
        link_preview: bool = True,
        **kwargs
    ) -> Message:
        """Send text with translation."""
        payload = {
            "conversationId": self._translate_chat_id(chat_id),
            "messageText": text,
            "showPreview": link_preview,
            **self._translate_reply_to(reply_to),
            **self._translate_mentions(mentions)
        }
        
        response = self._http_post("/sendMessage", payload)
        return self._transform_response(response)
```

### 3. Handle Unsupported Features

```python
def _translate_mentions(self, mentions: Optional[list[str]]) -> dict:
    """Translate mentions - with fallback."""
    if not mentions:
        return {}
    
    if self.provider_supports_mentions():
        return {"taggedUsers": mentions}
    else:
        # Log warning
        logger.warning(f"[{self.provider_name}] mentions not supported")
        # Optionally emulate
        return {}
```

### 4. Document Support

Update `docs/providers/your_provider.md`:
```markdown
## Feature Support

- ✅ `reply_to`: Fully supported (mapped to inReplyTo)
- ⚠️ `mentions`: Partial support (limited to 5 mentions)
- ❌ `link_preview`: Not supported
```

## Best Practices

1. **Always translate, never expose provider details**
   ```python
   # ❌ Bad - exposes provider details
   client.send_message(chatId="123@c.us", quotedMessageId="...")
   
   # ✅ Good - unified interface
   client.send_text_message(chat_id="123", reply_to="...")
   ```

2. **Handle missing features gracefully**
   ```python
   if feature_not_supported:
       logger.warning(f"Feature not supported by {provider}")
       # Continue without the feature or emulate it
   ```

3. **Document everything**
   - Parameter mappings
   - Feature support
   - Known limitations

4. **Test translations thoroughly**
   - Unit tests for each translation method
   - Integration tests with real API (optional)

## Summary

The unified interface ensures:
- ✅ **Write once, run anywhere** - Same code works with all providers
- ✅ **Clear translation** - Each provider handles its own mapping
- ✅ **Graceful degradation** - Unsupported features handled properly
- ✅ **Easy to extend** - Adding providers is straightforward

When in doubt, follow WAHA's parameter names and structure as the reference!
