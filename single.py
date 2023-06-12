import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

import proc as prc
from config import IMG_ICON_PATH

def about() -> str:
    """ Displays an information window about the application"""
    ABOUT = """
Program made by:
Yaroslav Litavrin
Pavel Okhotnikov
Artem Golubev
Tatiana Anisimova

Ural Federal University, 2023"""

    mb.showinfo("About program", ABOUT)

    return ABOUT


def clear() -> None:
    """ Cleans up file input forms and result entry paths"""
    global files
    global out_path
    files = ""
    out_path = ""
    filename.delete(0, tk.END)
    pathname.delete(0, tk.END)


def insert_files() -> None:
    """ Calls the file selection dialog box.
    The selected files (path, name) are written to a global variable.
    """
    global files
    global out_path
    clear()
    files = fd.askopenfilenames()
    out_path = os.path.dirname(files[0])
    filename.insert(0, files)
    pathname.insert(0, out_path)


def insert_path() -> None:
    """ Calls the dialog box for choosing the path to write the results.
    The selected path is written to the global variable.
    """
    global out_path
    pathname.delete(0, tk.END)
    out_path = fd.askdirectory()
    pathname.insert(0, out_path)


def start() -> str:
    """ Processes selected files by YOLO8 model"""
    if not files:
        mb.showerror("Error", "Select files to analyze")
        return "No video files selected"

    if not out_path:
        mb.showerror("Error", "Choose a path to write results")
        return "No path for results entered"

    try:
        model = prc.load_model(model_size=model_size.get())
    except Exception as error_code:
        mb.showerror("Error", "Error loading model.")
        return error_code

    for video_file in files:
        try:
            vid_capture = prc.video_capture(video_file)
        except Exception as error_code:
            mb.showerror("Error", f"Error opening {video_file} video file.")
            return error_code

        try:
            video_param = prc.get_video_stats(vid_capture)
        except Exception as error_code:
            mb.showerror("Error", f"Error getting {video_file} video stats.")
            return error_code

        try:
            filename = os.path.split(video_file)[1]

            video_report = prc.create_videoreport(out_path,
                                                  filename,
                                                  video_param)
        except Exception as error_code:
            mb.showerror("Error", "Error creating videoreport file")
            print(error_code)
            return error_code

        prc.video_processing(vid_capture,
                             video_report,
                             model,
                             process_speed.get(),
                             show_vid.get())
    clear()

    return "Ok"


# Global variables
files = ""
out_path = ""


root = tk.Tk()

root.geometry("450x300")
root.title("Keen eye")

img_file = tk.PhotoImage(file=IMG_ICON_PATH)
tk.Button(root, image=img_file, command=about).\
    grid(row=0, column=0, columnspan=2, rowspan=8)

model_size = tk.StringVar()
model_size.set("m")
tk.Label(text="Model size:").\
    grid(row=0, column=2, sticky=tk.N, padx=10)
tk.Radiobutton(text="Small", variable=model_size,
               value="n").\
    grid(row=1, column=2, sticky=tk.W, padx=10)
tk.Radiobutton(text="Medium", variable=model_size,
               value="s").\
    grid(row=2, column=2, sticky=tk.W, padx=10)
tk.Radiobutton(text="Large", variable=model_size,
               value="m").\
    grid(row=3, column=2, sticky=tk.W, padx=10)

process_speed = tk.IntVar()
process_speed.set(1)
tk.Label(text="Processing speed:").\
    grid(row=0, column=3, sticky=tk.N, padx=10)
tk.Radiobutton(text="every frame", variable=process_speed, value=1).\
    grid(row=1, column=3, sticky=tk.W, padx=10)
tk.Radiobutton(text="every 2-nd", variable=process_speed, value=2).\
    grid(row=2, column=3, sticky=tk.W, padx=10)
tk.Radiobutton(text="every 4-th", variable=process_speed, value=4).\
    grid(row=3, column=3, sticky=tk.W, padx=10)
tk.Radiobutton(text="every 8-th", variable=process_speed, value=8).\
    grid(row=4, column=3, sticky=tk.W, padx=10)

tk.Label(text="").\
    grid(row=8, column=0, sticky=tk.W, padx=10, columnspan=4)

tk.Label(text="Select files to analyze:").\
    grid(row=9, column=0, sticky=tk.W, padx=10, columnspan=4)

filename = tk.Entry(width=35)
filename.grid(row=10, column=0, sticky=tk.W, padx=10, columnspan=4)

tk.Button(text="Select files", width=15, command=insert_files).\
    grid(row=10, column=3, sticky=tk.S, padx=10)

tk.Label(text="Select the output path:").\
    grid(row=12, column=0, sticky=tk.W, padx=10, columnspan=4)

pathname = tk.Entry(width=35)
pathname.grid(row=13, column=0, sticky=tk.W, padx=10, columnspan=4)

tk.Button(text="Select path", width=15, command=insert_path).\
    grid(row=13, column=3, sticky=tk.S, padx=10)

tk.Label(text="").\
    grid(row=14, column=0, sticky=tk.W, padx=10, columnspan=4)

show_vid = tk.BooleanVar()
show_vid.set("False")

tk.Checkbutton(text="Show violations", variable=show_vid,
               onvalue="True", offvalue="False",).\
    grid(row=15, column=0, sticky=tk.W, padx=10, columnspan=4)

start_button = tk.Button(text="Start processing", width=15, command=start)
start_button["bg"] = "#fa4400"
start_button.grid(row=15, column=3, sticky=tk.S, padx=10)

root.mainloop()
