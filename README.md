#  Gesture Volume Control

Control your system’s volume using simple hand gestures—with Python, OpenCV, and MediaPipe.

---

##  Overview

This project uses real-time hand landmark detection to measure the distance between your thumb and index finger, then maps that gesture to system volume levels. A fun, intuitive, and sleek way to adjust volume without touching your device.

---

##  Features
  
- Maps finger distance to system volume range (e.g., min to max)  
- Smooth, real-time volume control via webcam input  
- Visual feedback: circles on finger tips, line between them, optional volume percentage display  

---

##  Requirements

- Python 3.x  
- Required libraries:
  - `opencv-python`
  - `mediapipe`
  - `numpy`
  - System audio control packages (e.g., `pycaw`, `comtypes`)
- (Optional) `ctypes`, `screen_brightness_control` depending on enhancements

Example install command:
```bash
pip install opencv-python mediapipe numpy pycaw comtypes
