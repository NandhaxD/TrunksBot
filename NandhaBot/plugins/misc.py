import config
import time
import io
import secureme


from NandhaBot.rank import (
RANK_A_USER as a,
RANK_B_USER as b,
RANK_C_USER as c )

from pyrogram import filters
from pyrogram.types import *
from NandhaBot import bot
from NandhaBot.helpers.tools import get_readable_time
from countryinfo import CountryInfo


COUNTRYINFO_TEXT = """ **Countryinfo:**

**capital**: {}
**currencies**: {}
**language**: {}
**borders**: {}
**alt_names**: {}

MADE BY [TRUNKS](tg://user?id={})
"""

@bot.on_message(filters.command("countryinfo",config.COMMANDS))
def countryinfo (_, message):
     if len(message.command) <2:
         return message.reply_text("Give County Name.")
     county_name = message.text.split(None, 1)[1]
     msg = message.reply_text("processing...")
     try:
       cuntry = CountryInfo(country_name)
     except Exception as e:
           msg.edit_text(str(e))
     else:
         country = CountryInfo(country_name)
         capital = county.captital()
         currencies = country.currencies()
         language = cuntry.language()
         borders = country.borders()
         alt_names = county.alt_spellings()
         user_id = bot.get_me().id
         msg.edit_text(COUNTRYINFO_TEXT.format(
          capital, currencies,language,borders,
           alt_names,user_id))

StartTime = time.time()

@bot.on_message(filters.command("ping",config.COMMANDS))
def ping(_, message):
   if message.from_user.id in a or b or c:
      start_time = time.time()
      end_time = time.time()
      ping_time = round((end_time - start_time) * 1000, 3)
      uptime = get_readable_time((time.time() - StartTime))
      msg = message.reply_text("processing...")
      msg.edit_text(f"**PONG**: `{ping_time}`\n**UPTIME**: `{uptime}`")
   else:
        message.reply_text("Only Rank User Can Acces")


@bot.on_message(filters.command("msginfo",config.COMMANDS))
def messageinfo(_, message):
     if message.reply_to_message:
        try:
          message.reply_text(message.reply_to_message)
        except Exception as e:
           with io.BytesIO(str.encode(str(message.reply_to_message))) as file:
               file.name = "msg.text"
               message.reply_document(
                document=file, caption=e)
     else:
        message.reply_text(message)

@bot.on_message(filters.command(["encode","encrypt"],config.COMMANDS))
def encrypted(_, message):
    reply = message.reply_to_message
    if not reply:
        return message.reply_text("`Reply to Message`")
    if reply:
         encrypt = secureme.encrypt(message.reply_to_message.text or message.reply_to_message.caption)
         message.reply_text(encrypt)

@bot.on_message(filters.command(["decode","decrypt"],config.COMMANDS))
def decrypted(_, message):
    reply = message.reply_to_message
    if not reply:
        return message.reply_text("`Reply to Message`")
    if reply:
         decrypt = secureme.decrypt(message.reply_to_message.text or message.reply_to_message.caption)
         message.reply_text(decrypt)


