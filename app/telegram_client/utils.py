from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(name=os.getenv('TELEGRAM_ID'), api_id=os.getenv('TELEGRAM_CLIENT_ID'),
                api_hash=os.getenv('TELEGRAM_CLIENT_HASH'), phone_number=os.getenv('TELEGRAM_NUMBER'))


def is_group(chat):
    return chat.type.name == 'GROUP'


def is_channel(chat):
    return chat.type.name == 'CHANNEL'


async def get_user_dialogs(client):
    result_dict = {}
    dialogs_list = []

    chat_count = 1
    async for i in client.get_dialogs():
        if i.chat.title is not None and is_group(i.chat):
            dialogs_list.append({
                'chat_id': i.chat.id,
                'title': i.chat.title,
                'members_count': i.chat.members_count,
                'unread_count': i.unread_messages_count,
            })
            chat_count += 1

    dialogs_list = sorted(
        dialogs_list,
        key=lambda x: (x['members_count'], x['unread_count']),
        reverse=True
    )

    for idx, dialog in enumerate(dialogs_list, start=1):
        result_dict[idx] = dialog

    return result_dict


async def get_user_channels(client):
    result_dict = {}
    dialogs_list = []

    chat_count = 1
    async for i in client.get_dialogs():
        if i.chat.title is not None and is_channel(i.chat):
            dialogs_list.append({
                'chat_id': i.chat.id,
                'title': i.chat.title,
                'members_count': i.chat.members_count,
                'unread_count': i.unread_messages_count,
            })
            chat_count += 1

    dialogs_list = sorted(
        dialogs_list,
        key=lambda x: (x['members_count'], x['unread_count']),
        reverse=True
    )

    for idx, dialog in enumerate(dialogs_list, start=1):
        result_dict[idx] = dialog

    return result_dict


async def get_last_messages_from_dialog(client: Client, unread_messages_count, chat):
    result_dict = {}

    async for message in client.get_chat_history(chat_id=chat, limit=unread_messages_count + 100):
        result_dict.update({
            message.id: {
                'from': message.from_user.username,
                'text': message.text if message.text else 'Document',
                'sent_at': message.date
            }
        })
    return result_dict


async def get_last_messages_from_channel(client: Client, unread_messages_count, chat):
    result_dict = {}

    async for message in client.get_chat_history(chat_id=chat, limit=unread_messages_count + 100):
        result_dict.update({
            message.id: {
                'from': message.sender_chat.username,
                'message': message.text or f'{message.media}: {message.caption}',
                'sent_at': message.date,
            }
        })
    return result_dict




