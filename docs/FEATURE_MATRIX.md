# WhatsFuse Feature Matrix

> **Auto-generated** from `api_spec.json` - Do not edit manually!

**Version**: 0.2.0  
**Last Updated**: 2025-10-01  
**Generated**: 2025-10-01 14:43:27

---

## 📋 Table of Contents

- [send_text_message()](#user-content-sendtextmessage)
- [send_image()](#user-content-sendimage)
- [send_video()](#user-content-sendvideo)
- [send_file()](#user-content-sendfile)
- [send_voice()](#user-content-sendvoice)
- [send_location()](#user-content-sendlocation)
- [send_contact()](#user-content-sendcontact)
- [send_poll()](#user-content-sendpoll)
- [send_buttons()](#user-content-sendbuttons)
- [send_list_message()](#user-content-sendlistmessage)
- [send_event()](#user-content-sendevent)
- [forward_message()](#user-content-forwardmessage)
- [edit_message()](#user-content-editmessage)
- [delete_message()](#user-content-deletemessage)
- [star_message()](#user-content-starmessage)
- [pin_message()](#user-content-pinmessage)
- [unpin_message()](#user-content-unpinmessage)
- [get_messages()](#user-content-getmessages)
- [get_message()](#user-content-getmessage)
- [mark_chat_read()](#user-content-markchatread)
- [archive_chat()](#user-content-archivechat)
- [unarchive_chat()](#user-content-unarchivechat)
- [set_disappearing_chat()](#user-content-setdisappearingchat)
- [download_file()](#user-content-downloadfile)
- [upload_file()](#user-content-uploadfile)
- [get_last_incoming_messages()](#user-content-getlastincomingmessages)
- [get_last_outgoing_messages()](#user-content-getlastoutgoingmessages)
- [show_messages_queue()](#user-content-showmessagesqueue)
- [clear_messages_queue()](#user-content-clearmessagesqueue)
- [get_messages_count()](#user-content-getmessagescount)
- [send_text_status()](#user-content-sendtextstatus)
- [send_media_status()](#user-content-sendmediastatus)
- [update_group_settings()](#user-content-updategroupsettings)

---

## 📖 Legend

### Support Status
- ✅ **Fully Supported** - Works as documented
- ⚠️ **Partial Support** - Works with limitations
- 🔧 **In Progress** - Currently being implemented
- ❌ **Not Supported** - Feature unavailable
- 📋 **Planned** - Scheduled for future

---

## 💬 Message Sending

### send_text_message()

**Status**: ✅ Implemented

**Purpose**: Send a text message to a chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | The unique identifier for the chat |
| `text` | `str` | ✅ Yes | - | ✅ | ✅ | The message text to send |
| `reply_to` | `Optional[str]` | ❌ No | `None` | ✅ | ✅ | Optional message ID to reply to |
| `mentions` | `Optional[list[str]]` | ❌ No | `None` | ✅ | ⚠️ | Optional list of phone numbers to mention |
| `link_preview` | `bool` | ❌ No | `True` | ✅ | ✅ | Whether to show link preview |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "text": text,
    "linkPreview": link_preview,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "message": text,
    "linkPreview": link_preview,
}
```
**Support**: ✅ Most features, ⚠️ mentions partial

---

### send_image()

**Status**: 📋 Planned

**Purpose**: Send an image message to a chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | The unique identifier for the chat |
| `file` | `FileData` | ✅ Yes | - | ✅ | ✅ | File data (url or base64) |
| `caption` | `Optional[str]` | ❌ No | `None` | ✅ | ✅ | Optional caption for the image |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "file": file,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "urlFile or file": file,
}
```
**Support**: ✅ All features fully supported

---

### send_video()

**Status**: 📋 Planned

**Purpose**: Send a video message to a chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `file` | `FileData` | ✅ Yes | - | ✅ | ✅ | - |
| `caption` | `Optional[str]` | ❌ No | `None` | ✅ | ✅ | - |
| `as_note` | `bool` | ❌ No | `False` | ✅ | ❌ | Send as video note |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "file": file,
    "asNote": as_note,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "urlFile": file,
}
```
**Support**: ✅ All features fully supported

---

### send_file()

**Status**: 📋 Planned

**Purpose**: Send a file/document message to a chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `file` | `FileData` | ✅ Yes | - | ✅ | ✅ | - |
| `caption` | `Optional[str]` | ❌ No | `None` | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "file": file,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "urlFile or file": file,
}
```
**Support**: ✅ All features fully supported

---

### send_voice()

**Status**: 📋 Planned

**Purpose**: Send a voice message to a chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `file` | `FileData` | ✅ Yes | - | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "file": file,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "urlFile": file,
}
```
**Support**: ✅ All features fully supported

---

### send_location()

**Status**: 📋 Planned

**Purpose**: Send a location message to a chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `latitude` | `float` | ✅ Yes | - | ✅ | ✅ | - |
| `longitude` | `float` | ✅ Yes | - | ✅ | ✅ | - |
| `name` | `Optional[str]` | ❌ No | `None` | ✅ | ✅ | - |
| `address` | `Optional[str]` | ❌ No | `None` | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "latitude": latitude,
    "longitude": longitude,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "latitude": latitude,
    "longitude": longitude,
}
```
**Support**: ✅ All features fully supported

---

### send_contact()

**Status**: 📋 Planned

**Purpose**: Send a contact card (vCard) to a chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `contact` | `ContactData` | ✅ Yes | - | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "contact": contact,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "contact": contact,
}
```
**Support**: ✅ All features fully supported

---

### send_poll()

**Status**: 📋 Planned

**Purpose**: Send a poll message to a chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `name` | `str` | ✅ Yes | - | ✅ | ✅ | Poll question |
| `options` | `list[str]` | ✅ Yes | - | ✅ | ✅ | - |
| `multiple_answers` | `bool` | ❌ No | `False` | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "poll.name": name,
    "poll.options": options,
    "poll.multipleAnswers": multiple_answers,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "message": name,
    "options": options,
    "multipleAnswers": multiple_answers,
}
```
**Support**: ✅ All features fully supported

---

### send_buttons()

**Status**: 📋 Planned

**Purpose**: Send a message with interactive buttons

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ⚠️ | ✅ | - |
| `text` | `str` | ✅ Yes | - | ⚠️ | ✅ | - |
| `buttons` | `list[Button]` | ✅ Yes | - | ⚠️ | ✅ | - |
| `footer` | `Optional[str]` | ❌ No | `None` | ❌ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "text": text,
    "buttons": buttons,
}
```
**Support**: ✅ Most features, ⚠️ chat_id, text, buttons partial

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "message": text,
    "buttons": buttons,
}
```
**Support**: ✅ All features fully supported

---

### send_list_message()

**Status**: 📋 Planned

**Purpose**: Send a message with a list of selectable items

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ❌ | ✅ | - |
| `title` | `str` | ✅ Yes | - | ❌ | ✅ | - |
| `description` | `str` | ✅ Yes | - | ❌ | ✅ | - |
| `button_text` | `str` | ✅ Yes | - | ❌ | ✅ | - |
| `sections` | `list[Section]` | ✅ Yes | - | ❌ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "title": title,
    "description": description,
    "buttonText": button_text,
    "sections": sections,
}
```
**Support**: ✅ All features fully supported

---

### send_event()

**Status**: 📋 Planned

**Purpose**: Send an event/calendar message to a chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ❌ | - |
| `event` | `EventData` | ✅ Yes | - | ✅ | ❌ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "event": event,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

---

### forward_message()

**Status**: 📋 Planned

**Purpose**: Forward a message to another chat

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `message_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "messageId": message_id,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "idMessage": message_id,
}
```
**Support**: ✅ All features fully supported

---

## ✏️ Message Management

### edit_message()

**Status**: 📋 Planned

**Purpose**: Edit an existing message

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `message_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `text` | `str` | ✅ Yes | - | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "messageId": message_id,
    "text": text,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "idMessage": message_id,
    "message": text,
}
```
**Support**: ✅ All features fully supported

---

### delete_message()

**Status**: 📋 Planned

**Purpose**: Delete a message

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `message_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "messageId": message_id,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "idMessage": message_id,
}
```
**Support**: ✅ All features fully supported

---

### star_message()

**Status**: 📋 Planned

**Purpose**: Star or unstar a message

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ❌ | - |
| `message_id` | `str` | ✅ Yes | - | ✅ | ❌ | - |
| `star` | `bool` | ✅ Yes | - | ✅ | ❌ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "messageId": message_id,
    "star": star,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

---

### pin_message()

**Status**: 📋 Planned

**Purpose**: Pin a message in a chat

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ❌ | - |
| `message_id` | `str` | ✅ Yes | - | ✅ | ❌ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "messageId": message_id,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

---

### unpin_message()

**Status**: 📋 Planned

**Purpose**: Unpin a message in a chat

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ❌ | - |
| `message_id` | `str` | ✅ Yes | - | ✅ | ❌ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "messageId": message_id,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

---

## 📥 Message Retrieval

### get_messages()

**Status**: 📋 Planned

**Purpose**: Get messages from a chat

**Returns**: `list[Message]`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `limit` | `Optional[int]` | ❌ No | `None` | ⚠️ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
}
```
**Support**: ✅ Most features, ⚠️ limit partial

**Green API Provider:**
```python
{
    "chatId": chat_id,
}
```
**Support**: ✅ All features fully supported

---

### get_message()

**Status**: 📋 Planned

**Purpose**: Get a specific message by ID

**Returns**: `Message`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |
| `message_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
    "messageId": message_id,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "idMessage": message_id,
}
```
**Support**: ✅ All features fully supported

---

### get_last_incoming_messages()

**Status**: 📋 Planned

**Purpose**: Get last incoming messages

**Returns**: `list[Message]`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `minutes` | `Optional[int]` | ❌ No | `1440` | ❌ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "minutes": minutes,
}
```
**Support**: ✅ All features fully supported

---

### get_last_outgoing_messages()

**Status**: 📋 Planned

**Purpose**: Get last outgoing messages

**Returns**: `list[Message]`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `minutes` | `Optional[int]` | ❌ No | `1440` | ❌ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "minutes": minutes,
}
```
**Support**: ✅ All features fully supported

---

## 💭 Chat Management

### mark_chat_read()

**Status**: 📋 Planned

**Purpose**: Mark all messages in a chat as read

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ✅ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
    "chatId": chat_id,
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
}
```
**Support**: ✅ All features fully supported

---

### archive_chat()

**Status**: 📋 Planned

**Purpose**: Archive a chat

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ❌ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
}
```
**Support**: ✅ All features fully supported

---

### unarchive_chat()

**Status**: 📋 Planned

**Purpose**: Unarchive a chat

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ❌ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
}
```
**Support**: ✅ All features fully supported

---

### set_disappearing_chat()

**Status**: 📋 Planned

**Purpose**: Set disappearing messages timer for a chat

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `chat_id` | `str` | ✅ Yes | - | ❌ | ✅ | - |
| `ephemeral_expiration` | `int` | ✅ Yes | - | ❌ | ✅ | Expiration in seconds |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "chatId": chat_id,
    "ephemeralExpiration": ephemeral_expiration,
}
```
**Support**: ✅ All features fully supported

---

## 📁 File Operations

### download_file()

**Status**: 📋 Planned

**Purpose**: Download a file from a message

**Returns**: `FileData`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `message_id` | `str` | ✅ Yes | - | ⚠️ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ Most features, ⚠️ message_id partial

**Green API Provider:**
```python
{
    "idMessage": message_id,
}
```
**Support**: ✅ All features fully supported

---

### upload_file()

**Status**: 📋 Planned

**Purpose**: Upload a file to send later

**Returns**: `str`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `file` | `bytes` | ✅ Yes | - | ❌ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "file": file,
}
```
**Support**: ✅ All features fully supported

---

## 📊 Queue Management

### show_messages_queue()

**Status**: 📋 Planned

**Purpose**: Show messages waiting to be sent

**Returns**: `list[QueuedMessage]`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

---

### clear_messages_queue()

**Status**: 📋 Planned

**Purpose**: Clear all messages from the outgoing queue

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

---

### get_messages_count()

**Status**: 📋 Planned

**Purpose**: Get count of messages in outgoing queue

**Returns**: `int`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

---

## 📢 Status Updates

### send_text_status()

**Status**: 📋 Planned

**Purpose**: Send a text status update

**Returns**: `Status`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `text` | `str` | ✅ Yes | - | ❌ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "message": text,
}
```
**Support**: ✅ All features fully supported

---

### send_media_status()

**Status**: 📋 Planned

**Purpose**: Send a media status update

**Returns**: `Status`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `file` | `FileData` | ✅ Yes | - | ❌ | ✅ | - |
| `caption` | `Optional[str]` | ❌ No | `None` | ❌ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ All features fully supported

**Green API Provider:**
```python
{
    "urlFile": file,
}
```
**Support**: ✅ All features fully supported

---

## 👥 Group Management

### update_group_settings()

**Status**: 📋 Planned

**Purpose**: Update group settings

**Returns**: `bool`

#### Parameters

| Parameter | Type | Required | Default | WAHA | Green API | Description |
|-----------|------|----------|---------|------|-----------|-------------|
| `group_id` | `str` | ✅ Yes | - | ⚠️ | ✅ | - |
| `settings` | `GroupSettings` | ✅ Yes | - | ⚠️ | ✅ | - |

#### Provider Mapping

**WAHA Provider:**
```python
{
}
```
**Support**: ✅ Most features, ⚠️ group_id, settings partial

**Green API Provider:**
```python
{
    "groupId": group_id,
}
```
**Support**: ✅ All features fully supported

---

## 📊 Summary

### Methods Overview

| Method | Category | Status | WAHA | Green API |
|--------|----------|--------|------|-----------|
| `send_text_message` | messaging | ✅ | ✅ | ⚠️ |
| `send_image` | messaging | 📋 | ✅ | ✅ |
| `send_video` | messaging | 📋 | ✅ | ⚠️ |
| `send_file` | messaging | 📋 | ✅ | ✅ |
| `send_voice` | messaging | 📋 | ✅ | ✅ |
| `send_location` | messaging | 📋 | ✅ | ✅ |
| `send_contact` | messaging | 📋 | ✅ | ✅ |
| `send_poll` | messaging | 📋 | ✅ | ✅ |
| `send_buttons` | messaging | 📋 | ⚠️ | ✅ |
| `send_list_message` | messaging | 📋 | ⚠️ | ✅ |
| `send_event` | messaging | 📋 | ✅ | ⚠️ |
| `forward_message` | messaging | 📋 | ✅ | ✅ |
| `edit_message` | message_management | 📋 | ✅ | ✅ |
| `delete_message` | message_management | 📋 | ✅ | ✅ |
| `star_message` | message_management | 📋 | ✅ | ⚠️ |
| `pin_message` | message_management | 📋 | ✅ | ⚠️ |
| `unpin_message` | message_management | 📋 | ✅ | ⚠️ |
| `get_messages` | retrieval | 📋 | ⚠️ | ✅ |
| `get_message` | retrieval | 📋 | ✅ | ✅ |
| `mark_chat_read` | chat_management | 📋 | ✅ | ✅ |
| `archive_chat` | chat_management | 📋 | ⚠️ | ✅ |
| `unarchive_chat` | chat_management | 📋 | ⚠️ | ✅ |
| `set_disappearing_chat` | chat_management | 📋 | ⚠️ | ✅ |
| `download_file` | files | 📋 | ⚠️ | ✅ |
| `upload_file` | files | 📋 | ⚠️ | ✅ |
| `get_last_incoming_messages` | retrieval | 📋 | ⚠️ | ✅ |
| `get_last_outgoing_messages` | retrieval | 📋 | ⚠️ | ✅ |
| `show_messages_queue` | queue | 📋 | ✅ | ✅ |
| `clear_messages_queue` | queue | 📋 | ✅ | ✅ |
| `get_messages_count` | queue | 📋 | ✅ | ✅ |
| `send_text_status` | status | 📋 | ⚠️ | ✅ |
| `send_media_status` | status | 📋 | ⚠️ | ✅ |
| `update_group_settings` | groups | 📋 | ⚠️ | ✅ |

---

## 📝 Maintenance

This document is **automatically generated** from `api_spec.json`.

**To update this documentation:**
1. Edit `api_spec.json`
2. Run `python scripts/generate_docs.py`
3. Commit both files

**Do not edit this file manually!**

---

*Generated by WhatsFuse docs generator v0.2.0*
