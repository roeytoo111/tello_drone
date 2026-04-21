# Tello Drone Experiments

Small collection of Python scripts for controlling a DJI Tello drone and doing simple computer-vision tasks (color tracking, face tracking, and Haar-cascade “weapon” detection demos).

## Project demo

- [LinkedIn post: gesture-controlled Tello](https://www.linkedin.com/posts/roey-turjeman-584788246_computervision-drones-dji-activity-7062679241259180032-yokL?utm_source=share&utm_medium=member_desktop&rcm=ACoAADz7tTQBizBVsBPCufr8ugIvaXUZp77DhhA)

## Project layout

```text
assets/                         # non-code files (cascades, etc.)
  cascades/weapon_cascade.xml
  haarcascades/haarcascade_frontalface_default.xml
scripts/                        # runnable scripts
  color_detection.py
  tello/
    faceTracking.py
    HandTracking.py
    handD.py
    manual_control_opencv.py
    record_video.py
  weapon_detection/
    color_trackbar.py
    follow_orange.py
    weapon_detection.py
    weapon_follower.py
    weapon_flipflop.py
src/tello_drone/                 # (placeholder) python package
requirements.txt
```

## Prerequisites

- Python 3.9+ recommended
- A DJI Tello on the same Wi‑Fi network as this machine

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running scripts

Run scripts from the **repo root**.

### Manual control (keyboard + OpenCV window)

```bash
python scripts/tello/manual_control_opencv.py
```

Keys:
- **W/A/S/D**: forward/left/back/right
- **R/F**: up/down
- **Q/E**: rotate
- **ESC**: land and exit

### Record a short flight to `video.avi`

```bash
python scripts/tello/record_video.py
```

### Detect red color in the Tello camera feed

```bash
python scripts/color_detection.py
```

### Face tracking (uses Haar cascade in `assets/`)

```bash
python scripts/tello/faceTracking.py
```

### Weapon detection (Haar cascade demo)

```bash
python scripts/weapon_detection/weapon_detection.py
```

Other variants:

```bash
python scripts/weapon_detection/weapon_follower.py
python scripts/weapon_detection/weapon_flipflop.py
```

## Notes / safety

- These scripts can **take off immediately** (some call `takeoff()` on start). Run in a safe area.
- If the video window freezes during movement, that’s expected in the simplest examples (commands block while the drone moves).

## Troubleshooting

- **No video / black frame**: ensure `streamon()` succeeded; restart the drone and try again.
- **Cascade load errors**: the scripts load cascades from `assets/`; run them from the repo root as shown above.

