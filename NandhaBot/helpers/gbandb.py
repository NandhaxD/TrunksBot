import config

from NandhaBot import mongodb
collection = mongodb["GBAN"]

from NandhaBot import bot

async def gban_user(chat):
    doc = {"_id": "Gban", "users": [chat]}
    r = await collection.find_one({"_id": "Gban"})
    if r:
        await collection.update_one({"_id": "Gban"}, {"$push": {"users": chat}})
    else:
        await collection.insert_one(doc)

async def get_gbaned_users():
    results = await collection.find_one({"_id": "Gban"})
    if results:
        return results["users"]
    else:
        return []

async def ungban_user(chat):
    await collection.update_one({"_id": "Gban"}, {"$pull": {"users": chat}})

@bot.on_message(filters.groups)
def gbans(_, message):
   chat = message.chat
   chat_id = message.chat.id
   if message.from_user.id in (await get_gbaned_users()):
       chat.ban_member(message.from_user.id)
       bot.send_message(config.GROUP_ID, f"gbanned user {} banned from {}".format(message.from_user.first_name, message.chat.title))
