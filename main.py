import cv2
import mediapipe as mp
import pyautogui
import time
import util
from pynput.mouse import Button, Controller

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

draw_utils = mp.solutions.drawing_utils

# Smoothening variables
prev_x, prev_y = 0, 0
smoothening = 5

# Debounce timers
gesture_cooldown = 1.0  # in seconds
last_gesture_time = 0


def move_mouse_smooth(index_tip):
    global prev_x, prev_y
    if index_tip:
        x = int(index_tip.x * screen_width)
        y = int(index_tip.y * screen_height / 2)
        curr_x = prev_x + (x - prev_x) / smoothening
        curr_y = prev_y + (y - prev_y) / smoothening
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y


def detect_and_act(frame, landmarks, processed):
    global last_gesture_time
    now = time.time()

    if len(landmarks) < 21:
        return

    index_tip = find_index_tip(processed)
    thumb_index_dist = util.get_distance([landmarks[4], landmarks[8]])

    move_mouse_smooth(index_tip)

    if now - last_gesture_time < gesture_cooldown:
        return  # prevent repeated gestures too quickly

    # Gesture detections
    if is_left_click(landmarks, thumb_index_dist):
        mouse.click(Button.left)
        cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        last_gesture_time = now

    elif is_right_click(landmarks, thumb_index_dist):
        mouse.click(Button.right)
        cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        last_gesture_time = now

    elif is_double_click(landmarks, thumb_index_dist):
        pyautogui.doubleClick()
        cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        last_gesture_time = now

    elif is_screenshot(landmarks, thumb_index_dist):
        screenshot = pyautogui.screenshot()
        screenshot.save(f'my_screenshot_{int(time.time())}.png')
        cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        last_gesture_time = now


def is_left_click(landmarks, dist):
    return util.get_angle(landmarks[5], landmarks[6], landmarks[8]) < 40 and dist > 100


def is_right_click(landmarks, dist):
    return util.get_angle(landmarks[9], landmarks[10], landmarks[12]) < 40 and dist > 100


def is_double_click(landmarks, dist):
    return (util.get_angle(landmarks[5], landmarks[6], landmarks[8]) < 40 and
            util.get_angle(landmarks[9], landmarks[10], landmarks[12]) < 40 and dist > 100)


def is_screenshot(landmarks, dist):
    return (util.get_angle(landmarks[5], landmarks[6], landmarks[8]) < 40 and
            util.get_angle(landmarks[9], landmarks[10], landmarks[12]) < 40 and dist < 50)


def find_index_tip(processed):
    if processed.multi_hand_landmarks:
        tip = processed.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        return tip
    return None


def main():
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            landmark_list = []
            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                draw_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_and_act(frame, landmark_list, result)

            cv2.imshow('Virtual Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
