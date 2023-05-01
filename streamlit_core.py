import os
import streamlit as st
import media_processing as mp
from ultralyticsplus import YOLO


def set_model():
    st.sidebar.write("## Choose model")
    option = st.sidebar.selectbox(
        "**Which model would you choose?**",
        ["m - slow model", "s - faster model", "n - the fastest model"]
    )

    f"You selected: {option}"

    option_selected = option[0]

    # load model
    if option_selected:
        st.write(option)

        @st.cache_resource()
        def load_model():
            return YOLO(
                f"keremberke/yolov8{option_selected}-hard-hat-detection"
            )

        model = load_model()
    else:
        model = YOLO("keremberke/yolov8n-hard-hat-detection")

    st.sidebar.write("## Set model parameters")

    conf = st.sidebar.slider(
        'Select confidence threshold, %',
        0, 100, 25,
        step=1
    )

    iou = st.sidebar.slider(
        'Select IoU threshold, %',
        0, 100, 45,
        step=1
    )

    max_det = st.sidebar.slider(
        'Select maximum number of detections per image',
        0, 100, 50,
        step=1
    )

    agnostic_nms = st.sidebar.selectbox(
        "NMS class-agnostic",
        [False, True]
    )
    model.overrides["conf"] = conf / 100  # NMS confidence threshold
    model.overrides["iou"] = iou / 100  # NMS IoU threshold
    model.overrides["agnostic_nms"] = agnostic_nms  # NMS class-agnostic
    # maximum number of detections per image
    model.overrides["max_det"] = max_det

    if model:
        st.success("Model loaded")
    return model


def load_file(
    is_photo: bool = True
) -> None:
    helper = """
    Here you should paste correct path of the file you want to analyze
    """
    if is_photo:
        input_file_path = st.text_input(
            "Input your file path",
            value="",
            max_chars=None,
            key=None,
            type="default",
            help=helper,
            autocomplete=None,
            on_change=None,
            args=None,
            kwargs=None,
            placeholder=None,
            disabled=False,
            label_visibility="visible"
        )
        if input_file_path:
            input_file_path = os.path.abspath(input_file_path)
            if os.path.isfile(input_file_path):
                return input_file_path
            else:
                st.warning("Write correct path!")
                input_file_path = None
    else:
        input_file_path, output_folder_path = None, None
        input_file_path = st.text_input(
            "Input your file path",
            value="",
            max_chars=None,
            key=None,
            type="default",
            help=helper,
            autocomplete=None,
            on_change=None,
            args=None,
            kwargs=None,
            placeholder=None,
            disabled=False,
            label_visibility="visible"
        )
        if input_file_path:
            input_file_path = os.path.abspath(input_file_path)
            if os.path.isfile(input_file_path):
                helper_video = """
                Here you should paste correct path for folder of outfile
                """
                output_folder_path = st.text_input(
                    "Input your outfile folder path",
                    value="",
                    max_chars=None,
                    key=None,
                    type="default",
                    help=helper_video,
                    autocomplete="",
                    on_change=None,
                    args=None,
                    kwargs=None,
                    placeholder=None,
                    disabled=False,
                    label_visibility="visible"
                )
                if output_folder_path:
                    output_folder_path = os.path.abspath(output_folder_path)
                    if os.path.exists(output_folder_path):
                        return input_file_path, output_folder_path
                    else:
                        st.warning("Write correct path!")
                        input_file_path, output_folder_path = None, None
                        return input_file_path, output_folder_path
            else:
                st.warning("Write correct path!")
                input_file_path, output_folder_path = None, None
                return input_file_path, output_folder_path
        return input_file_path, output_folder_path


def analyze_image(
    model: YOLO = None,
    image: str = None
):
    if image is None:
        pass
    else:
        analyze_button = st.button(
            "Analyze! 🎲",
            key=1,
            help=None,
            on_click=None,
            args=None,
            kwargs=None,
            type="secondary",
            disabled=False,
            use_container_width=False
        )

        if analyze_button:
            if image:
                render, stats = mp.detect(
                    image=image,
                    model=model,
                    with_render=True
                )
                st.write("___")
                st.write("## Analysed image ✅")
                st.image(
                    render,
                    caption=None,
                    width=None,
                    use_column_width=None,
                    clamp=False,
                    channels="RGB",
                    output_format="auto"
                )
                st.markdown("### Statistics:")
                st.markdown(f"Persons with hardhat: **{len(stats[1])}**")
                st.markdown(f"Persons without hardhat: **{len(stats[0])}**")
            else:
                st.warning("Input something above")


def set_process_speed():
    process_speed = st.slider(
        'Select analysis speed',
        1, 10, 4,
        step=1
    )
    return process_speed


def analyze_video(
    model: YOLO = None,
    video: str = None,
    process_speed: int = 5,
    out_path: str = "./"
):
    if video is None:
        pass
    else:
        # output_video_path = False
        analyze_button = st.button(
            "Analyze! 🎲",
            key=None,
            help=None,
            on_click=None,
            args=None,
            kwargs=None,
            type="secondary",
            disabled=False,
            use_container_width=False
        )
        if analyze_button:
            with st.spinner(text="In progress..."):
                output_video_path = mp.video_processing(
                    model=model,
                    process_speed=process_speed,
                    video_file_path=video,
                    out_path=out_path,
                    show_vid=False
                )
            if output_video_path:
                st.success(f"Done! Out video is here:\n\n{output_video_path}")
                show_video = open(output_video_path, "rb")
                show_video_bytes = show_video.read()
                st.video(show_video_bytes)
