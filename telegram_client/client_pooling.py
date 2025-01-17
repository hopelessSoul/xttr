from pyrogram import Client
import dotenv
import os

dotenv.load_dotenv()

client = Client(name=os.getenv('TELEGRAM_ID'), api_id=os.getenv('TELEGRAM_CLIENT_ID'),
                api_hash=os.getenv('TELEGRAM_CLIENT_HASH'), phone_number=os.getenv('TELEGRAM_NUMBER'))


def pool_client(client):
    client.start()
