import os

import cv2
from ultralyticsplus import YOLO


def load_model(model_size: str) -> YOLO:
    """ Loads a YOLOv8 model for the further photo or video processing"""
    model = YOLO(model_size)

    model.overrides['conf'] = 0.3
    model.overrides['iou'] = 0.45
    model.overrides['agnostic_nms'] = False
    model.overrides['max_det'] = 1000

    return model


def video_capture(video_file) -> cv2.VideoCapture:
    """ Capture the video"""
    return cv2.VideoCapture(video_file)


def get_video_stats(vid_capture: cv2.VideoCapture) -> tuple:
    """ Gets the statistic of video"""
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    fps = int(vid_capture.get(5))
    frame_count = int(vid_capture.get(7))

    frame_size = (frame_width, frame_height)
    video_time = frame_count / fps

    return frame_size, fps, video_time


def create_videoreport(out_path: str,
                       filename: str,
                       video_param: tuple) -> cv2.VideoWriter:
    """ Creates video report file"""
    frame_size = video_param[0]
    fps = video_param[1]

    report_videofile = os.path.join(out_path, f"out_{filename}")
    out_video = cv2.VideoWriter(report_videofile,
                                cv2.VideoWriter_fourcc(*"XVID"),
                                fps,
                                frame_size)
    return out_video


def video_processing(vid_capture: cv2.VideoCapture,
                     video_report: cv2.VideoWriter,
                     model: YOLO,
                     process_speed: int = 1,
                     show_violation_frames: bool = False) -> None:
    """ Main function of video processing"""
    frame_counter = 0
    record_frame_counter = 0

    while vid_capture.isOpened():
        video_available, frame = vid_capture.read()

        if video_available:
            frame_counter += 1

            if record_frame_counter:
                video_report.write(frame)
                record_frame_counter -= 1

                if show_violation_frames:
                    cv2.imshow("NoHardHat", frame)
                    cv2.waitKey(1)

                continue

            if frame_counter % process_speed:
                continue

            if detect(frame, model):
                record_frame_counter = 30

        else:
            break

    vid_capture.release()
    cv2.destroyAllWindows()


def detect(image: any, model: YOLO) -> bool:
    """Using YOLOv8 model, detects people without a hard hat in the photo"""
    results = model.predict(image)

    # Iterations over tensors in order to locate the necessary objects
    for box in results[0].boxes:
        if int(box.cls) == 1:

            return True

    return False
