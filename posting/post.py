import tkinter as tk
from tkinter import ttk
from reddit_post import post_on_reddit
import os
from dotenv import load_dotenv

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
        

        # checkboxes
        self.discord_var = tk.BooleanVar()
        self.reddit_var = tk.BooleanVar()
        
        ttk.Checkbutton(platform_frame, text="Discord", 
                       variable=self.discord_var).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Checkbutton(platform_frame, text="Reddit", 
                       variable=self.reddit_var).pack(side=tk.LEFT)


        # Post button
        ttk.Button(main_frame, text="Post", 
                  command=self.post).pack(pady=(10, 0))

    def post(self):
        heading = self.heading_input.get()
        text = self.content_input.get("1.0", tk.END)

        args = [heading, text]
        if self.reddit_var.get():
            res = post_on_reddit(os.getenv("REDDIT_ID"), os.getenv("REDDIT_SECRET"), os.getenv("SUBREDDIT"), os.getenv("REDDIT_USERNAME"),
                                os.getenv("REDDIT_PASSWORD"), args)
            print(res)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    load_dotenv()
    app = PostApp()
    app.run()
