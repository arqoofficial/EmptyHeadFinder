import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import media_processing as mp


def about() -> str:
    """
    Displays an information window about the application.
    Returns an information string-constant ABOUT
    """
    ABOUT = "UrFU + Skillfactory forever!"
    mb.showinfo("About program", ABOUT)

    return ABOUT


def clear() -> None:
    """
    Cleans up file input forms and result entry paths.
    Does not accept or return any parameters.
    """
    global files
    global out_path
    files = ""
    out_path = ""
    filename.delete(0, tk.END)
    pathname.delete(0, tk.END)


def insert_files() -> None:
    """
    Calls the file selection dialog box.
    Does not accept or return any parameters.
    The selected files (path, name) are written to a global variable.
    """
    global files
    global out_path
    clear()
    files = fd.askopenfilenames()
    path, file = mp.path_file_split(files[0])
    out_path = path
    filename.insert(0, files)
    pathname.insert(0, out_path)


def insert_path() -> None:
    """
    Calls the dialog box for choosing the path to write the results.
    Does not accept or return any parameters.
    The selected path is written to the global variable.
    """
    global out_path
    pathname.delete(0, tk.END)
    out_path = fd.askdirectory()
    pathname.insert(0, out_path)


def start() -> list:
    """
    Processes selected files by YOLO8 model.
    Does not accept any parameters.
    Returns a list of video reports or an error message.
    """
    if not files:
        mb.showerror("Error", "Select files to analyze")
        return ["Error"]

    if not out_path:
        mb.showerror("Error", "Choose a path to write results")
        return ["Error"]

    model = mp.load_model(model_size=model_size.get())

    report_videofiles = []

    for video_file in files:
        report_videofiles.append(
            mp.video_processing(
                model,
                video_file,
                out_path,
                process_speed.get(),
                show_vid.get()
            )
        )
    clear()

    return report_videofiles


# Global variables are needed here!
files = ""
out_path = ""


root = tk.Tk()
root.geometry("500x350")
root.title("Keen eye")

img_file = tk.PhotoImage(file="images/image.png")
tk.Button(root, image=img_file, command=about).grid(row=0,
                                                    column=0,
                                                    columnspan=2,
                                                    rowspan=8)
tk.Label(text="Model size:").grid(row=0,
                                  column=2,
                                  sticky=tk.N,
                                  padx=10)
model_size = tk.StringVar()
model_size.set("m")

tk.Radiobutton(text="Base",
               variable=model_size, value="n").grid(row=1,
                                                    column=2,
                                                    sticky=tk.W,
                                                    padx=10)
tk.Radiobutton(text="Small",
               variable=model_size, value="s").grid(row=2,
                                                    column=2,
                                                    sticky=tk.W,
                                                    padx=10)
tk.Radiobutton(text="Medium",
               variable=model_size, value="m").grid(row=3,
                                                    column=2,
                                                    sticky=tk.W,
                                                    padx=10)
# tk.Radiobutton(text="Large",
#               variable=model_size, value="l").grid(row=4,
#                                                    column=2,
#                                                    sticky=tk.W,
#                                                    padx=10)

tk.Label(text="processing speed:").grid(row=0,
                                        column=3,
                                        sticky=tk.N,
                                        padx=10)
process_speed = tk.IntVar()
process_speed.set(1)

tk.Radiobutton(text="every frame",
               variable=process_speed, value=1).grid(row=1,
                                                     column=3,
                                                     sticky=tk.W,
                                                     padx=10)
tk.Radiobutton(text="every 2-nd",
               variable=process_speed, value=2).grid(row=2,
                                                     column=3,
                                                     sticky=tk.W,
                                                     padx=10)
tk.Radiobutton(text="every 4-th",
               variable=process_speed, value=4).grid(row=3,
                                                     column=3,
                                                     sticky=tk.W,
                                                     padx=10)
tk.Radiobutton(text="every 8-th",
               variable=process_speed, value=8).grid(row=4,
                                                     column=3,
                                                     sticky=tk.W,
                                                     padx=10)

tk.Label(text="").grid(row=8,
                       column=0,
                       sticky=tk.W,
                       padx=10,
                       columnspan=4)

tk.Label(text="Select files to analyze:").grid(row=9,
                                               column=0,
                                               sticky=tk.W,
                                               padx=10,
                                               columnspan=4)
filename = tk.Entry(width=35)
filename.grid(row=10,
              column=0,
              sticky=tk.W,
              padx=10,
              columnspan=4)

tk.Button(text="Select files",
          width=15, command=insert_files).grid(row=10,
                                               column=3,
                                               sticky=tk.S,
                                               padx=10)

tk.Label(text="Select the output path:").grid(row=12,
                                              column=0,
                                              sticky=tk.W,
                                              padx=10,
                                              columnspan=4)
pathname = tk.Entry(width=35)
pathname.grid(row=13,
              column=0,
              sticky=tk.W,
              padx=10,
              columnspan=4)

tk.Button(text="Select path",
          width=15, command=insert_path).grid(row=13,
                                              column=3,
                                              sticky=tk.S,
                                              padx=10)
tk.Label(text="").grid(row=14,
                       column=0,
                       sticky=tk.W,
                       padx=10,
                       columnspan=4)

show_vid = tk.BooleanVar()
show_vid.set("False")

tk.Checkbutton(root, text="Show violations", variable=show_vid,
               onvalue="True", offvalue="False").grid(row=15,
                                                       column=0,
                                                       sticky=tk.W,
                                                       padx=10,
                                                       columnspan=4)

start_button = tk.Button(text="Start processing", width=15, command=start)
start_button["bg"] = "#fa4400"
start_button.grid(row=15,
                  column=3,
                  sticky=tk.S,
                  padx=10)

root.mainloop()
