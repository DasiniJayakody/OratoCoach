#!/usr/bin/env python3
"""
OratoCoach - Main Orchestrator
Runs face analysis, hands analysis, and pose analysis in sequence
Then generates charts and final PDF report
"""

import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from fpdf import FPDF

def generate_gesture_chart(gesture_data):
    """Generate gesture pie chart from hands analysis data"""
    print("📊 Generating gesture pie chart...")
    
    if not gesture_data or 'gesture_counts' not in gesture_data:
        print("❌ No gesture data available")
        return False
    
    gesture_counts = gesture_data['gesture_counts']
    
    if not gesture_counts:
        print("❌ No gestures detected")
        return False
    
    # Create pie chart
    plt.figure(figsize=(8, 6))
    plt.title("Gesture Analysis Results", fontsize=16, fontweight='bold')
    
    # Use different colors for each gesture
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    
    wedges, texts, autotexts = plt.pie(
        gesture_counts.values(), 
        labels=gesture_counts.keys(), 
        autopct='%1.1f%%',
        colors=colors[:len(gesture_counts)],
        startangle=90
    )
    
    # Enhance text appearance
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.axis('equal')
    
    # Save chart
    os.makedirs("data", exist_ok=True)
    plt.savefig("data/gesture_pie_chart.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Gesture pie chart saved to data/gesture_pie_chart.png")
    return True

def generate_pacing_heatmap(movement_data):
    """Generate pacing heatmap from pose analysis data"""
    print("📊 Generating pacing heatmap...")
    
    if not movement_data or 'movement_positions' not in movement_data:
        print("❌ No movement data available")
        return False
    
    positions = movement_data['movement_positions']
    
    if not positions:
        print("❌ No movement positions recorded")
        return False
    
    # Extract x and y coordinates
    x_positions = [pos[0] for pos in positions]
    y_positions = [pos[1] for pos in positions]
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    plt.title("Movement Pacing Heatmap", fontsize=16, fontweight='bold')
    
    # Create 2D histogram
    heatmap, xedges, yedges = np.histogram2d(x_positions, y_positions, bins=20)
    
    # Plot heatmap
    im = plt.imshow(heatmap.T, origin='lower', cmap='hot', interpolation='nearest')
    plt.xlabel('Horizontal Movement (%)', fontsize=12)
    plt.ylabel('Vertical Movement (%)', fontsize=12)
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Time Spent', fontsize=12)
    
    # Add grid
    plt.grid(True, alpha=0.3)
    
    # Save chart
    os.makedirs("data", exist_ok=True)
    plt.savefig("data/pacing_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Pacing heatmap saved to data/pacing_heatmap.png")
    return True

def generate_pdf_report(face_data, hands_data, pose_data):
    """Generate comprehensive PDF report with professional layout"""
    print("📄 Generating PDF report...")
    
    pdf = FPDF()
    pdf.add_page()
    
    # Set margins for better layout
    pdf.set_margins(20, 20, 20)
    
    # Title with better formatting
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(44, 62, 80)  # Dark blue-gray
    pdf.cell(0, 20, "OratoCoach", ln=True, align='C')
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, "Presentation Analysis Report", ln=True, align='C')
    pdf.ln(15)
    
    # Add a decorative line
    pdf.set_draw_color(52, 152, 219)  # Blue
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(10)
    
    # Executive Summary with better formatting
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 12, "Executive Summary", ln=True)
    pdf.ln(5)
    
    # Create a summary box
    pdf.set_fill_color(236, 240, 241)  # Light gray background
    pdf.rect(20, pdf.get_y(), 170, 40, 'F')
    
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(52, 73, 94)
    
    # Face analysis summary
    if face_data:
        eye_contact_score = face_data.get('average_score', 0)
        pdf.cell(0, 8, f"Eye Contact Score: {eye_contact_score:.1f}%", ln=True)
    
    # Pose analysis summary
    if pose_data:
        posture_score = pose_data.get('average_posture_score', 0)
        pdf.cell(0, 8, f"Posture Score: {posture_score:.1f}%", ln=True)
    
    # Hands analysis summary
    if hands_data:
        total_gestures = hands_data.get('total_gestures', 0)
        pdf.cell(0, 8, f"Total Gestures Detected: {total_gestures}", ln=True)
    
    pdf.ln(15)
    
    # Detailed Analysis with better organization
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 12, "Detailed Analysis", ln=True)
    pdf.ln(5)
    
    # Face analysis details with better formatting
    if face_data:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(52, 152, 219)  # Blue
        pdf.cell(0, 10, "Face Analysis", ln=True)
        
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(52, 73, 94)
        
        # Create a formatted list
        details = [
            f"Total Frames Analyzed: {face_data.get('total_frames', 0)}",
            f"Good Eye Contact Frames: {face_data.get('good_eye_contact_frames', 0)}",
            f"Eye Contact Percentage: {face_data.get('eye_contact_percentage', 0):.1f}%"
        ]
        
        for detail in details:
            pdf.cell(10, 6, "", ln=False)  # Indent
            pdf.cell(0, 6, f"- {detail}", ln=True)
        
        pdf.ln(5)
    
    # Pose analysis details
    if pose_data:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(46, 204, 113)  # Green
        pdf.cell(0, 10, "Pose Analysis", ln=True)
        
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(52, 73, 94)
        
        details = [
            f"Total Frames Analyzed: {pose_data.get('total_frames', 0)}",
            f"Good Posture Frames: {pose_data.get('good_posture_frames', 0)}",
            f"Posture Percentage: {pose_data.get('posture_percentage', 0):.1f}%",
            f"Movement Positions Recorded: {len(pose_data.get('movement_positions', []))}"
        ]
        
        for detail in details:
            pdf.cell(10, 6, "", ln=False)  # Indent
            pdf.cell(0, 6, f"- {detail}", ln=True)
        
        pdf.ln(5)
    
    # Hands analysis details
    if hands_data:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(155, 89, 182)  # Purple
        pdf.cell(0, 10, "Hands Analysis", ln=True)
        
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(52, 73, 94)
        
        details = [
            f"Total Frames Analyzed: {hands_data.get('total_frames', 0)}",
            f"Frames with Hands Detected: {hands_data.get('frames_with_hands', 0)}",
            f"Total Gestures Detected: {hands_data.get('total_gestures', 0)}"
        ]
        
        for detail in details:
            pdf.cell(10, 6, "", ln=False)  # Indent
            pdf.cell(0, 6, f"- {detail}", ln=True)
        
        # Gesture breakdown in a table format
        gesture_counts = hands_data.get('gesture_counts', {})
        if gesture_counts:
            pdf.cell(10, 6, "", ln=False)  # Indent
            pdf.cell(0, 6, "- Gesture Breakdown:", ln=True)
            
            # Create a simple table for gestures
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(20, 6, "", ln=False)  # Extra indent
            pdf.cell(60, 6, "Gesture Type", ln=False)
            pdf.cell(30, 6, "Count", ln=False)
            pdf.cell(30, 6, "Percentage", ln=True)
            
            pdf.set_font("Arial", size=10)
            for gesture, count in gesture_counts.items():
                percentage = (count / hands_data['total_gestures']) * 100
                pdf.cell(20, 5, "", ln=False)  # Extra indent
                pdf.cell(60, 5, gesture.replace('_', ' ').title(), ln=False)
                pdf.cell(30, 5, str(count), ln=False)
                pdf.cell(30, 5, f"{percentage:.1f}%", ln=True)
        
        pdf.ln(8)
    
    # Visual Analysis section
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 12, "Visual Analysis", ln=True)
    pdf.ln(5)
    
    # Gesture pie chart - positioned first
    gesture_chart_path = "data/gesture_pie_chart.png"
    if os.path.exists(gesture_chart_path):
        try:
            # Get current Y position for first chart
            current_y = pdf.get_y()
            
            # Center the chart on the page
            chart_width = 120
            chart_x = (210 - chart_width) / 2  # Center horizontally
            pdf.image(gesture_chart_path, x=chart_x, y=current_y, w=chart_width)
            
            # Calculate Y position for caption (chart height is approximately 90mm)
            caption_y = current_y + 90 + 5  # Chart height + 5mm spacing
            pdf.set_y(caption_y)
            
            # Add caption below the chart
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(52, 73, 94)
            pdf.cell(0, 8, "Gesture Distribution Analysis", ln=True, align='C')
            pdf.ln(15)  # Add space after first chart
        except Exception as e:
            print(f"Error adding gesture chart: {e}")
    
    # Pacing heatmap - positioned below the pie chart
    heatmap_path = "data/pacing_heatmap.png"
    if os.path.exists(heatmap_path):
        try:
            # Get current Y position for second chart
            current_y = pdf.get_y()
            
            # Center the chart on the page
            chart_width = 120
            chart_x = (210 - chart_width) / 2  # Center horizontally
            pdf.image(heatmap_path, x=chart_x, y=current_y, w=chart_width)
            
            # Calculate Y position for caption (chart height is approximately 90mm)
            caption_y = current_y + 90 + 5  # Chart height + 5mm spacing
            pdf.set_y(caption_y)
            
            # Add caption below the chart
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(52, 73, 94)
            pdf.cell(0, 8, "Movement Pacing Heatmap", ln=True, align='C')
        except Exception as e:
            print(f"Error adding heatmap: {e}")
    
    pdf.ln(15)
    
    # Recommendations page
    pdf.add_page()
    
    # Recommendations header
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 15, "Recommendations for Improvement", ln=True, align='C')
    pdf.ln(10)
    
    # Add decorative line
    pdf.set_draw_color(52, 152, 219)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(15)
    
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(52, 73, 94)
    
    # Eye contact recommendations with icons
    if face_data:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(52, 152, 219)
        pdf.cell(0, 10, "Eye Contact Recommendations", ln=True)
        pdf.ln(3)
        
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(52, 73, 94)
        
        eye_score = face_data.get('average_score', 0)
        if eye_score < 60:
            recommendation = "Practice maintaining direct eye contact with your audience. Try to look at the camera lens directly and hold eye contact for 3-5 seconds before looking away."
        elif eye_score < 80:
            recommendation = "Good eye contact, but try to maintain more consistent eye contact throughout your presentation. Vary your gaze naturally."
        else:
            recommendation = "Excellent eye contact! You're engaging well with your audience. Keep up the great work!"
        
        pdf.multi_cell(0, 6, recommendation)
        pdf.ln(8)
    
    # Posture recommendations
    if pose_data:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(46, 204, 113)
        pdf.cell(0, 10, "Posture Recommendations", ln=True)
        pdf.ln(3)
        
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(52, 73, 94)
        
        posture_score = pose_data.get('average_posture_score', 0)
        if posture_score < 60:
            recommendation = "Focus on standing straight with shoulders back and relaxed. Keep your feet shoulder-width apart and distribute weight evenly."
        elif posture_score < 80:
            recommendation = "Good posture, but try to maintain it more consistently throughout your presentation. Remember to breathe naturally."
        else:
            recommendation = "Excellent posture! You're presenting confidently with good body alignment. Maintain this strong presence!"
        
        pdf.multi_cell(0, 6, recommendation)
        pdf.ln(8)
    
    # Gesture recommendations
    if hands_data:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(155, 89, 182)
        pdf.cell(0, 10, "Gesture Recommendations", ln=True)
        pdf.ln(3)
        
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(52, 73, 94)
        
        gesture_counts = hands_data.get('gesture_counts', {})
        if 'no_gesture' in gesture_counts and gesture_counts['no_gesture'] > 50:
            recommendation = "Try using more hand gestures to engage your audience. Use open palms, pointing gestures, and natural movements to emphasize key points."
        elif 'pointing' in gesture_counts and gesture_counts['pointing'] > 30:
            recommendation = "Good use of pointing gestures, but try to vary them more. Include open palms, counting gestures, and descriptive hand movements."
        else:
            recommendation = "Good variety of gestures! You're using your hands effectively to communicate. Continue to use natural, purposeful movements."
        
        pdf.multi_cell(0, 6, recommendation)
        pdf.ln(8)
    
    # Overall tips section
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 12, "General Presentation Tips", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(52, 73, 94)
    
    tips = [
        "Practice your presentation multiple times to build confidence",
        "Use pauses effectively to emphasize important points",
        "Vary your vocal tone and pace to maintain audience interest",
        "Prepare for questions and practice your responses",
        "Record yourself presenting to identify areas for improvement"
    ]
    
    for i, tip in enumerate(tips, 1):
        pdf.cell(10, 6, "", ln=False)  # Indent
        pdf.cell(0, 6, f"{i}. {tip}", ln=True)
    
    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(149, 165, 166)
    pdf.cell(0, 8, "Generated by OratoCoach - AI-Powered Presentation Analysis", ln=True, align='C')
    pdf.cell(0, 6, "For best results, practice regularly and review your progress", ln=True, align='C')
    
    # Save PDF
    os.makedirs("data", exist_ok=True)
    pdf_path = "data/presentation_summary.pdf"
    try:
        pdf.output(pdf_path)
        print(f"✅ PDF report generated: {pdf_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving PDF: {e}")
        return False

def main():
    """Main orchestrator function"""
    print("🎯 OratoCoach - Complete Presentation Analysis")
    print("=" * 50)
    print("This will run all three analyses in sequence:")
    print("1. Face Analysis (Eye Contact)")
    print("2. Hands Analysis (Gestures)")
    print("3. Pose Analysis (Posture & Movement)")
    print("Then generate charts and final PDF report")
    print("=" * 50)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Step 1: Face Analysis
    print("\n🔍 STEP 1: Starting Face Analysis...")
    from face_analysis import analyze_face
    face_data = analyze_face()
    
    if not face_data:
        print("⚠️  Face analysis failed or was skipped")
        face_data = None
    
    # Step 2: Hands Analysis
    print("\n✋ STEP 2: Starting Hands Analysis...")
    from hands_analysis import analyze_hands
    hands_data = analyze_hands()
    
    if not hands_data:
        print("⚠️  Hands analysis failed or was skipped")
        hands_data = None
    
    # Step 3: Pose Analysis
    print("\n🧍 STEP 3: Starting Pose Analysis...")
    from pose_analysis import analyze_pose
    pose_data = analyze_pose()
    
    if not pose_data:
        print("⚠️  Pose analysis failed or was skipped")
        pose_data = None
    
    # Generate charts and PDF
    print("\n📊 STEP 4: Generating Charts and Report...")
    
    # Generate gesture chart
    if hands_data:
        generate_gesture_chart(hands_data)
    
    # Generate pacing heatmap
    if pose_data:
        generate_pacing_heatmap(pose_data)
    
    # Generate final PDF report
    generate_pdf_report(face_data, hands_data, pose_data)
    
    print("\n🎉 Analysis Complete!")
    print("📁 Check the 'data' folder for your results:")
    if face_data:
        print("   • data/face_analysis_stats.json")
    if hands_data:
        print("   • data/hands_analysis_stats.json")
    if pose_data:
        print("   • data/pose_analysis_stats.json")
    print("   • data/gesture_pie_chart.png")
    print("   • data/pacing_heatmap.png")
    print("   • data/presentation_summary.pdf")

if __name__ == "__main__":
    main()
