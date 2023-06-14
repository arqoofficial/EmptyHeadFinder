"""Processing functions for tkinter app (single.py) and streamlit_core.py"""
import os
from typing import Tuple

import cv2
from ultralyticsplus import YOLO


def load_model(
    model_size: str,
    conf: float = 0.3,
    iou: float = 0.45,
    agnostic_nms: bool = False,
    max_det: int = 1000,
) -> YOLO:
    """Loads a YOLOv8 model for the further photo or video processing.
    You can also specify model parameters if necessary."""
    model_sizes_list = ["n", "s", "m"]
    if model_size in model_sizes_list:
        model_name = f"keremberke/yolov8{model_size}-hard-hat-detection"
    else:
        raise ValueError(
            f"Input correct model size! Choose from {model_sizes_list}"
        )

    if 0 <= conf <= 1:
        pass
    else:
        raise ValueError(
            "Input correct conf value (should be in range [0, 1])!"
        )

    if 0 <= iou <= 1:
        pass
    else:
        raise ValueError(
            "Input correct iou value (should be in range [0, 1])!"
        )

    if isinstance(agnostic_nms, bool):
        pass
    else:
        raise ValueError(
            "Input correct agnostic_nms value (should be bool)!"
        )

    if isinstance(max_det, int) and 0 <= max_det <= 1000:
        pass
    else:
        raise ValueError(
            "Input correct max_det (should be int in range [0, 1000])!"
        )

    model = YOLO(model_name)

    model.overrides["conf"] = conf
    model.overrides["iou"] = iou
    model.overrides["agnostic_nms"] = agnostic_nms
    model.overrides["max_det"] = max_det

    return model


def get_video_stats(
    vid_capture: cv2.VideoCapture
) -> Tuple[tuple, int, float]:
    """Gets the statistic of video"""
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    fps = int(vid_capture.get(5))
    frame_count = int(vid_capture.get(7))

    frame_size = (frame_width, frame_height)
    video_time = frame_count / fps

    return frame_size, fps, video_time


def create_videoreport(
    out_path: str,
    filename: str,
    video_param: tuple
) -> cv2.VideoWriter:
    """Creates video report file"""
    frame_size = video_param[0]
    fps = video_param[1]

    out_video_path = os.path.join(out_path, f"out_{filename}")
    out_video = cv2.VideoWriter(
        out_video_path,
        cv2.VideoWriter_fourcc(*"XVID"),
        fps,
        frame_size
    )

    return out_video


def detect(image: any, model: YOLO) -> bool:
    """Using YOLOv8 model, detects people without a hardhat in the photo"""
    results = model.predict(image)

    # Iterations over tensors in order to locate the necessary objects
    for box in results[0].boxes:
        if int(box.cls) == 1:
            return True

    return False


def video_processing(
    vid_capture: cv2.VideoCapture,
    video_report: cv2.VideoWriter,
    model: YOLO,
    process_speed: int = 1,
    show_violation_frames: bool = False,
) -> None:
    """Main function of video processing"""
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
