import asyncio

from cleantext import clean
from rich.console import Console
from rich.layout import Layout
from rich.prompt import Prompt
from rich.table import Table

from telegram_client.utils import get_user_dialogs, client, get_last_messages_from_dialog, \
    get_last_messages_from_channel, get_user_channels

console = Console()
layout = Layout(name='main')
client.start()


async def main():
    while True:
        choice = Prompt.ask('Do you want to get groups or channels', choices=['groups', 'channels', 'exit'],
                            show_choices=True).lower()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", justify="center", width=10)
        table.add_column("Title", justify="center", width=20)
        table.add_column("Members count", justify="center", width=20)
        table.add_column("Unread count", justify="center", width=20)
        table.width = 150

        if choice == 'groups':
            dialogs = await get_user_dialogs(client)
            for id in range(1, len(dialogs)):
                table.add_row(str(id), str(clean(dialogs[id]['title'], no_emoji=True, to_ascii=False)),
                              str(dialogs[id]['members_count']),
                              str(dialogs[id]['unread_count']))
            console.print(table)
            while True:
                try:
                    dialog_id = Prompt.ask('Enter dialog id to see its history (type exit to exit)',
                                       choices=[str(i) for i in range(1, len(dialogs) - 1)].append('exit'), show_choices=True)
                    if dialog_id == 'exit':
                        console.print('Farewell')
                        exit(1)
                    int(dialog_id)
                    break
                except Exception:
                    console.print('try again')
            history = await get_last_messages_from_dialog(client, dialogs[int(dialog_id)]['unread_count'],
                                                          dialogs[int(dialog_id)]['chat_id'])

            await render_chat_history(history)
        elif choice == 'channels':
            channels = await get_user_channels(client)
            for id in range(1, len(channels)):
                table.add_row(str(id), str(clean(channels[id]['title'], no_emoji=True, to_ascii=False)),
                              str(channels[id]['members_count']),
                              str(channels[id]['unread_count']))
            console.print(table)
            while True:
                try:
                    channel_id = Prompt.ask('Enter channel id to see its history (type exit to exit)')
                    if channel_id == 'exit':
                        console.print('Farewell')
                        exit(1)
                    int(channel_id)
                    break
                except Exception:
                    console.print('try again')

            history = await get_last_messages_from_channel(client, channels[int(channel_id)]['unread_count'],
                                                           channels[int(channel_id)]['chat_id'])

            await render_channel_history(history)
        else:
            console.print('Farewell')
            exit(1)
        console.print('\n\n\n')
        summary = Prompt.ask('Want to get dialog summary?', choices=['y', 'n'], show_choices=True)
        if summary == 'y':
            console.print('nice')
            # make_summary(history)


async def render_chat_history(history):
    for message in history:
        console.print(f'{history[message]['from']}: {history[message]['text']} ({history[message]['sent_at']})')


async def render_channel_history(history):
    for message in history:
        console.print(f'{history[message]['from']}: {history[message]['message']} ({history[message]['sent_at']})')


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
