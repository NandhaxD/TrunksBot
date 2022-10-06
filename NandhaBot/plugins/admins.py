import config

from pyrogram import enums
from pyrogram.enums import ChatType
from pyrogram import filters
from NandhaBot import bot




@bot.on_message(filters.command(["admins","adminlist"],config.COMMANDS))
async def admins(_, message):
      chat_id = message.chat.id
      admin_list = f"𝗔𝗗𝗠𝗜𝗡𝗦 in {message.chat.title}\n\n"
      bot_list = "\n𝗕𝗢𝗧𝗦:\n"

      if message.chat.type == ChatType.PRIVATE:
           await message.reply_text("This command work on group only!")
      else:
        async for admin in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
               
               if admin.user.is_bot:
                   bot_list += f"⊗ {admin.user.mention}\n"
               else:
                  admin_list += f"✮ {admin.user.mention}\n"
        await message.reply_text(admin_list+bot_list)


@bot.on_message(filters.command(["removephoto","deletephoto",]))
async def deletechatphoto(_, message):
      
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("processing....")
      admin_check = await bot.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("`This command work on groups!`") 
      try:
         if admin_check.privileges.can_change_info:
             await bot.delete_chat_photo(chat_id)
             await msg.edit("Successfully Removed Profile Photo from group!\nby {}".format(message.from_user.mention))    
      except:
          await msg.edit("`the user most need change info admin rights to remove group photo!`")





@bot.on_message(filters.command("setphoto"))
async def setchatphoto(_, message):
      reply = message.reply_to_message
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("processing....")
      admin_check = await bot.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("`This command work on groups!`") 
      elif not reply:
           await msg.edit("`reply to a photo or document.`")
      elif reply:
          try:
             if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit_text("Successfully New Profile Photo insert!\nby {}".format(message.from_user.mention))
             else:
                await msg.edit("`somthing wrong happened try Another photo!`")
     
          except:
              await msg.edit("`the user most need change info admin rights to change group photo!`")






                

