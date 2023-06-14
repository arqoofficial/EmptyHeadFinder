import streamlit as st

import streamlit_core as stc


st.set_page_config(
    layout="centered",
    page_title="Photo",
    page_icon="📸"
)
st.write("# Photo 📸")
st.write("___")

model = stc.load_model_st()
model = stc.set_model_st(model)
images = stc.upload_media_st()
stc.create_tmp_folder_st()
stc.analyze_media_st(images, model)
