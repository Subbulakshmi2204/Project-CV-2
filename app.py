import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("🐾 AI Virtual Pet Interaction")

class PetTracker(VideoTransformerBase):

    def __init__(self):
        self.pet_x = 300
        self.pet_y = 300

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = cv2.flip(img, 1)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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

                    cv2.circle(img,(cx,cy),10,(0,255,0),-1)

                    self.pet_x = int(self.pet_x + (cx - self.pet_x) * 0.1)
                    self.pet_y = int(self.pet_y + (cy - self.pet_y) * 0.1)

        cv2.circle(img,(self.pet_x,self.pet_y),30,(0,0,255),-1)

        cv2.putText(img,"Virtual Pet",(self.pet_x-40,self.pet_y-40),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

        return img


webrtc_streamer(
    key="pet-tracker",
    video_transformer_factory=PetTracker
)
