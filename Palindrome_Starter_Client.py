import socket
import tkinter as tk
from tkinter import messagebox

import time

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
MAX_RETRIES = 3
TIMEOUT = 5  # seconds

# Function to connect to server and send the request
def send_request(check_type):
    """Handles the client-server communication based on user input."""
    retries = 0
    input_string = input_text.get().strip()

    # Check if input is empty or still contains placeholder text
    if not input_string or input_string == "Enter text here...":
        messagebox.showerror("Input Error", "Please enter a valid string.")
        return

    # Convert check type to server format
    request_type = "simple" if check_type == "Simple" else "complex"
    message = f"{request_type}|{input_string}"

    while retries < MAX_RETRIES:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(TIMEOUT)
                client_socket.connect((SERVER_HOST, SERVER_PORT))

                client_socket.send(message.encode())
                response = client_socket.recv(1024).decode()

                # Display response with animation
                result_label.config(text=f"Server Response:\n{response}", fg="#0aff0a")
                return

        except socket.timeout:
            retries += 1
            result_label.config(text=f"Timeout! Retrying {retries}/{MAX_RETRIES}...", fg="red")

        except socket.error as e:
            retries += 1
            result_label.config(text=f"Connection error: {e}. Retrying...", fg="red")
            time.sleep(2)

    # If all retries fail
    messagebox.showerror("Server Error", "Failed to connect to server after multiple attempts.")

# Function to exit application
def exit_app():
    root.destroy()

# ---------------- UI DESIGN -----------------
root = tk.Tk()
root.title("Mochi the Checker 🐼")
root.geometry("600x550")
root.resizable(False, False)
root.configure(bg="#0D0D0D")  # Dark mode cyberpunk background

# Title Label
title_label = tk.Label(root, text="Detective Mochi 🐼", font=("Consolas", 22, "bold"), bg="#0D0D0D", fg="#00FFFF")
title_label.pack(pady=5)

# Input Text Box with Neon Glow
def on_entry_click(event):
    """Removes placeholder text when clicked."""
    if input_text.get() == "Enter text here...":
        input_text.delete(0, tk.END)
        input_text.config(fg="white", bg="#222222")

def on_focus_out(event):
    """Restores placeholder text if empty."""
    if not input_text.get():
        input_text.insert(0, "Enter text here...")
        input_text.config(fg="#AAAAAA", bg="#181818")

input_text = tk.Entry(root, font=("Consolas", 14), width=35, borderwidth=3, relief="solid", fg="#AAAAAA", bg="#181818", insertbackground="white")
input_text.insert(0, "Enter text here...")
input_text.bind("<FocusIn>", on_entry_click)
input_text.bind("<FocusOut>", on_focus_out)
input_text.pack(pady=15)

# Function to animate button hover effect
def on_hover(btn, color):
    btn.config(bg=color, fg="black")

def on_leave(btn, color):
    btn.config(bg=color, fg="white")

# Simple Palindrome Check Button
simple_button = tk.Button(root, text="🔹 Simple Check", font=("Consolas", 14, "bold"), bg="#0059b3", fg="white", padx=20, pady=10, borderwidth=2, relief="solid", command=lambda: send_request("Simple"))
simple_button.pack(pady=10)
simple_button.bind("<Enter>", lambda event: on_hover(simple_button, "#00aaff"))
simple_button.bind("<Leave>", lambda event: on_leave(simple_button, "#0059b3"))

# Complex Palindrome Check Button
complex_button = tk.Button(root, text="🔸 Complex Check", font=("Consolas", 14, "bold"), bg="#b30059", fg="white", padx=20, pady=10, borderwidth=2, relief="solid", command=lambda: send_request("Complex"))
complex_button.pack(pady=10)
complex_button.bind("<Enter>", lambda event: on_hover(complex_button, "#ff0066"))
complex_button.bind("<Leave>", lambda event: on_leave(complex_button, "#b30059"))

# Result Label
result_label = tk.Label(root, text="Result will appear here", font=("Consolas", 14), bg="#0D0D0D", fg="#00FF00", wraplength=500, justify="center", borderwidth=2, relief="solid", padx=10, pady=10)
result_label.pack(pady=15)

# Exit Button with hover effect
exit_button = tk.Button(root, text="❌ Exit", font=("Consolas", 14, "bold"), bg="#990000", fg="white", padx=20, pady=10, borderwidth=2, relief="solid", command=exit_app)
exit_button.pack(pady=10)
exit_button.bind("<Enter>", lambda event: on_hover(exit_button, "#ff3333"))
exit_button.bind("<Leave>", lambda event: on_leave(exit_button, "#990000"))

# Run the GUI
root.mainloop()
