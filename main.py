import cv2
import time
from detector import HandDetector
from counter import HandCounter, check_clap
from display import draw_scoreboard, draw_no_hand_warning

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

# Window setup
cv2.namedWindow("Hand Counter", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Counter", 1280, 720)

# Detector and counters
detector = HandDetector(max_hands=2)
counters = {
    "Left":  HandCounter(smoothing=7, threshold=0.015),
    "Right": HandCounter(smoothing=7, threshold=0.015)
}

# Clap exit gesture
clap_frames = 0
CLAP_FRAMES_NEEDED = 10

# FPS tracking
prev_time = 0
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_count += 1

    # Detect every 2nd frame for better performance
    if frame_count % 2 == 0:
        landmarks_list = detector.find_hands(frame)
    else:
        landmarks_list = detector.latest_result.hand_landmarks \
            if detector.latest_result else []

    detector.draw(frame)

    if landmarks_list:
        # Check for clap exit gesture
        if check_clap(landmarks_list):
            clap_frames += 1

            # Progress bar
            progress = clap_frames / CLAP_FRAMES_NEEDED
            h, w = frame.shape[:2]
            bar_w = int(200 * progress)
            cv2.rectangle(frame, (w//2 - 100, h - 50), (w//2 + 100, h - 30), (50, 50, 50), -1)
            cv2.rectangle(frame, (w//2 - 100, h - 50), (w//2 - 100 + bar_w, h - 30), (0, 255, 100), -1)
            cv2.putText(frame, "Clap to stop...", (w//2 - 80, h - 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 100), 1)

            if clap_frames >= CLAP_FRAMES_NEEDED:
                break
        else:
            clap_frames = 0

        # Route each hand to correct counter using handedness
        if detector.latest_result and detector.latest_result.handedness:
            handedness_list = detector.latest_result.handedness
            for i, hand_lm in enumerate(landmarks_list):
                if i >= len(handedness_list):
                    continue
                label = handedness_list[i][0].category_name
                label = "Right" if label == "Left" else "Left"  # flip because frame is mirrored
                wrist_y = hand_lm[0].y
                counters[label].update(wrist_y)
    else:
        clap_frames = 0
        draw_no_hand_warning(frame)

    # Scoreboard
    draw_scoreboard(
        frame,
        [counters["Left"], counters["Right"]],
        hand_labels=["Left", "Right"]
    )

    # FPS counter
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time + 0.001))
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {fps}", (500, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

    cv2.imshow("Hand Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()