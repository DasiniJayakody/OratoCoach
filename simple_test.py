#!/usr/bin/env python3
"""
Simple test to verify analysis selection functionality
"""

import json
import subprocess
import time
import os

def test_selection_functionality():
    """Test the analysis selection functionality"""
    print("🧪 Testing Analysis Selection Functionality")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {"name": "Hands Analysis Only", "analyses": ["hands"]},
        {"name": "Face Analysis Only", "analyses": ["face"]},
        {"name": "Pose Analysis Only", "analyses": ["pose"]},
        {"name": "Face and Hands", "analyses": ["face", "hands"]},
        {"name": "All Analyses", "analyses": ["face", "hands", "pose"]},
    ]
    
    print("📋 Test Cases:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"   {i}. {test_case['name']}: {test_case['analyses']}")
    
    print("\n💡 Instructions:")
    print("1. Open http://localhost:5000/analysis in your browser")
    print("2. Select ONLY the analysis types you want to test")
    print("3. Click 'Start Analysis'")
    print("4. Check the console output to see which analyses are actually running")
    print("5. Verify that ONLY the selected analyses open webcam windows")
    
    print("\n🔍 Expected Behavior:")
    print("- If you select 'Hands Analysis Only', only hands analysis should run")
    print("- If you select 'Face Analysis Only', only face analysis should run")
    print("- If you select multiple, only those should run")
    print("- Check the terminal/console for debug messages")
    
    print("\n📊 Debug Messages to Look For:")
    print("- '🎯 Selected analyses: [list]' - shows what was selected")
    print("- '🎬 Starting run_complete_analysis with: [list]' - shows what will run")
    print("- '⏭️  Skipping [analysis] (not selected)' - shows what's being skipped")
    print("- '🔍 Starting [analysis]...' - shows what's actually running")

if __name__ == "__main__":
    test_selection_functionality() 