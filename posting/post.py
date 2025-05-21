#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from platforms.reddit_post import post_on_reddit
from platforms.discord_posts import discord_message
import os
from dotenv import load_dotenv
from text_work import convert_premium_to_short

class PostApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Post Creator")
        self.setup_ui()

    def setup_ui(self):
        # Window setup
        self.root.geometry("800x600")
        self.root.minsize(400, 300)

        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Heading input
        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(heading_frame, text="Heading:").pack(side=tk.LEFT)
        self.heading_input = ttk.Entry(heading_frame, width=50)
        self.heading_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Content input (big text area with scrollbar)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(content_frame, text="Content:").pack(anchor=tk.W)
        
        # Create a frame for the text widget and scrollbar
        text_frame = ttk.Frame(content_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget with scrollbar
        self.content_input = tk.Text(text_frame, height=10, width=50, 
                                   yscrollcommand=scrollbar.set)
        self.content_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.content_input.yview)

        platform_frame = ttk.Frame(main_frame)
        platform_frame.pack(fill=tk.X, pady=(0, 10))
        

        # Discord section
        discord_frame = ttk.Frame(platform_frame)
        discord_frame.pack(side=tk.LEFT, padx=(0, 30))
        
        self.discord_var = tk.BooleanVar()
        self.discord_short_var = tk.BooleanVar()
        
        ttk.Checkbutton(discord_frame, text="Discord", 
                        variable=self.discord_var).pack(side=tk.LEFT)
        ttk.Checkbutton(discord_frame, text="Shortened", 
                        variable=self.discord_short_var).pack(side=tk.LEFT, padx=(5, 0))


        # Reddit section
        reddit_frame = ttk.Frame(platform_frame)
        reddit_frame.pack(side=tk.LEFT, padx=(0, 30))
        
        self.reddit_var = tk.BooleanVar()
        self.reddit_short_var = tk.BooleanVar()
        
        ttk.Checkbutton(reddit_frame, text="Reddit", 
                        variable=self.reddit_var).pack(side=tk.LEFT)
        ttk.Checkbutton(reddit_frame, text="Shortened", 
                        variable=self.reddit_short_var).pack(side=tk.LEFT, padx=(5, 0))


        # Patreon section
        patreon_frame = ttk.Frame(platform_frame)
        patreon_frame.pack(side=tk.LEFT, padx=(0, 30))
        
        self.patreon_var = tk.BooleanVar()
        self.patreon_short_var = tk.BooleanVar()

        ttk.Checkbutton(patreon_frame, text="Patreon", 
                        variable=self.patreon_var).pack(side=tk.LEFT)
        ttk.Checkbutton(patreon_frame, text="Shortened", 
                        variable=self.patreon_short_var).pack(side=tk.LEFT, padx=(5, 0))


        # Add log area at the bottom
        log_frame = ttk.LabelFrame(main_frame, text="Logs")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create scrollbar for logs
        log_scrollbar = ttk.Scrollbar(log_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget for logs
        self.log_output = tk.Text(log_frame, height=6, width=50,
                                 yscrollcommand=log_scrollbar.set)
        self.log_output.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        log_scrollbar.config(command=self.log_output.yview)

        # Post button
        ttk.Button(main_frame, text="Post", 
                  command=self.post).pack(pady=(10, 0))

    def log_message(self, message):
        self.log_output.config(state="normal")
        self.log_output.insert(tk.END, f"{message}\n")
        self.log_output.see(tk.END)  # Auto-scroll to bottom
        self.log_output.config(state="disabled")

    def clear_logs(self):
        self.log_output.config(state="normal")
        self.log_output.delete(1.0, tk.END)
        self.log_output.config(state="disabled")

    def post(self):
        heading = self.heading_input.get()
        text = self.content_input.get("1.0", tk.END)
        
        self.clear_logs()  # Clear previous logs
        vars = [self.reddit_var.get(), self.discord_var.get(), self.patreon_var.get()]
        
        for index, var in enumerate(vars):
            if var:
                msg = convert_premium_to_short(text) if self.reddit_short_var.get() else text
                if msg == "":
                    res = "\n    Message couldn't be converted into short form, so it wasnt sent.\n    Compare the text format with the one in posting/tutorials/sample_long.txt, or send it in long(unedited) form."
                else:
                    if index == 0: # reddit
                        args = [heading, msg]
                        res = post_on_reddit(
                            os.getenv("REDDIT_ID"),
                            os.getenv("REDDIT_SECRET"),
                            os.getenv("SUBREDDIT"),
                            os.getenv("REDDIT_USERNAME"),
                            os.getenv("REDDIT_PASSWORD"),
                            args
                        )
                        self.log_message(f"Reddit Response: {res}")

                    elif index == 1: # discord
                        discord_text = heading + "\n\n" + msg

                        messages = discord_message(discord_text)
                        self.log_message("Discord Response:")
                        for m in messages:
                            self.log_message(f"    {m}")

                    elif index == 2: # patreon
                        pass #TODO
                    

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    load_dotenv()
    app = PostApp()
    app.run()
