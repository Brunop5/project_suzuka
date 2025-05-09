import tkinter as tk
import discord
from dotenv import load_dotenv
import os

from discord_posts import Test_discord
from reddit_post import test_reddit

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

        self.keys["REDDIT_ID"] = os.getenv("REDDIT_ID")
        self.keys["REDDIT_SECRET"] = os.getenv("REDDIT_SECRET")
        self.keys["REDDIT_USERNAME"] = os.getenv("REDDIT_USERNAME")
        self.keys["REDDIT_PASSWORD"] = os.getenv("REDDIT_PASSWORD")
        self.keys["SUBREDDIT"] = os.getenv("SUBREDDIT")



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

        tk.Button(self.root, text="Reset_Keys", command=self.get_data).pack()

        # discord
        tk.Label(self.root, text="DISCORD")
        self.input_field("Bot token:", "DISCORD_TOKEN")
        self.input_field("Channel ID:", "DISCORD_CHANNEL")
        tk.Button(self.root, text="Test discord connection", command=self.test_dc).pack()

        # reddit
        tk.Label(self.root, text="REDDIT")
        self.input_field("Client ID:", "REDDIT_ID")
        self.input_field("Secret:", "REDDIT_SECRET")
        self.input_field("Username:", "REDDIT_USERNAME")
        self.input_field("Password:", "REDDIT_PASSWORD")
        self.input_field("Name of the subreddit:", "SUBREDDIT")
        tk.Button(self.root, text="Test reddit connection", command=self.test_reddit).pack()

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

            client = Test_discord(messages=messages, channel_id=int(self.keys["DISCORD_CHANNEL"]), intents=intents)
            client.run(self.keys["DISCORD_TOKEN"])
            for m in messages:
                tk.Label(self.root, text=m).pack()
        except Exception as e:
            tk.Label(self.root, text=e).pack()

    def test_reddit(self):
        self.save_new_keys()
        print(self.keys["REDDIT_ID"])
        res = test_reddit(client_id=self.keys["REDDIT_ID"], secret=self.keys["REDDIT_SECRET"], subreddit_name=self.keys["SUBREDDIT"],
                        username=self.keys["REDDIT_USERNAME"], password=self.keys["REDDIT_PASSWORD"])
        tk.Label(self.root, text=res).pack()



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