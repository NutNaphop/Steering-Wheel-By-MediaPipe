import numpy as np
import config as cfg
from .hand_tracker import HandTracker

def calculate_steering(left_landmarks, right_landmarks, calibration_offset):
    """คำนวณ Steering จากมุมของมือทั้งสองข้าง"""
    left_angle = HandTracker.get_hand_angle(left_landmarks)
    right_angle = HandTracker.get_hand_angle(right_landmarks)
    
    avg_angle = (left_angle + right_angle) / 2
    steering_angle = avg_angle - 90
    
    # คำนวณค่า steering และหักลบด้วยค่า calibration
    steering = np.clip(steering_angle / cfg.MAX_ANGLE, -1.0, 1.0)
    return steering - calibration_offset

def get_throttle_brake(left_landmarks, right_landmarks):
    left_fingers = HandTracker.count_extended_fingers(left_landmarks)
    right_fingers = HandTracker.count_extended_fingers(right_landmarks)
    avg_fingers = (left_fingers + right_fingers) / 2.0
    print(f"fingers L:{left_fingers} R:{right_fingers} avg:{avg_fingers:.1f}")
    if avg_fingers >= cfg.THROTTLE_THRESHOLD:
        return 1.0, 0.0   # แบมือ = เร่ง, brake ต้องเป็น 0 เสมอ
    elif avg_fingers <= cfg.BRAKE_THRESHOLD:
        return 0.0, 1.0   # กำมือ = เบรก, throttle ต้องเป็น 0 เสมอ
    else:
        return 0.0, 0.0   # neutral ทั้งคู่เป็น 0