# Eye-Controlled Mouse (Face Mesh Prototype)

This project uses [MediaPipe's Face Mesh](https://google.github.io/mediapipe/solutions/face_mesh) and OpenCV to capture facial landmarks in real time from your webcam. It's a foundational step toward building an eye-controlled mouse or gaze-based interaction system.

## Features

- Real-time webcam capture using OpenCV
- Face landmark detection using MediaPipe's Face Mesh
- Safety check for empty webcam frames
- ESC key to exit cleanly

## Requirements

- Python 3.7+
- [OpenCV](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://pypi.org/project/mediapipe/)

## Installation

Install dependencies:

```bash
pip install opencv-python mediapipe
```

## Usage


Run the script:

```bash
python main.py
```

- A window will display your webcam feed.
- Facial landmark data is printed to the terminal.
- Press ESC to exit the application.

## Notes for macOS Users

If you're on macOS, make sure Python has camera permissions:

Go to **System Preferences > Security & Privacy > Camera**
and grant access to your terminal or VSCode (whichever you're using).

## Roadmap

- Overlay facial landmarks visually on the webcam feed
- Map eye movement to cursor position
- Implement blink detection for clicking
- Add calibration mode for screen mapping

