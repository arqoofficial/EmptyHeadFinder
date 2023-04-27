import os
import streamlit as st
import media_processing as mp
from ultralyticsplus import YOLO, render_result


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
    
    # file_name = os.path.split(file)[1]
    
    if is_photo:
        file = st.text_input(
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
        if file:
            if os.path.isfile(file):
                return file
            else:
                st.warning("Write correct path!")
                file = None
    else:
        file, out_folder = None, None
        file = st.text_input(
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
        if file:
            if os.path.isfile(file):
                helper_video = """
                Here you should paste correct path for folder of outfile
                """
                out_folder = st.text_input(
                    "Input your outfile folder path",
                    value="", # os.path.abspath("./videos/output"),
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
                if out_folder:
                    if os.path.exists(out_folder):
                        # output_file_path = os.path.abspath(
                        #     os.path.join(out_folder, f"out_{file_name}")
                        # )
                        return file, out_folder
                    else:
                        st.warning("Write correct path!")
                        out_folder = None
                        file = None
                        return file, out_folder
            else:
                st.warning("Write correct path!")
                file = None
                # out_folder = None
                return file, out_folder
        return file, out_folder


def analyze_image(
    model: YOLO = None,
    image: str = None
):
    if image is None:
        pass
    else:
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
            if image:
                results = model.predict(image)
                render = render_result(
                    model=model,
                    image=image,
                    result=results[0]
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
            else:
                st.warning("Input something above")


def set_process_speed():
    process_speed = st.slider(
        'Select analysis speed',
        1, 10, 5,
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
            if video:
                output_path = mp.video_processing(
                    model=model,
                    process_speed=process_speed,
                    files=[video],
                    out_path=out_path,
                    show_vid=False
                )
                return os.path.relpath(output_path)
            else:
                st.warning("Input something above")
                video = None
                

def show_video(
    
) -> None:
    pass
