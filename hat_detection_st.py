import streamlit as st
import pandas as pd
import numpy as np
import time

from ultralyticsplus import YOLO, render_result

st.set_page_config(
    layout="centered", 
    page_title="Model configuration", 
    page_icon="🛎"
)   # Полнооконное представление приложения


st.write("# Model configuration 👨🏾‍🔧")
st.write("___")
st.write("## There are three yolov8 models:")
st.write("* m - the slowest, but large model")
st.write("* s - medium speed, medium size model")
st.write("* n - the fastest, but small model")

option = st.selectbox(
    "**Which model would you choose?**",
    ["m - slow", "s - faster", "n - the fastes"]
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

st.write("___")
st.write("## Set model parameters")

conf = st.slider(
    'Select confidence threshold, %',
    0, 100, (25),
    step=1
)

iou = st.slider(
    'Select IoU threshold, %',
    0, 100, (45),
    step=1
)

max_det = st.slider(
    'Select maximum number of detections per image',
    0, 100, (10),
    step=1
)

agnostic_nms = st.selectbox(
    "NMS class-agnostic",
    [False, True]
)

model.overrides["conf"] = conf/100  # NMS confidence threshold
model.overrides["iou"] = iou/100  # NMS IoU threshold
model.overrides["agnostic_nms"] = agnostic_nms  # NMS class-agnostic
model.overrides["max_det"] = max_det  # maximum number of detections per image

st.write("___")
st.write("# Load image 👷🏻‍♂️")

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