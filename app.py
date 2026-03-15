import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("🕶️ Virtual Glasses Try-On (AR)")
st.write("Look at the camera and try virtual glasses.")

# Load face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Load glasses image with alpha channel
glasses = cv2.imread("assets/glasses.png", cv2.IMREAD_UNCHANGED)

class GlassesFilter(VideoTransformerBase):

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            # Resize glasses
            new_width = w
            new_height = int(glasses.shape[0] * (new_width / glasses.shape[1]))

            resized_glasses = cv2.resize(glasses, (new_width, new_height))

            # Position glasses slightly below forehead
            y1 = y + int(h * 0.3)
            y2 = y1 + new_height
            x1 = x
            x2 = x + new_width

            # Check frame boundaries
            if y2 > img.shape[0] or x2 > img.shape[1]:
                continue

            # Separate alpha and color channels
            alpha = resized_glasses[:, :, 3] / 255.0
            color = resized_glasses[:, :, :3]

            # Overlay glasses using alpha blending
            for c in range(3):
                img[y1:y2, x1:x2, c] = (
                    alpha * color[:, :, c] +
                    (1 - alpha) * img[y1:y2, x1:x2, c]
                )

        return img


webrtc_streamer(
    key="glasses-filter",
    video_transformer_factory=GlassesFilter
)
