```bat
.venv\Scripts\activate.bat
```

</details>

<details>
<summary><strong>macOS / Linux — activate the environment</strong></summary>

```bash
source .venv/bin/activate
```

Use `python3` instead of `python` to create the environment if required by your system.

</details>

**2 · Install the packages**

```bash
python -m pip install --upgrade pip
python -m pip install "numpy==1.26.4" "opencv-contrib-python==4.11.0.86"
python -m pip install "mediapipe==0.10.21"
```

**3 · Start playing**

```bash
python main.py
```

If your script has another name, replace `main.py` with that filename.

<details>
<summary>Why are the dependency versions pinned?</summary>

The code uses the legacy `mp.solutions.hands` API. The setup pins MediaPipe to retain that API; newer releases may not include it. See the [MediaPipe compatibility discussion](https://github.com/google-ai-edge/mediapipe/issues/6192).

`opencv-contrib-python` supplies `cv2` and satisfies MediaPipe's OpenCV dependency. Avoid installing another OpenCV package in the same environment. Python already includes `random` and `time`.

These are suggested dependency versions, not a claim of testing on every platform. Check the [MediaPipe package files](https://pypi.org/project/mediapipe/0.10.21/#files) if installation fails.

</details>

## How to play

1. **Get in position.** Keep one hand fully visible in the webcam, with your palm toward the camera and fingers pointing upward.
2. **Choose your move.** Show a fist for Rock, an open palm for Paper, or extend your index and middle fingers for Scissors.
3. **Hold it steady.** The game confirms your move after ten consecutive matching frames.
4. **Check the result.** The computer picks a random move, and the winner earns one point. Ties leave the score unchanged.
5. **Go again.** The next round becomes available after the two-second cooldown.

> **Keep your hand ready:** rounds happen automatically. Holding the same gesture can play it again after the cooldown.

| Control | Action |
| :---: | --- |
| <kbd>Q</kbd> | Quit the game |
| <kbd>R</kbd> | Reset both scores |

Click the game window first so it receives keyboard input. Press the letter keys without Shift. Scores last for the current session; resetting them leaves the displayed moves and cooldown unchanged.

## Behind the scenes

**Webcam → Hand landmarks → Gesture check → Move confirmation → Result**

OpenCV captures and mirrors the webcam feed. MediaPipe tracks a single hand, and NumPy helps compare landmark coordinates to identify extended fingers. Once a gesture is stable, Python selects the computer's move and applies the game rules.

The opponent is labeled **AI** in the interface, but its moves come from `random.choice()` rather than a predictive model. All move graphics are drawn in code—no separate image assets are needed.

## Make it your own

Adjust these values in the source code:

| Setting | Default | What it changes |
| --- | :---: | --- |
| `move_cooldown` | `2` | Seconds between rounds; keep above zero |
| `move_consistency_required` | `10` | Matching frames needed to confirm a move |
| `min_detection_confidence` | `0.7` | Hand detection confidence threshold |
| `min_tracking_confidence` | `0.7` | Hand tracking confidence threshold |
| `cv2.VideoCapture(0)` | `0` | Camera index |

## Need a hand?

<details>
<summary><strong>The webcam won’t open</strong></summary>

Check camera permissions and close other apps using your webcam. If you have more than one camera, try `cv2.VideoCapture(1)` in the source code.

</details>

<details>
<summary><strong>My gesture isn’t detected correctly</strong></summary>

Use good lighting, show only one hand, and keep the whole hand in frame. Face your palm toward the camera and hold your gesture steady. The classifier uses simple coordinate comparisons, including a direction-dependent thumb check, so changing your hand orientation or trying the other hand may help.

</details>

<details>
<summary><strong>MediaPipe says “solutions” is missing</strong></summary>

Activate your virtual environment and reinstall the pinned dependencies from Quick start. Make sure your script is not named `mediapipe.py`, which could shadow the package.

</details>

<details>
<summary><strong>No game window appears</strong></summary>

Run the script in a local desktop session with webcam access. Use the OpenCV package listed above; headless OpenCV packages do not provide the game window.

</details>

## Ideas for future rounds

- [ ] Best-of-five match mode
- [ ] Sound effects and a round countdown
- [ ] Improved recognition for both hands and different orientations
- [ ] Scores saved between sessions
- [ ] Migration to the MediaPipe Tasks API

---

<p align="center"><strong>Three gestures. One webcam. Your next move.</strong><br>✊ &nbsp; ✋ &nbsp; ✌️</p>
