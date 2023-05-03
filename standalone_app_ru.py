import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import media_processing as mp


def about() -> str:
    """
    Вывод информационного окна о приложении.
    Вызывается по кнопке-картинке в левом верхнем углу.
    Возвращает информационную строку-константу ABOUT
    """
    ABOUT = "УрФУ + Скиллфактори forever!"
    mb.showinfo("О программе", ABOUT)

    return ABOUT


def clear() -> None:
    """
    Очистка форм ввода файлов и пути записи результатов.
    Никаких параметров не принимает и не возвращает.
    """
    global files
    global out_path
    files = ""
    out_path = ""
    filename.delete(0, tk.END)
    pathname.delete(0, tk.END)


def insert_files() -> None:
    """
    Вызов диалогового окна выбора файлов.
    Никаких параметров не принимает и не возвращает.
    Выбранные файлы (path, name) записывает в глобальную переменную.
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
    Вызов диалогового окна выбора пути для записи результатов.
    Никаких параметров не принимает и не возвращает.
    Выбранный путь записывает в глобальную переменную.
    """
    global out_path
    pathname.delete(0, tk.END)
    out_path = fd.askdirectory()
    pathname.insert(0, out_path)


def start() -> list:
    """
    Обработка выбранных файлов моделью YOLO8.
    Никаких параметров не принимает.
    Возвращает список созданных видеофайлов-отчётов или сообщение об ошибке.
    """
    if not files:
        mb.showerror("Ошибка", "Выберите файлы для расшифровки")
        return ["Error"]

    if not out_path:
        mb.showerror("Ошибка", "Выберите путь для записи результатов")
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


# Глобальные переменные здесь необходимы!
files = ""
out_path = ""

# Инициализация основного диалогового окна и его параметры
root = tk.Tk()
root.geometry("500x350")
root.title("Зоркий глаз")

# Изображение в левом верхнем углу
img_file = tk.PhotoImage(file="images/image.png")
tk.Button(root, image=img_file, command=about).grid(row=0,
                                                    column=0,
                                                    columnspan=2,
                                                    rowspan=8)
# Селектор выбора используемой модели
tk.Label(text="Размер модели:").grid(row=0,
                                     column=2,
                                     sticky=tk.N,
                                     padx=10)
model_size = tk.StringVar()
model_size.set("m")

tk.Radiobutton(text="Базовая",
               variable=model_size, value="n").grid(row=1,
                                                    column=2,
                                                    sticky=tk.W,
                                                    padx=10)
tk.Radiobutton(text="Малая",
               variable=model_size, value="s").grid(row=2,
                                                    column=2,
                                                    sticky=tk.W,
                                                    padx=10)
tk.Radiobutton(text="Средняя",
               variable=model_size, value="m").grid(row=3,
                                                    column=2,
                                                    sticky=tk.W,
                                                    padx=10)
# tk.Radiobutton(text="Большая",
#               variable=model_size, value="l").grid(row=4,
#                                                    column=2,
#                                                    sticky=tk.W,
#                                                    padx=10)

# Селектор выбора скорости обработки
tk.Label(text="Обработка моделью:").grid(row=0,
                                         column=3,
                                         sticky=tk.N,
                                         padx=10)
process_speed = tk.IntVar()
process_speed.set(1)

tk.Radiobutton(text="каждый кадр",
               variable=process_speed, value=1).grid(row=1,
                                                     column=3,
                                                     sticky=tk.W,
                                                     padx=10)
tk.Radiobutton(text="каждый 2-й",
               variable=process_speed, value=2).grid(row=2,
                                                     column=3,
                                                     sticky=tk.W,
                                                     padx=10)
tk.Radiobutton(text="каждый 4-й",
               variable=process_speed, value=4).grid(row=3,
                                                     column=3,
                                                     sticky=tk.W,
                                                     padx=10)
tk.Radiobutton(text="каждый 8-й",
               variable=process_speed, value=8).grid(row=4,
                                                     column=3,
                                                     sticky=tk.W,
                                                     padx=10)

# Выбор файлов для расшифровки (метка и кнопка)
tk.Label(text="").grid(row=8,
                       column=0,
                       sticky=tk.W,
                       padx=10,
                       columnspan=4)

tk.Label(text="Выберите файлы для расшифровки:").grid(row=9,
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

tk.Button(text="Выбрать файлы",
          width=15, command=insert_files).grid(row=10,
                                               column=3,
                                               sticky=tk.S,
                                               padx=10)

# Выбор пути вывода результатов
tk.Label(text="Выберите путь вывода результатов:").grid(row=12,
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

tk.Button(text="Выбрать путь",
          width=15, command=insert_path).grid(row=13,
                                              column=3,
                                              sticky=tk.S,
                                              padx=10)
tk.Label(text="").grid(row=14,
                       column=0,
                       sticky=tk.W,
                       padx=10,
                       columnspan=4)

# Чекбокс выбора вывода видео во время расшифровки
show_vid = tk.BooleanVar()
show_vid.set("False")

tk.Checkbutton(root, text="Показывать видео нарушений", variable=show_vid,
               onvalue="True", offvalue="False",).grid(row=15,
                                                       column=0,
                                                       sticky=tk.W,
                                                       padx=10,
                                                       columnspan=4)

# Главная красная кнопка запуска процесса обработки видео
start_button = tk.Button(text="Старт обработки", width=15, command=start)
start_button["bg"] = "#fa4400"
start_button.grid(row=15,
                  column=3,
                  sticky=tk.S,
                  padx=10)

root.mainloop()
