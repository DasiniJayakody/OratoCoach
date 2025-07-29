import cv2
import mediapipe as mp
import numpy as np
import sys
import json
import os

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calculate_eye_contact_score(landmarks, frame_width, frame_height):
    """Calculate eye contact score based on multiple factors"""
    
    def get_point(index):
        landmark = landmarks.landmark[index]
        return [int(landmark.x * frame_width), int(landmark.y * frame_height)]
    
    try:
        # Get key facial landmarks
        left_eye = get_point(33)
        right_eye = get_point(263)
        nose_tip = get_point(1)
        left_ear = get_point(234)
        right_ear = get_point(454)
        
        # Get additional eye landmarks for better detection
        left_eye_inner = get_point(133)
        left_eye_outer = get_point(33)
        right_eye_inner = get_point(362)
        right_eye_outer = get_point(263)
        
        # Calculate face center
        face_center_x = (left_ear[0] + right_ear[0]) / 2
        face_center_y = (left_eye[1] + right_eye[1]) / 2
        
        # Calculate frame center
        frame_center_x = frame_width / 2
        frame_center_y = frame_height / 2
        
        # Factor 1: Face position relative to frame center (more lenient)
        distance_from_center = euclidean_distance(
            [face_center_x, face_center_y], 
            [frame_center_x, frame_center_y]
        )
        
        # Factor 2: Eye level difference (tolerance for natural head tilt)
        eye_level_diff = abs(left_eye[1] - right_eye[1])
        
        # Factor 3: Face size (closer = better eye contact potential)
        face_width = euclidean_distance(left_ear, right_ear)
        face_height = euclidean_distance(left_eye, nose_tip) * 2
        
        # Factor 4: Eye openness (squinting might indicate looking away)
        left_eye_openness = euclidean_distance(left_eye_inner, left_eye_outer)
        right_eye_openness = euclidean_distance(right_eye_inner, right_eye_outer)
        avg_eye_openness = (left_eye_openness + right_eye_openness) / 2
        
        # Factor 5: Head rotation (check if face is reasonably forward-facing)
        head_rotation = abs(left_ear[0] - right_ear[0]) / face_width
        
        # Scoring system (0-100)
        score = 100
        
        # Deduct points for each factor
        # Position penalty (more lenient)
        if distance_from_center > 150:
            score -= 30
        elif distance_from_center > 100:
            score -= 15
        elif distance_from_center > 50:
            score -= 5
        
        # Eye level penalty (allow natural head tilt)
        if eye_level_diff > 30:
            score -= 20
        elif eye_level_diff > 20:
            score -= 10
        elif eye_level_diff > 10:
            score -= 5
        
        # Face size penalty (too far or too close)
        if face_width < 100 or face_width > 300:
            score -= 20
        elif face_width < 150 or face_width > 250:
            score -= 10
        
        # Eye openness penalty
        if avg_eye_openness < 15:
            score -= 15
        elif avg_eye_openness < 20:
            score -= 5
        
        # Head rotation penalty (allow some natural movement)
        if head_rotation > 0.3:
            score -= 25
        elif head_rotation > 0.2:
            score -= 15
        elif head_rotation > 0.1:
            score -= 5
        
        # Ensure score is within bounds
        score = max(0, min(100, score))
        
        return score
        
    except Exception as e:
        print(f"Error calculating eye contact score: {e}")
        return 0

def analyze_face():
    """Analyze face and collect eye contact statistics"""
    print("🔍 Starting Face Analysis...")
    print("Look directly at the camera for best results")
    print("Press 'q' to stop analysis")
    
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return None
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    eye_contact_scores = []
    total_frames = 0
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                
                # Calculate eye contact score
                score = calculate_eye_contact_score(landmarks, frame_width, frame_height)
                eye_contact_scores.append(score)
                total_frames += 1
                
                # Display score on frame
                cv2.putText(frame, f"Eye Contact: {score:.1f}%", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Draw face mesh
                for face_landmarks in results.multi_face_landmarks:
                    def get_point(index):
                        landmark = face_landmarks.landmark[index]
                        return [int(landmark.x * frame_width), int(landmark.y * frame_height)]
                    
                    # Draw key points
                    key_points = [33, 263, 1, 133, 362]  # eyes, nose, eye corners
                    for point_id in key_points:
                        point = get_point(point_id)
                        cv2.circle(frame, point, 3, (0, 255, 0), -1)
            
            cv2.imshow("Face Analysis", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n⏹️  Analysis stopped by user")
    except Exception as e:
        print(f"❌ Error during face analysis: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Calculate final statistics
    if eye_contact_scores:
        avg_score = sum(eye_contact_scores) / len(eye_contact_scores)
        good_eye_contact_frames = sum(1 for score in eye_contact_scores if score >= 70)
        eye_contact_percentage = (good_eye_contact_frames / len(eye_contact_scores)) * 100
        
        print(f"\n📊 Face Analysis Results:")
        print(f"   Total Frames Analyzed: {total_frames}")
        print(f"   Average Eye Contact Score: {avg_score:.2f}%")
        print(f"   Good Eye Contact Frames: {good_eye_contact_frames}/{total_frames}")
        print(f"   Eye Contact Percentage: {eye_contact_percentage:.2f}%")
        
        # Save statistics
        stats = {
            "total_frames": total_frames,
            "eye_contact_scores": eye_contact_scores,
            "average_score": avg_score,
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
        return None

if __name__ == "__main__":
    analyze_face()
