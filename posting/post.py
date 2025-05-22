#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from platforms.reddit_post import post_on_reddit
from platforms.discord_posts import discord_message
from platforms.patreon_post import patreon_post
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
        self.root.geometry("1500x800")  # Made window bigger
        self.root.minsize(800, 600)

        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel for input
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Heading input
        heading_frame = ttk.Frame(left_panel)
        heading_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(heading_frame, text="Heading:").pack(side=tk.LEFT)
        self.heading_input = ttk.Entry(heading_frame, width=50)
        self.heading_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Content input
        content_frame = ttk.Frame(left_panel)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(content_frame, text="Content:").pack(anchor=tk.W)
        
        text_frame = ttk.Frame(content_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.content_input = tk.Text(text_frame, height=10, width=50, 
                                   yscrollcommand=scrollbar.set)
        self.content_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.content_input.yview)

        # Right panel for platforms
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Platform sections
        self.setup_platform_section(right_panel, "Discord", 0)
        self.setup_platform_section(right_panel, "Reddit", 1)
        self.setup_platform_section(right_panel, "Patreon", 2)

        # Main log area at the bottom
        log_frame = ttk.LabelFrame(main_frame, text="Posting Logs")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        log_scrollbar = ttk.Scrollbar(log_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_output = tk.Text(log_frame, height=6, width=50,
                                 yscrollcommand=log_scrollbar.set)
        self.log_output.pack(fill=tk.BOTH, expand=True)
        
        log_scrollbar.config(command=self.log_output.yview)

        # Post button
        ttk.Button(main_frame, text="Post", 
                  command=self.post).pack(pady=(10, 0))

    def setup_platform_section(self, parent, platform_name, index):
        # Create a frame for each platform
        platform_frame = ttk.LabelFrame(parent, text=platform_name)
        platform_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Checkboxes frame
        checkbox_frame = ttk.Frame(platform_frame)
        checkbox_frame.pack(fill=tk.X, pady=(5, 5))
        
        # Platform checkbox
        var_name = f"{platform_name.lower()}_var"
        setattr(self, var_name, tk.BooleanVar())
        ttk.Checkbutton(checkbox_frame, text=platform_name, 
                       variable=getattr(self, var_name)).pack(side=tk.LEFT)
        
        # Shortened checkbox
        short_var_name = f"{platform_name.lower()}_short_var"
        setattr(self, short_var_name, tk.BooleanVar())
        ttk.Checkbutton(checkbox_frame, text="Shortened", 
                       variable=getattr(self, short_var_name)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Cookie reset checkbox for Patreon
        if platform_name == "Patreon":
            reset_var_name = f"{platform_name.lower()}_reset_var"
            setattr(self, reset_var_name, tk.BooleanVar())
            ttk.Checkbutton(checkbox_frame, text="Debug", 
                           variable=getattr(self, reset_var_name)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Preview button
        ttk.Button(checkbox_frame, text="Show", 
                  command=lambda: self.show_preview(platform_name)).pack(side=tk.RIGHT)
        
        # Preview text area
        preview_frame = ttk.Frame(platform_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 5))
        
        preview_scrollbar = ttk.Scrollbar(preview_frame)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        preview_text = tk.Text(preview_frame, height=4, width=30,
                              yscrollcommand=preview_scrollbar.set)
        preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_text.config(state="disabled")
        
        preview_scrollbar.config(command=preview_text.yview)
        
        # Store the preview text widget
        setattr(self, f"{platform_name.lower()}_preview", preview_text)

    def show_preview(self, platform_name):
        heading = self.heading_input.get()
        text = self.content_input.get("1.0", tk.END)
        short_var = getattr(self, f"{platform_name.lower()}_short_var")
        
        preview_text = getattr(self, f"{platform_name.lower()}_preview")
        preview_text.config(state="normal")
        preview_text.delete(1.0, tk.END)
        
        if short_var.get():
            msg = convert_premium_to_short(text)
            if msg == "":
                preview_text.insert(tk.END, "Message couldn't be converted into short form.\nCompare the text format with the one in posting/tutorials/sample_long.txt, or send it in long(unedited) form.")
            else:
                preview_text.insert(tk.END, f"{heading}\n\n{msg}")
        else:
            preview_text.insert(tk.END, f"{heading}\n\n{text}")
        
        preview_text.config(state="disabled")

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
                if index == 0: # reddit
                    msg = convert_premium_to_short(text) if self.reddit_short_var.get() else text
                    if msg == "":
                        res = "\n    Message couldn't be converted into short form, so it wasnt sent.\n    Compare the text format with the one in posting/tutorials/sample_long.txt, or send it in long(unedited) form."
                    else:
                        args = [heading, msg]
                        res = post_on_reddit(args)
                    self.log_message(f"Reddit Response: {res}")

                elif index == 1: # discord
                    msg = convert_premium_to_short(text) if self.discord_short_var.get() else text
                    if msg == "":
                        messages = ["\n    Message couldn't be converted into short form, so it wasnt sent.\n    Compare the text format with the one in posting/tutorials/sample_long.txt, or send it in long(unedited) form."]
                    else:
                        discord_text = heading + "\n\n" + msg

                        messages = discord_message(discord_text)
                    self.log_message("Discord Response:")
                    for m in messages:
                        self.log_message(f"    {m}")

                elif index == 2: # patreon
                    msg = convert_premium_to_short(text) if self.patreon_short_var.get() else text
                    if msg == "":
                        messages = ["\n    Message couldn't be converted into short form, so it wasnt sent.\n    Compare the text format with the one in posting/tutorials/sample_long.txt, or send it in long(unedited) form."]
                    else:
                        messages = patreon_post(heading, msg, self.patreon_reset_var.get())
                    self.log_message("Patreon Response:")
                    for m in messages:
                        self.log_message(f"    {m}")


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    load_dotenv()
    app = PostApp()
    app.run()
