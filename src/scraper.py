import os
import sys
import json
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.discover_channels import get_discovered_channels


load_dotenv()
API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')

class Solution:
    def __init__(self):
        self.client = TelegramClient('scraping_session', API_ID, API_HASH)
        # We start with your specific required channels
        self.target_channels = ['CheMed123', 'tikvahpharma', 'lobelia4cosmetics']

    async def scrape_channel(self, channel_username):
        print(f"--- Scraping: {channel_username} ---")
        messages_data = []
        
        try:
            image_dir = f"data/raw/images/{channel_username}"
            os.makedirs(image_dir, exist_ok=True)

            async for message in self.client.iter_messages(channel_username, limit=100):
                data = {
                    "message_id": message.id,
                    "channel_name": channel_username,
                    "message_date": str(message.date),
                    "message_text": message.text or "",
                    "has_media": message.media is not None,
                    "views": message.views or 0,
                    "forwards": message.forwards or 0,
                    "image_path": None
                }

                if message.photo:
                    file_path = f"{image_dir}/{message.id}.jpg"
                    await self.client.download_media(message.photo, file=file_path)
                    data["image_path"] = file_path
                
                messages_data.append(data)
            today_str = datetime.now().strftime("%Y-%m-%d")
            json_dir = f"data/raw/telegram_messages/{today_str}"
            os.makedirs(json_dir, exist_ok=True)
            
            with open(f"{json_dir}/{channel_username}.json", 'w', encoding='utf-8') as f:
                json.dump(messages_data, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Saved {len(messages_data)} records for {channel_username}")

        except Exception as e:
            print(f"❌ Error on {channel_username}: {e}")

    async def run(self):
        await self.client.start()
        
        # 1. Discover more channels
        discovered = await get_discovered_channels(self.client)
        
        # 2. Combine required + discovered (use set to avoid duplicates)
        all_channels = list(set(self.target_channels + discovered))
        print(f"Total unique channels to scrape: {len(all_channels)}")

        # 3. Scrape them all
        for channel in all_channels:
            await self.scrape_channel(channel)

if __name__ == '__main__':
    sol = Solution()
    with sol.client:
        sol.client.loop.run_until_complete(sol.run())