from client_pooling import pool_client, client
import asyncio
pool_client(client)


def is_group(chat):
    return chat.type.name == 'GROUP' or chat.type.name == 'SUPERGROUP'


async def get_user_dialogs():
    result_dict = {}
    async for i in client.get_dialogs():
        if i.chat.title is not None and is_group(i.chat):
            result_dict.update({
                i.chat.title: {
                    'members_count': i.chat.members_count,
                    'unread_count': i.unread_messages_count,
                }
            })
    return result_dict


