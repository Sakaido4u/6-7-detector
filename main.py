import cv2
from detector import HandDetector
from counter import HandCounter,check_clap
import time 
from display import draw_scoreboard, draw_no_hand_warning

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
detector = HandDetector(max_hands=2)

# Fixed slots by hand identity
counters = {
    "Left": HandCounter(smoothing=7, threshold=0.015),
    "Right": HandCounter(smoothing=7, threshold=0.015)
}
# Clap needs to be held briefly to avoid accidental triggers
clap_frames = 0
CLAP_FRAMES_NEEDED = 10  # must hold clap for 10 frames (~0.3 seconds)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    landmarks_list = detector.find_hands(frame)
    detector.draw(frame)

    if landmarks_list:
        # Check for clap exit gesture
        if check_clap(landmarks_list):
            clap_frames += 1
            
            # Show countdown indicator so user knows it's registering
            progress = clap_frames / CLAP_FRAMES_NEEDED
            h, w = frame.shape[:2]
            bar_w = int(200 * progress)
            cv2.rectangle(frame, (w//2 - 100, h - 50), (w//2 + 100, h - 30), (50, 50, 50), -1)
            cv2.rectangle(frame, (w//2 - 100, h - 50), (w//2 - 100 + bar_w, h - 30), (0, 255, 100), -1)
            cv2.putText(frame, "Clap to stop...", (w//2 - 80, h - 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 100), 1)
            
            if clap_frames >= CLAP_FRAMES_NEEDED:
                break  # exit the loop
        else:
            clap_frames = 0  # reset if hands separate

        handedness_list = detector.latest_result.handedness

        for i, hand_lm in enumerate(landmarks_list):
            label = handedness_list[i][0].category_name
            label = "Right" if label == "Left" else "Left"
            wrist_y = hand_lm[0].y
            counters[label].update(wrist_y)
    else:
        clap_frames = 0
        draw_no_hand_warning(frame)

    draw_scoreboard(
        frame,
        [counters["Left"], counters["Right"]],
        hand_labels=["Left", "Right"]
    )

    cv2.imshow("Hand Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    small = cv2.resize(frame, (640, 360))
    landmarks_list = detector.find_hands(small)
    detector.draw(frame)

    if landmarks_list:
        handedness_list = detector.latest_result.multi_handedness \
            if hasattr(detector.latest_result, 'multi_handedness') \
            else detector.latest_result.handedness

        for i, hand_lm in enumerate(landmarks_list):
            # Get the label MediaPipe assigned ("Left" or "Right")
            label = handedness_list[i][0].category_name  # "Left" or "Right"
            
            # Because frame is flipped, swap the label
            label = "Right" if label == "Left" else "Left"

            wrist_y = hand_lm[0].y
            counters[label].update(wrist_y)
    else:
        draw_no_hand_warning(frame)

    # Pass as list to display, consistent order
    draw_scoreboard(
        frame,
        [counters["Left"], counters["Right"]],
        hand_labels=["Left", "Right"]
    )

    cv2.imshow("Hand Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()