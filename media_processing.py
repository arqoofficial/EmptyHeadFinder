from ultralyticsplus import YOLO, render_result
import cv2
import os


def load_model(
    model_size: str = "m",
    conf: int = 25,
    iou: int = 45,
    agnostic_nms: bool = False,
    max_det: int = 1000,
    with_status: bool = False,
) -> YOLO:
    """
    Loads a YOLOv8 model for the further photo or video processing.

    Args:
        * model_size (str, optional):
        size of model ("n", "s", "m"). Defaults to "m".
        * conf (int, optional): NMS confidence threshold. Defaults to 25.
        * iou (int, optional): NMS IoU threshold. Defaults to 45.
        * agnostic_nms (bool, optional): NMS class-agnostic. Defaults to False.
        * max_det (int, optional):
        Maximum number of detections per image. Defaults to 1000.
        * with_status (bool, optional): whether to return load status. Defaults to False.

    Raises:
        ValueError: Wrong size of the model

    Returns:
        YOLO: Object of YOLO class - model for hardhat detection
    """
    sizes_list = ["n", "s", "m"]
    # global model
    if model_size in sizes_list:
        model = YOLO(f"keremberke/yolov8{model_size}-hard-hat-detection")
    else:
        return f"Choose the model size {sizes_list}"

    # Setting model parameters
    model.overrides["conf"] = conf / 100  # NMS confidence threshold
    model.overrides["iou"] = iou / 100  # NMS IoU threshold
    model.overrides["agnostic_nms"] = agnostic_nms  # NMS class-agnostic
    model.overrides["max_det"] = max_det  # maximum number of detections per image

    if not with_status:
        return model
    else:
        return (model, "Ok")


def calc_time(video_stats: tuple) -> str:
    """
    Converts time from video_stats into HH:MM:SS format.

    Args:
        * video_stats (tuple): tuple from video_stats().

    Returns:
        str: Time from video_stats in HH:MM:SS format.
    """
    raw_minutes = round((video_stats[2] / video_stats[3] / 60), 2)
    hours = int(raw_minutes // 60)
    minutes = int(raw_minutes // 1)
    seconds = int(round(((raw_minutes % 1) * 60), 0))
    if minutes >= 60:
        minutes = minutes - hours * 60
    if minutes <= 9:
        minutes = f"0{minutes}"
    if seconds <= 9:
        seconds = f"0{seconds}"
    result = f"""
    resolution = {video_stats[0]}*{video_stats[1]}
    time = {hours}:{minutes}:{seconds}
    fps = {video_stats[3]}
    """
    return result


def video_stats(
                vid_capture: cv2.VideoCapture,
                with_time: bool = False
) -> tuple:
    """
    Gets video parameters (fps, number of frames and frame size)
    and returns them as a tuple.

    Args:
        * vid_capture (cv2.VideoCapture): object of cv2.VideoCapture class.
        * with_time (bool, optional): whether to return time codes. Defaults to False.

    Returns:
        tuple: (frame_width, frame_height, frame_count, fps)
    """

    if vid_capture.isOpened() is False:
        return "Error opening video file."

    else:
        frame_width = int(vid_capture.get(3))
        frame_height = int(vid_capture.get(4))
        fps = int(vid_capture.get(5))
        frame_count = int(vid_capture.get(7))

        result_tuple = (frame_width, frame_height, frame_count, fps)

        if with_time:
            return (calc_time(video_stats=result_tuple), result_tuple)
        else:
            return result_tuple


def detect(
           image: any,
           model: YOLO,
           with_render: bool = False
) -> tuple:
    """
    Using YOLOv8 model, detects people without a hard hat in the photo.
    Returns a list with coordinates of boxes with heads not wearing a hard hat.

    Args:
        * image (any): image to process. Defaults to None.
        * model (YOLO): model to use. Defaults to None.
        * with_render (bool, optional): whether to render video. Defaults to False.

    Returns:
        None
    """
    results = model.predict(image)

    no_hardhat_person = []
    hardhat_person = []

    # Iterations over tensors in order to locate the necessary objects
    for box in results[0].boxes:
        if int(box.cls) == 1:
            no_hardhat_person.append(box.xyxy.tolist())

        elif int(box.cls) == 0:
            hardhat_person.append(box.xyxy.tolist())

    return no_hardhat_person, hardhat_person

    if with_render:
        render = render_result(model=model, image=image, result=results[0])

        return render, (no_hardhat_person, hardhat_person)

    else:
        return no_hardhat_person, hardhat_person


def video_processing(
    model: YOLO,
    video_file_path: str,
    out_path: str = './',
    process_speed: int = 1,
    show_vid: bool = False,
) -> None:
    """
    Main function of video precessing.
    Gets a file list, model size, fps, path to output folder,
    and a flag whether to show the video report with results.

    Args:
        * model (YOLO): model to use.
        * video_file_path (str): path to the video.
        * out_path (str): path to the output folder. Defaults to "./".
        * process_speed (int, optional): process speed. Defaults to 1.
        * show_vid (bool, optional): whether to show video with violators. Defaults to False.

    Returns:
        Processed video report to the output folder.
    """

    vid_capture = cv2.VideoCapture(video_file_path)

    # Video stats
    frame_width, frame_height, frame_count, fps = video_stats(vid_capture)
    frame_size = (frame_width, frame_height)

    # Name for the video report
    path, filename = path_file_split(video_file_path)
    out_file = out_path + "/" + "out_" + filename

    output = cv2.VideoWriter(out_file,
                             cv2.VideoWriter_fourcc(*"XVID"),
                             20,
                             frame_size)
    # Frames counter
    frame_cnt = 0
    # Recordings counter
    rec_cnt = 0

    while vid_capture.isOpened():
        ret, frame = vid_capture.read()

        if ret:
            frame_cnt += 1
            # If a person without a hard hat is detected, abv frames start recording to the output file
            if rec_cnt <= 0:
                if (frame_cnt % process_speed) == 0:
                    no_hardhat_person, hardhat_person = detect(frame, model)
                    if no_hardhat_person:
                        # How many frames to save after detecting the violation
                        rec_cnt = 60
            else:
                # Show the video with violations
                if show_vid:
                    cv2.imshow("NoHardHat", frame)
                # Write the video into the file
                output.write(frame)
                # Reduce the counter
                rec_cnt -= 1

            key = cv2.waitKey(1)

            if (key == ord("q")) or key == 27:
                break
        else:
            break

    # Освободить объект захвата видео
    vid_capture.release()
    cv2.destroyAllWindows()

    return out_file


def path_file_split(full_path: str) -> tuple:
    """
    Splits the full file name into path and file name.
    """
    path, filename = os.path.split(full_path)

    return path, filename


def clear_tmp(dir: str) -> None:
    """
    Clears temporary files in tmp.
    """
    for file in os.scandir(dir):
        os.remove(file.path)


if __name__ == "__main__":  # Run tests if started as the main script
    model = load_model(model_size="m")
    img = cv2.imread("images/nasialnika.jpg")
    no_hardhat_person, hardhat_person = detect(image=img, model=model)
    print(
        f"There are {len(no_hardhat_person)} dummies without a hard hat,\
 and {len(hardhat_person)} responsible workers wearing a hard hat in the photo."
    )

# if __name__ == "__main__":  # To check the cycle with video

#     model = load_model(model_size="m")
#     res = video_processing(
#         model=model,
#         process_speed=1,
#         files=["/Users/artemgolubev/Desktop/CODE/GIT/EmptyHeadFinder-1/out_2323.mp4"],
#         show_vid=False,
#     )
#     print(res)
