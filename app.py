import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="AI Virtual Pet Interaction", layout="wide")

st.title("🐾 AI Virtual Pet Interaction System")
st.write("Move a **blue colored object** in front of your webcam and the virtual pet will follow it.")

run = st.checkbox("Start Camera")

FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(0)

pet_x, pet_y = 300, 300

while run:
    ret, frame = cap.read()

    if not ret:
        st.write("Camera not working")
        break

    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100,150,50])
    upper_blue = np.array([140,255,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    mask = cv2.GaussianBlur(mask,(5,5),0)

    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        if cv2.contourArea(c) > 1000:

            M = cv2.moments(c)

            if M["m00"] != 0:

                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                cv2.circle(frame,(cx,cy),10,(0,255,0),-1)

                pet_x = int(pet_x + (cx - pet_x) * 0.1)
                pet_y = int(pet_y + (cy - pet_y) * 0.1)

    cv2.circle(frame,(pet_x,pet_y),30,(0,0,255),-1)

    cv2.putText(frame,"Virtual Pet",(pet_x-40,pet_y-40),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

    FRAME_WINDOW.image(frame, channels="BGR")

cap.release()
