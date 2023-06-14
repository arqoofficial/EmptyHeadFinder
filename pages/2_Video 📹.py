import streamlit as st

import streamlit_core as stc


st.set_page_config(
    layout="centered",
    page_title="Video",
    page_icon="📹"
)
st.write("# Video 📹")
st.write("___")

model = stc.load_model_st()
model = stc.set_model_st(model)
videos = stc.upload_media_st(is_photo=False)
stc.create_tmp_folder_st(is_photo=False)
stc.analyze_media_st(videos, model, is_photo=False)
