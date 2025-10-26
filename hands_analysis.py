import cv2
import mediapipe as mp
import numpy as np
import json
import os
from collections import Counter

def classify_gesture(landmarks):
    """Classify hand gesture based on landmarks"""
    if not landmarks:
        return "no_gesture"
    
    # Get key landmarks
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    index_tip = landmarks[8]
    index_pip = landmarks[6]
    middle_tip = landmarks[12]
    middle_pip = landmarks[10]
    ring_tip = landmarks[16]
    ring_pip = landmarks[14]
    pinky_tip = landmarks[20]
    pinky_pip = landmarks[18]
    
    # Count extended fingers
    fingers_up = 0
    
    # Thumb (compare x coordinates)
    if thumb_tip.x > thumb_ip.x:
        fingers_up += 1
    
    # Other fingers (compare y coordinates)
    finger_tips = [index_tip, middle_tip, ring_tip, pinky_tip]
    finger_pips = [index_pip, middle_pip, ring_pip, pinky_pip]
    
    for tip, pip in zip(finger_tips, finger_pips):
        if tip.y < pip.y:
            fingers_up += 1
    
    # Classify based on finger count and positions
    if fingers_up == 0:
        return "closed_fist"
    elif fingers_up == 1:
        if index_tip.y < index_pip.y:
            return "pointing"
        else:
            return "thumbs_up"
    elif fingers_up == 2:
        if index_tip.y < index_pip.y and middle_tip.y < middle_pip.y:
            return "peace_sign"
        else:
            return "partial_open"
    elif fingers_up == 5:
        return "open_palm"
    else:
        return "partial_open"

def analyze_hands():
    """Analyze hand gestures and collect gesture statistics"""
    print("✋ Starting Hands Analysis...")
    print("Use natural hand gestures while presenting")
    print("Press 'q' to stop analysis")
    
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return {"error": "Could not open camera"}
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    gesture_list = []
    total_frames = 0
    frames_with_hands = 0
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            
            current_gestures = []
            
            if results.multi_hand_landmarks:
                frames_with_hands += 1
                
                for hand_landmarks in results.multi_hand_landmarks:
                    # Classify gesture
                    gesture = classify_gesture(hand_landmarks.landmark)
                    current_gestures.append(gesture)
                    
                    # Draw landmarks
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Display current gestures
                gesture_text = ", ".join(set(current_gestures))
                cv2.putText(frame, f"Gestures: {gesture_text}", (30, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                current_gestures = ["no_gesture"]
                cv2.putText(frame, "No hands detected", (30, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Store gestures for this frame
            gesture_list.extend(current_gestures)
            total_frames += 1
            
            # Display frame counter
            cv2.putText(frame, f"Frames: {total_frames}", (10, frame_height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('Hands Analysis', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n⏹️  Analysis stopped by user")
    except Exception as e:
        print(f"❌ Error during hands analysis: {e}")
        return {"error": str(e)}
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Calculate final statistics
    if gesture_list:
        gesture_counts = Counter(gesture_list)
        total_gestures = len(gesture_list)
        
        # Calculate percentages
        gesture_percentages = {
            gesture: (count / total_gestures) * 100 
            for gesture, count in gesture_counts.items()
        }
        
        print(f"\n📊 Hands Analysis Results:")
        print(f"   Total Frames Analyzed: {total_frames}")
        print(f"   Frames with Hands Detected: {frames_with_hands}")
        print(f"   Total Gestures Detected: {total_gestures}")
        print(f"   Gesture Breakdown:")
        
        for gesture, count in gesture_counts.items():
            percentage = gesture_percentages[gesture]
            print(f"     - {gesture.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
        
        # Save statistics
        stats = {
            "total_frames": total_frames,
            "frames_with_hands": frames_with_hands,
            "total_gestures": total_gestures,
            "gesture_counts": dict(gesture_counts),
            "gesture_percentages": gesture_percentages,
            "gesture_list": gesture_list
        }
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        with open("data/hands_analysis_stats.json", "w") as f:
            json.dump(stats, f, indent=2)
        
        print("✅ Hands analysis statistics saved to data/hands_analysis_stats.json")
        return stats
    else:
        print("❌ No gesture data collected")
        return {"error": "No gesture data collected"}

if __name__ == "__main__":
    analyze_hands()
