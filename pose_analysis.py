import cv2
import mediapipe as mp
import numpy as np
import json
import os

def calculate_angle(a, b, c):
    """Calculate angle between three points"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle

def analyze_pose():
    """Analyze body pose and posture"""
    print("🧍 Starting Pose Analysis...")
    print("Stand naturally and move around for movement analysis")
    print("Press 'q' to stop analysis")
    
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return None
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    posture_scores = []
    movement_positions = []
    total_frames = 0
    good_posture_frames = 0
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                
                # Get key pose points
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                
                # Calculate posture angle (shoulder-hip-knee)
                left_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                right_angle = calculate_angle(right_shoulder, right_hip, right_knee)
                avg_angle = (left_angle + right_angle) / 2
                
                # Score posture (0-100)
                if avg_angle >= 160:
                    posture_score = 100
                elif avg_angle >= 150:
                    posture_score = 80
                elif avg_angle >= 140:
                    posture_score = 60
                elif avg_angle >= 130:
                    posture_score = 40
                else:
                    posture_score = 20
                
                posture_scores.append(posture_score)
                
                if posture_score >= 70:
                    good_posture_frames += 1
                    feedback = "Good posture"
                    color = (0, 255, 0)
                else:
                    feedback = "Fix your posture!"
                    color = (0, 0, 255)
                
                # Record movement position (center of shoulders)
                center_x = (left_shoulder[0] + right_shoulder[0]) / 2
                center_y = (left_shoulder[1] + right_shoulder[1]) / 2
                movement_positions.append((center_x * 100, center_y * 100))  # Scale to 0-100
                
                # Display feedback on frame
                cv2.putText(frame, f"{feedback} ({int(avg_angle)}°)", (30, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.putText(frame, f"Posture Score: {posture_score:.0f}%", (30, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                
                # Draw pose landmarks
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            total_frames += 1
            
            # Display frame counter
            cv2.putText(frame, f"Frames: {total_frames}", (10, frame_height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('Pose Analysis', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n⏹️  Analysis stopped by user")
    except Exception as e:
        print(f"❌ Error during pose analysis: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Calculate final statistics
    if posture_scores:
        avg_posture_score = sum(posture_scores) / len(posture_scores)
        posture_percentage = (good_posture_frames / len(posture_scores)) * 100
        
        print(f"\n📊 Pose Analysis Results:")
        print(f"   Total Frames Analyzed: {total_frames}")
        print(f"   Average Posture Score: {avg_posture_score:.2f}%")
        print(f"   Good Posture Frames: {good_posture_frames}/{len(posture_scores)}")
        print(f"   Posture Percentage: {posture_percentage:.2f}%")
        print(f"   Movement Positions Recorded: {len(movement_positions)}")
        
        # Save statistics
        stats = {
            "total_frames": total_frames,
            "posture_scores": posture_scores,
            "average_posture_score": avg_posture_score,
            "good_posture_frames": good_posture_frames,
            "posture_percentage": posture_percentage,
            "movement_positions": movement_positions
        }
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        with open("data/pose_analysis_stats.json", "w") as f:
            json.dump(stats, f, indent=2)
        
        print("✅ Pose analysis statistics saved to data/pose_analysis_stats.json")
        return stats
    else:
        print("❌ No pose data collected")
        return None

if __name__ == "__main__":
    analyze_pose()

