import cv2
import mediapipe as mp
import numpy as np
import json
import os

def analyze_face():
    """Analyze face and eye contact patterns"""
    print("👁️ Starting Face Analysis...")
    print("Look at the camera for best eye contact detection")
    print("Press 'q' to stop analysis")
    
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return {"error": "Could not open camera"}
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    eye_contact_scores = []
    total_frames = 0
    good_eye_contact_frames = 0
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image_rgb)
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Calculate eye contact score based on eye landmarks
                    landmarks = face_landmarks.landmark
                    
                    # Get eye landmarks (simplified approach)
                    left_eye = landmarks[33]
                    right_eye = landmarks[263]
                    nose_tip = landmarks[1]
                    
                    # Calculate gaze direction (simplified)
                    eye_center_x = (left_eye.x + right_eye.x) / 2
                    eye_center_y = (left_eye.y + right_eye.y) / 2
                    
                    # Distance from center (0.5, 0.5)
                    center_distance = np.sqrt((eye_center_x - 0.5)**2 + (eye_center_y - 0.5)**2)
                    
                    # Score based on proximity to center
                    eye_contact_score = max(0, 100 - (center_distance * 200))
                    eye_contact_scores.append(eye_contact_score)
                    
                    if eye_contact_score > 70:
                        good_eye_contact_frames += 1
                        feedback = "Good eye contact!"
                        color = (0, 255, 0)
                    else:
                        feedback = "Look at the camera"
                        color = (0, 0, 255)
                    
                    # Display feedback
                    cv2.putText(frame, feedback, (30, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                    cv2.putText(frame, f"Score: {eye_contact_score:.1f}%", (30, 90),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    # Draw face landmarks
                    mp_drawing.draw_landmarks(
                        frame, face_landmarks,
                        mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing.DrawingSpec(
                            color=(0, 255, 0), thickness=1, circle_radius=1)
                    )
            
            total_frames += 1
            
            # Display frame counter
            cv2.putText(frame, f"Frames: {total_frames}", (10, frame_height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('Face Analysis', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n⏹️  Analysis stopped by user")
    except Exception as e:
        print(f"❌ Error during face analysis: {e}")
        return {"error": str(e)}
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Calculate final statistics
    if eye_contact_scores:
        average_score = sum(eye_contact_scores) / len(eye_contact_scores)
        eye_contact_percentage = (good_eye_contact_frames / len(eye_contact_scores)) * 100
        
        print(f"\n📊 Face Analysis Results:")
        print(f"   Total Frames Analyzed: {total_frames}")
        print(f"   Average Eye Contact Score: {average_score:.2f}%")
        print(f"   Good Eye Contact Frames: {good_eye_contact_frames}/{len(eye_contact_scores)}")
        print(f"   Eye Contact Percentage: {eye_contact_percentage:.2f}%")
        
        # Save statistics
        stats = {
            "total_frames": total_frames,
            "eye_contact_scores": eye_contact_scores,
            "average_score": average_score,
            "good_eye_contact_frames": good_eye_contact_frames,
            "eye_contact_percentage": eye_contact_percentage
        }
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        with open("data/face_analysis_stats.json", "w") as f:
            json.dump(stats, f, indent=2)
        
        print("✅ Face analysis statistics saved to data/face_analysis_stats.json")
        return stats
    else:
        print("❌ No face data collected")
        return {"error": "No face data collected"}

if __name__ == "__main__":
    analyze_face()
