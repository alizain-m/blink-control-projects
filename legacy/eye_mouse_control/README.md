# Eye-Controlled Mouse (Face Mesh Prototype)

This project uses [MediaPipe's Face Mesh](https://google.github.io/mediapipe/solutions/face_mesh) and OpenCV to capture facial landmarks in real time from your webcam. It's a foundational step toward building an eye-controlled mouse or gaze-based interaction system.

## Features

- Real-time webcam capture using OpenCV
- Real-time facial landmark detection using MediaPipe
- Safety check for empty webcam frames
- Right eye tracking to control the mouse cursor
- Blink-based clicking using eyelid landmarks (preliminary)
- ESC key to cleanly exit the app

## Requirements

- Python 3.7+
- [OpenCV](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://pypi.org/project/mediapipe/)
- pyautogui (used to control mouse movements and simulate clicks)

## Installation

Install dependencies:
bash
pip install opencv-python mediapipe pyautogui numpy
## Usage

Run the script:
bash
python main.py
- A window will display your webcam feed.
- Facial landmark data is printed to the terminal.
- Press ESC to exit the application.

## Notes for macOS Users

- If you're on macOS, make sure Python has camera permissions & accessibility permissions:
    - Go to **System Preferences >  Privacy & Security > Camera**
and grant access to your terminal or VSCode (whichever you're using).

    - Go to **System Preferences > Privacy & Security > Accessibility**
and grant access to your terminal or VSCode (whichever you're using).

- Blink detection is currently based on vertical eyelid distance (landmarks 145 and 159) and may be sensitive to lighting and head angle.

- Cursor control is based on one eye; performance may vary depending on webcam resolution and positioning.

## Roadmap

- [x] Move mouse pointer using eye tracking
- [x] Blink-to-click functionality
- [ ] Improve blink detection using Eye Aspect Ratio (EAR)
- [ ] Add smoothing and stabilization to cursor movement
- [ ] Calibrate eye-to-screen mapping
- [ ] Support click-and-drag gestures