# Hand Counter

A real-time hand rep counter using your webcam. Tracks how many times each hand goes up and down using MediaPipe hand landmark detection.

---

## Requirements

- Python 3.8+
- A webcam

Install dependencies:
```bash
pip install mediapipe opencv-python
```

---

## Project Structure

```
head_counter/
├── main.py         # entry point, webcam loop
├── detector.py     # MediaPipe hand detection and drawing
├── counter.py      # rep counting state machine
├── display.py      # scoreboard and timer overlay
└── hand_landmarker.task  # auto-downloaded on first run
```

---

## How to Run

```bash
python main.py
```

The hand landmark model will download automatically on the first run.

---

## Controls

| Action | Result |
|---|---|
| Raise / lower hand | Counts a rep |
| Clap both hands together | Stops the program |
| Hold clap for ~0.3s | Confirms exit (green progress bar shown) |
| Press `q` | Force quit |

---

## Features

- Tracks left and right hand reps independently
- Semi-transparent scoreboard overlay with live rep count
- Colour-coded state indicator — green for UP, blue for DOWN
- Session timer displayed in the scoreboard
- Skeleton overlay on detected hands, turns orange when tracking is cached
- Clap gesture to exit

---

## Tuning

All tuning values are at the top of each file.

**`detector.py`** — tracking sensitivity:
```python
min_hand_detection_confidence = 0.5  # lower = detects more easily
min_hand_presence_confidence  = 0.3  # lower = holds track longer
min_tracking_confidence       = 0.3  # lower = smoother but less accurate
```

**`counter.py`** — rep detection:
```python
smoothing  = 7     # higher = less jitter, slightly more lag
threshold  = 0.015 # higher = requires bigger movement to count a rep
```

**`main.py`** — clap exit sensitivity:
```python
CLAP_FRAMES_NEEDED = 10   # frames clap must be held to exit (~0.3s)
# threshold in check_clap()
clap threshold     = 0.15 # lower = hands must be closer to trigger
```

---

## Performance Tips

- If tracking is slow, reduce the capture resolution in `main.py`:
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
```
- Enable frame skipping in `main.py` by detecting every 2nd frame
- Check live FPS displayed in the top right of the window
