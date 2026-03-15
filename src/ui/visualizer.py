import cv2
import numpy as np

def draw_steering_wheel(frame, center_x, center_y, radius, angle_deg):
    """วาดพวงมาลัยหมุนตามมุม steering"""
    # rim
    cv2.circle(frame, (center_x, center_y), radius, (200, 200, 200), 3)
    # hub
    cv2.circle(frame, (center_x, center_y), 15, (200, 200, 200), -1)
    # spokes
    for i in range(3):
        spoke_angle = np.radians(angle_deg + i * 120)
        x1 = int(center_x + 15 * np.cos(spoke_angle))
        y1 = int(center_y + 15 * np.sin(spoke_angle))
        x2 = int(center_x + radius * np.cos(spoke_angle))
        y2 = int(center_y + radius * np.sin(spoke_angle))
        cv2.line(frame, (x1, y1), (x2, y2), (200, 200, 200), 3)
    # grips
    left_grip = (
        int(center_x + radius * np.cos(np.radians(angle_deg + 180))),
        int(center_y + radius * np.sin(np.radians(angle_deg + 180)))
    )
    right_grip = (
        int(center_x + radius * np.cos(np.radians(angle_deg))),
        int(center_y + radius * np.sin(np.radians(angle_deg)))
    )
    cv2.circle(frame, left_grip, 12, (0, 200, 255), -1)
    cv2.circle(frame, right_grip, 12, (0, 200, 255), -1)

def draw_hud(frame, steering, throttle, brake, is_calibrated):
    h, w = frame.shape[:2]
    # Steering Bar
    bar_y, bar_half = 70, 200
    cv2.rectangle(frame, (w//2 - bar_half, bar_y - 10), (w//2 + bar_half, bar_y + 10), (50, 50, 50), -1)
    bar_x = int(w//2 + steering * bar_half)
    bar_color = (0, 200, 100) if abs(steering) < 0.5 else (0, 80, 255)
    cv2.rectangle(frame, (w//2, bar_y - 10), (bar_x, bar_y + 10), bar_color, -1)
    
    # Text Info
    cv2.putText(frame, f"Steering: {steering:+.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, f"Throttle: {throttle:.2f}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 100), 2)
    cv2.putText(frame, f"Brake:    {brake:.2f}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 100, 255), 2)

    # Status
    cal_text = "✅ Calibrated" if is_calibrated else "⚠️ Press C to calibrate"
    cal_color = (0, 255, 100) if is_calibrated else (0, 165, 255)
    cv2.putText(frame, cal_text, (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cal_color, 2)

def draw_hand_guides(frame, left_lms, right_lms):
    h, w = frame.shape[:2]
    if left_lms and right_lms:
        lx, ly = int(left_lms[0].x * w), int(left_lms[0].y * h)
        rx, ry = int(right_lms[0].x * w), int(right_lms[0].y * h)
        cv2.line(frame, (lx, ly), (rx, ry), (255, 100, 100), 2)

    for lms, color in [(left_lms, (100, 255, 100)), (right_lms, (100, 100, 255))]:
        if lms:
            wx, wy = int(lms[0].x * w), int(lms[0].y * h)
            mx, my = int(lms[9].x * w), int(lms[9].y * h)
            cv2.arrowedLine(frame, (wx, wy), (mx, my), color, 2, tipLength=0.3)
            for lm in lms:
                cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 4, (0, 255, 0), -1)