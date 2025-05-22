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
def discord_message(text):
    messages = []
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    id = os.getenv("DISCORD_CHANNEL")
    if DISCORD_TOKEN == None or id == None:
        messages.append("Token or channel ID missing! Add them via setup.py, or uncheck the discord input.")
        return messages
    CHANNEL_ID = int(id)


    class CustomClient(discord.Client):
        def __init__(self, messages, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.messages = messages

        async def on_ready(self):
            self.messages.append(f'Logged in as {self.user} (ID: {self.user.id})')
            channel = self.get_channel(CHANNEL_ID)

            if channel:
                await channel.send(content=text, suppress_embeds=True)
                self.messages.append("Message sent successfully.")
            else:
                self.messages.append("Channel not found.")
            await self.close()

    intents = discord.Intents.default()
    client = CustomClient(messages=messages, intents=intents)
    client.run(DISCORD_TOKEN)
    return messages
