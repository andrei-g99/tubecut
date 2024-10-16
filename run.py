import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
import re
from tkinter import messagebox 
from tubecut.commands import _download_video, _trim_video

# Create the main window
root = tk.Tk()
root.title("TubeCut")
# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size proportional to the screen size (e.g., 30% width and 15% height)
window_width = int(screen_width * 0.4)
window_height = int(screen_height * 0.3)

# Set the geometry of the window using the calculated width and height
root.geometry(f"{window_width}x{window_height}")

# Create a font for scaling and bold button text
label_font = font.Font(size=12)  # Larger font for labels and entries
entry_font = font.Font(size=14)  # Larger font for entry fields
button_font = font.Font(size=12)  # Larger font and bold for buttons
bold_button_font = font.Font(size=12, weight="bold")  # Larger font and bold for buttons

# Customize the style of the notebook tabs and buttons
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 12), background="#D3D3D3")  # Darker tab background
style.map("TNotebook.Tab", background=[("selected", "#A9A9A9")])  # Even darker when selected

download_url = tk.StringVar()
download_output_dir_path = tk.StringVar()
download_output_filename = tk.StringVar()

cut_file_path = tk.StringVar()
cut_output_filename = tk.StringVar()
cut_output_dir_path = tk.StringVar()
start_time = tk.StringVar()
end_time = tk.StringVar()

download_format_var = tk.StringVar()
cut_format_var = tk.StringVar()


formats = [
    "mp4",
    "mkv",
    "webm",
    "mp3",
    "mp4a",
    "opus"
]

def on_download():
    try:
        format = download_format_var.get()
        if format == formats[0] or format == formats[1] or format == formats[2]:
            audio_only = False
        elif format == formats[3] or format == formats[4] or format == formats[5]:
            audio_only = True

        _download_video(url=download_url.get(), output_dir=download_output_dir_path.get(), filename=download_output_filename.get(), format=download_format_var.get(), audio_only=audio_only)
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {str(e)}")

def on_trim():
    try:
        _trim_video(file_path=cut_file_path.get(), output_dir=cut_output_dir_path.get(), start_time=start_time.get(), end_time=end_time.get(), output_filename=cut_output_filename.get(), output_format=cut_format_var.get())
        messagebox.showinfo("Success", "Video trimmed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to trim video: {str(e)}")

# Function to handle directory selection (empty handler)
def on_directory_select():
    dir_path = filedialog.askdirectory()
    if dir_path:
        dir_path_entry.delete(0, tk.END)  # Clear current entry
        dir_path_entry.insert(0, dir_path)
        print(f"Directory selected: {dir_path}")

def on_cut_output_dir_select():
    dir_path = filedialog.askdirectory()
    if dir_path:
        cut_output_dir_entry.delete(0, tk.END)  # Clear current entry
        cut_output_dir_entry.insert(0, dir_path)
        print(f"Directory selected: {dir_path}")

# Function to handle directory selection for cutting
def on_cut_file_select():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.webm")]
    )
    if file_path:
        cut_file_path_entry.delete(0, tk.END)  # Clear the entry field
        cut_file_path_entry.insert(0, file_path)  # Insert the selected file path
        print(f"File selected: {file_path}")  # Output the selected file path to console

def on_cut_output_file_select():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.webm")]
    )
    if file_path:
        cut_output_dir_entry.delete(0, tk.END)  # Clear the entry field
        cut_output_dir_entry.insert(0, file_path)  # Insert the selected file path
        print(f"File selected: {file_path}")  # Output the selected file path to console


# Create a Notebook (for tabs)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, expand=True, fill="both")

# Create frames for the two tabs
download_frame = tk.Frame(notebook, width=700, height=250)
cut_frame = tk.Frame(notebook, width=700, height=250)

# Add the tabs to the notebook
notebook.add(download_frame, text="YT Download")
notebook.add(cut_frame, text="Cut")

# --- Download Tab UI ---
# URL Entry Field for Download tab
url_label = tk.Label(download_frame, text="Enter URL:", font=label_font)
url_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

url_entry = tk.Entry(download_frame, font=entry_font, textvariable=download_url)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew", columnspan=6)

# Create a dropdown (Combobox) for format selection in download_frame
format_combobox = ttk.Combobox(download_frame, textvariable=download_format_var, values=formats, state="readonly", font=entry_font)
format_combobox.set("Select a format")  # Set the default text
format_combobox.grid(row=3, column=4, padx=10, pady=10, sticky="ew")  # Place in the grid of download_frame


url_button = tk.Button(download_frame, text="Download", command=on_download, font=bold_button_font)
url_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

# Directory Path Entry Field for Download tab
dir_path_label = tk.Label(download_frame, text="Select output directory:", font=label_font)
dir_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

dir_path_entry = tk.Entry(download_frame, font=entry_font, textvariable=download_output_dir_path)
dir_path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=6)

# Directory Path Entry Field for Download tab
filename_label = tk.Label(download_frame, text="Insert output file name:", font=label_font)
filename_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

filename_entry = tk.Entry(download_frame, font=entry_font, textvariable=download_output_filename)
filename_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew", columnspan=6)

dir_path_button = tk.Button(download_frame, text="Browse", command=on_directory_select, font=button_font)
dir_path_button.grid(row=1, column=7, padx=10, pady=10, sticky="ew")


# --- Cut Tab UI ---
# File Selection for Cut tab
cut_file_path_label = tk.Label(cut_frame, text="Select file to cut:", font=label_font)
cut_file_path_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

cut_file_path_entry = tk.Entry(cut_frame, font=entry_font, textvariable=cut_file_path)
cut_file_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew", columnspan=4)

cut_file_path_button = tk.Button(cut_frame, text="Browse", command=on_cut_file_select, font=button_font)
cut_file_path_button.grid(row=0, column=6, padx=10, pady=10, sticky="ew")

# Labels and entries for start and end time in HH:MM:SS format
start_time_label = tk.Label(cut_frame, text="Start Time (HH:MM:SS):", font=label_font)
start_time_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

start_time_entry = tk.Entry(cut_frame, font=entry_font, width=10, textvariable=start_time)
start_time_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

start_time_label = tk.Label(cut_frame, text="Empty for first frame", font=label_font)
start_time_label.grid(row=3, column=3, padx=1, pady=1, sticky="e")

end_time_label = tk.Label(cut_frame, text="End Time (HH:MM:SS):", font=label_font)
end_time_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

end_time_entry = tk.Entry(cut_frame, font=entry_font, width=10, textvariable=end_time)
end_time_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

start_time_label = tk.Label(cut_frame, text="Empty for last frame", font=label_font)
start_time_label.grid(row=4, column=3, padx=1, pady=1, sticky="e")

# Directory Path Entry Field for Download tab
filename_cut_label = tk.Label(cut_frame, text="Insert output file name:", font=label_font)
filename_cut_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

filename_cut_entry = tk.Entry(cut_frame, font=entry_font, textvariable=cut_output_filename)
filename_cut_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=5)

# Directory Path Entry Field for Download tab
cut_output_dir_label = tk.Label(cut_frame, text="Select output directory:", font=label_font)
cut_output_dir_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

cut_output_dir_entry = tk.Entry(cut_frame, font=entry_font, textvariable=cut_output_dir_path)
cut_output_dir_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew", columnspan=5)

cut_output_dir_button = tk.Button(cut_frame, text="Browse", command=on_cut_output_dir_select, font=button_font)
cut_output_dir_button.grid(row=2, column=6, padx=10, pady=10, sticky="ew")

# Submit button for trimming video
submit_button = tk.Button(cut_frame, text="Trim Video", font=bold_button_font, command=on_trim)
submit_button.grid(row=5, column=1, padx=10, pady=20, sticky="ew")

# Create a dropdown (Combobox) for format selection in download_frame
format_combobox_cut = ttk.Combobox(cut_frame, textvariable=cut_format_var, values=formats, state="readonly", font=entry_font)
format_combobox_cut.set("Select output file format")  # Set the default text
format_combobox_cut.grid(row=5, column=4, padx=10, pady=10, sticky="ew")  # Place in the grid of download_frame

# Start the Tkinter event loop
root.mainloop()
