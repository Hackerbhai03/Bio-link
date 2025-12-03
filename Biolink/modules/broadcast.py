#𝐀𝐚𝐬𝐡𝐢𝐤 𝐓ᴇᴀᴍ
import asyncio
from config import OWNER_ID
from pyrogram import *
from pyrogram.types import *
from Biolink import Biolink as app
from Biolink.helper.database import get_users, get_chats

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


@app.on_message(filters.command("bcast") & filters.user(OWNER_ID))
async def broadcast(_, message):
    if not message.reply_to_message:
        await message.reply_text("✦ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ɪᴛ.")
        return    
    exmsg = await message.reply_text("✦ sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ !")
    all_chats = (await get_chats()) or {}
    all_users = (await get_users()) or {}
    done_chats = 0
    done_users = 0
    failed_chats = 0
    failed_users = 0
    for chat in all_chats:
        try:
            await send_msg(chat, message.reply_to_message)
            done_chats += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
            failed_chats += 1

    for user in all_users:
        try:
            await send_msg(user, message.reply_to_message)
            done_users += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
            failed_users += 1
    if failed_users == 0 and failed_chats == 0:
        await exmsg.edit_text(
            f"**✦ sᴜᴄᴄᴇssғᴜʟʟʏ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ♥︎**\n\n❅ **ᴄʜᴀᴛs** ➠ `{done_chats}`\n❅ **ᴜsᴇʀs** ➠ `{done_users}` ",
        )
    else:
        await exmsg.edit_text(
            f"**✦ sᴜᴄᴄᴇssғᴜʟʟʏ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ♥︎**\n\n❅ **ᴄʜᴀᴛs** ➠ `{done_chats}` \n❅ **ᴜsᴇʀs** ➠ `{done_users}` \n\n**✦ ɴᴏᴛᴇ ➥ ** `ᴅᴜᴇ ᴛᴏ sᴏᴍᴇ ɪssᴜᴇ ᴄᴀɴ'ᴛ ᴀʙʟᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ`\n\n❅ **ғᴀɪʟᴅ ᴜsᴇʀs** ➠ `{failed_users}`\n❅ **ғᴀɪʟᴅ ᴄʜᴀᴛs** ➠ `{failed_chats}` ",
        )





@app.on_message(filters.command("announce") & filters.user(OWNER_ID))
async def announced(_, message):
    if message.reply_to_message:
      to_send=message.reply_to_message.id
    if not message.reply_to_message:
      return await message.reply_text("✦ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ ғᴏʀ ᴀɴɴᴏᴜɴᴄᴇ.")
    chats = await get_chats() or []
    users = await get_users() or []
    print(chats)
    print(users)
    failed = 0
    for chat in chats:
      try:
        await Nexus.forward_messages(chat_id=int(chat), from_chat_id=message.chat.id, message_ids=to_send)
        await asyncio.sleep(1)
      except Exception:
        failed += 1
    
    failed_user = 0
    for user in users:
      try:
        await Nexus.forward_messages(chat_id=int(user), from_chat_id=message.chat.id, message_ids=to_send)
        await asyncio.sleep(1)
      except Exception as e:
        failed_user += 1


    await message.reply_text("✦ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ {} ɢʀᴏᴜᴘs ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇ, ᴘʀᴏʙᴀʙʟʏ ᴅᴜᴇ ᴛᴏ ʙᴇɪɴɢ ᴋɪᴄᴋᴇᴅ.\n\n✦  {} ᴜsᴇʀs ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇ, ᴘʀᴏʙᴀʙʟʏ ᴅᴜᴇ ᴛᴏ ʙᴇɪɴɢ ʙᴀɴɴᴇᴅ.".format(failed, failed_user))
      
