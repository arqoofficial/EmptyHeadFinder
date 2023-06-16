# EmptyHeadFinder :construction_worker:

[![Tests](https://github.com/YaRoLit/EmptyHeadFinder/actions/workflows/python-app.yml/badge.svg)](https://github.com/YaRoLit/EmptyHeadFinder/actions/workflows/python-app.yml)

## Contents

[1. App Description](https://github.com/YaRoLit/EmptyHeadFinder/blob/main/README.md#App-Description)

[2. Model in Use](https://github.com/YaRoLit/EmptyHeadFinder/blob/main/README.md#Model-in-Use)

[3. How to Try the App](https://github.com/YaRoLit/EmptyHeadFinder/blob/main/README.md#How-to-Try-the-App)

[3.1. How to Run the Pre-deployed App](https://github.com/YaRoLit/EmptyHeadFinder/blob/main/README.md#Option-1-(the-easiest-one):-Use-the-Pre-deployed-App)

[3.2. How to Run the Streamlit App](https://github.com/YaRoLit/EmptyHeadFinder/blob/main/README.md#Option-2:-Run-the-Streamlit-App)

[3.3. How to Run the Tkinter App](https://github.com/YaRoLit/EmptyHeadFinder/blob/main/README.md#Option-3:-Run-the-Tkinter-App)

[4. Authors](https://github.com/YaRoLit/EmptyHeadFinder/blob/main/README.md#Authors)


## App Description

**EmptyHeadFinder** is designed to detect people who wear a hard hat and those who do not. The app is cable of finding people with/without hard hat in a photo as well as in a video. 

The application uses the following fine-tuned YOLOv8 models:
1. [YOLOv8n](https://huggingface.co/keremberke/yolov8n-hard-hat-detection)
2. [YOLOv8s](https://huggingface.co/keremberke/yolov8s-hard-hat-detection)
3. [YOLOv8m](https://huggingface.co/keremberke/yolov8m-hard-hat-detection)


## Model in Use
<img src = 'https://github.com/YaRoLit/EmptyHeadFinder/blob/main/images/stroiteli_a.jpg' alt = 'analysed image' align='center'/>


## How to Try the App

### Option 1 (the easiest one): Use the Pre-deployed App

Check how the app works at:

http://51.250.31.169:8501/

### Option 2: Run the Streamlit App

Clone the repo

```
$ git clone git@github.com:YaRoLit/EmptyHeadFinder.git
```

Install the necessary libraries:

```
$ cd EmptyHeadFinder && pip install -r requirements.txt 
```

Launch the app:

```
$ streamlit run Welcome.py
```

### Option 3: Run the Tkinter App

Clone the repo

```
$ git clone git@github.com:YaRoLit/EmptyHeadFinder.git
```

Install the necessary libraries:

```
$ pip install tkinter 
```

Launch the app:

```
$ cd EmptyHeadFinder && python3 single.py
```

## Authors

- Yaroslav Litavrin ([YaRoLit](https://github.com/yarolit))
- Artem Golubev ([arqoofficial](https://github.com/arqoofficial))
- Tatiana Anisimova ([t-linguist](https://github.com/t-linguist))
- Pavel Okhotnikov ([PavelOkh](https://github.com/pavelokh))
