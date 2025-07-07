from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InputMediaPhoto, InputMediaDocument, InputMediaVideo, InputMediaAnimation, InputMediaAudio

@Client.on_message(filters.command('replace') & filters.private)
async def replace(client, message):
    # Check if the command is used in reply to a message
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message with new content using /replace", quote=True)
        return

    # Check if a link is provided with the command
    if len(message.command) < 2:
        await message.reply_text("❌ Missing URL. Example: /replace https://t.me/ChannelUsername/123", quote=True)
        return

    link = message.command[1]
    try:
        # Extract chat_id and message_id from the link
        parts = link.split('/')
        if 't.me' not in parts[-3]:
            raise ValueError("Invalid Telegram link")
        
        # Handle both channel username and chat ID formats
        if parts[-2].startswith('-100'):
            chid = int(parts[-2])
        else:
            # For channel username, we need to resolve it
            try:
                chat = await client.get_chat(parts[-2])
                chid = chat.id
            except Exception:
                chid = int("-100" + parts[-2]) if parts[-2].isdigit() else None
                if not chid:
                    raise ValueError("Could not resolve chat ID")
        
        msg_id = int(parts[-1])
    except (IndexError, ValueError):
        await message.reply_text("❌ Invalid URL format. Example: /replace https://t.me/ChannelUsername/123", quote=True)
        return

    # Check if the user is an admin in the channel
    try:
        is_admin = await client.get_chat_member(chat_id=chid, user_id=message.from_user.id)
    except UserNotParticipant:
        await message.reply_text("❌ You must be an admin in that channel to replace content.", quote=True)
        return

    if is_admin.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        await message.reply_text("❌ You must be an admin in that channel to replace content.", quote=True)
        return

    # Get the original message to check its type
    try:
        original_message = await client.get_messages(chat_id=chid, message_ids=msg_id)
    except Exception as e:
        await message.reply_text(f"❌ Could not fetch original message: {e}", quote=True)
        return

    reply_message = message.reply_to_message
    
    # Case 1: Replace media with media (original functionality)
    if reply_message.media and original_message.media:
        await replace_media_with_media(client, message, reply_message, chid, msg_id)
    
    # Case 2: Replace text with media
    elif reply_message.media and not original_message.media:
        await replace_text_with_media(client, message, reply_message, chid, msg_id)
    
    # Case 3: Replace media with text
    elif not reply_message.media and original_message.media:
        await replace_media_with_text(client, message, reply_message, chid, msg_id)
    
    # Case 4: Replace text with text (with formatting preservation)
    elif not reply_message.media and not original_message.media:
        await replace_text_with_text(client, message, reply_message, chid, msg_id)
    
    else:
        await message.reply_text("❌ Unsupported replacement type.", quote=True)


async def replace_media_with_media(client, message, reply_message, chid, msg_id):
    """Replace media with media (original functionality)"""
    media = reply_message
    
    # Get caption with entities (formatting)
    caption = media.caption or ""
    caption_entities = media.caption_entities or []
    
    if media.photo:
        new_media = InputMediaPhoto(media.photo.file_id, caption=caption, caption_entities=caption_entities)
    elif media.document:
        new_media = InputMediaDocument(media.document.file_id, caption=caption, caption_entities=caption_entities)
    elif media.video:
        new_media = InputMediaVideo(media.video.file_id, caption=caption, caption_entities=caption_entities)
    elif media.animation:
        new_media = InputMediaAnimation(media.animation.file_id, caption=caption, caption_entities=caption_entities)
    elif media.audio:
        new_media = InputMediaAudio(media.audio.file_id, caption=caption, caption_entities=caption_entities)
    else:
        await message.reply_text("❌ Unsupported media type.", quote=True)
        return

    try:
        await client.edit_message_media(
            chat_id=chid,
            message_id=msg_id,
            media=new_media
        )
        await message.reply_text("✅ Hᴜʀʀᴀʏ Mᴇᴅɪᴀ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error replacing media: {e}", quote=True)


async def replace_text_with_media(client, message, reply_message, chid, msg_id):
    """Replace text message with media"""
    media = reply_message
    
    # Get caption with entities (formatting)
    caption = media.caption or ""
    caption_entities = media.caption_entities or []
    
    if media.photo:
        new_media = InputMediaPhoto(media.photo.file_id, caption=caption, caption_entities=caption_entities)
    elif media.document:
        new_media = InputMediaDocument(media.document.file_id, caption=caption, caption_entities=caption_entities)
    elif media.video:
        new_media = InputMediaVideo(media.video.file_id, caption=caption, caption_entities=caption_entities)
    elif media.animation:
        new_media = InputMediaAnimation(media.animation.file_id, caption=caption, caption_entities=caption_entities)
    elif media.audio:
        new_media = InputMediaAudio(media.audio.file_id, caption=caption, caption_entities=caption_entities)
    else:
        await message.reply_text("❌ Unsupported media type.", quote=True)
        return

    try:
        await client.edit_message_media(
            chat_id=chid,
            message_id=msg_id,
            media=new_media
        )
        await message.reply_text("✅ Hᴜʀʀᴀʏ Tᴇxᴛ Rᴇᴘʟᴀᴄᴇᴅ Wɪᴛʜ Mᴇᴅɪᴀ 🎉", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error replacing text with media: {e}", quote=True)


async def replace_media_with_text(client, message, reply_message, chid, msg_id):
    """Replace media message with text"""
    try:
        # Get text with entities (formatting)
        text = reply_message.text or reply_message.caption or ""
        entities = reply_message.entities or reply_message.caption_entities or []
        
        await client.edit_message_text(
            chat_id=chid,
            message_id=msg_id,
            text=text,
            entities=entities
        )
        await message.reply_text("✅ Hᴜʀʀᴀʏ Mᴇᴅɪᴀ Rᴇᴘʟᴀᴄᴇᴅ Wɪᴛʜ Tᴇxᴛ 🎉", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error replacing media with text: {e}", quote=True)


async def replace_text_with_text(client, message, reply_message, chid, msg_id):
    """Replace text message with text (preserving formatting)"""
    try:
        # Get text with entities (formatting) - this preserves bold, italic, mono, spoiler, underline, blockquote
        text = reply_message.text or ""
        entities = reply_message.entities or []
        
        await client.edit_message_text(
            chat_id=chid,
            message_id=msg_id,
            text=text,
            entities=entities
        )
        await message.reply_text("✅ Hᴜʀʀᴀʏ Tᴇxᴛ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error replacing text: {e}", quote=True)


# Optional: Add a command to show formatting help
@Client.on_message(filters.command('format_help') & filters.private)
async def format_help(client, message):
    help_text = """
🎨 **Formatting Guide for /replace command:**

**Bold Text:** `**text**` or `__text__`
*Italic Text:* `*text*` or `_text_`
`Monospace:` \`text\`
~~Strikethrough:~~ `~~text~~`
__Underline:__ `++text++`
||Spoiler:|| `||text||`
> Blockquote: `> text`

**Examples:**
• `/replace https://t.me/channel/123` - Reply with media/text
• Media → Media: Replaces file with new file
• Text → Media: Converts text post to media post  
• Media → Text: Converts media post to text post
• Text → Text: Updates text while preserving formatting

**Note:** All formatting (bold, italic, spoiler, etc.) is automatically preserved when replacing content.
"""
    await message.reply_text(help_text, quote=True)


# Optional: Add a command to test formatting
@Client.on_message(filters.command('test_format') & filters.private)
async def test_format(client, message):
    test_text = """
🧪 **Formatting Test Message**

This is **bold text**
This is *italic text*
This is `monospace text`
This is ~~strikethrough text~~
This is __underlined text__
This is ||spoiler text||
> This is a blockquote

You can use this message to test the /replace command!
"""
    await message.reply_text(test_text, quote=True)
