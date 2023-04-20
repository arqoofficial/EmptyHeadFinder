from ultralyticsplus import YOLO
import cv2


def load_model(model_size):
    """
    Функция используется для загрузки модели yolo8 для последующей обработки
    кадров видеоряда с её помощью. Реализуется в виде функции с присвоением
    объекта модели в глобальную переменную чтобы реализовать возможность
    выбора размера модели (передается в параметрах), а также обеспечить
    её использование в других функциях модуля
    """
    global model

    model = YOLO(model_size)

    # Установка параметров модели
    model.overrides["conf"] = 0.25  # NMS confidence threshold
    model.overrides["iou"] = 0.45  # NMS IoU threshold
    model.overrides["agnostic_nms"] = False  # NMS class-agnostic
    model.overrides["max_det"] = 1000  # maximum number of detections per image

    return "Ok"


def video_stats(vid_capture):
    """
    Определяем параметры видеофайла:
    количество кадров и скорость воспроизведения (кадр/сек)
    а также размеры кадра, возвращаем эти параметры в виде кортежа
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
    Функция обработки yolo8 для определения наличия на нём людей без каски.
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


if __name__ == "__main__":  # Тесты при запуске в качестве основного скрипта
    vid_capture = cv2.VideoCapture('2323.mp4')

    frame_width, frame_height, frame_count, fps = video_stats(vid_capture)

    print(f"Размеры кадра: ширина {frame_width}, высота: {frame_height}")
    print(f"Кол-во кадров: {frame_count}, fps: {fps}, длит-ть видео (сек.): {frame_count/fps}")

    load_model("keremberke/yolov8m-hard-hat-detection")

    img = cv2.imread("1212.jpeg")
    no_hardhat_person, hardhat_person = detect(img)
    print(no_hardhat_person, hardhat_person)
    print(f"На фото изображено {len(no_hardhat_person)} балбесов без касок,\
    и {len(hardhat_person)} ответственных работников в касках")
