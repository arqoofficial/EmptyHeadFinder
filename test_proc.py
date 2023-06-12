import os
import cv2

from config import (
    # Internal directories' paths
    VIDEOS_DIR,
    VIDEOS_OUT_DIR,
    IMAGES_DIR,
    PAGES_DIR,
    # Project files' paths
    VID_2323_PATH,
    VID_SERBIAN_PATH,
    VID_OUT_SERBIAN_PATH,
    IMG_CROWD_PATH,
    IMG_ICON_PATH,
    IMG_NASIALNIKA_PATH,
    IMG_STROITELI_A_PATH,
    IMG_STROITELI_PATH,
    IMG_ZIDANE_PATH,
    PAGE_WELCOME_PATH,
    PAGE_1_PATH,
    PAGE_2_PATH,
)

from proc import (
    load_model,
    get_video_stats,
    create_videoreport,
    detect,
    video_processing
)

def test_project_dir():
    assert os.path.exists(VIDEOS_DIR)
    assert os.path.exists(VIDEOS_OUT_DIR)
    assert os.path.exists(PAGES_DIR)
    assert os.path.exists(IMAGES_DIR)


def test_project_files():
    # Check videos
    assert os.path.isfile(VID_2323_PATH)
    assert os.path.isfile(VID_SERBIAN_PATH)
    assert os.path.isfile(VID_OUT_SERBIAN_PATH)
    # Check images
    assert os.path.isfile(IMG_ICON_PATH)
    assert os.path.isfile(IMG_STROITELI_PATH)
    assert os.path.isfile(IMG_STROITELI_A_PATH)
    assert os.path.isfile(IMG_CROWD_PATH)
    assert os.path.isfile(IMG_ZIDANE_PATH)
    assert os.path.isfile(IMG_NASIALNIKA_PATH)
    # Check pages
    assert os.path.isfile(PAGE_1_PATH)
    assert os.path.isfile(PAGE_2_PATH)
    assert os.path.isfile(PAGE_WELCOME_PATH)

def test_load_model():
    model_size = "m"

    assert load_model(model_size).overrides['conf'] == 0.3
    assert load_model(model_size).overrides['iou'] == 0.45
    assert not load_model(model_size).overrides['agnostic_nms']
    assert load_model(model_size).overrides['max_det'] == 1000


def test_get_video_stats():
    video = cv2.VideoCapture(VID_2323_PATH)

    assert get_video_stats(video) == ((1920, 1080), 25, 132.04)


def test_create_videoreport():
    in_video_name = "test_video.mp4"
    create_videoreport(
        VIDEOS_OUT_DIR,
        in_video_name,
        ((1920, 1080), 25, 132.04)
    )
    out_video_name = f"out_{in_video_name}"
    out_video_path = os.path.join(VIDEOS_OUT_DIR, out_video_name)
    
    assert os.path.isfile(out_video_path)

    os.remove(out_video_path)


def test_detect():
    img_1 = cv2.imread(IMG_STROITELI_PATH)
    img_2 = cv2.imread(IMG_CROWD_PATH)
    model_size = "m"
    model = load_model(model_size)

    assert detect(img_1, model)
    assert not detect(img_2, model)


def test_video_processing():
    in_video_name = "test_video.mp4"
    in_video = cv2.VideoCapture(VID_2323_PATH)
    out_video = create_videoreport(
        VIDEOS_OUT_DIR,
        in_video_name,
        ((1920, 1080), 25, 132.04)
    )
    
    out_video_name = f"out_{in_video_name}"
    out_video_path = os.path.join(VIDEOS_OUT_DIR, out_video_name)
    
    model_size = "s"
    model = load_model(model_size)

    video_processing(in_video,
                     out_video,
                     model,
                     process_speed=4)

    assert os.path.isfile(out_video_path)
    assert os.path.getsize(out_video_path) == 6029356

    os.remove(out_video_path)
