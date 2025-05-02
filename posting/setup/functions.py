import tkinter as tk
from tkinter import messagebox
import subprocess
import discord


class Custom_dc_client(discord.Client):
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


class Setup_app:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Setup Window")
        self.setup_ui()

    def setup_ui(self):
        # for now just discord input and tests
        self.root.geometry("1000x700")
        self.root.minsize(500, 400)

        # discord
        tk.Label(self.root, text="Discord bot token:").pack()
        self.dc_token = tk.Entry(self.root, width=100)
        self.dc_token.pack()

        tk.Label(self.root, text="Discord channel ID:").pack()
        self.dc_channel_ID = tk.Entry(self.root, width=50)
        self.dc_channel_ID.pack()

        tk.Button(self.root, text="Test discord connection", command=self.test_dc).pack()
        tk.Button(self.root, text="Save", command=self.save_dc).pack()
        tk.Button(self.root, text="Done", command=self.done).pack()

    def done(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def test_dc(self):
        try:
            messages = []
            intents = discord.Intents.default()
            client = Custom_dc_client(messages=messages, channel_id=int(self.dc_channel_ID.get()), intents=intents)
            client.run(self.dc_token.get())
            for m in messages:
                tk.Label(self.root, text=m).pack()
        except discord.LoginFailure as e:

            tk.Label(self.root, text=e).pack()

    def save_dc(self):
        res = subprocess.run(["./posting/setup/keys_input", f"DISCORD_TOKEN={self.dc_token.get()}", f"DISCORD_CHANNEL={self.dc_channel_ID.get()}"], capture_output=True, text=True)
        tk.Label(self.root, text=res.stdout).pack()


app = Setup_app()
app.run()