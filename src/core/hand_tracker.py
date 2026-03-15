import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, model_path):
        base_options = mp_python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame_rgb):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        return self.detector.detect(mp_image)

    @staticmethod
    def get_hand_angle(landmarks):
        """คำนวณมุมการหมุนของมือ จากแนวนิ้วกลาง → ข้อมือ"""
        wrist = np.array([landmarks[0].x, landmarks[0].y])
        middle_mcp = np.array([landmarks[9].x, landmarks[9].y])
        dx = middle_mcp[0] - wrist[0]
        dy = middle_mcp[1] - wrist[1]
        return np.degrees(np.arctan2(-dy, dx))

    @staticmethod
    def count_extended_fingers(landmarks):
        """นับนิ้วที่เหยียดออก โดยเช็คระยะจากข้อมือ"""
        wrist = np.array([landmarks[0].x, landmarks[0].y])
        tips = [8, 12, 16, 20]   # tip
        mcps = [5, 9, 13, 17]    # โคนนิ้ว (mcp)
        
        count = 0
        for tip, mcp in zip(tips, mcps):
            tip_pos = np.array([landmarks[tip].x, landmarks[tip].y])
            mcp_pos = np.array([landmarks[mcp].x, landmarks[mcp].y])
            
            # นิ้วเหยียด = tip ไกลจากข้อมือมากกว่า mcp
            if np.linalg.norm(tip_pos - wrist) > np.linalg.norm(mcp_pos - wrist) * 1.2:
                count += 1
        
        # นิ้วโป้ง — เช็คระยะจากข้อมือเหมือนกัน
        thumb_tip = np.array([landmarks[4].x, landmarks[4].y])
        thumb_mcp = np.array([landmarks[2].x, landmarks[2].y])
        if np.linalg.norm(thumb_tip - wrist) > np.linalg.norm(thumb_mcp - wrist) * 1.2:
            count += 1
        
        return count