import os
import streamlit as st
import streamlit_core as stc
import media_processing as mp

st.set_page_config(
    layout="centered",
    page_title="Photo",
    page_icon="📸"
)

st.write("# Photo 📸")
st.write("___")

model = stc.set_model()
supported_formats = ["png", "jpg", "jpeg"]
supported_formats_str = ", ".join(str(format) for format in supported_formats)
help_image = f"Supported image formats: {supported_formats_str}"
images = st.file_uploader(
    "Upload your photo",
    accept_multiple_files=True,
    type=supported_formats,
    help=help_image
)

tmp_folder_path = os.path.relpath("./images/tmp/")
if os.path.exists(tmp_folder_path):
    pass
else:
    os.mkdir(tmp_folder_path)

analyze_button = st.button("Analyze! 🎲")
if analyze_button:
    mp.clear_tmp(tmp_folder_path)
    if images:
        for image in images:
            with st.spinner(text="In progress..."):
                image_path = os.path.join(tmp_folder_path, image.name)
                with open(image_path, "wb") as temp_file:
                    temp_file.write(image.read())
                stc.analyze_image(
                    model=model,
                    image=image_path
                )
    else:
        st.warning("Upload some images!")
mp.clear_tmp(tmp_folder_path)
