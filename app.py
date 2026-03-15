import cv2
import numpy as np
import urllib.request
import os
import time
import config as cfg

from src.core.hand_tracker import HandTracker
from src.core.utils import apply_dead_zone, smooth, to_vjoy
from src.ui.visualizer import draw_steering_wheel, draw_hud, draw_hand_guides
from src.core.logic import calculate_steering, get_throttle_brake
from src.hardware.controller import VirtualJoystick

if not os.path.exists(os.path.dirname(cfg.MODEL_PATH)):
    os.makedirs(os.path.dirname(cfg.MODEL_PATH))

if not os.path.exists(cfg.MODEL_PATH):
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(cfg.MODEL_URL, cfg.MODEL_PATH)
    print("Downloaded!")

# --- Init Systems ---
vj = VirtualJoystick(cfg.VJOY_ID)
tracker = HandTracker(cfg.MODEL_PATH)

# --- State ---
state = {
    "calibration_offset": 0.0,
    "is_calibrated": False,
    "prev_steering": 0.0,
    "cal_countdown": 0,
    "cal_start_time": 0.0,
    "assign_mode": False
}

# --- Main loop ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("🎮 Starting...")
print("  C = Calibrate (จับมือตรงๆ แล้วกด C)")
print("  Q = Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w = frame.shape[:2]
    result = tracker.detect(rgb)
    
    left_lms = right_lms = None
    steering = throttle = brake = 0.0

    if result.hand_landmarks and result.handedness:
        for landmarks, handedness in zip(result.hand_landmarks, result.handedness):
            if handedness[0].category_name == "Left": left_lms = landmarks
            else: right_lms = landmarks

        if left_lms and right_lms:
            # เรียกใช้ logic ที่แยกออกมา
            raw_steering = calculate_steering(left_lms, right_lms, state["calibration_offset"])
            raw = apply_dead_zone(raw_steering, cfg.DEAD_ZONE)
            steering = smooth(raw, state["prev_steering"], cfg.SMOOTHING)
            throttle, brake = get_throttle_brake(left_lms, right_lms)
            draw_hand_guides(frame, left_lms, right_lms)
            
    state["prev_steering"] = steering
    vj.update(steering, throttle, brake)

    # --- Calibration countdown ---
    if state["cal_countdown"] > 0:
        elapsed = time.time() - state["cal_start_time"]
        remaining = state["cal_countdown"] - elapsed
        if remaining <= 0:
            if left_lms and right_lms:
                avg_angle = (HandTracker.get_hand_angle(left_lms) + HandTracker.get_hand_angle(right_lms)) / 2
                state["calibration_offset"] = (avg_angle - 90) / cfg.MAX_ANGLE
                state["is_calibrated"] = state["cal_countdown"] = 0
                print(f"✅ Calibrated: {state['calibration_offset']:.3f}")
            else:
                state["cal_countdown"] = 0
                print("❌ Fail: No hands")
        else:
            cv2.putText(frame, f"Hold... {remaining:.1f}s", (w//2-100, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 200, 255), 3)
    
    # --- Assign Mode ---
    if state["assign_mode"]:
        cv2.putText(frame, "🎮 ASSIGN MODE - Y/Z disabled | A=Exit", (20, h - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        
    draw_hud(frame, steering, throttle, brake, state["is_calibrated"])
    draw_steering_wheel(frame, w - 130, h - 130, 100, steering * 90)

    cv2.imshow("🎮 F1 Steering", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    elif key == ord('c'):
        state["cal_countdown"] = cfg.CALIBRATION_DURATION
        state["cal_start_time"] = time.time()
    elif key == ord('a'):
        state["assign_mode"] = not state["assign_mode"]
        print("🎮 Assign Mode ON - Y/Z = 0 ตลอด" if state["assign_mode"] else "✅ Assign Mode OFF")

    if state["assign_mode"]:
        vj.update(steering, cfg.VJOY_CENTER, cfg.VJOY_MAX)
    else:
        vj.update(steering, throttle, brake)

vj.reset()
cap.release()