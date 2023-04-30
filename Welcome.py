import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.markdown(
    """
    # EmptyHeadFinder👷🏻‍♂️

    Данное приложение позволяет определять
    наличие строительных касок на фото и видео

    ## Участники проекта:

    - Анисимова Татьяна (t-linguist)
    - Голубев Артём (arqoofficial)
    - Литаврин Ярослав (YaRoLit)
    - Охотников Павел (PavelOkh)

    ## Используемые модели:

    https://huggingface.co/keremberke/yolov8n-hard-hat-detection

    https://huggingface.co/keremberke/yolov8s-hard-hat-detection

    https://huggingface.co/keremberke/yolov8m-hard-hat-detection

    ## Пример работы модели на картинке:
"""
)
stroiteli_image = Image.open("./images/stroiteli_analysed.jpg")
st.image(stroiteli_image)
