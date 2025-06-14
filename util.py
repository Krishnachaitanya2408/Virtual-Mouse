import numpy as np

def get_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    if angle > 180:
        angle = 360 - angle
    return angle

def get_distance(landmarks):
    if len(landmarks) < 2:
        return 0
    (x1, y1), (x2, y2) = landmarks[0], landmarks[1]
    dist = np.hypot(x2 - x1, y2 - y1)
    return np.interp(dist, [0, 1], [0, 1000])  # maps to [0, 1000] for easier thresholding
