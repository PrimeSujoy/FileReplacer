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
