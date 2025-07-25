import cv2
import mediapipe as mp
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Setup webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Mediapipe hands setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Pycaw setup for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volumeControl = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volumeControl.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

lastVol = None  # Store last adjusted volume

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    handDetected = False

    if results.multi_hand_landmarks:
        handDetected = True
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        # Get thumb tip (id 4) and index tip (id 8)
        if len(lmList) >= 9:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            # Draw circles and line
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # Distance between fingers
            length = math.hypot(x2 - x1, y2 - y1)

            # Convert length to volume
            vol = np.interp(length, [30, 200], [minVol, maxVol])
            volumeControl.SetMasterVolumeLevel(vol, None)
            lastVol = vol  # Save latest volume

            # Volume Bar UI
            volBar = np.interp(length, [30, 200], [400, 150])
            volPer = np.interp(length, [30, 200], [0, 100])
            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    else:
        # No hand detected, maintain last volume (do nothing)
        if lastVol is not None:
            volumeControl.SetMasterVolumeLevel(lastVol, None)

    cv2.imshow("Gesture Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
