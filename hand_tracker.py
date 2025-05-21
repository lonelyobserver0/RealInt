import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands(static_image_mode=False,
                                              max_num_hands=1,
                                              min_detection_confidence=0.7,
                                              min_tracking_confidence=0.7)

    def get_hand_landmarks(self):
        success, frame = self.capture.read()
        if not success:
            return None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0].landmark
        return None
