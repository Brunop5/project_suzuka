import discord
import asyncio
import os

def discord_message(message):
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL"))


    class CustomClient(discord.Client):
        async def on_ready(self):
            print(f'Logged in as {self.user} (ID: {self.user.id})')
            channel = self.get_channel(CHANNEL_ID)

            if channel:
                await channel.send(message)
                print("Message sent successfully.")
            else:
                print("Channel not found.")
            await self.close()

    intents = discord.Intents.default()
    client = CustomClient(intents=intents)
    client.run(DISCORD_TOKEN)
