# Hand Gesture Mouse Control

A Python application that allows you to control your computer's mouse using hand gestures captured through your webcam.

## Features

- Move cursor using index finger
- Left click gesture
- Right click gesture
- Double click gesture
- Screenshot capture gesture

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- MediaPipe
- PyAutoGUI
- NumPy
- pynput

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install opencv-python mediapipe pyautogui numpy pynput
```

## Usage

Run the application:
```bash
python main.py
```

### Gesture Controls

1. **Mouse Movement**: Point your index finger with thumb close to palm
2. **Left Click**: Bend index finger while keeping middle finger straight
3. **Right Click**: Bend middle finger while keeping index finger straight
4. **Double Click**: Bend both index and middle fingers with thumb away
5. **Screenshot**: Bend both index and middle fingers with thumb close

Press 'q' to quit the application.

## Files

- `main.py`: Main application logic and gesture detection
- `util.py`: Utility functions for angle and distance calculations

## Notes

- The application uses your default webcam
- Works best in good lighting conditions
- Requires clear hand visibility
- Calibrated for single hand detection
