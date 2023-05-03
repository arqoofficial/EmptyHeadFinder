import os
import streamlit as st
import streamlit_core as stc
import media_processing as mp
import zipfile


st.set_page_config(
    layout="centered",
    page_title="Video",
    page_icon="📹"
)  # Полнооконное представление приложения


st.write("# Video 📹")
st.write("___")


model = stc.set_model()

process_speed = stc.set_process_speed()

supported_formats = ["mp4", "avi"]
supported_formats_str = ", ".join(str(format) for format in supported_formats)
help_video = f"Supported video formats: {supported_formats_str}"

video_files = st.file_uploader(
    "Upload your video file(s)",
    accept_multiple_files=True,
    type=supported_formats,
    help=supported_formats_str
)
temp_folder_path = os.path.relpath("./videos/tmp")
start_button = st.button("Analyze 🎲")
outfiles_list = []

if start_button:
    outfiles_list = []
    mp.clear_tmp(temp_folder_path)

    if video_files:
        with st.spinner(text="In progress..."):
            for video_file in video_files:
                video_file_path = os.path.join(
                    temp_folder_path, video_file.name)
                with open(video_file_path, "wb") as temp_file:
                    temp_file.write(video_file.read())

                out_file = mp.video_processing(
                    model,
                    video_file_path,
                    out_path=temp_folder_path,
                    process_speed=process_speed
                )

                outfiles_list.append(out_file)

                # создаем архив видеоотчётов для выгрузки одним файлом
                zip_file_path = os.path.relpath("./videos/tmp/out_videos.zip")
                with zipfile.ZipFile(
                    zip_file_path,
                    mode="a",
                    compression=zipfile.ZIP_DEFLATED
                ) as zip_file:
                    zip_file.write(out_file)
    else:
        st.error("Choose file(s)")


if outfiles_list:
    st.success("The video report is ready", icon="✅")
    with open(zip_file_path, "rb") as zip_file:
        download_button = st.download_button(
            label="Download archive",
            data=zip_file,
            file_name=zip_file_path
        )
    mp.clear_tmp(temp_folder_path)
    outfiles_list = []
