import os
import requests
import time
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

# Function to download an image from a URL
def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# Function to handle the "Download" button click
def download_images():
    global success_label, url_button

    # Get the folder path
    folder_path = folder_var.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder to save the images.")
        return

    # Get the URLs from the text area
    urls = text_area.get("1.0", "end").strip().split("\n")
    if not urls or urls == [""]:
        messagebox.showerror("Error", "Please enter at least one valid URL.")
        return

    # Count total URLs and initialize progress bar
    total_urls = len([url for url in urls if url.strip()])
    if total_urls == 0:
        messagebox.showerror("Error", "No valid URLs entered.")
        return

    progress_bar.set(0)
    progress_bar.pack(pady=10)

    success_count = 0
    for idx, url in enumerate(urls):
        if url.strip():
            try:
                base_url = "https://i.pinimg.com/"
                parts = url.split("/")
                if len(parts) >= 5 and "x" in parts[3]:
                    parts[3] = "1200x"
                    modified_url = "/".join(parts)
                else:
                    modified_url = url

                file_name = modified_url.split("/")[-1]
                save_path = os.path.join(folder_path, file_name)

                if download_image(modified_url, save_path):
                    success_count += 1

                progress_bar.set((idx + 1) / total_urls)
                root.update_idletasks()
                time.sleep(1)

            except Exception as e:
                ctk.messagebox.showwarning("Warning", f"Failed to download {url}: {e}")

    show_success_message(success_count)

# Function to clear the form
def clear_form():
    global success_label, url_button
    text_area.delete("1.0", "end")
    folder_var.set("")
    progress_bar.set(0)
    progress_bar.pack_forget()
    url_count_label.configure(text="Total URLs: 0")

    if success_label:
        success_label.pack_forget()
        success_label = None
    if url_button:
        url_button.pack_forget()
        url_button = None

# Function to show the success message and button
def show_success_message(success_count):
    global success_label, url_button

    if success_label:
        success_label.pack_forget()
    if url_button:
        url_button.pack_forget()

    success_label = ctk.CTkLabel(root, text=f"Successfully downloaded {success_count} HD images.")
    success_label.pack(pady=10)

    url_button = ctk.CTkButton(
        root,
        text="Buy Me a Coffee ♡",
        fg_color="#078a00",
        corner_radius=24,
        command=lambda: webbrowser.open("https://lynk.id/masziraf/zz251qy81ej5")
    )
    url_button.pack(pady=5)

# Function to update URL count
def update_url_count(event=None):
    urls = text_area.get("1.0", "end").strip().split("\n")
    count = len([url for url in urls if url.strip()])
    url_count_label.configure(text=f"Total URLs: {count}")

# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main window
root = ctk.CTk()
root.title("Pinterest HD Downloader by Mas Ziraf")
root.geometry("500x550")

# Global variables
success_label = None
url_button = None
url_count_label = None

# URL input
ctk.CTkLabel(root, text="Enter one URL per line:").pack(pady=5)
text_area = ctk.CTkTextbox(root, height=100, width=400)
text_area.pack(pady=5)
text_area.bind("<KeyRelease>", update_url_count)

# URL count label
url_count_label = ctk.CTkLabel(root, text="Total URLs: 0")
url_count_label.pack(pady=5)

# Folder selection
folder_var = ctk.StringVar()
ctk.CTkLabel(root, text="Select folder to save images:").pack(pady=5)
ctk.CTkButton(root, text="Browse Folder", command=lambda: folder_var.set(ctk.filedialog.askdirectory())).pack(pady=5)
ctk.CTkLabel(root, textvariable=folder_var).pack(pady=5)

# Progress bar
progress_bar = ctk.CTkProgressBar(root, width=300)
progress_bar.set(0)

# Buttons
ctk.CTkButton(root, text="Download Images", command=download_images).pack(pady=10)
ctk.CTkButton(root, text="Clear Form", command=clear_form).pack(pady=5)

# Start app
root.mainloop()
