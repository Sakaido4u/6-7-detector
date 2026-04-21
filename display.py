import cv2
import time
def draw_scoreboard(frame, counters, hand_labels=None):
    h, w = frame.shape[:2]
    
    panel_w = 220
    panel_h = 40 + len(counters) * 60
    
    # Semi-transparent background panel
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (10 + panel_w, 10 + panel_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    
    # Title
    cv2.putText(frame, "HAND COUNTER", (20, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.line(frame, (20, 45), (10 + panel_w - 10, 45), (255, 255, 255), 1)
    
    # Per-hand rows
    for i, counter in enumerate(counters):
        label = hand_labels[i] if hand_labels and i < len(hand_labels) else f"Hand {i+1}"
        state = counter.state or "---"
        count = counter.count
        y = 75 + i * 60
        
        # Colored dot based on state
        if state == "UP":
            color = (0, 255, 100)    # green
        elif state == "DOWN":
            color = (0, 100, 255)    # blue
        else:
            color = (150, 150, 150)  # gray when idle
        
        cv2.circle(frame, (28, y - 8), 7, color, -1)
        
        # Hand label
        cv2.putText(frame, label, (44, y - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
        
        # Rep count
        cv2.putText(frame, f"{count} reps", (44, y + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        
        # State text
        cv2.putText(frame, state, (160, y - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)


def draw_no_hand_warning(frame):
    """Shows a warning when no hands are detected"""
    h, w = frame.shape[:2]
    cv2.putText(frame, "No hands detected", (w // 2 - 120, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)

_start_time = time.time()

def get_elapsed():
    elapsed = int(time.time() - _start_time)
    mins = elapsed // 60
    secs = elapsed % 60
    return f"{mins:02d}:{secs:02d}"

def draw_scoreboard(frame, counters, hand_labels=None):
    h, w = frame.shape[:2]
    
    panel_w = 220
    panel_h = 40 + len(counters) * 60 + 35  # extra space for timer
    
    # Semi-transparent background panel
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (10 + panel_w, 10 + panel_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    
    # Title
    cv2.putText(frame, "HAND COUNTER", (20, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.line(frame, (20, 45), (10 + panel_w - 10, 45), (255, 255, 255), 1)
    
    # Per-hand rows
    for i, counter in enumerate(counters):
        label = hand_labels[i] if hand_labels and i < len(hand_labels) else f"Hand {i+1}"
        state = counter.state or "---"
        count = counter.count
        y = 75 + i * 60
        
        if state == "UP":
            color = (0, 255, 100)
        elif state == "DOWN":
            color = (0, 100, 255)
        else:
            color = (150, 150, 150)
        
        cv2.circle(frame, (28, y - 8), 7, color, -1)
        cv2.putText(frame, label, (44, y - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
        cv2.putText(frame, f"{count} reps", (44, y + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        cv2.putText(frame, state, (160, y - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    # Timer at the bottom of the panel
    timer_y = 75 + len(counters) * 60 + 20
    cv2.line(frame, (20, timer_y - 12), (10 + panel_w - 10, timer_y - 12), (255, 255, 255), 1)
    cv2.putText(frame, f"TIME  {get_elapsed()}", (20, timer_y + 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)


def draw_no_hand_warning(frame):
    h, w = frame.shape[:2]
    cv2.putText(frame, "No hands detected", (w // 2 - 120, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)