import streamlit as st
import streamlit_core as stc

st.set_page_config(
    layout="centered",
    page_title="Video",
    page_icon="📹"
)  # Полнооконное представление приложения

st.write("# Video 📹")
st.write("___")

model = stc.set_model()
if model:
    process_speed = stc.set_process_speed()
    input_video_path, output_folder_path = stc.load_file(
        is_photo=False
    )
    if input_video_path and output_folder_path:
        video = stc.analyze_video(
            model=model,
            video=input_video_path,
            process_speed=process_speed,
            out_path=output_folder_path
        )
