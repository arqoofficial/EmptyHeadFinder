import os


# Project directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Internal directories' paths
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
VIDEOS_OUT_DIR = os.path.join(VIDEOS_DIR, "output")
VIDEOS_TMP_DIR = os.path.join(VIDEOS_DIR, "tmp")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
IMAGES_TMP_DIR = os.path.join(IMAGES_DIR, "tmp")
PAGES_DIR = os.path.join(BASE_DIR, "pages")

# Project files' paths
VID_2323_PATH = os.path.join(VIDEOS_DIR, "2323.mp4")
VID_SERBIAN_PATH = os.path.join(VIDEOS_DIR, "Serbian.mp4")
VID_OUT_SERBIAN_PATH = os.path.join(VIDEOS_OUT_DIR, "out_Serbian.mp4")
IMG_CROWD_PATH = os.path.join(IMAGES_DIR, "crowd.jpg")
IMG_ICON_PATH = os.path.join(IMAGES_DIR, "icon.png")
IMG_NASIALNIKA_PATH = os.path.join(IMAGES_DIR, "nasialnika.jpg")
IMG_STROITELI_A_PATH = os.path.join(IMAGES_DIR, "stroiteli_a.jpg")
IMG_STROITELI_PATH = os.path.join(IMAGES_DIR, "stroiteli.jpg")
IMG_ZIDANE_PATH = os.path.join(IMAGES_DIR, "zidane.jpg")
PAGE_WELCOME_PATH = os.path.join(BASE_DIR, "Welcome.py")
PAGE_1_PATH = os.path.join(PAGES_DIR, "1_Photo 📸.py")
PAGE_2_PATH = os.path.join(PAGES_DIR, "2_Video 📹.py")

ABOUT = """
Program made by:
Yaroslav Litavrin
Artem Golubev
Tatiana Anisimova
Pavel Okhotnikov

Ural Federal University, 2023
"""

# Print all paths in console
if __name__ == "__main__":
    print()
    print("Project directory path:", BASE_DIR, sep="\n", end="\n\n")
    print(
        "Internal directories paths:",
        VIDEOS_DIR,
        VIDEOS_OUT_DIR,
        VIDEOS_TMP_DIR,
        IMAGES_DIR,
        IMAGES_TMP_DIR,
        PAGES_DIR,
        sep="\n",
        end="\n\n"
    )
    print(
        "Project files paths:",
        VID_2323_PATH,
        VID_SERBIAN_PATH,
        VID_OUT_SERBIAN_PATH,
        IMG_CROWD_PATH,
        IMG_ICON_PATH,
        IMG_NASIALNIKA_PATH,
        IMG_STROITELI_A_PATH,
        IMG_STROITELI_PATH,
        IMG_ZIDANE_PATH,
        PAGE_WELCOME_PATH,
        PAGE_1_PATH,
        PAGE_2_PATH,
        sep="\n",
        end="\n\n"
    )
