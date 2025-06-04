from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
import sys
import os
from tkinter import messagebox 
from tubecut.commands import _download_video, _trim_video

APP_VERSION = "3.0.0"

if getattr(sys, 'frozen', False): 
    current_dir = Path(sys.executable).parent 
else:
    current_dir = Path(__file__).parent 


ffmpeg_path = current_dir / 'bin' / 'ffmpeg'

# Add .exe extension if running on Windows
if os.name == 'nt':  # 'nt' is for Windows
    ffmpeg_path = current_dir / 'bin' / 'ffmpeg.exe'

root = tk.Tk()
root.title("TubeCut")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 0.6)
window_height = int(screen_height * 0.5)

root.geometry(f"{window_width}x{window_height}")

label_font = font.Font(size=12)  
entry_font = font.Font(size=14) 
button_font = font.Font(size=12) 
bold_button_font = font.Font(size=12, weight="bold") 

style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 12), background="#D3D3D3") 
style.map("TNotebook.Tab", background=[("selected", "#A9A9A9")]) 

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

cookies_file_path = tk.StringVar()
use_cookies = tk.BooleanVar(value=False)
is_playlist_download = tk.BooleanVar(value=False)


formats = [
    "mp4",
    "mkv",
    "webm",
    "mp3",
    "mp4a",
    "opus"
]

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if total:
            percent = int(downloaded / total * 100)
            download_progress["value"] = percent
            root.update_idletasks()
    elif d['status'] == 'finished':
        download_progress["value"] = 100
        root.update_idletasks()

def on_download():
    try:
        format = download_format_var.get()
        if format == formats[0] or format == formats[1] or format == formats[2]:
            audio_only = False
        elif format == formats[3] or format == formats[4] or format == formats[5]:
            audio_only = True

        download_progress["value"] = 0
        download_progress.grid()  # Show the progress bar
        root.update_idletasks()

        _download_video(url=download_url.get(),
                        output_dir=download_output_dir_path.get(),
                        filename=None if is_playlist_download.get() else download_output_filename.get(),
                        format=download_format_var.get(),
                        ffmpeg_path=ffmpeg_path,
                        audio_only=audio_only,
                        cookies_path=cookies_file_path.get() if use_cookies.get() else None,
                        progress_hook=progress_hook)
        messagebox.showinfo("Success", "Video downloaded successfully!")
        download_progress.grid_remove()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {str(e)}")
        download_progress.grid_remove()

def on_trim():
    try:
        _trim_video(file_path=cut_file_path.get(),
                    output_dir=cut_output_dir_path.get(),
                    start_time=start_time.get(),
                    end_time=end_time.get(),
                    output_filename=cut_output_filename.get(),
                    ffmpeg_path=ffmpeg_path,
                    output_format=cut_format_var.get())
        messagebox.showinfo("Success", "Video trimmed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to trim video: {str(e)}")

def on_directory_select():
    dir_path = filedialog.askdirectory()
    if dir_path:
        dir_path_entry.delete(0, tk.END) 
        dir_path_entry.insert(0, dir_path)
        print(f"Directory selected: {dir_path}")

def on_cut_output_dir_select():
    dir_path = filedialog.askdirectory()
    if dir_path:
        cut_output_dir_entry.delete(0, tk.END) 
        cut_output_dir_entry.insert(0, dir_path)
        print(f"Directory selected: {dir_path}")

def on_cut_file_select():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Video and Audio Files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.webm *.mp3 *.wav *.aac *.flac *.ogg *.m4a")]
    )
    if file_path:
        cut_file_path_entry.delete(0, tk.END) 
        cut_file_path_entry.insert(0, file_path)  
        print(f"File selected: {file_path}")

def on_cut_output_file_select():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.webm")]
    )
    if file_path:
        cut_output_dir_entry.delete(0, tk.END)
        cut_output_dir_entry.insert(0, file_path) 
        print(f"File selected: {file_path}")

def on_cookies_file_select():
    file_path = filedialog.askopenfilename(
        title="Select cookies.txt file",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        cookies_file_path.set(file_path)
        print(f"Cookies file selected: {file_path}")

def toggle_filename_field():
    if is_playlist_download.get():
        download_output_filename.set("")
        filename_entry.config(state="disabled")
    else:
        filename_entry.config(state="normal")


# --- App Title ---
title_frame = tk.Frame(root)
title_frame.pack(pady=(10, 0))

title_label = tk.Label(
    title_frame,
    text="TubeCut - YouTube Downloader and Editor",
    font=("Arial", 20, "bold")
)
title_label.pack()

def open_github(event=None):
    import webbrowser
    webbrowser.open_new("https://github.com/andrei-g99")

subtitle_frame = tk.Frame(title_frame)
subtitle_frame.pack(pady=(5, 10))

subtitle_text = tk.Label(
    subtitle_frame,
    text="Download or trim YouTube videos and playlists — by ",
    font=("Consolas", 12),
    fg="gray"
)
subtitle_text.pack(side="left")

author_link = tk.Label(
    subtitle_frame,
    text="andrei-g99",
    font=("Consolas", 12, "underline"),
    fg="blue",
    cursor="hand2"
)
author_link.pack(side="left")
author_link.bind("<Button-1>", open_github)

version_label = tk.Label(
    subtitle_frame,
    text=f" · v{APP_VERSION}",
    font=("Consolas", 12),
    fg="gray"
)
version_label.pack(side="left")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, expand=True, fill="both")

download_frame = tk.Frame(notebook, width=700, height=250)
cut_frame = tk.Frame(notebook, width=700, height=250)

notebook.add(download_frame, text="YT Download")
notebook.add(cut_frame, text="Cut / Convert")

# --- Download Tab UI ---
url_label = tk.Label(download_frame, text="Enter URL:", font=label_font)
url_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

url_entry = tk.Entry(download_frame, font=entry_font, textvariable=download_url)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew", columnspan=6)

format_combobox = ttk.Combobox(download_frame, textvariable=download_format_var, values=formats, state="readonly", font=entry_font)
format_combobox.set("Select a format")  
format_combobox.grid(row=3, column=4, padx=10, pady=10, sticky="ew") 


url_button = tk.Button(download_frame, text="Download", command=on_download, font=bold_button_font)
url_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

download_progress = ttk.Progressbar(download_frame, orient="horizontal", length=400, mode="determinate")
download_progress.grid(row=6, column=1, columnspan=5, padx=10, pady=10, sticky="ew")
download_progress.grid_remove()  # <-- Initially hide it

dir_path_label = tk.Label(download_frame, text="Select output directory:", font=label_font)
dir_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

dir_path_entry = tk.Entry(download_frame, font=entry_font, textvariable=download_output_dir_path)
dir_path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=6)

filename_label = tk.Label(download_frame, text="Insert output file name:", font=label_font)
filename_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

filename_entry = tk.Entry(download_frame, font=entry_font, textvariable=download_output_filename)
filename_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew", columnspan=6)

playlist_checkbox = tk.Checkbutton(
    download_frame,
    text="Downloading a YouTube playlist",
    variable=is_playlist_download,
    font=label_font,
    command=lambda: toggle_filename_field()
)
playlist_checkbox.grid(row=2, column=7, padx=10, pady=10, sticky="w")

dir_path_button = tk.Button(download_frame, text="Browse", command=on_directory_select, font=button_font)
dir_path_button.grid(row=1, column=7, padx=10, pady=10, sticky="ew")

# --- Optional Cookies Input ---
cookies_checkbox = tk.Checkbutton(
    download_frame, 
    text="Add YouTube session cookies", 
    variable=use_cookies, 
    font=label_font,
    command=lambda: cookies_button.config(state="normal" if use_cookies.get() else "disabled")
)
cookies_checkbox.grid(row=4, column=0, padx=10, pady=10, sticky="w", columnspan=3)

cookies_button = tk.Button(
    download_frame, 
    text="Browse cookies.txt", 
    font=button_font,
    state="disabled",
    command=lambda: on_cookies_file_select()
)
cookies_button.grid(row=4, column=3, padx=10, pady=10, sticky="ew", columnspan=2)

cookies_label = tk.Label(download_frame, textvariable=cookies_file_path, font=("Arial", 10), anchor="w")
cookies_label.grid(row=4, column=5, columnspan=3, padx=10, pady=10, sticky="w")

# --- Cut Tab UI ---
cut_file_path_label = tk.Label(cut_frame, text="Select file to cut:", font=label_font)
cut_file_path_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

cut_file_path_entry = tk.Entry(cut_frame, font=entry_font, textvariable=cut_file_path)
cut_file_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew", columnspan=4)

cut_file_path_button = tk.Button(cut_frame, text="Browse", command=on_cut_file_select, font=button_font)
cut_file_path_button.grid(row=0, column=6, padx=10, pady=10, sticky="ew")

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

filename_cut_label = tk.Label(cut_frame, text="Insert output file name:", font=label_font)
filename_cut_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

filename_cut_entry = tk.Entry(cut_frame, font=entry_font, textvariable=cut_output_filename)
filename_cut_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=5)

cut_output_dir_label = tk.Label(cut_frame, text="Select output directory:", font=label_font)
cut_output_dir_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

cut_output_dir_entry = tk.Entry(cut_frame, font=entry_font, textvariable=cut_output_dir_path)
cut_output_dir_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew", columnspan=5)

cut_output_dir_button = tk.Button(cut_frame, text="Browse", command=on_cut_output_dir_select, font=button_font)
cut_output_dir_button.grid(row=2, column=6, padx=10, pady=10, sticky="ew")

submit_button = tk.Button(cut_frame, text="Trim Video", font=bold_button_font, command=on_trim)
submit_button.grid(row=5, column=1, padx=10, pady=20, sticky="ew")

format_combobox_cut = ttk.Combobox(cut_frame, textvariable=cut_format_var, values=formats, state="readonly", font=entry_font)
format_combobox_cut.set("Select output file format") 
format_combobox_cut.grid(row=5, column=4, padx=10, pady=10, sticky="ew") 

root.mainloop()
