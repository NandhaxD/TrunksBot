import config
import strings

from pyrogram import Client, filters
from pyrogram.types import (
InlineKeyboardMarkup,
InlineKeyboardButton,
CallbackQuery,
ChatPermissions
)

from NandhaBot.helpers.groupsdb import (
add_chats, get_chats, is_chats)

from NandhaBot import bot

@bot.on_message(filters.new_chat_members)
async def res(client, message):
     for member in message.new_chat_members:
        is_bot = member.is_bot
        if (await is_chats(message.chat.id)) == False:
               await add_chats(message.chat.id)
               chats_count = len(await get_chats())
               await bot.send_message(config.GROUP_ID, text=strings.NEW_CHATS.format(message.chat.id, message.chat.title, chats_count))
        if is_bot == True:
             try:
                await bot.restrict_chat_member(message.chat.id, member.id, ChatPermissions(can_send_messages=False))
                key = InlineKeyboardMarkup([[InlineKeyboardButton("BAN", callback_data=f"botban:{member.id}"),
                   InlineKeyboardButton("UNMUTE", callback_data=f"botunm:{member.id}"),]])
                await message.reply_text("BOT ARRIVED ON CHAT",reply_markup=key)
             except Exception as e:
                    await message.reply_text(str(e))
        elif is_bot == False:
               try:
                   await bot.restrict_chat_member(message.chat.id, member.id, ChatPermissions(can_send_messages=False))
                   key = InlineKeyboardMarkup([[InlineKeyboardButton("I'm a human", callback_data=f"unres:{member.id}")]])
                   await message.reply(f"Hello ( {member.mention} ) You are restricted to make sure you are not a robot", reply_markup=key)
               except Exception as e:
                   await message.reply_text(str(e))


@bot.on_callback_query(filters.regex("botban"))
async def botban(_, query):
     chat = query.message.chat
     bot_id = int(query.data.split(":")[1])
     admin_check = await bot.get_chat_member(query.message.chat.id, query.from_user.id)
     try:
       if admin_check.privileges.can_restrict_members:
           await chat.ban_member(bot_id)
           await query.message.edit("BOT WAS REMOVED BY ADMINS!")
     except Exception as e:
         await message.reply_text(str(e))

@bot.on_callback_query(filters.regex("botunm"))
async def botum(_, query):
     chat = query.message.chat
     bot_id = int(query.data.split(":")[1])
     admin_check = await bot.get_chat_member(query.message.chat.id, query.from_user.id)
     try:
       if admin_check.privileges.can_restrict_members:
           await bot.restrict_chat_member(query.message.chat.id, bot_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
           await query.message.edit("BOT UNMUTED BY ADMINS!")
     except Exception as e:
         await query.message.reply_text(str(e))

@bot.on_callback_query(filters.regex("unres"))
async def unres(_, query):
   user_id = int(query.data.split(":")[1])
   if not query.from_user.id == user_id:
     await query.answer("This message is not for you!", show_alert=True)
   else:
     try:
       name = (await bot.get_users(user_id)).first_name
       await query.edit_message_text(f"Verified successfully {name} can chat in the group now!")
       await bot.restrict_chat_member(query.message.chat.id, user_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
     except Exception as e:
          await query.message.edit_message_text(str(e))
