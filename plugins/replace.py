from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InputMediaPhoto, InputMediaDocument, InputMediaVideo, InputMediaAnimation, InputMediaAudio

@Client.on_message(filters.command('replace') & filters.private)
async def replace(client, message):
    # Check if the command is used in reply to a message
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("❌ Reply to a message with new file using /replace", quote=True)
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
        await message.reply_text("❌ You must be an admin in that channel to replace media.", quote=True)
        return

    if is_admin.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        await message.reply_text("❌ You must be an admin in that channel to replace media.", quote=True)
        return

    # Prepare the media to replace
    media = message.reply_to_message
    if media.photo:
        new_media = InputMediaPhoto(media.photo.file_id, caption=media.caption or "")
    elif media.document:
        new_media = InputMediaDocument(media.document.file_id, caption=media.caption or "")
    elif media.video:
        new_media = InputMediaVideo(media.video.file_id, caption=media.caption or "")
    elif media.animation:
        new_media = InputMediaAnimation(media.animation.file_id, caption=media.caption or "")
    elif media.audio:
        new_media = InputMediaAudio(media.audio.file_id, caption=media.caption or "")
    else:
        await message.reply_text("❌ Unsupported media type.", quote=True)
        return

    # Replace the message
    try:
        await client.edit_message_media(
            chat_id=chid,
            message_id=msg_id,
            media=new_media
        )
        await message.reply_text("✅ Hᴜʀʀᴀʏ Fɪʟᴇ Rᴇᴘʟᴀᴄᴇᴅ 🎉", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}", quote=True)
