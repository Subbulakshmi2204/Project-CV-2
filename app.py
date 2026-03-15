import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("🕶️ Virtual Glasses Try-On (AR)")
st.write("Look at the camera and try virtual glasses!")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

glasses = cv2.imread("assets/glasses.png", -1)

class GlassesFilter(VideoTransformerBase):

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            glass_width = w
            glass_height = int(glass_width * glasses.shape[0] / glasses.shape[1])

            resized_glass = cv2.resize(glasses, (glass_width, glass_height))

            for i in range(glass_height):
                for j in range(glass_width):

                    if resized_glass[i, j][3] != 0:
                        img[y + int(h/4) + i, x + j] = resized_glass[i, j][:3]

        return img


webrtc_streamer(
    key="glasses",
    video_transformer_factory=GlassesFilter
)
