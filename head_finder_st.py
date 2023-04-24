import streamlit as st
import media_processing as mp
import cv2
from ultralyticsplus import render_result

st.set_page_config(
    layout="centered",
    page_title="Model configuration",
    page_icon="🛎"
)  # Полнооконное представление приложения

st.write("# Model configuration 👨🏾‍🔧")
st.write("___")
st.write("## There are three yolov8 models:")
st.write("* m - the slowest, but large model")
st.write("* s - medium speed, medium size model")
st.write("* n - the fastest, but small model")

option = st.selectbox(
    "**Which model would you choose?**",
    ["m - slow", "s - faster", "n - the fastest"]
)

f"You selected: {option}"

option_selected = option[0]

conf = st.slider(
    'Select confidence threshold, %',
    0, 100, 25,
    step=1
)

iou = st.slider(
    'Select IoU threshold, %',
    0, 100, 45,
    step=1
)

max_det = st.slider(
    'Select maximum number of detections per image',
    0, 100, 10,
    step=1
)

agnostic_nms = st.selectbox(
    "NMS class-agnostic",
    [False, True]
)

model = mp.load_model(
    model_size=option_selected,
    conf=conf,
    iou=iou,
    agnostic_nms=agnostic_nms,
    max_det=max_det
)

helper = """
Here you should paste correct URL of the photo you want to analyze
"""

image = st.text_input(
    "Input your image URL",
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

image_button = st.button(
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

if image_button:
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

    no_hardhat_person, hardhat_person = mp.detect(
        image=image,
        model=model
    )

    st.text(f"На фото изображено {len(no_hardhat_person)} балбесов без касок,\n\
и {len(hardhat_person)} ответственных работников в касках")


video = st.text_input(
    "Input your video path",
    value="",
    max_chars=None,
    key=None,
    type="default",
    help=None,
    autocomplete=None,
    on_change=None,
    args=None,
    kwargs=None,
    placeholder=None,
    disabled=False,
    label_visibility="visible"
)

video_button = st.button(
    "Analyze!",
    key=1,
    help=None,
    on_click=None,
    args=None,
    kwargs=None,
    type="secondary",
    disabled=False,
    use_container_width=False
)

if video_button:
    vid_capture = cv2.VideoCapture(video)
    video_stats = mp.video_stats(
        vid_capture=vid_capture,
        beatiful=True
    )
    st.text(video_stats[0])
    mp.video_processing(
        model=model,
        process_speed=1,
        files=[video],
        show_vid=True
    )
# /Users/artemgolubev/Desktop/CODE/GIT/EmptyHeadFinder-1/2323.mp4
