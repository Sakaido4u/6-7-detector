from collections import deque

class HandCounter:
    def __init__(self, smoothing=5, threshold=0.02):
        self.history = deque(maxlen=smoothing)
        self.state = None
        self.count = 0
        self.threshold = threshold

    def update(self, y_normalized):
        self.history.append(y_normalized)
        smooth_y = sum(self.history) / len(self.history)

        if len(self.history) < 2:
            return self.count

        prev = list(self.history)[-2]
        delta = smooth_y - prev

        if delta > self.threshold and self.state != "DOWN":
            if self.state == "UP":
                self.count += 1
            self.state = "DOWN"
        elif delta < -self.threshold and self.state != "UP":
            if self.state == "DOWN":
                self.count += 1
            self.state = "UP"

        return self.count


# This is OUTSIDE the class — no indentation
def check_clap(hand_landmarks, threshold=0.15):
    """Returns True if both hands are close together (clap gesture)"""
    if len(hand_landmarks) < 2:
        return False

    wrist1 = hand_landmarks[0][0]
    wrist2 = hand_landmarks[1][0]

    dist = ((wrist1.x - wrist2.x) ** 2 + (wrist1.y - wrist2.y) ** 2) ** 0.5

    return dist < threshold