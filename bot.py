
from pyrogram import Client, filters
from pymongo import MongoClient
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["telegram_bot"]
users_collection = db["users"]

@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    users_collection.update_one({"_id": user_id}, {"$set": {"name": message.from_user.first_name}}, upsert=True)
    message.reply_text(f"Hello {message.from_user.first_name}! Your data has been saved to MongoDB.")

app.run()
