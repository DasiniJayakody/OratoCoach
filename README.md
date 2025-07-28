# 🚀 OratoCoach Project Testing Guide

This guide will help you verify that your OratoCoach presentation coaching system is working correctly.

## 📋 Prerequisites Check

### Step 1: Verify Environment Setup

```bash
# Make sure you're in the project directory
cd D:\OratoCoach

# Activate virtual environment (if not already active)
venv\Scripts\activate

# Check Python version
python --version
```

### Step 2: Run Automated Test Suite

```bash
# Run the comprehensive test suite
python test_project.py
```

**Expected Output:**

- ✅ All 5 tests should pass
- No critical errors should appear
- Webcam access should be confirmed

## 🔍 Individual Component Testing

### Step 3: Test Webcam Access

```bash
# Test basic webcam functionality
python test_webcam.py
```

**What to expect:**

- A window should open showing your webcam feed
- You should see yourself in real-time
- Press 'q' to quit the application

**If it fails:**

- Check if your webcam is connected and not being used by another application
- Try different camera indices (0, 1, 2) in the code

### Step 4: Test Face Analysis

```bash
# Test face detection and analysis
python face_analysis.py
```

**What to expect:**

- Webcam window with face mesh overlay
- Real-time feedback on eye contact and smile
- Green text for good eye contact: "✅ Good eye contact"
- Blue text for smiling: "😁 Great smile!"
- Press 'q' to quit

**Testing scenarios:**

1. **Eye Contact Test**: Look directly at the camera
   - Should show "✅ Good eye contact"
2. **Look Away Test**: Look to the side
   - Should show "👀 Look at the camera!"
3. **Smile Test**: Smile naturally
   - Should show "😁 Great smile!"
4. **Neutral Face Test**: Keep a straight face
   - Should show "😊 Smile more!"

### Step 5: Test Posture Analysis

```bash
# Test posture detection
python pose_analysis.py
```

**What to expect:**

- Webcam window with pose skeleton overlay
- Real-time posture feedback
- Angle measurements displayed
- Press 'q' to quit

**Testing scenarios:**

1. **Good Posture**: Stand/sit straight with shoulders back
   - Should show "Good posture" in green
   - Angle should be ≥150°
2. **Poor Posture**: Slouch or lean forward
   - Should show "Fix your posture!" in red
   - Angle will be <150°

### Step 6: Test Hand Detection

```bash
# Test hand gesture detection
python hands_analysis.py
```

**What to expect:**

- Webcam window with hand landmark overlay
- Hand skeleton should appear when hands are visible
- Press 'q' to quit

**Testing scenarios:**

1. **Show hands**: Hold your hands up to the camera
   - Should see hand skeleton overlay
2. **Move hands**: Wave or gesture
   - Skeleton should follow hand movements
3. **Hide hands**: Put hands behind back
   - Skeleton should disappear

## 🧪 Advanced Testing

### Step 7: Test Report Generation

```bash
# Test the report generation system
python -c "
from report_generator import export_pdf_report
export_pdf_report(85.5, 92.3, {'pointing': 30.0, 'open_palms': 25.0, 'closed_fists': 15.0, 'no_gesture': 30.0})
print('Report generated successfully!')
"
```

**What to expect:**

- PDF report should be created in `data/presentation_summary.pdf`
- Console should show "PDF report generated: data/presentation_summary.pdf"

### Step 8: Test Main Application Logic

```bash
# Test the main analysis function
python -c "
from main import generate_report
import numpy as np

# Simulate data
posture_scores = [1, 1, 0, 1, 1] * 20  # 100 frames
eye_contact_flags = [1, 1, 1, 0, 1] * 20
gesture_labels = ['pointing', 'open_palms', 'no_gesture'] * 33 + ['pointing']
positions = [(np.random.randint(0, 100), np.random.randint(0, 100)) for _ in range(100)]

generate_report(posture_scores, eye_contact_flags, gesture_labels, positions)
print('Main analysis completed!')
"
```

**What to expect:**

- Console output showing scores and percentages
- Two image files should be created:
  - `gesture_pie_chart.png`
  - `pacing_heatmap.png`

## 🔧 Troubleshooting Common Issues

### Issue 1: Webcam Not Working

**Symptoms:** No video feed or "Camera not available" error

**Solutions:**

1. Check if webcam is connected
2. Close other applications using the camera
3. Try different camera index:
   ```python
   cap = cv2.VideoCapture(1)  # Try 1, 2, etc.
   ```

### Issue 2: MediaPipe Models Not Loading

**Symptoms:** "MediaPipe models - FAILED" error

**Solutions:**

1. Reinstall MediaPipe: `pip install --upgrade mediapipe`
2. Check internet connection (models download on first use)
3. Restart Python environment

### Issue 3: Face Not Detected

**Symptoms:** No face mesh overlay appears

**Solutions:**

1. Ensure good lighting
2. Face the camera directly
3. Remove glasses or hats if needed
4. Check if face is within camera frame

### Issue 4: Pose Detection Issues

**Symptoms:** No pose skeleton or incorrect angles

**Solutions:**

1. Ensure full body is visible
2. Stand at appropriate distance from camera
3. Wear contrasting clothing
4. Check lighting conditions

### Issue 5: Report Generation Fails

**Symptoms:** PDF creation errors

**Solutions:**

1. Ensure `data/` directory exists
2. Check write permissions
3. Verify FPDF installation: `pip install fpdf`

## ✅ Success Criteria

Your project is working correctly if:

1. **✅ Automated tests pass** (5/5 tests)
2. **✅ Webcam feed displays** in all modules
3. **✅ Face analysis provides feedback** on eye contact and smile
4. **✅ Posture analysis shows skeleton** and angle measurements
5. **✅ Hand detection displays landmarks** when hands are visible
6. **✅ Reports generate successfully** with PDF output
7. **✅ No critical errors** in console output

## 🎯 Performance Benchmarks

**Expected Performance:**

- **Frame Rate**: 15-30 FPS (depending on hardware)
- **Detection Accuracy**: >80% for face and pose
- **Response Time**: <100ms for real-time feedback
- **Memory Usage**: <500MB RAM

## 📞 Next Steps

If all tests pass:

1. **Start using the system** for presentation practice
2. **Customize thresholds** in the code for your preferences
3. **Integrate with your workflow** for regular practice sessions

If tests fail:

1. **Check the troubleshooting section** above
2. **Verify all dependencies** are installed correctly
3. **Test on different hardware** if available
4. **Check system requirements** (Windows 10+, Python 3.8+)

---

**Need Help?** Check the console output for specific error messages and refer to the troubleshooting section above.
