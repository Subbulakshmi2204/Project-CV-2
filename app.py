import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("🎨 Air Canvas - Hand Gesture Drawing")
st.write("Use a **blue object or marker** to draw in the air!")

class AirCanvas(VideoTransformerBase):

    def __init__(self):
        self.points = []
        self.color = (255, 0, 0)

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img,1)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([100,150,50])
        upper_blue = np.array([140,255,255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = cv2.GaussianBlur(mask,(5,5),0)

        contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:

            c = max(contours, key=cv2.contourArea)

            if cv2.contourArea(c) > 1000:

                M = cv2.moments(c)

                if M["m00"] != 0:

                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])

                    self.points.append((cx,cy))

                    cv2.circle(img,(cx,cy),10,(0,255,0),-1)

        for i in range(1,len(self.points)):
            cv2.line(img,self.points[i-1],self.points[i],self.color,5)

        cv2.putText(img,"Draw with blue object",(20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        return img


webrtc_streamer(
    key="air-canvas",
    video_transformer_factory=AirCanvas
)
