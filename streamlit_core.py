"""Functions for GUI and files processing at streamlit pages"""
import os
import zipfile
from typing import Tuple

import cv2
import streamlit as st
from PIL import Image
from ultralyticsplus import YOLO, render_result

import proc as pr
from config import IMAGES_TMP_DIR, VIDEOS_TMP_DIR


def load_model_st() -> YOLO:
    """Loads a YOLOv8 model for the further photo or video processing"""
    st.sidebar.write("## Choose model")
    option = st.sidebar.selectbox(
        "**Which model would you choose?**",
        ["m - slow model", "s - faster model", "n - the fastest model"],
    )
    f"You selected: {option}"
    model_size = option[0]
    st.sidebar.write("## Set model parameters")
    model_sizes_list = ["n", "s", "m"]
    if model_size in model_sizes_list:
        model_name = f"keremberke/yolov8{model_size}-hard-hat-detection"
    else:
        raise ValueError(
            f"Input correct model size! Choose from {model_sizes_list}"
        )

    @st.cache_resource()  # for proper streamlit work
    def _load(model_name: str) -> YOLO:
        """Loads YOLO model with specific name and cashes it.
        Internal function.
        """
        model = YOLO(model_name)
        return model

    model = _load(model_name)
    if model:
        st.success("Model loaded")
    return model


def set_model_st(model: YOLO) -> YOLO:
    """Sets and overwrites model parameters using st.sidebar"""
    conf = st.sidebar.slider(
        "Select confidence threshold, %",
        0, 100, 25, step=1
    )
    iou = st.sidebar.slider(
        "Select IoU threshold, %",
        0, 100, 30, step=1
    )
    max_det = st.sidebar.slider(
        "Select maximum number of detections per image",
        0, 100, 50, step=1
    )
    agnostic_nms = st.sidebar.selectbox(
        "NMS class-agnostic",
        [False, True]
    )
    model.overrides["conf"] = conf / 100
    model.overrides["iou"] = iou / 100
    model.overrides["agnostic_nms"] = agnostic_nms
    model.overrides["max_det"] = max_det
    return model


def upload_media_st(is_photo: bool = True) -> st.file_uploader:
    """Creates st.file_uploader with predetermined files format"""
    if is_photo:
        supported_formats = ["png", "jpg", "jpeg"]
        media = "photo"
    else:
        supported_formats = ["mp4", "avi"]
        media = "video"
    supported_formats_str = ", ".join(
        str(format) for format in supported_formats
    )
    helper = f"Supported {media} formats: {supported_formats_str}"
    files = st.file_uploader(
        f"Upload your {media}(s)",
        accept_multiple_files=True,
        type=supported_formats,
        help=helper,
    )
    return files


def create_tmp_folder_st(is_photo: bool = True) -> None:
    """Creates temporary folder if it doesn't exist"""
    if is_photo:
        tmp_folder_path = IMAGES_TMP_DIR
    else:
        tmp_folder_path = VIDEOS_TMP_DIR
    if os.path.exists(tmp_folder_path):
        pass
    else:
        os.mkdir(tmp_folder_path)


def clear_tmp_st(directory: os.path) -> None:
    """Clears temporary files in tmp"""
    for file in os.scandir(directory):
        os.remove(file.path)


def set_process_speed_st():
    """Sets speed of video processing at streamlit page using st.slider"""
    process_speed = st.slider(
        "Select analysis speed",
        1, 10, 4, step=1
    )
    return process_speed


def detect_st(
    image: any,
    model: YOLO,
) -> Tuple[Image.Image, Tuple[int, int]]:
    """Analyzes image and returns tuple with render and hardhat stats"""
    results = model.predict(image)
    no_hardhat_person = []
    hardhat_person = []
    for box in results[0].boxes:
        if int(box.cls) == 1:
            no_hardhat_person.append(box.xyxy.tolist())
        elif int(box.cls) == 0:
            hardhat_person.append(box.xyxy.tolist())
    render = render_result(image, model, result=results[0])
    stats = (no_hardhat_person, hardhat_person)
    return render, stats


def video_processing_st(
    model: YOLO,
    video_file_path: os.path,
    out_path: os.path,
    process_speed: int = 1,
    show_vid: bool = False,
) -> str:
    """Main function for video processing at streamlit pages"""
    video_file_path = os.path.relpath(video_file_path)
    out_path = os.path.relpath(out_path)
    vid_capture = cv2.VideoCapture(video_file_path)
    frame_size = pr.get_video_stats(vid_capture)[0]
    filename = os.path.basename(video_file_path)
    out_file = os.path.join(out_path, f"out_{filename}")

    output = cv2.VideoWriter(
        out_file,
        cv2.VideoWriter_fourcc(*"XVID"),
        20,
        frame_size
    )
    frame_counter = 0
    record_frames_counter = 0
    while vid_capture.isOpened():
        video_available, frame = vid_capture.read()
        if video_available:
            frame_counter += 1
            if record_frames_counter <= 0:
                if frame_counter % process_speed == 0:
                    no_hardhat_person = pr.detect(frame, model)
                    if no_hardhat_person:
                        record_frames_counter = 30
            else:
                if show_vid:
                    cv2.imshow("NoHardHat", frame)
                output.write(frame)
                record_frames_counter -= 1
            key = cv2.waitKey(1)
            if (key == ord("q")) or key == 27:
                break
        else:
            break
    vid_capture.release()
    cv2.destroyAllWindows()
    return out_file


def analyze_media_st(
    files: any,
    model: YOLO,
    is_photo: bool = True,
) -> None:
    """Analyzes photo or video at streamlit page and compile zipfile"""
    if is_photo:
        media = "photo"
        tmp_folder_path = os.path.relpath(IMAGES_TMP_DIR)
    else:
        media = "video"
        tmp_folder_path = os.path.relpath(VIDEOS_TMP_DIR)
        process_speed = set_process_speed_st()
    start_button = st.button("Analyze 🎲")
    outfiles_list = []
    # Start analysis
    if start_button:
        outfiles_list = []
        clear_tmp_st(tmp_folder_path)
        if files:
            with st.spinner(text="In progress..."):
                for file in files:
                    file_name = file.name
                    file_path = os.path.join(
                        tmp_folder_path,
                        file_name
                    )
                    with open(file_path, "wb") as temp_file:
                        temp_file.write(file.read())
                    # Analyze images or videos
                    if is_photo:
                        out_image_name = f"out_{file_name}"
                        out_image_path = os.path.join(
                            tmp_folder_path,
                            out_image_name
                        )
                        render, stats = detect_st(file_path, model)
                        st.write("___")
                        st.write("## Analysed image ✅")
                        st.image(render)
                        st.markdown("### Statistics:")
                        st.markdown(
                            f"Persons without hardhat: **{len(stats[0])}**"
                        )
                        st.markdown(
                            f"Persons with hardhat: **{len(stats[1])}**"
                        )
                        render.save(out_image_path)
                        out_file = out_image_path
                    else:
                        out_file = video_processing_st(
                            model,
                            file_path,
                            tmp_folder_path,
                            process_speed=process_speed,
                        )
                    outfiles_list.append(out_file)
                    # Compile an archive of video reports
                    zip_file_path = os.path.join(
                        tmp_folder_path,
                        f"out_{media}s.zip"
                    )
                    with zipfile.ZipFile(
                        zip_file_path,
                        mode="a",
                        compression=zipfile.ZIP_DEFLATED
                    ) as zip_file:
                        zip_file.write(out_file)
        else:
            st.error("Choose file(s)")
    # Download zipfile with analised files
    if outfiles_list:
        st.success(f"The {media} report is ready", icon="✅")
        with open(zip_file_path, "rb") as zip_file:
            st.download_button(
                label="Download archive",
                data=zip_file,
                file_name=zip_file_path
            )
        clear_tmp_st(tmp_folder_path)
        outfiles_list = []
