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

outfiles_list = []

video_files = st.file_uploader("Загрузите видеофайл(ы)",
                               accept_multiple_files=True,
                               type=["mp4", "avi"],
                               help="поддерживаются только mp4 и avi")

start_btn = st.button("Старт обработки")

if start_btn:
    outfiles_list = []
    mp.clear_tmp("./videos/tmp")

    if len(video_files) > 0:
        with st.spinner(text="In progress..."):
            for video_file in video_files:
                with open(f"./videos/tmp/{video_file.name}", "wb") as temp_file:
                    temp_file.write(video_file.read())

                out_file = mp.video_processing(f"./videos/tmp/{video_file.name}",
                                               out_path="./videos/tmp",
                                               model=model,
                                               process_speed=process_speed)

                outfiles_list.append(out_file)

                # создаем архив видеоотчётов для выгрузки одним файлом
                with zipfile.ZipFile('./videos/tmp/out_videos.zip',
                                     mode='a',
                                     compression=zipfile.ZIP_DEFLATED) as zf:

                    zf.write(out_file)

    elif len(video_files) == 0:
        st.error("Выберите файл")


if len(outfiles_list) > 0:
    st.success("Видеофайл(ы) отчёта подготовлен(ы)", icon="✅")

    with open('./videos/tmp/out_videos.zip', "rb") as zf:
        download_btn = st.download_button(
                           label="Загрузить архив видеотчётов",
                           data=zf,
                           file_name='./videos/tmp/out_videos.zip')
