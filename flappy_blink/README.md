# Flappy Blink 🐦

A playful twist on Flappy Bird, controlled entirely by your eyes. This game uses MediaPipe's Face Mesh and OpenCV to detect blinks in real-time, allowing you to flap the bird and avoid pipes — no hands required.

## Features

- Real-time webcam input using OpenCV
- Blink detection using Eye Aspect Ratio (EAR)
- Hands-free gameplay: blink to flap!
- Dynamic difficulty: pipes get tighter as your score increases
- Game state management with start, play, and game-over screens
- Persistent high score tracking
- FPS display for performance monitoring

## Requirements

- Python 3.7+
- [OpenCV](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://pypi.org/project/mediapipe/)
- [Pygame](https://pypi.org/project/pygame/)

## Installation

Install dependencies:

```bash
pip install opencv-python mediapipe pygame pyautogui
```

## Usage

Run the script:

```bash
python flappy_blink.py
```

- Blink to make the bird flap.
- Avoid the pipes.
- Try to beat your high score!
- Press any key to start or restart.

## Notes for macOS Users

Be sure to give your terminal or code editor permission to use the webcam and control accessibility:
- System Settings > Privacy & Security > Camera

- System Settings > Privacy & Security > Accessibility

## Known Limitations

Blink detection may be affected by lighting conditions and head angle.

Works best with a stable, well-lit webcam setup.

Not optimized for multi-player (unless you’ve got two faces 😅)

## Roadmap

- [x] Blink-based control
- [x] Game over + restart screen
- [x] Difficulty scaling by score
- [x] Persistent high score
- [ ] Add sound effects
- [ ] Multiple difficulty modes
- [ ] UI skin/theme customization
- [ ] Optional keyboard controls