import os
import cv2
from ultralyticsplus import YOLO

from proc import load_model,\
                 video_capture,\
                 get_video_stats,\
                 create_videoreport,\
                 detect,\
                 video_processing


def test_project_dir():
    """ Проверка целостности структуры папок проекта
    """
    assert os.path.exists("./videos")
    assert os.path.exists("./videos/output")
    assert os.path.exists("./pages")
    assert os.path.exists("./images")


def test_project_files():
    """ Проверка наличия всех критичных файлов в проекте
    """
    assert os.path.isfile("./videos/2323.mp4")
    assert os.path.isfile("./videos/Serbian.mp4")
    assert os.path.isfile("./videos/output/out_Serbian.mp4")
    assert os.path.isfile("./pages/1_Photo 📸.py")
    assert os.path.isfile("./pages/2_Video 📹.py")
    assert os.path.isfile("./images/image.png")
    assert os.path.isfile("./images/stroiteli.jpg")
    assert os.path.isfile("./images/mnogo_stroiteley.jpg")


def test_load_model():
    model_size = "keremberke/yolov8m-hard-hat-detection"

    assert load_model(model_size).overrides['conf'] == 0.3
    assert load_model(model_size).overrides['iou'] == 0.45
    assert not load_model(model_size).overrides['agnostic_nms']
    assert load_model(model_size).overrides['max_det'] == 1


def test_get_video_stats():
    video = cv2.VideoCapture("./videos/2323.mp4")

    assert get_video_stats(video) == ((1920, 1080), 25, 132.04)


def test_create_videoreport():
    create_videoreport("./videos/output",
                       "test_video.mp4",
                       ((1920, 1080), 25, 132.04))

    assert os.path.isfile("./videos/output/out_test_video.mp4")

    os.remove("./videos/output/out_test_video.mp4")


def test_detect():
    img_1 = cv2.imread("./images/stroiteli.jpg")
    img_2 = cv2.imread("./images/mnogo_stroiteley.jpg")
    model_size = "keremberke/yolov8m-hard-hat-detection"
    model = YOLO(model_size)

    assert detect(img_1, model)
    assert not detect(img_2, model)


def test_videoprocessing():
    in_video = video_capture("./videos/2323.mp4")
    out_video = create_videoreport("./videos/output",
                                   "test_video.mp4",
                                   ((1920, 1080), 25, 132.04))

    model_size = "keremberke/yolov8s-hard-hat-detection"
    model = YOLO(model_size)

    video_processing(in_video,
                     out_video,
                     model,
                     process_speed=4)

    assert os.path.isfile("./videos/output/out_test_video.mp4")
    assert os.path.getsize("./videos/output/out_test_video.mp4") == 6029356

    os.remove("./videos/output/out_test_video.mp4")
