import os
import streamlit as st
import streamlit_core as stc
import media_processing as mp

st.set_page_config(
    layout="centered",
    page_title="Video",
    page_icon="📹"
)  # Полнооконное представление приложения

st.write("# Video 📹")
st.write("___")

model = stc.set_model()
process_speed = stc.set_process_speed()
video, out_path = stc.load_file(is_photo=False)
if video and out_path:
    with st.spinner(text="In progress..."):
        result_video = stc.analyze_video(
            model=model,
            video=video,
            process_speed=process_speed,
            out_path=out_path
        )
    if result_video:
        st.success(f"Done! Out video is here: {result_video}")
        show_button = st.button("Show result wideo?")
        if show_button:
            show_video = open(result_video, "rb")
            show_video_bytes = show_video.read()
            st.video(show_video_bytes)