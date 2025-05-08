import tkinter as tk
import subprocess
import discord
from dotenv import load_dotenv
import os


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
        self.keys = {}
        self.inputs = {}
        self.get_data()
        self.setup_ui()

    def get_data(self):
        self.keys["DISCORD_TOKEN"] = os.getenv("DISCORD_TOKEN")
        self.keys["DISCORD_CHANNEL"] = os.getenv("DISCORD_CHANNEL")

    def input_field(self, label_text, variable_name):
        tk.Label(self.root, text=label_text).pack()
        tk.Label(self.root, text=self.keys[variable_name]).pack()
        input_field = tk.Entry(self.root, width=100)
        input_field.pack()
        self.inputs[variable_name] = input_field

    def setup_ui(self):
        # for now just discord input and tests
        self.root.geometry("1000x700")
        self.root.minsize(500, 400)

        # discord
        self.input_field("Discord bot token:", "DISCORD_TOKEN")
        self.input_field("Discord channel ID:", "DISCORD_CHANNEL")

        tk.Button(self.root, text="Test discord connection", command=self.test_dc).pack()
        tk.Button(self.root, text="Save", command=self.save).pack()
        tk.Button(self.root, text="Done", command=self.done).pack()


    def done(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


    def save_new_keys(self):
        for key,value in self.keys.items():
            self.keys[key] = self.inputs[key].get() or value


    def test_dc(self):
        try:
            messages = []
            intents = discord.Intents.default()

            self.save_new_keys()

            client = Custom_dc_client(messages=messages, channel_id=int(self.keys["DISCORD_CHANNEL"]), intents=intents)
            client.run(self.keys["DISCORD_TOKEN"])
            for m in messages:
                tk.Label(self.root, text=m).pack()
        except Exception as e:
            tk.Label(self.root, text=e).pack()

    def save(self):
        self.save_new_keys()
        with open('.env', 'w') as file:
            for key, value in self.keys.items():
                file.write(f"{key}={value}\n")
        tk.Label(self.root, text="SAVED SUCCESSFULLY").pack()


if __name__ == "__main__":
    load_dotenv();
    app = Setup_app()
    app.run()