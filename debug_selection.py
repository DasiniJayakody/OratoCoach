#!/usr/bin/env python3
"""
Debug script to test analysis selection in isolation
"""

import json
import threading
import time

# Mock the analysis functions to see what's being called
def mock_analyze_face():
    print("🔍 MOCK: Face analysis called")
    return {"mock": "face_data"}

def mock_analyze_hands():
    print("🤚 MOCK: Hands analysis called")
    return {"mock": "hands_data"}

def mock_analyze_pose():
    print("🧍 MOCK: Pose analysis called")
    return {"mock": "pose_data"}

def test_run_complete_analysis(selected_analyses):
    """Test the run_complete_analysis function with mock data"""
    print(f"🎬 Testing run_complete_analysis with: {selected_analyses}")
    
    analysis_results = {
        'face_data': None,
        'hands_data': None,
        'pose_data': None,
        'analysis_completed': False,
        'pdf_generated': False
    }
    
    analysis_status = {
        'is_running': True,
        'current_step': '',
        'progress': 0
    }
    
    try:
        print(f"🎬 Starting run_complete_analysis with: {selected_analyses}")
        analysis_status['is_running'] = True
        analysis_status['progress'] = 0
        
        total_steps = len(selected_analyses)
        current_step = 0
        
        print(f"📊 Total steps to run: {total_steps}")
        
        # Face Analysis
        if 'face' in selected_analyses:
            current_step += 1
            progress = (current_step / total_steps) * 100
            analysis_status['current_step'] = 'Analyzing eye contact and facial expressions...'
            analysis_status['progress'] = progress
            print("🔍 Starting face analysis...")
            face_data = mock_analyze_face()
            analysis_results['face_data'] = face_data
            print("✅ Face analysis completed")
        else:
            print("⏭️  Skipping face analysis (not selected)")
        
        # Hands Analysis
        if 'hands' in selected_analyses:
            current_step += 1
            progress = (current_step / total_steps) * 100
            analysis_status['current_step'] = 'Analyzing hand gestures and movements...'
            analysis_status['progress'] = progress
            print("🤚 Starting hands analysis...")
            hands_data = mock_analyze_hands()
            analysis_results['hands_data'] = hands_data
            print("✅ Hands analysis completed")
        else:
            print("⏭️  Skipping hands analysis (not selected)")
        
        # Pose Analysis
        if 'pose' in selected_analyses:
            current_step += 1
            progress = (current_step / total_steps) * 100
            analysis_status['current_step'] = 'Analyzing body posture and movement...'
            analysis_status['progress'] = progress
            print("🧍 Starting pose analysis...")
            pose_data = mock_analyze_pose()
            analysis_results['pose_data'] = pose_data
            print("✅ Pose analysis completed")
        else:
            print("⏭️  Skipping pose analysis (not selected)")
        
        # Mark analysis as completed
        analysis_results['analysis_completed'] = True
        analysis_status['progress'] = 100
        analysis_status['current_step'] = 'Analysis completed!'
        
        print(f"✅ Analysis completed successfully! Ran: {', '.join(selected_analyses)}")
        print(f"📊 Final results: {analysis_results}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        analysis_status['current_step'] = f'Error: {str(e)}'
    finally:
        analysis_status['is_running'] = False

def main():
    """Test different selection scenarios"""
    print("🧪 Debug Analysis Selection")
    print("=" * 50)
    
    test_cases = [
        ["hands"],
        ["face"],
        ["pose"],
        ["face", "hands"],
        ["face", "hands", "pose"]
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case {i}: {test_case}")
        print("-" * 30)
        test_run_complete_analysis(test_case)
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print("🎯 Debug Summary:")
    print("If the above tests show correct behavior, the issue is elsewhere.")
    print("If you see all analyses running regardless of selection, there's a logic error.")

if __name__ == "__main__":
    main() 