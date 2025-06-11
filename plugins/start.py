from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_MSG = """**Hᴇʏ {}, Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ Fɪʟᴇ Rᴇᴘʟᴀᴄᴇ Bᴏᴛ!**

Yᴏᴜ ᴄᴀɴ ᴇᴀsɪʟʏ ʀᴇᴘʟᴀᴄᴇ ᴍᴇssᴀɢᴇs ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴡɪᴛʜ ɴᴇᴡ ғɪʟᴇs & ᴄᴀᴘᴛɪᴏɴs!

Hᴏᴡ ᴛᴏ ᴜsᴇ: 

1. Reply to a file with /replace command

2. Use /replace {Link To Replace}.

✨ Powered by @SuperToppers"""

HELP_MSG = """
**Follow these steps**

1. Reply to a file with /replace command.

2. Use /replace {Link To Replace}.

**<u>Note</u>:- Both you & the bot must be an admin in the target channel.**"""

@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    await message.reply_text(
        text=START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('❣️ ᴅᴇᴠᴇʟᴏᴘᴇʀ ❣️', url='https://t.me/UncleChipssBot')],
            [
                InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/SuperToppers0'),
                InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ɢʀᴏᴜᴘ', url='https://t.me/SuperToppers')
            ],
            [InlineKeyboardButton('💝 sᴜʙsᴄʀɪʙᴇ ᴍʏ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ', url='https://youtube.com/@SuperToppers')]
        ]),
        quote=True
    )

@Client.on_message(filters.command('help') & filters.private)
async def help(client, message):
    await message.reply_text(
        text=HELP_MSG,
        quote=True
    )
