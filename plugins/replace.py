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
        chid = int("-100" + parts[-2])
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

    # Get the replacement content
    replacement_message = message.reply_to_message
    
    try:
        # Check what type of content we're replacing with
        if replacement_message.media:
            # Replacing with media
            if replacement_message.photo:
                new_media = InputMediaPhoto(
                    replacement_message.photo.file_id, 
                    caption=replacement_message.caption or "",
                    caption_entities=replacement_message.caption_entities or []
                )
            elif replacement_message.document:
                new_media = InputMediaDocument(
                    replacement_message.document.file_id, 
                    caption=replacement_message.caption or "",
                    caption_entities=replacement_message.caption_entities or []
                )
            elif replacement_message.video:
                new_media = InputMediaVideo(
                    replacement_message.video.file_id, 
                    caption=replacement_message.caption or "",
                    caption_entities=replacement_message.caption_entities or []
                )
            elif replacement_message.animation:
                new_media = InputMediaAnimation(
                    replacement_message.animation.file_id, 
                    caption=replacement_message.caption or "",
                    caption_entities=replacement_message.caption_entities or []
                )
            elif replacement_message.audio:
                new_media = InputMediaAudio(
                    replacement_message.audio.file_id, 
                    caption=replacement_message.caption or "",
                    caption_entities=replacement_message.caption_entities or []
                )
            elif replacement_message.voice:
                # For voice messages, we need to handle them differently
                # Voice messages cannot be used with edit_message_media, so we'll copy the message
                await client.copy_message(
                    chat_id=chid,
                    from_chat_id=message.chat.id,
                    message_id=replacement_message.id
                )
                # Delete the original message
                await client.delete_messages(chat_id=chid, message_ids=msg_id)
                await message.reply_text("✅ Hᴜʀʀᴀʏ Vᴏɪᴄᴇ Mᴇssᴀɢᴇ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
                return
            elif replacement_message.video_note:
                # For video notes, similar handling as voice
                await client.copy_message(
                    chat_id=chid,
                    from_chat_id=message.chat.id,
                    message_id=replacement_message.id
                )
                await client.delete_messages(chat_id=chid, message_ids=msg_id)
                await message.reply_text("✅ Hᴜʀʀᴀʏ Vɪᴅᴇᴏ Nᴏᴛᴇ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
                return
            elif replacement_message.sticker:
                # For stickers, copy and delete original
                await client.copy_message(
                    chat_id=chid,
                    from_chat_id=message.chat.id,
                    message_id=replacement_message.id
                )
                await client.delete_messages(chat_id=chid, message_ids=msg_id)
                await message.reply_text("✅ Hᴜʀʀᴀʏ Sᴛɪᴄᴋᴇʀ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
                return
            else:
                await message.reply_text("❌ Unsupported media type.", quote=True)
                return

            # Replace the message with media
            await client.edit_message_media(
                chat_id=chid,
                message_id=msg_id,
                media=new_media
            )
            await message.reply_text("✅ Hᴜʀʀᴀʏ Mᴇᴅɪᴀ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
            
        elif replacement_message.text:
            # Replacing with text (including formatted text)
            await client.edit_message_text(
                chat_id=chid,
                message_id=msg_id,
                text=replacement_message.text,
                entities=replacement_message.entities or [],
                disable_web_page_preview=True
            )
            await message.reply_text("✅ Hᴜʀʀᴀʏ Tᴇxᴛ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
            
        else:
            # If it's neither media nor text, try to copy the entire message
            await client.copy_message(
                chat_id=chid,
                from_chat_id=message.chat.id,
                message_id=replacement_message.id
            )
            # Delete the original message
            await client.delete_messages(chat_id=chid, message_ids=msg_id)
            await message.reply_text("✅ Hᴜʀʀᴀʏ Mᴇssᴀɢᴇ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
            
    except Exception as e:
        # If direct editing fails, try the copy-delete approach
        try:
            await client.copy_message(
                chat_id=chid,
                from_chat_id=message.chat.id,
                message_id=replacement_message.id
            )
            await client.delete_messages(chat_id=chid, message_ids=msg_id)
            await message.reply_text("✅ Hᴜʀʀᴀʏ Cᴏɴᴛᴇɴᴛ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
        except Exception as e2:
            await message.reply_text(f"❌ Error: {e2}", quote=True)
