import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("📚 Interactive AR Educational System")
st.write("Show a **triangle, square, or circle card** to the camera to see educational information.")

class ShapeAR(VideoTransformerBase):

    def detect_shape(self, contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        sides = len(approx)

        if sides == 3:
            return "Triangle"
        elif sides == 4:
            return "Square"
        elif sides > 6:
            return "Circle"
        else:
            return "Unknown"

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)

        _, thresh = cv2.threshold(blur, 60,255,cv2.THRESH_BINARY)

        contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:

            if cv2.contourArea(c) < 2000:
                continue

            shape = self.detect_shape(c)

            M = cv2.moments(c)

            if M["m00"] == 0:
                continue

            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.drawContours(img,[c],-1,(0,255,0),3)

            text = ""

            if shape == "Triangle":
                text = "Triangle: Area = 1/2 * base * height"
            elif shape == "Square":
                text = "Square: Area = side^2"
            elif shape == "Circle":
                text = "Circle: Area = π r^2"

            cv2.putText(img,shape,(cx-50,cy),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)

            cv2.putText(img,text,(30,40),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

        return img


webrtc_streamer(
    key="ar-education",
    video_transformer_factory=ShapeAR
)
