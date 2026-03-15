import os

MODEL_PATH = os.path.join("assets", "hand_landmarker.task")
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"

# vJoy Config
VJOY_ID = 1
VJOY_CENTER = 16384
VJOY_MAX = 32767

# Driving Parameters
DEAD_ZONE = 0.08
SMOOTHING = 0.7
MAX_ANGLE = 45  # องศาสูงสุดจากกึ่งกลาง
THROTTLE_THRESHOLD = 4   
BRAKE_THRESHOLD = 2   

CALIBRATION_DURATION = 2 # วินาที