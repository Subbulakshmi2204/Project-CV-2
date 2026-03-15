# 🎨 Air Canvas – Hand Gesture Drawing System

## 📌 Project Overview

Air Canvas is a **computer vision based drawing application** that allows users to draw on the screen using hand gestures or a colored object. Instead of using a mouse or stylus, the user simply moves a **blue colored marker or object in front of a webcam**, and the system tracks the motion to create drawings in real time.

This project demonstrates how **OpenCV and Streamlit** can be used to build an **interactive augmented reality drawing interface**.

---

## 🚀 Features

* Real-time webcam drawing
* Color detection using HSV filtering
* Contour detection for object tracking
* Image moments to calculate the drawing point
* Smooth line drawing using tracked coordinates
* Browser-based interface using Streamlit

---

## 🧠 Technologies Used

* **Python**
* **OpenCV**
* **Streamlit**
* **NumPy**
* **WebRTC (streamlit-webrtc)**

---

## 📚 Computer Vision Concepts Used

This project demonstrates the following topics:

* Image Filtering (HSV Color Filtering)
* Contour Detection
* Contour Moments (Object Center Detection)
* Drawing Functions in OpenCV
* Real-time Video Processing

---

## 📂 Project Structure

```
air-canvas-streamlit/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/air-canvas-streamlit.git
cd air-canvas-streamlit
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

---

## 🎯 How It Works

1. The webcam captures live video frames.
2. Frames are converted into **HSV color space**.
3. A **blue colored object** is detected using color filtering.
4. The system finds the **largest contour** of the detected object.
5. Using **image moments**, the center of the object is calculated.
6. The movement of the object is used to **draw lines on the screen**.

---

## 📸 Expected Output

* Webcam opens in a Streamlit web interface.
* When a **blue marker or object** is moved in front of the camera, the system detects it.
* The movement is tracked and used to **draw lines in the air**.

This creates a **virtual drawing experience using hand gestures**.

---

## 🌍 Deployment

This project can be deployed easily using:

* **Streamlit Cloud**
* **GitHub**

Steps:

1. Push the project to GitHub
2. Go to **https://streamlit.io/cloud**
3. Connect your GitHub repository
4. Deploy `app.py`

---

## 🔮 Future Improvements

Possible enhancements include:

* Multiple drawing colors
* Gesture-based eraser
* Finger tracking without marker
* Save drawings as images
* AI-based hand gesture recognition

---

## 👩‍💻 Author

Developed as a **Computer Vision mini project using OpenCV and Streamlit**.

---
