
```bash
python -m venv .venv
```

Activate it on Windows (Command Prompt):

```bat
.venv\Scripts\activate.bat
```

Or on macOS / Linux:

```bash
source .venv/bin/activate
```

If your system uses `python3`, use it instead of `python` when creating the environment.

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install "mediapipe==0.10.21" "opencv-contrib-python==4.11.0.86" "numpy==1.26.4"
```

This setup pins MediaPipe because the code uses its legacy `mp.solutions.hands` API. Newer releases may not expose that API. See the [MediaPipe compatibility discussion](https://github.com/google-ai-edge/mediapipe/issues/6192) and [MediaPipe 0.10.21 package information](https://pypi.org/project/mediapipe/0.10.21/).

`opencv-contrib-python` provides the `cv2` module and satisfies MediaPipe's OpenCV dependency. Use this package in the virtual environment without also installing another OpenCV package. `random` and `time` are part of Python's standard library and need no separate installation.

### 3. Run the game

```bash
python main.py
```

## How to Play

1. Stand or sit in front of your webcam with your hand clearly visible.
2. Show one of the gestures below with your fingers pointing upward.
3. Hold the gesture steady until it is recognized consistently for 10 frames.
4. The computer chooses a move, and the result appears on screen.
5. After the two-second cooldown, show a gesture for the next round.

| Move | Hand gesture | Beats |
| --- | --- | --- |
| ✊ Rock / Stone | Closed fist | Scissors |
| ✋ Paper | Open palm with fingers extended | Rock |
| ✌️ Scissors | Extend your index and middle fingers; fold the others | Paper |

Each win adds one point to the winner's score. Ties do not change either score.

**Rounds start automatically.** Keeping the same recognized gesture visible can trigger another round after the cooldown; you do not need to change your gesture or press a start button.

### Controls

Click the game window to give it keyboard focus before using these controls.

| Key | Action |
| --- | --- |
| `q` | Quit the game |
| `r` | Reset both scores to zero |

Resetting the score does not clear the displayed moves or restart the cooldown. Scores are kept only for the current session.

## How It Works

1. **Capture:** OpenCV reads frames from the default webcam and mirrors the image.
2. **Track:** MediaPipe detects landmarks for one hand.
3. **Classify:** The code compares finger landmark positions to identify a gesture.
4. **Confirm:** A buffer checks for 10 consecutive matching detections.
5. **Play:** The computer selects a move using `random.choice()`, and the game applies the usual Rock Paper Scissors rules.
6. **Display:** OpenCV draws the hand landmarks, computer move, result, scoreboard, and cooldown indicator.

No separate image assets are required; the computer's move graphics are drawn in code.

## Customization

You can adjust these values in the source code:

| Setting | Default | Purpose |
| --- | --- | --- |
| `self.move_cooldown` | `2` | Minimum interval between rounds, in seconds; keep it greater than zero |
| `self.move_consistency_required` | `10` | Consecutive matching frames needed to confirm a move |
| `min_detection_confidence` | `0.7` | Minimum confidence for hand detection |
| `min_tracking_confidence` | `0.7` | Minimum confidence for hand tracking |
| `cv2.VideoCapture(0)` | Camera index `0` | Webcam used by the game |
| Frame width and height | `1280 × 720` | Requested camera resolution; actual resolution depends on the webcam |

## Troubleshooting

**The camera does not open**

- Check that your webcam is connected and camera permission is enabled.
- Close other applications that may be using the camera.
- If you have multiple cameras, try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`.

**Gestures are recognized incorrectly**

- Use good lighting and keep your entire hand in the frame.
- Face your palm toward the camera and keep your fingers pointing upward.
- Show only one hand and hold your gesture steady.
- Try the other hand or adjust its orientation. The current classifier uses simple coordinate comparisons, including a direction-dependent thumb check, so rotated hands and different hand orientations can affect recognition.

**MediaPipe reports that `solutions` is missing**

- Activate the virtual environment and install the pinned dependencies above.
- Make sure your script is not named `mediapipe.py`, which can shadow the installed package.

**A dependency cannot be installed**

- Check that the virtual environment uses Python 3.10 or 3.11.
- Package availability depends on your operating system and processor. Check the [available MediaPipe wheels](https://pypi.org/project/mediapipe/0.10.21/#files) for your platform.

**The game window does not appear**

- Run the script locally in a desktop session with webcam access.
- Use the desktop OpenCV package from the installation instructions; a headless OpenCV package does not provide the game window.

## Possible Improvements

- Improve recognition for both hands and different hand orientations.
- Add a countdown and an explicit start-round control.
- Add sound effects and match formats such as best of five.
- Save scores between sessions.
- Migrate from the legacy MediaPipe Solutions API to MediaPipe Tasks.
