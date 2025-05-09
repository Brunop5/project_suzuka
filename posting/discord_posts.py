import discord
import asyncio
import os


# test
class Test_discord(discord.Client):
    def __init__(self, messages, channel_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        self.messages = messages

    async def on_ready(self):
        self.messages.append(f'Logged in as {self.user} (ID: {self.user.id})')
        channel = self.get_channel(self.channel_id)

        if channel:
            self.messages.append("Connected to channel successfully.")
        else:
            self.messages.append("Channel not found.")
        await self.close()

# real
def discord_message(message):
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL"))


    class CustomClient(discord.Client):
        async def on_ready(self):
            print(f'Logged in as {self.user} (ID: {self.user.id})')
            channel = self.get_channel(CHANNEL_ID)

            if channel:
                await channel.send(content=message)
                print("Message sent successfully.")
            else:
                print("Channel not found.")
            await self.close()

    intents = discord.Intents.default()
    client = CustomClient(intents=intents)
    client.run(DISCORD_TOKEN)
