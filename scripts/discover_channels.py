import os
from telethon import TelegramClient, functions, types
from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')

async def get_discovered_channels(client):
    """
    Pass the existing client to this function to find channels.
    """
    keywords = ['medicine', 'pharmacy', 'health', 'ethiopia medical']
    found_channels = set()

    for query in keywords:
        result = await client(functions.contacts.SearchRequest(q=query, limit=20))
        for chat in result.chats:
            if hasattr(chat, 'username') and chat.username:
                if isinstance(chat, types.Channel) and chat.broadcast:
                    found_channels.add(chat.username)
    
    return list(found_channels)