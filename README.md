# AI Virtual Steering Wheel Controller 🏎️

> *"This is an interesting development"* — Crofty, probably

Control F1 25 with just your bare hands and a webcam. No wheel. No pedals. No excuses.  
Built with MediaPipe + vJoy. Powered by hand landmarks and questionable decision-making.

---

## 🎬 Demo — First Lap at Spa

[![Demo Video](https://img.youtube.com/vi/lJw4LImnTfQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=lJw4LImnTfQ)

> ⬆️ Click to watch — First ever lap at Spa-Francorchamps using hand gesture controls.  
> Lap time: not great. Dignity: totaled. Spirit: unbroken. 🏆

---

## ✨ Features

- **Steering Control** — Calculates steering angle from the tilt of both hands (Wrist → Middle Finger MCP vector)
- **Throttle & Brake** — Gesture-based pedal system: open palm = throttle, closed fist = brake
- **Calibration System** — Press `C` to set your neutral hand position as the steering center
- **Assign Mode** — Press `A` to disable throttle/brake axes temporarily for clean in-game axis mapping
- **Smoothing & Dead Zone** — Input filtering for stable, fluid control with reduced jitter
- **HUD Overlay** — Real-time feedback with a virtual steering wheel, steering bar, and status indicators

---

## 📋 Prerequisites

1. **Windows OS** — vJoy is Windows-only
2. **vJoy Driver** — Download and install from [vJoy Releases](https://github.com/jshafer817/vJoy/releases)
3. **vJoy Configuration** — Open **vJoy Configure** and enable **X Axis**, **Y Axis**, and **Z Axis** on Device 1, then click Apply
4. **Python 3.8+**

---

## 🚀 Installation

```bash
pip install opencv-python numpy mediapipe pyvjoy
```

The MediaPipe hand landmark model (`hand_landmarker.task`) will be downloaded automatically on first run.

---

## 🕹️ Usage

```bash
python app.py
```

### Keyboard Controls

| Key | Action |
|-----|--------|
| `C` | Calibrate — hold hands in neutral position, then press |
| `A` | Toggle Assign Mode — disables Y/Z axes for in-game axis mapping |
| `Q` | Quit |

### Hand Gestures

| Gesture | Action |
|---------|--------|
| Open palm (4–5 fingers extended) | Throttle |
| Closed fist (0–1 fingers extended) | Brake |
| Tilt both hands left/right | Steer |

---

## ⚙️ Configuration

Edit `config.py` to tune the controller to your preference:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAX_ANGLE` | `45` | Maximum hand tilt angle mapped to full steering lock |
| `DEAD_ZONE` | `0.08` | Center dead zone — reduces jitter when hands are neutral |
| `SMOOTHING` | `0.7` | Input smoothing factor (0.0 = raw, 1.0 = maximum smooth) |
| `THROTTLE_THRESHOLD` | `4` | Minimum fingers extended to trigger throttle |
| `BRAKE_THRESHOLD` | `1` | Maximum fingers extended to trigger brake |

---

## 🎮 Mapping Controls in F1 25 (Step-by-Step)

This is the trickiest part — follow this order carefully to avoid binding conflicts.

### Before You Start

1. Make sure vJoy Device 1 is visible in `joy.cpl` (Win+R → `joy.cpl`)
2. Run `app.py` and keep it running in the background
3. Open F1 25 → **Settings → Controls, Vibration & Force Feedback**
4. Make sure you are at the **Main Menu**, not inside a session (settings are locked during sessions)

### Step 1 — Select the Right Profile

- Choose **Custom Control Scheme** (not Keyboard Preset)
- Press **F2** to switch the input device to **vJoy Device**
- You should see "VJOY DEVICE" in the top-left corner

### Step 2 — Temporarily Change Thresholds in config.py

Before mapping steer, open `config.py` and change these two values:

```python
THROTTLE_THRESHOLD = 5   # was 4
BRAKE_THRESHOLD = 0      # was 1
```

This makes the neutral zone very wide (1–4 fingers = no input), so Y and Z stay at 0 while you map steer.  
**Remember to revert these values after mapping is done.**

### Step 3 — Enter Assign Mode

Press **`A`** in the app window to enter **Assign Mode**.  
This disables the Y and Z axes so only the steering (X axis) is active — preventing binding conflicts when mapping steer.

### Step 3 — Map Steer Left and Steer Right

- Select **Steer Left** → press assign → tilt both hands to the **left** and hold until detected
- Select **Steer Right** → press assign → tilt both hands to the **right** and hold until detected

### Step 4 — Exit Assign Mode

Press **`A`** again to return to normal mode (Y and Z axes re-enabled).

### Step 6 — Revert config.py

Before mapping throttle and brake, revert `config.py` back to normal:

```python
THROTTLE_THRESHOLD = 4   # back to default
BRAKE_THRESHOLD = 1      # back to default
```

Restart `app.py` after saving.

### Step 7 — Map Throttle and Brake

- Select **Accelerate** → press assign → **open your palm fully** (all fingers extended) and hold
- Select **Brake/Reverse** → press assign → **make a fist** (all fingers closed) and hold

> ⚠️ **Important:** When mapping Accelerate, make sure your hands are in a neutral position first — do not have your fist clenched, as the Z axis rising will interfere with detection.

### Step 6 — Calibration Settings in F1 25

Go to **Calibration** (top of the Controls menu) and set:

| Setting | Recommended Value |
|---------|------------------|
| Steering Deadzone | 0% |
| Steering Saturation | 100% |
| Throttle Deadzone | 0% |
| Brake Deadzone | 0% |

### Step 7 — Test in Time Trial

Use **Time Trial** mode for testing — no AI, no damage, perfect for calibrating feel.  
If steering feels too sensitive, increase `MAX_ANGLE` in `config.py`. If it feels sluggish, decrease it.

---

## 📂 Project Structure

```
├── app.py                  # Main entry point and game loop
├── config.py               # All tunable parameters
└── src/
    ├── core/
    │   ├── hand_tracker.py # MediaPipe hand detection
    │   ├── logic.py        # Steering and throttle/brake calculations
    │   └── utils.py        # Math helpers, smoothing, value mapping
    ├── hardware/
    │   └── controller.py   # vJoy communication
    └── ui/
        └── visualizer.py   # HUD and steering wheel overlay
```

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| vJoy Device not found in `joy.cpl` | Run `app.py` first, then open `joy.cpl` — the device only exists while the script is running |
| Binding conflict when mapping axes | Use **Assign Mode** (`A`) when mapping steer, exit it before mapping throttle/brake |
| Steering drifts when hands are neutral | Press `C` to recalibrate with hands in neutral position |
| Throttle triggers when steering | Increase `THROTTLE_THRESHOLD` to `5` in `config.py` |
| Brake not detected reliably | Decrease `BRAKE_THRESHOLD` to `0` in `config.py` |
| Hand detection unstable | Improve lighting — MediaPipe performs best in well-lit environments |

---

## 💡 Tips for Best Experience

- **Lighting matters** — face a light source, avoid backlighting. MediaPipe can't see your hands in the dark, unlike your race engineer who can always see your mistakes
- **Camera position** — place the webcam at chest height facing you directly
- **Calibrate first** — always press `C` before starting a session with hands in your natural driving position
- **Open palm is most reliable** — flat open hands give the most consistent landmark detection. Yes, you will look like you're doing jazz hands. Embrace it.
- **Start with Time Trial** — get comfortable with the controls before racing against AI. The AI has no mercy. Neither does Eau Rouge.
- **Spa is hard** — if your first lap was rough, that's normal. Even real F1 drivers crash at Spa. You're basically Verstappen. 🏆

---

*Developed with ❤️ using MediaPipe & OpenCV*  
*Tested at Spa-Francorchamps. Barriers were harmed in the making of this project.*