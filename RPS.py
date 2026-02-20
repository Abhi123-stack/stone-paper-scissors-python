import cv2
import numpy as np
import mediapipe as mp
import random
import time

class RockPaperScissorsGame:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=1 
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.computer_move = None
        self.user_move = "Waiting..."
        self.result = "Show your hand"
        self.last_move_time = 0
        self.move_cooldown = 2  
        self.score = {"User": 0, "AI": 0}
        self.game_active = False
        self.move_confirmed = False
        self.move_display_timer = 0
        self.move_consistency_buffer = []
        self.move_consistency_required = 10  
        
        self.COLOR_BLUE = (255, 0, 0)
        self.COLOR_GREEN = (0, 255, 0)
        self.COLOR_RED = (0, 0, 255)
        self.COLOR_YELLOW = (0, 255, 255)
        self.COLOR_CYAN = (255, 255, 0)
        self.COLOR_MAGENTA = (255, 0, 255)
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_GRAY = (200, 200, 200)

    def get_hand_label(self, hand_landmarks):
        landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
        extended_fingers = [0] * 5  
        
        thumb_ip = landmarks[3]
        thumb_tip = landmarks[4]
        if thumb_tip[0] < thumb_ip[0]: 
            extended_fingers[0] = 1
            
        for finger_idx in range(1, 5):
            base_idx = finger_idx * 4 + 1  
            tip_idx = finger_idx * 4 + 4   
            
            if landmarks[tip_idx][1] < landmarks[base_idx][1]:
                extended_fingers[finger_idx] = 1
        
        total_extended = sum(extended_fingers)
        
        if total_extended <= 1:
            return "Rock"
        
        elif total_extended >= 4 and extended_fingers[1] == 1:
            return "Paper"
        
        elif extended_fingers[1] == 1 and extended_fingers[2] == 1 and extended_fingers[3] == 0:
            return "Scissors"
            
        return "Unknown"

    def determine_winner(self, user, computer):
        if user == computer:
            return "Tie!"
        elif (user == "Rock" and computer == "Scissors") or \
             (user == "Paper" and computer == "Rock") or \
             (user == "Scissors" and computer == "Paper"):
            self.score["User"] += 1
            return "You win!"
        else:
            self.score["AI"] += 1
            return "AI wins!"

    def draw_computer_move(self, frame, ai_area):
        center_x = ai_area[0] + ai_area[2] // 2
        center_y = ai_area[1] + ai_area[3] // 2
        
        if self.computer_move == "Rock":
            
            cv2.circle(frame, (center_x, center_y), 60, self.COLOR_GRAY, -1)
            cv2.circle(frame, (center_x, center_y), 60, self.COLOR_RED, 3)
            for i in range(10):
                x = center_x + random.randint(-40,40)
                y = center_y + random.randint(-40, 40)
                if (x - center_x)*2 + (y - center_y)*2 < 50*2:
                    cv2.circle(frame, (x, y), random.randint(3, 8), (70, 70, 70), -1)
                    
        elif self.computer_move == "Paper":
            pts = np.array([[center_x-50, center_y-70], [center_x+50, center_y-70], 
                           [center_x+70, center_y+50], [center_x-70, center_y+50]], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.fillPoly(frame, [pts], self.COLOR_WHITE)
            cv2.polylines(frame, [pts], True, self.COLOR_GREEN, 3)
            
            for i in range(-40, 40, 15):
                pt1 = (center_x - 60, center_y + i)
                pt2 = (center_x + 60, center_y + i)
                cv2.line(frame, pt1, pt2, (220, 220, 220), 2)
                
        elif self.computer_move == "Scissors":
            
            cv2.circle(frame, (center_x-20, center_y-20), 25, self.COLOR_BLUE, -1)
            cv2.circle(frame, (center_x+20, center_y-20), 25, self.COLOR_BLUE, -1)
            
            cv2.circle(frame, (center_x-20, center_y-20), 15, self.COLOR_WHITE, -1)
            cv2.circle(frame, (center_x+20, center_y-20), 15, self.COLOR_WHITE, -1)
            
            pts1 = np.array([[center_x-15, center_y], [center_x+15, center_y], 
                           [center_x+30, center_y+70], [center_x, center_y+70]], np.int32)
            pts1 = pts1.reshape((-1, 1, 2))
            
            pts2 = np.array([[center_x-15, center_y], [center_x+15, center_y], 
                           [center_x-30, center_y+70], [center_x-60, center_y+70]], np.int32)
            pts2 = pts2.reshape((-1, 1, 2))
            
            cv2.fillPoly(frame, [pts1], self.COLOR_MAGENTA)
            cv2.fillPoly(frame, [pts2], self.COLOR_MAGENTA)
            
        cv2.putText(frame, self.computer_move, (center_x - 40, ai_area[1] + ai_area[3] + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.COLOR_RED, 2)

    def draw_UI(self, frame):
        h, w, _ = frame.shape
        
        cv2.rectangle(frame, (10, 10), (300, 260), (40, 40, 40), -1)
        cv2.rectangle(frame, (10, 10), (300, 260), self.COLOR_WHITE, 2)
        
        cv2.putText(frame, f'Your move: {self.user_move}', (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.COLOR_BLUE, 2)
        cv2.putText(frame, f'AI move: {self.computer_move if self.computer_move else "Waiting..."}', (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.COLOR_RED, 2)
        
        result_color = self.COLOR_YELLOW
        if "win" in self.result:
            if "You" in self.result:
                result_color = self.COLOR_GREEN
            else:
                result_color = self.COLOR_RED
                
        cv2.rectangle(frame, (20, 115), (290, 155), (40, 40, 40), -1)
        cv2.putText(frame, self.result, (25, 145),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, result_color, 2)
        
        cv2.putText(frame, "SCORE", (130, 180), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.COLOR_YELLOW, 2)
        cv2.putText(frame, f'YOU: {self.score["User"]}', (30, 210),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.COLOR_BLUE, 2)
        cv2.putText(frame, f'AI: {self.score["AI"]}', (200, 210),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.COLOR_RED, 2)
        
        if self.game_active:
            current_time = time.time()
            time_left = max(0, self.move_cooldown - (current_time - self.last_move_time))
            
            bar_width = 260
            filled_width = int(bar_width * (1 - time_left / self.move_cooldown))
            
            cv2.rectangle(frame, (20, 230), (20 + bar_width, 250), (60, 60, 60), -1)
            cv2.rectangle(frame, (20, 230), (20 + filled_width, 250), (0, 165, 255), -1)
            cv2.putText(frame, f'Next move: {time_left:.1f}s', (80, 247),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.COLOR_WHITE, 2)
        
        cv2.putText(frame, "Show Rock, Paper or Scissors", (w//2 - 180, h - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.COLOR_GREEN, 2)
        cv2.putText(frame, "Press 'q' to quit, 'r' to reset score", (w//2 - 180, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.COLOR_WHITE, 2)

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
            
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture image.")
                    break

                frame = cv2.flip(frame, 1)
                h, w, _ = frame.shape
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                hand_result = self.hands.process(rgb)
                
                ai_area = (w - 300, 60, 250, 250)
                cv2.rectangle(frame, (ai_area[0], ai_area[1]), 
                             (ai_area[0] + ai_area[2], ai_area[1] + ai_area[3]), 
                             self.COLOR_GRAY, -1)
                
                temp_move = "Waiting..."
                if hand_result.multi_hand_landmarks:
                    for hand_landmarks in hand_result.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            frame, 
                            hand_landmarks, 
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_draw.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                            self.mp_draw.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                        )
                        
                        detected_move = self.get_hand_label(hand_landmarks)
                        
                        if detected_move != "Unknown":
                            temp_move = detected_move
                
                current_time = time.time()
                
                self.move_consistency_buffer.append(temp_move)
                if len(self.move_consistency_buffer) > self.move_consistency_required:
                    self.move_consistency_buffer.pop(0)
                
                cooldown_passed = current_time - self.last_move_time > self.move_cooldown
                
                if (all(move == self.move_consistency_buffer[0] for move in self.move_consistency_buffer) and
                    self.move_consistency_buffer[0] in ["Rock", "Paper", "Scissors"] and
                    (not self.game_active or cooldown_passed) and
                    len(self.move_consistency_buffer) == self.move_consistency_required):
                    
                    if not self.move_confirmed or cooldown_passed:
                        self.user_move = self.move_consistency_buffer[0]
                        self.computer_move = random.choice(["Rock", "Paper", "Scissors"])
                        self.result = self.determine_winner(self.user_move, self.computer_move)
                        self.last_move_time = current_time
                        self.game_active = True
                        self.move_confirmed = True
                        self.move_consistency_buffer = []
            
                if cooldown_passed:
                    self.move_confirmed = False
                
                if self.computer_move:
                    self.draw_computer_move(frame, ai_area)
                    
                self.draw_UI(frame)
                
                cv2.imshow("Rock Paper Scissors - AI Game", frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    self.score = {"User": 0, "AI": 0}
                    
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.hands.close()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()