import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from ultralyticsplus import YOLO
import cv2
import os


def about() -> str:
    """ Displays an information window about the application.
    """
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
    """ Cleans up file input forms and result entry paths.
    """
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
    path, file = os.path.split(files[0])
    out_path = path
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


def start() -> None:
    """ Processes selected files by YOLO8 model.
    """
    if not files:
        mb.showerror("Error", "Select files to analyze")
        return

    if not out_path:
        mb.showerror("Error", "Choose a path to write results")
        return

    try:
        model = load_model(model_size=model_size.get())
    except:
        mb.showerror("Error", "Error loading model")

    for video_file in files:
        try:
            vid_capture = cv2.VideoCapture(video_file)
        except:
            mb.showerror("Error", f"Error opening {video_file} video file.")

        try:
            frame_size = get_video_stats(vid_capture)[0]
        except:
            mb.showerror("Error", f"Error getting {video_file} video statistic.")

        try:
            path, filename = os.path.split(video_file)

            video_report = create_videoreport(out_path,
                                              filename,
                                              frame_size)
        except:
            mb.showerror("Error", "Error creating videoreport file")

        video_processing(vid_capture,
                         video_report,
                         model,
                         process_speed.get(),
                         show_vid.get())
    clear()

    return


def load_model(model_size: str) -> YOLO:
    """ Loads a YOLOv8 model for the further photo or video processing.
    """
    model = YOLO(model_size)

    model.overrides['conf'] = 0.3
    model.overrides['iou'] = 0.45
    model.overrides['agnostic_nms'] = False
    model.overrides['max_det'] = 1

    return model


def get_video_stats(vid_capture: cv2.VideoCapture) -> tuple:
    """ Getting the statistic of video:
    """
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    fps = int(vid_capture.get(5))
    frame_count = int(vid_capture.get(7))

    frame_size = (frame_width, frame_height)
    video_time = frame_count / fps

    return frame_size, video_time


def create_videoreport(out_path: str,
                       filename: str,
                       frame_size: tuple) -> cv2.VideoWriter:
    """ Create video report file:
    """
    report_videofile = out_path + "/" + "out_" + filename

    out_video = cv2.VideoWriter(report_videofile,
                                cv2.VideoWriter_fourcc(*"XVID"),
                                20,
                                frame_size)
    return out_video


def video_processing(vid_capture: cv2.VideoCapture,
                     video_report: cv2.VideoWriter,
                     model: YOLO,
                     process_speed: int=1,
                     show_vid: bool=False) -> None:
    """ Main function of video processing.
    """
    frames_cnt = 0
    rec_cnt = 0

    while vid_capture.isOpened():
        ret, frame = vid_capture.read()

        if ret:
            frames_cnt += 1

            if rec_cnt:
                video_report.write(frame)
                rec_cnt -= 1
                continue

            if frames_cnt % process_speed:
                continue

            if detect(frame, model):
                rec_cnt = 30

                if show_vid:
                    cv2.imshow("NoHardHat", frame)
                    cv2.waitKey(1)
        else:
            break

    vid_capture.release()
    cv2.destroyAllWindows()


def detect(image: any, model: YOLO) -> bool:
    """
    Using YOLOv8 model, detects people without a hard hat in the photo.
    """
    results = model.predict(image)

    # Iterations over tensors in order to locate the necessary objects
    for box in results[0].boxes:
        if int(box.cls) == 1:
            return True


# Global variables
files = ""
out_path = ""


root = tk.Tk()

root.geometry("450x300")
root.title("Keen eye")

img_file = tk.PhotoImage(file="images/image.png")
tk.Button(root, image=img_file, command=about).\
    grid(row=0, column=0, columnspan=2, rowspan=8)

model_size = tk.StringVar()
model_size.set("keremberke/yolov8m-hard-hat-detection")
tk.Label(text="Model size:").\
    grid(row=0, column=2, sticky=tk.N, padx=10)
tk.Radiobutton(text="Small", variable=model_size,
               value="keremberke/yolov8n-hard-hat-detection").\
    grid(row=1, column=2, sticky=tk.W, padx=10)
tk.Radiobutton(text="Medium", variable=model_size,
               value="keremberke/yolov8s-hard-hat-detection").\
    grid(row=2, column=2, sticky=tk.W, padx=10)
tk.Radiobutton(text="Large", variable=model_size,
               value="keremberke/yolov8m-hard-hat-detection").\
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
