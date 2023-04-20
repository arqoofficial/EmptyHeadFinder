from ultralyticsplus import YOLO
import cv2
import os


def load_model(
    model_size: str = "m",
    conf: int = 25,
    iou: int = 45,
    agnostic_nms: bool = False,
    max_det: int = 1000
) -> YOLO:
    """
    Функция используется для загрузки модели yolo8 для последующей обработки
    фото или кадров видеоряда с её помощью.
    
    Args:
        model_size (str, optional): Choose size of model from ["n", "s", "m"]. Defaults to "m".
        conf (int, optional): NMS confidence threshold. Defaults to 25.
        iou (int, optional): NMS IoU threshold. Defaults to 45.
        agnostic_nms (bool, optional): NMS class-agnostic. Defaults to False.
        max_det (int, optional): Maximum number of detections per image. Defaults to 1000.

    Raises:
        ValueError: if you choose wrong model size raises ValueError

    Returns:
        YOLO: Object of YOLO class - model for hardhat detection
    """
    sizes_list = ["n", "s", "m"]
    # global model
    if model_size in sizes_list:
        model = YOLO(f"keremberke/yolov8{model_size}-hard-hat-detection")
    else:
        raise ValueError(f"Choose from these options {sizes_list}")

    # Установка параметров модели
    model.overrides["conf"] = conf/100  # NMS confidence threshold
    model.overrides["iou"] = iou/100  # NMS IoU threshold
    model.overrides["agnostic_nms"] = agnostic_nms  # NMS class-agnostic
    model.overrides["max_det"] = max_det  # maximum number of detections per image

    return model


def video_stats(vid_capture):
    """
    Определяем параметры видео, которое передается в качестве аргумента:
    количество кадров и скорость воспроизведения (fps), а также размеры кадра,
    возвращаем эти параметры в виде кортежа
    """

    if vid_capture.isOpened() is False:
        return "Ошибка открытия видеофайла"

    else:
        frame_width = int(vid_capture.get(3))
        frame_height = int(vid_capture.get(4))
        fps = int(vid_capture.get(5))
        frame_count = int(vid_capture.get(7))

        return (frame_width, frame_height, frame_count, fps)


def detect(img):
    """
    Функция обнаружения в кадре людей без каски с помощью yolo8.
    Принимает в качестве аргумента изображение (кадр из видеоряда)
    Возвращает список, содержащий координаты ограничивающих рамок
    с изображением голов, на которых каска не выявлена
    """
    results = model.predict(img)

    no_hardhat_person = []
    hardhat_person = []
    # Перебираем тензоры в целях обнаружения нужных нам объектов
    for box in results[0].boxes:
        if int(box.cls) == 1:
            no_hardhat_person.append(box.xyxy.tolist())  # float(box.conf),

        elif int(box.cls) == 0:
            hardhat_person.append(box.xyxy.tolist())  # float(box.conf),

    return no_hardhat_person, hardhat_person


def video_processing(
    files, 
    model_size, 
    process_speed, 
    show_vid, 
    out_path
):
    """
    Основная функция обработки видео. В качестве параметров получает:
    список файлов, размер модели, скорость обработки, флаг для показа видео
    с нарушениями в ходе обработки (True - показывать, False - нет),
    путь для записи итогового видеофайла.
    """
    # Грузим модель
    load_model(model_size)

    for file in files:
        vid_capture = cv2.VideoCapture(file)

        # Выводим статистику по видеофайлу
        frame_width, frame_height, frame_count, fps = video_stats(vid_capture)
        frame_size = (frame_width, frame_height)

        # Определяем имя для видеофайла-отчёта
        path, filename = os.path.split(file)
        out_file = "out_" + filename
        output = cv2.VideoWriter(
            out_path + "/" + out_file,
            cv2.VideoWriter_fourcc(*"XVID"),
            20, frame_size
        )

        # счётчик кадров
        frame_cnt = 0

        # счетчик записи
        rec_cnt = 0

        while vid_capture.isOpened():
            ret, frame = vid_capture.read()

            if ret:
                frame_cnt += 1

                # Если на видео будет обнаружен объект без каски,
                # с этого момента начинается запись abv количества кадров
                # в выходной видеофайл. Это сделано, чтобы в видео сохранялись
                # не единичные картинки, а полноценный видеоряд
                if rec_cnt <= 0:

                    if (frame_cnt % process_speed) == 0:
                        no_hardhat_person, hardhat_person = detect(frame)

                        if no_hardhat_person:
                            # Тут указываем, сколько кадров сохранить в файле
                            # с моментa обнаружения нарушения
                            rec_cnt = 60
                else:
                    # Выводим видео с нарушениями (если есть соответствующая
                    # галочка в диалоговом окне)
                    if show_vid:
                        cv2.imshow("NoHardHat", frame)
                    # Пишем видео в файл
                    output.write(frame)
                    # Уменьшаем счётчик
                    rec_cnt -= 1

                key = cv2.waitKey(1)

                if (key == ord("q")) or key == 27:
                    break
            else:
                break

        # Освободить объект захвата видео
        vid_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":  # Тесты при запуске в качестве основного скрипта

    model = load_model(model_size="m")
    img = cv2.imread("1212.jpeg")
    no_hardhat_person, hardhat_person = detect(img)
    print(f"На фото изображено {len(no_hardhat_person)} балбесов без касок,\
    и {len(hardhat_person)} ответственных работников в касках")
