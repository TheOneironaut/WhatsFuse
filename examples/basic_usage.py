"""
Basic usage example for WhatsFuse.

This example demonstrates the simplest way to use WhatsFuse to send messages.
"""

from whatsfuse import WhatsFuse

def main():
    # Initialize WhatsFuse with WAHA provider
    client = WhatsFuse(
        provider="waha",
        api_url="http://localhost:3000",
        api_key="your-api-key-here"
    )
    
    # Send a simple text message
    message = client.send_text_message(
        chat_id="1234567890@c.us",
        text="Hello from WhatsFuse! 👋"
    )
    
    print(f"✅ Message sent successfully!")
    print(f"Message ID: {message.id}")
    print(f"Timestamp: {message.timestamp}")
    
    # Send a message with unified parameters
    reply_message = client.send_text_message(
        chat_id="1234567890@c.us",
        text="This is a reply with mentions!",
        reply_to=message.id,           # Reply to previous message
        mentions=["972501234567"],     # Mention someone
        link_preview=False             # Disable link preview
    )
    
    print(f"✅ Reply sent with unified parameters!")
    
    # Send an image with caption and reply
    image_message = client.send_image(
        chat_id="1234567890@c.us",
        image="https://example.com/image.jpg",
        caption="Check out this image! 📸",
        reply_to=message.id            # Reply to original message
    )
    
    print(f"✅ Image sent! ID: {image_message.id}")
    
    # Get recent chats
    chats = client.get_chats(limit=10)
    
    print(f"\n📱 Recent chats ({len(chats)}):")
    for chat in chats:
        print(f"  - {chat.name}: {chat.last_message}")


def switch_providers_example():
    """Example of switching between providers with unified parameters."""
    
    # Start with WAHA
    client_waha = WhatsFuse(
        provider="waha",
        api_url="http://localhost:3000",
        api_key="waha-key"
    )
    
    # Switch to Green API - SAME API!
    client_green = WhatsFuse(
        provider="green_api",
        instance_id="1234567890",
        api_token="green-api-token"
    )
    
    # SAME CODE works with BOTH providers! 🎯
    # The unified parameters work identically
    message1 = client_waha.send_text_message(
        chat_id="123@c.us",
        text="From WAHA with unified params",
        reply_to="msg_123",
        mentions=["972501234567"],
        link_preview=False
    )
    
    message2 = client_green.send_text_message(
        chat_id="123",
        text="From Green API with unified params",
        reply_to="msg_123",        # Translated to quotedMessageId internally
        mentions=["972501234567"],  # Translated to Green API format
        link_preview=False
    )
    
    print("✅ Sent via both providers using the SAME unified API!")
    print("   WAHA and Green API both used reply_to, mentions, link_preview")


def env_config_example():
    """Example using environment variables."""
    
    # Set these in your .env file:
    # WHATSFUSE_PROVIDER=waha
    # WHATSFUSE_API_URL=http://localhost:3000
    # WHATSFUSE_API_KEY=your-key
    
    # Load configuration from environment
    client = WhatsFuse.from_env()
    
    message = client.send_text_message(
        chat_id="1234567890@c.us",
        text="Using env config!"
    )
    
    print(f"✅ Message sent using env config: {message.id}")


def context_manager_example():
    """Example using context manager for automatic cleanup."""
    
    with WhatsFuse(provider="waha", api_url="...", api_key="...") as client:
        message = client.send_text_message(
            chat_id="1234567890@c.us",
            text="Using context manager 🎯"
        )
        print(f"✅ Message sent: {message.id}")
    
    # Client automatically cleaned up after with block
    print("✅ Client closed automatically")


if __name__ == "__main__":
    # NOTE: These examples will fail until provider implementations are complete
    print("⚠️  Provider implementations are in progress.")
    print("⚠️  These examples show the intended API design.")
    
    # Uncomment when providers are implemented:
    # main()
    # switch_providers_example()
    # env_config_example()
    # context_manager_example()

