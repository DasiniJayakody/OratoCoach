import cv2
import mediapipe as mp
import numpy as np
import json
import os

def classify_gesture(hand_landmarks, frame_width, frame_height):
    """Classify hand gesture based on landmark positions"""
    
    def get_point(index):
        landmark = hand_landmarks.landmark[index]
        return [int(landmark.x * frame_width), int(landmark.y * frame_height)]
    
    try:
        # Get key hand landmarks
        thumb_tip = get_point(4)
        index_tip = get_point(8)
        middle_tip = get_point(12)
        ring_tip = get_point(16)
        pinky_tip = get_point(20)
        
        thumb_ip = get_point(3)
        index_pip = get_point(6)
        middle_pip = get_point(10)
        ring_pip = get_point(14)
        pinky_pip = get_point(18)
        
        wrist = get_point(0)
        
        # Calculate distances
        def distance(p1, p2):
            return np.linalg.norm(np.array(p1) - np.array(p2))
        
        # Check if fingers are extended
        thumb_extended = distance(thumb_tip, wrist) > distance(thumb_ip, wrist)
        index_extended = distance(index_tip, wrist) > distance(index_pip, wrist)
        middle_extended = distance(middle_tip, wrist) > distance(middle_pip, wrist)
        ring_extended = distance(ring_tip, wrist) > distance(ring_pip, wrist)
        pinky_extended = distance(pinky_tip, wrist) > distance(pinky_pip, wrist)
        
        # Classify gestures
        if all([index_extended, middle_extended, ring_extended, pinky_extended]) and not thumb_extended:
            return "pointing"
        elif all([index_extended, middle_extended, ring_extended, pinky_extended, thumb_extended]):
            return "open_palms"
        elif not any([index_extended, middle_extended, ring_extended, pinky_extended, thumb_extended]):
            return "closed_fists"
        elif index_extended and not any([middle_extended, ring_extended, pinky_extended, thumb_extended]):
            return "pointing"
        elif all([index_extended, middle_extended]) and not any([ring_extended, pinky_extended, thumb_extended]):
            return "peace_sign"
        elif thumb_extended and not any([index_extended, middle_extended, ring_extended, pinky_extended]):
            return "thumbs_up"
        elif pinky_extended and not any([index_extended, middle_extended, ring_extended, thumb_extended]):
            return "wave"
        else:
            return "other_gesture"
            
    except Exception as e:
        print(f"Error classifying gesture: {e}")
        return "unknown"

def analyze_hands():
    """Analyze hands and collect gesture statistics"""
    print("✋ Starting Hands Analysis...")
    print("Make various hand gestures for analysis")
    print("Press 'q' to stop analysis")
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return None
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    gesture_counts = {}
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
                    gesture = classify_gesture(hand_landmarks, frame_width, frame_height)
                    current_gestures.append(gesture)
                    
                    # Count gestures
                    gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
                    
                    # Draw landmarks
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # Display gesture on frame
                    cv2.putText(frame, f"Gesture: {gesture}", (10, 30 + len(current_gestures) * 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            total_frames += 1
            
            # Display statistics
            cv2.putText(frame, f"Frames with hands: {frames_with_hands}/{total_frames}", (10, frame_height - 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow("Hands Analysis", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n⏹️  Analysis stopped by user")
    except Exception as e:
        print(f"❌ Error during hands analysis: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Calculate final statistics
    if gesture_counts:
        total_gestures = sum(gesture_counts.values())
        gesture_percentages = {gesture: (count / total_gestures) * 100 for gesture, count in gesture_counts.items()}
        
        print(f"\n📊 Hands Analysis Results:")
        print(f"   Total Frames Analyzed: {total_frames}")
        print(f"   Frames with Hands Detected: {frames_with_hands}")
        print(f"   Total Gestures Detected: {total_gestures}")
        print(f"   Gesture Breakdown:")
        for gesture, percentage in gesture_percentages.items():
            print(f"     • {gesture}: {percentage:.1f}% ({gesture_counts[gesture]} times)")
        
        # Save statistics
        stats = {
            "total_frames": total_frames,
            "frames_with_hands": frames_with_hands,
            "total_gestures": total_gestures,
            "gesture_counts": gesture_counts,
            "gesture_percentages": gesture_percentages
        }
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        with open("data/hands_analysis_stats.json", "w") as f:
            json.dump(stats, f, indent=2)
        
        print("✅ Hands analysis statistics saved to data/hands_analysis_stats.json")
        return stats
    else:
        print("❌ No hand data collected")
        return None

if __name__ == "__main__":
    analyze_hands()
