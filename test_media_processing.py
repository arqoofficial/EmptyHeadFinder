import cv2
from media_processing import load_model, video_stats, detect


def test_load_model():
    assert load_model(model_size="n", with_status=True)[1] == "Ok"
    assert load_model(model_size="s", with_status=True)[1] == "Ok"
    assert load_model(model_size="m", with_status=True)[1] == "Ok"


def test_video_stats():
    vid_capture = cv2.VideoCapture("videos/2323.mp4")

    assert video_stats(vid_capture=vid_capture) == (1920, 1080, 3301, 25)


def test_detect():
    img = cv2.imread("images/stroiteli.jpg")
    no_hardhat_person, hardhat_person = detect(
        image=img,
        model=load_model(
            model_size="m"
        )
    )

    assert no_hardhat_person == ([[[44.0, 61.0, 119.0, 168.0]],
                                 [[378.0, 46.0, 460.0, 166.0]]])

    assert hardhat_person == ([[[254.0, 5.0, 364.0, 149.0]],
                              [[132.0, 35.0, 221.0, 158.0]],
                              [[474.0, 55.0, 565.0, 116.0]]])
