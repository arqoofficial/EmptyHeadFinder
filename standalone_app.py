import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import media_processing as mp


def about():
    """
    Вывод информационного окна о приложении.
    Вызывается по кнопке-картинке в левом верхнем углу.
    """
    mb.showinfo("О программе", "УрФУ + Скиллфактори forever!")


def clear():
    """
    Функция очистки форм ввода файлов и пути записи результатов.
    Никаких параметров не принимает и не возвращает.
    """
    global files
    global out_path
    files = ""
    out_path = ""
    filename.delete(0, tk.END)
    pathname.delete(0, tk.END)


def insert_files():
    """
    Функция выбора файлов для расшифровки.
    Ничего не принимает на вход.
    Выбранные файлы записывает в глобальную переменную.
    """
    global files
    global out_path
    clear()
    files = fd.askopenfilenames()
    path, file = os.path.split(files[0])
    out_path = path
    filename.insert(0, files)
    pathname.insert(0, out_path)


def insert_path():
    """
    Функция выбора пути для записи результатов.
    Ничего не принимает на вход.
    Выбранную директорию записывает в глобальную переменную.
    """
    global out_path
    pathname.delete(0, tk.END)
    out_path = fd.askdirectory()
    pathname.insert(0, out_path)


def start():
    """
    Запуск модуля ... с выбранными параметрами.
    """
    if not files:
        mb.showerror("Ошибка", "Выберите файлы для расшифровки")
        return

    if not out_path:
        mb.showerror("Ошибка", "Выберите путь для записи результатов")
        return

    mp.video_processing(files,
                        model_size.get(),
                        process_speed.get(),
                        show_vid.get(),
                        out_path)

    clear()


# Глобальные переменные (я не нашёл способа обойтись без них)
files = ""
out_path = ""


# Инициализация основного диалогового окна и его основные параметры
root = tk.Tk()
root.geometry("500x350")
root.title("Зоркий глаз")

# Изображение в левом верхнем углу
img_file = tk.PhotoImage(file="images/image.png")
tk.Button(root, image=img_file, command=about).grid(
    row=0, column=0, columnspan=2, rowspan=8
)

# Селектор выбора используемой модели
tk.Label(text="Размер модели:").grid(row=0, column=2, sticky=tk.N, padx=10)
model_size = tk.StringVar()
model_size.set("keremberke/yolov8m-hard-hat-detection")
base = tk.Radiobutton(
    text="Базовая", variable=model_size,
    value="keremberke/yolov8n-hard-hat-detection"
)
small = tk.Radiobutton(
    text="Малая", variable=model_size,
    value="keremberke/yolov8s-hard-hat-detection"
)
medium = tk.Radiobutton(
    text="Средняя", variable=model_size,
    value="keremberke/yolov8m-hard-hat-detection"
)
large = tk.Radiobutton(
    text="Большая", variable=model_size,
    value="keremberke/yolov8l-hard-hat-detection"
)
base.grid(row=1, column=2, sticky=tk.W, padx=10)
small.grid(row=2, column=2, sticky=tk.W, padx=10)
medium.grid(row=3, column=2, sticky=tk.W, padx=10)
large.grid(row=4, column=2, sticky=tk.W, padx=10)

# Селектор выбора типа вывода
tk.Label(text="Обработка моделью:").grid(row=0, column=3, sticky=tk.N, padx=10)
process_speed = tk.IntVar()
process_speed.set(1)
x1 = tk.Radiobutton(text="каждый кадр", variable=process_speed, value=1)
x2 = tk.Radiobutton(text="каждый 2-й", variable=process_speed, value=2)
x4 = tk.Radiobutton(text="каждый 4-й", variable=process_speed, value=4)
x8 = tk.Radiobutton(text="каждый 8-й", variable=process_speed, value=8)
x1.grid(row=1, column=3, sticky=tk.W, padx=10)
x2.grid(row=2, column=3, sticky=tk.W, padx=10)
x4.grid(row=3, column=3, sticky=tk.W, padx=10)
x8.grid(row=4, column=3, sticky=tk.W, padx=10)

# Выбор файлов для расшифровки (метка и кнопка)
tk.Label(text="").grid(row=8, column=0, sticky=tk.W, padx=10, columnspan=4)
tk.Label(text="Выберите файлы для расшифровки:").grid(
    row=9, column=0, sticky=tk.W, padx=10, columnspan=4
)
filename = tk.Entry(width=35)
filename.grid(row=10, column=0, sticky=tk.W, padx=10, columnspan=4)
tk.Button(text="Выбрать файлы", width=15, command=insert_files).grid(
    row=10, column=3, sticky=tk.S, padx=10
)

# Выбор пути вывода результатов
tk.Label(text="Выберите путь вывода результатов:").grid(
    row=12, column=0, sticky=tk.W, padx=10, columnspan=4
)
pathname = tk.Entry(width=35)
pathname.grid(row=13, column=0, sticky=tk.W, padx=10, columnspan=4)
tk.Button(text="Выбрать путь", width=15, command=insert_path).grid(
    row=13, column=3, sticky=tk.S, padx=10
)

# Чекбокс типа отображения процесса расшифровки
tk.Label(text="").grid(row=14, column=0, sticky=tk.W, padx=10, columnspan=4)
show_vid = tk.BooleanVar()
show_vid.set("False")
show_vid_check = tk.Checkbutton(
    root,
    text="Показывать видео нарушений",
    variable=show_vid,
    onvalue="True",
    offvalue="False",
)
show_vid_check.grid(row=15, column=0, sticky=tk.W, padx=10, columnspan=4)

# Главная красная кнопка
start_button = tk.Button(text="Старт обработки",
                         width=15, command=start)
start_button["bg"] = "#fa4400"
start_button.grid(row=15, column=3, sticky=tk.S, padx=10)

root.mainloop()
