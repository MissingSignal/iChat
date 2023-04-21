import tkinter as tk
from tkinter import scrolledtext
import threading

# Define the chat window
class ChatWindow:
    def __init__(self, master):
        self.master = master
        master.title("Chat Window")

        # Create text area for the chat messages
        self.text_area = scrolledtext.ScrolledText(master)
        self.text_area.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.text_area.configure(font=("Arial", 12))

        # Create input field for user to enter messages
        self.input_field = tk.Entry(master)
        self.input_field.grid(row=1, column=0, sticky="ew")
        self.input_field.configure(font=("Arial", 12))

        # Bind the Enter key to the send message function
        self.input_field.bind("<Return>", self.send_message)

        # Create send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, sticky="e")

        # Configure grid to resize with window
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=0)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=0)

    def send_message(self, event=None):
        # Get the user's message from the input field
        message = self.input_field.get()

        # Check if the input field is empty
        if not message:
            return

        # Clear the input field
        self.input_field.delete(0, tk.END)

        # Add the message to the chat window
        self.text_area.insert(tk.END, f"You: {message}\n")

# Define function to populate the chat window with messages
def populate_chat(chat_window):
    # List of example messages
    messages = [
        "Hello there!",
        "How are you?",
        "I'm doing well, thanks for asking.",
        "What have you been up to?",
        "Not much, just working on some scripts.",
        "Cool, what kind of scripts?",
        "Just some automation stuff.",
        "Nice, that sounds interesting.",
        "Yeah, it's been keeping me busy.",
        "Well, let me know if you want to chat more later.",
        "Sounds good, talk to you later!",
    ]

    # Loop through messages and add them to the chat window
    for i, message in enumerate(messages):
        # Set a delay between messages
        time.sleep(2)

        # Add the message to the chat window
        chat_window.text_area.insert(tk.END, f"Friend: {message}\n")

# Create the chat window
root = tk.Tk()
chat_window = ChatWindow(root)

# Start a thread to populate the chat window with messages
thread = threading.Thread(target=populate_chat, args=(chat_window,))
thread.daemon = True
thread.start()

# Set the size of the window
root.geometry("400x400")

# Run the GUI loop
while True:
    # Get the current size of the window
    width = root.winfo_width()
    height = root.winfo_height()

    # Calculate the font size based on the window size
    font_size = min(int(height / 25), int(width / 50))
    font = ("Arial", font_size)

    # Update the font size for the chat window and input field
    chat_window.text_area.configure(font=font)
    chat_window.input_field.configure(font=font)

    root.update()