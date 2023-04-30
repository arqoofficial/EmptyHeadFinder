import streamlit as st
import streamlit_core as stc

st.set_page_config(
    layout="centered",
    page_title="Photo",
    page_icon="📸"
)  # Полнооконное представление приложения

st.write("# Photo 📸")
st.write("___")

model = stc.set_model()
image = stc.load_file(is_photo=True)
if image:
    analyze = stc.analyze_image(
        model=model,
        image=image
    )
