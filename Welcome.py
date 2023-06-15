import streamlit as st
from PIL import Image

from config import IMG_STROITELI_A_PATH


st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.markdown(
    """
    # EmptyHeadFinder :construction_worker:

    **EmptyHeadFinder** is designed to detect people
     who wear a hard hat and those who do not.

    The application uses the following fine-tuned YOLOv8 models:
    1. [YOLOv8n](https://huggingface.co/keremberke/yolov8n-hard-hat-detection)
    2. [YOLOv8s](https://huggingface.co/keremberke/yolov8s-hard-hat-detection)
    3. [YOLOv8m](https://huggingface.co/keremberke/yolov8m-hard-hat-detection)

    ## Authors:

    - Yaroslav Litavrin ([YaRoLit](https://github.com/yarolit))
    - Artem Golubev ([arqoofficial](https://github.com/arqoofficial))
    - Tatiana Anisimova ([t-linguist](https://github.com/t-linguist))
    - Pavel Okhotnikov ([PavelOkh](https://github.com/pavelokh))

    ## Model in Use

    """
)

stroiteli_image = Image.open(IMG_STROITELI_A_PATH)
st.image(stroiteli_image)
