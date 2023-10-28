import os

import io
import cv2

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from ultralytics import YOLO
from streamlit_option_menu import option_menu
from PIL import Image, ImageEnhance, ImageFilter

#Demo for visualisation a weapon detection
def streamlit_menu():
    selected = option_menu(
        menu_title="Weapon Detection on images and videos",  
        options=["Images"], 
        icons=["card-image"],  
        menu_icon="cast",  
        default_index=0,  
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "rainbow"},
        },
    )
    return selected


selected = streamlit_menu()
class_colors = {
    0: (255, 0, 0), 
    1: (0, 255, 0), 
    2: (0, 0, 255)
}

class_font = cv2.FONT_HERSHEY_SIMPLEX
class_font_scale = 1.2

if selected == "Images":
    st.title(f"Weapon detection on {selected}")
    uploaded_files = st.file_uploader("Choose an image", accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        st.write("filename:", uploaded_file.name)
#        st.image(img)
        
        sharpened = img.filter(ImageFilter.SHARPEN)
        denoised = sharpened.filter(ImageFilter.MedianFilter(size=5))
        
        model = YOLO('best.pt')
        results = model(denoised)  
 
        for result in results:                                         
            boxes = result.boxes.cpu().numpy()
        
        img_np = np.array(denoised)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        for box in boxes:                                          
            r = box.xyxy[0].astype(int)                            
            cv2.rectangle(img_cv, (r[0], r[1]), (r[2], r[3]), (255, 255, 255), 2)
            cls = box.cls[0].astype(int)
            if cls == 0:
                label = "Man with weapon"
            if cls == 1:
                label = "Short weapons"
            if cls == 2:
                label = "Long weapons"
            box_color = class_colors.get(cls, (255, 255, 255))
            
            (label_width, label_height), _ = cv2.getTextSize(label, class_font, class_font_scale, 1)
            
            text_position = (r[0], r[1] - 3 - label_height)  

            cv2.rectangle(img_cv, (r[0], r[1]), (r[2], r[3]), box_color, 2)
            cv2.putText(img_cv, label, text_position, class_font, class_font_scale, box_color, 2)
            
        st.image(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB), use_column_width=True)
            
