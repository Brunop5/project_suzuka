#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import discord
from dotenv import load_dotenv
import os
import tkinter.messagebox as messagebox

from platforms.discord_posts import Test_discord
from platforms.reddit_post import test_reddit
from platforms.patreon_post import test_patreon_login

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

        self.keys["PATREON_MAIL"] = os.getenv("PATREON_MAIL")
        self.keys["PATREON_PSSWD"] = os.getenv("PATREON_PSSWD")

    def create_platform_frame(self, parent, platform_name):
        """Create a frame for each platform with its inputs and log area"""
        frame = ttk.LabelFrame(parent, text=platform_name)
        frame.pack(fill=tk.X, padx=5, pady=5)

        # Input fields container
        inputs_frame = ttk.Frame(frame)
        inputs_frame.pack(fill=tk.X, padx=5, pady=5)

        # Log area container
        log_frame = ttk.Frame(frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create text widget for logs with scrollbar
        log_text = tk.Text(log_frame, height=4, width=50)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=log_text.yview)
        log_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        return frame, inputs_frame, log_text

    def setup_ui(self):
        # --- window setup ---
        self.root.geometry("1200x700")
        self.root.minsize(500, 400)
        main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the main scrollable area
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # --- --- --- --- --- ---


        # Discord section
        self.discord_frame, discord_inputs, self.discord_log = self.create_platform_frame(scrollable_frame, "DISCORD")
        self.input_field(discord_inputs, "Bot token:", "DISCORD_TOKEN")
        self.input_field(discord_inputs, "Channel ID:", "DISCORD_CHANNEL")
        ttk.Button(discord_inputs, text="Test discord connection", 
                  command=lambda: self.test_dc(self.discord_log)).pack(pady=5)


        # Reddit section
        self.reddit_frame, reddit_inputs, self.reddit_log = self.create_platform_frame(scrollable_frame, "REDDIT")
        self.input_field(reddit_inputs, "Client ID:", "REDDIT_ID")
        self.input_field(reddit_inputs, "Secret:", "REDDIT_SECRET")
        self.input_field(reddit_inputs, "Username:", "REDDIT_USERNAME")
        self.input_field(reddit_inputs, "Password:", "REDDIT_PASSWORD")
        self.input_field(reddit_inputs, "Name of the subreddit:", "SUBREDDIT")
        ttk.Button(reddit_inputs, text="Test reddit connection", 
                  command=lambda: self.test_reddit(self.reddit_log)).pack(pady=5)


        # Patreon section
        self.patreon_frame, patreon_inputs, self.patreon_log = self.create_platform_frame(scrollable_frame, "PATREON")
        self.input_field(patreon_inputs, "Email:", "PATREON_MAIL")
        self.input_field(patreon_inputs, "Password:", "PATREON_PSSWD")
        ttk.Button(patreon_inputs, text="Test patreon connection", 
                  command=lambda: self.test_patreon(self.patreon_log)).pack(pady=5)


        # Bottom buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Done", command=self.done).pack(side=tk.LEFT, padx=5)

    def input_field(self, parent, label_text, variable_name):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame, text=label_text).pack(side=tk.LEFT)
        ttk.Label(frame, text=self.keys[variable_name]).pack(side=tk.LEFT, padx=5)
        input_field = ttk.Entry(frame, width=50)
        input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.inputs[variable_name] = input_field

    def clear_log(self, log_widget):
        log_widget.delete(1.0, tk.END)

    def log_message(self, log_widget, message):
        log_widget.insert(tk.END, f"{message}\n")
        log_widget.see(tk.END)

    def done(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def save_new_keys(self):
        for key,value in self.keys.items():
            self.keys[key] = self.inputs[key].get() or value

    def test_dc(self, log_widget):
        self.clear_log(log_widget)
        try:
            self.get_data()
            messages = []
            intents = discord.Intents.default()
            self.save_new_keys()

            client = Test_discord(messages=messages, 
                                channel_id=int(self.keys["DISCORD_CHANNEL"]), 
                                intents=intents)
            client.run(self.keys["DISCORD_TOKEN"])
            
            for m in messages:
                self.log_message(log_widget, m)
        except Exception as e:
            self.log_message(log_widget, f"Error: {str(e)}")

    def test_reddit(self, log_widget):
        self.clear_log(log_widget)
        self.get_data()
        self.save_new_keys()
        try:
            res = test_reddit(
                client_id=self.keys["REDDIT_ID"],
                secret=self.keys["REDDIT_SECRET"],
                subreddit_name=self.keys["SUBREDDIT"],
                username=self.keys["REDDIT_USERNAME"],
                password=self.keys["REDDIT_PASSWORD"]
            )
            self.log_message(log_widget, res)
        except Exception as e:
            self.log_message(log_widget, f"Error: {str(e)}")

    def test_patreon(self, log_widget):
        self.clear_log(log_widget)
        messages = []
        try:
            self.get_data()
            self.save_new_keys()

            test_patreon_login(self.keys["PATREON_MAIL"], self.keys["PATREON_PSSWD"], messages)
            self.log_message(log_widget, messages[0])
        except Exception as e:
            self.log_message(log_widget, f"Error: {str(e)}")

    def save(self):
        self.save_new_keys()
        with open('.env', 'w') as file:
            for key, value in self.keys.items():
                file.write(f"{key}={value}\n")
        messagebox.showinfo("Success", "Settings saved successfully!")

if __name__ == "__main__":
    load_dotenv();
    app = Setup_app()
    app.run()