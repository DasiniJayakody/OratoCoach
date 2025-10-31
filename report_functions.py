import os
import json
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import math
from datetime import datetime


def generate_gesture_chart(hands_data):
    """Generate pie chart for gesture analysis"""
    if not hands_data or "gesture_percentages" not in hands_data:
        return False

    try:
        # Create pie chart
        gestures = list(hands_data["gesture_percentages"].keys())
        percentages = list(hands_data["gesture_percentages"].values())

        # Use a more stable figure size for PDF
        plt.figure(figsize=(8, 6), dpi=100)
        colors = ["#3b82f6", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b", "#ef4444"]
        plt.pie(
            percentages,
            labels=gestures,
            autopct="%1.1f%%",
            colors=colors[: len(gestures)],
        )
        plt.title("Gesture Analysis Breakdown", fontsize=14, fontweight="bold")
        plt.axis("equal")

        # Save chart with optimized settings for PDF
        os.makedirs("data", exist_ok=True)
        plt.savefig(
            "data/gesture_pie_chart.png",
            dpi=150,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none",
            pad_inches=0.1,
        )
        plt.close()

        print("✅ Gesture pie chart saved to data/gesture_pie_chart.png")
        return True

    except Exception as e:
        print(f"❌ Error generating gesture chart: {e}")
        return False


def generate_pacing_heatmap(pose_data):
    """Generate heatmap for movement/pacing analysis"""
    if not pose_data or "movement_positions" not in pose_data:
        return False

    try:
        # Extract movement positions
        positions = pose_data["movement_positions"]
        if not positions:
            return False

        x_coords = [pos[0] for pos in positions]
        y_coords = [pos[1] for pos in positions]

        # Create heatmap with optimized settings
        plt.figure(figsize=(8, 6), dpi=100)
        plt.hist2d(x_coords, y_coords, bins=15, cmap="Blues")
        plt.colorbar(label="Frequency")
        plt.xlabel("Horizontal Position (%)", fontsize=10)
        plt.ylabel("Vertical Position (%)", fontsize=10)
        plt.title(
            "Movement Heatmap - Presentation Pacing", fontsize=14, fontweight="bold"
        )
        plt.grid(True, alpha=0.3)

        # Save chart with optimized settings for PDF
        os.makedirs("data", exist_ok=True)
        plt.savefig(
            "data/pacing_heatmap.png",
            dpi=150,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none",
            pad_inches=0.1,
        )
        plt.close()

        print("✅ Pacing heatmap saved to data/pacing_heatmap.png")
        return True

    except Exception as e:
        print(f"❌ Error generating pacing heatmap: {e}")
        return False


class ProfessionalPDF(FPDF):
    def header(self):
        # Professional header with softer blue
        self.set_fill_color(59, 130, 246)  # Softer blue color
        self.rect(0, 0, 210, 40, "F")

        # Logo/Title area
        self.set_font("Arial", "B", 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 25, "OratoCoach", ln=True, align="C")

        # Subtitle
        self.set_font("Arial", "I", 10)
        self.cell(0, 8, "AI-Powered Presentation Analysis", ln=True, align="C")

        # Reset position
        self.set_y(50)

    def footer(self):
        # Professional footer
        self.set_y(-25)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(
            0,
            5,
            "Empowering confident communication through AI-powered analysis",
            ln=True,
            align="C",
        )
        self.cell(
            0,
            5,
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            ln=True,
            align="C",
        )
        self.cell(0, 5, "Page " + str(self.page_no()) + "/{nb}", ln=True, align="C")

    def chapter_title(self, title):
        # Professional chapter title
        self.set_font("Arial", "B", 16)
        self.set_text_color(59, 130, 246)  # Softer blue color
        self.cell(0, 12, title, ln=True)
        self.ln(4)

    def section_title(self, title):
        # Professional section title
        self.set_font("Arial", "B", 12)
        self.set_text_color(59, 130, 246)  # Softer blue color
        self.cell(0, 8, title, ln=True)
        self.ln(2)

    def metric_box(self, title, value, description=""):
        # Professional metric display box
        self.set_fill_color(248, 250, 252)
        self.set_draw_color(226, 232, 240)
        self.rect(self.get_x(), self.get_y(), 85, 25, "FD")

        # Title
        self.set_font("Arial", "B", 9)
        self.set_text_color(59, 130, 246)  # Softer blue color
        self.cell(85, 8, title, ln=True)

        # Value
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 0, 0)
        self.cell(85, 10, str(value), ln=True)

        # Description
        if description:
            self.set_font("Arial", "", 7)
            self.set_text_color(100, 100, 100)
            self.cell(85, 6, description, ln=True)

        self.ln(2)

    def assessment_box(self, assessment, color_code="blue"):
        # Professional assessment display
        colors = {
            "excellent": (34, 197, 94),
            "good": (245, 158, 11),
            "needs_improvement": (239, 68, 68),
            "blue": (59, 130, 246),  # Softer blue color
        }

        color = colors.get(color_code, colors["blue"])
        self.set_fill_color(color[0], color[1], color[2])
        self.set_draw_color(color[0], color[1], color[2])
        self.rect(self.get_x(), self.get_y(), 170, 15, "FD")

        self.set_font("Arial", "B", 9)
        self.set_text_color(255, 255, 255)
        self.cell(170, 15, assessment, ln=True, align="C")
        self.ln(2)


def generate_pdf_report(face_data=None, hands_data=None, pose_data=None):
    """Generate professional PDF report with modern design"""
    try:
        # Helper to determine whether provided data is meaningful (i.e. user selected that analysis).
        def _has_valid_keys(data, keys):
            return bool(data) and not data.get("error") and any(k in data for k in keys)

        face_valid = _has_valid_keys(
            face_data, ["eye_contact_percentage", "total_frames"]
        )
        hands_valid = _has_valid_keys(
            hands_data, ["total_gestures", "gesture_percentages", "total_frames"]
        )
        pose_valid = _has_valid_keys(
            pose_data,
            [
                "average_posture_score",
                "movement_positions",
                "good_posture_frames",
                "total_frames",
            ],
        )

        # Determine which analyses were performed (only include truly valid ones)
        analyses_performed = []
        if face_valid:
            analyses_performed.append("Eye Contact Analysis")
        if hands_valid:
            analyses_performed.append("Hand Gesture Analysis")
        if pose_valid:
            analyses_performed.append("Body Posture Analysis")

        # Create PDF with professional settings
        pdf = ProfessionalPDF()
        pdf.alias_nb_pages()
        pdf.add_page()

        # Set professional margins
        pdf.set_margins(25, 50, 25)

        # ===== COVER PAGE =====
        # Professional cover design with softer blue
        pdf.set_fill_color(59, 130, 246)  # Softer blue color
        pdf.rect(0, 0, 210, 297, "F")

        # Center content
        pdf.set_y(80)

        # Main title - OratoCoach first
        pdf.set_font("Arial", "B", 36)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 25, "OratoCoach", ln=True, align="C")

        # Report title
        pdf.set_y(140)
        pdf.set_font("Arial", "B", 28)
        pdf.cell(0, 20, "Presentation", ln=True, align="C")
        pdf.cell(0, 20, "Analysis Report", ln=True, align="C")

        # Additional subtitle - make it dynamic based on analyses performed
        pdf.set_y(220)
        pdf.set_font("Arial", "I", 14)
        if len(analyses_performed) == 1:
            subtitle = f"AI-Powered {analyses_performed[0]}"
        elif len(analyses_performed) == 2:
            subtitle = f"AI-Powered {analyses_performed[0]} & {analyses_performed[1]}"
        elif len(analyses_performed) == 3:
            subtitle = "Comprehensive AI-Powered Assessment"
        else:
            subtitle = "AI-Powered Presentation Analysis"
        pdf.cell(0, 10, subtitle, ln=True, align="C")

        # Date
        pdf.set_y(250)
        pdf.set_font("Arial", "", 12)
        current_time = datetime.now().strftime("%B %d, %Y")
        pdf.cell(0, 10, current_time, ln=True, align="C")

        # ===== EXECUTIVE SUMMARY PAGE =====
        pdf.add_page()
        pdf.chapter_title("Executive Summary")

        # Overview text - make it dynamic based on analyses performed
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)

        if len(analyses_performed) == 1:
            overview_text = f"This analysis evaluates your presentation performance focusing on {analyses_performed[0].lower()}. The results provide actionable insights to enhance your public speaking effectiveness and audience engagement."
        elif len(analyses_performed) == 2:
            overview_text = f"This analysis evaluates your presentation performance across {analyses_performed[0].lower()} and {analyses_performed[1].lower()}. The results provide actionable insights to enhance your public speaking effectiveness and audience engagement."
        elif len(analyses_performed) == 3:
            overview_text = "This comprehensive analysis evaluates your presentation performance across multiple dimensions including eye contact, hand gestures, body posture, and movement patterns. The results provide actionable insights to enhance your public speaking effectiveness and audience engagement."
        else:
            overview_text = "No analyses were selected. Please run at least one analysis to generate a detailed report."

        pdf.multi_cell(0, 6, overview_text)
        pdf.ln(8)

        # Key metrics section
        pdf.section_title("Key Performance Indicators")

        # Calculate overall score only for performed analyses
        scores = []
        if face_valid:
            scores.append(face_data.get("eye_contact_percentage", 0))
        if pose_valid:
            scores.append(pose_data.get("average_posture_score", 0))
        if hands_valid:
            # Convert gesture count to a score
            total_gestures = hands_data.get("total_gestures", 0)
            gesture_score = (
                min(100, (total_gestures / 50) * 100) if total_gestures > 0 else 0
            )
            scores.append(gesture_score)

        overall_score = sum(scores) / len(scores) if scores else 0

        # Display key metrics in professional boxes
        x_start = pdf.get_x()
        y_start = pdf.get_y()

        # Overall Score (only show if multiple analyses were performed)
        if len(analyses_performed) > 1:
            pdf.metric_box(
                "Overall Score", f"{overall_score:.1f}%", "Combined performance"
            )

        # Eye Contact
        if face_valid:
            if len(analyses_performed) > 1:
                pdf.set_x(x_start + 95)
                pdf.set_y(y_start)
            eye_contact = face_data.get("eye_contact_percentage", 0)
            pdf.metric_box("Eye Contact", f"{eye_contact:.1f}%", "Audience engagement")

        # Posture Score
        if pose_valid:
            if len(analyses_performed) > 1:
                pdf.set_x(x_start)
                pdf.set_y(y_start + 35)
            posture = pose_data.get("average_posture_score", 0)
            pdf.metric_box("Posture Score", f"{posture:.1f}%", "Body language")

        # Gesture Count
        if hands_valid:
            if len(analyses_performed) > 1:
                pdf.set_x(x_start + 95)
                pdf.set_y(y_start + 35)
            gestures = hands_data.get("total_gestures", 0)
            pdf.metric_box("Gestures Used", f"{gestures}", "Hand movements")

        pdf.ln(15)

        # Overall assessment
        pdf.section_title("Overall Assessment")
        if overall_score >= 80:
            assessment = "EXCELLENT - Outstanding presentation skills demonstrated"
            color = "excellent"
        elif overall_score >= 60:
            assessment = "GOOD - Solid performance with room for enhancement"
            color = "good"
        else:
            assessment = "NEEDS IMPROVEMENT - Focus on key areas for better results"
            color = "needs_improvement"

        pdf.assessment_box(assessment, color)

        # ===== DETAILED ANALYSIS PAGE =====
        pdf.add_page()
        pdf.chapter_title("Detailed Analysis Results")

        # Face Analysis Section
        if face_valid:
            pdf.section_title("Eye Contact Analysis")

            # Data table
            pdf.set_font("Arial", "B", 9)
            pdf.set_text_color(59, 130, 246)  # Softer blue color
            pdf.cell(60, 8, "Metric", ln=False)
            pdf.cell(40, 8, "Value", ln=False)
            pdf.cell(60, 8, "Assessment", ln=True)

            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(0, 0, 0)

            # Total frames
            total_frames = face_data.get("total_frames", 0)
            pdf.cell(60, 8, "Frames Analyzed", ln=False)
            pdf.cell(40, 8, f"{total_frames:,}", ln=False)
            pdf.cell(60, 8, "Comprehensive analysis", ln=True)

            # Eye contact percentage
            eye_contact_pct = face_data.get("eye_contact_percentage", 0)
            pdf.cell(60, 8, "Eye Contact %", ln=False)
            pdf.cell(40, 8, f"{eye_contact_pct:.1f}%", ln=False)

            if eye_contact_pct >= 80:
                assessment = "Excellent engagement"
                color = "excellent"
            elif eye_contact_pct >= 60:
                assessment = "Good engagement"
                color = "good"
            else:
                assessment = "Needs improvement"
                color = "needs_improvement"

            pdf.cell(60, 8, assessment, ln=True)

            pdf.ln(8)
            pdf.assessment_box(f"Eye Contact Assessment: {assessment}", color)
            pdf.ln(10)

        # Hands Analysis Section
        if hands_valid:
            pdf.section_title("Hand Gesture Analysis")

            # Data table
            pdf.set_font("Arial", "B", 9)
            pdf.set_text_color(59, 130, 246)  # Softer blue color
            pdf.cell(60, 8, "Metric", ln=False)
            pdf.cell(40, 8, "Value", ln=False)
            pdf.cell(60, 8, "Assessment", ln=True)

            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(0, 0, 0)

            # Total frames
            total_frames = hands_data.get("total_frames", 0)
            pdf.cell(60, 8, "Frames Analyzed", ln=False)
            pdf.cell(40, 8, f"{total_frames:,}", ln=False)
            pdf.cell(60, 8, "Comprehensive analysis", ln=True)

            # Gestures detected
            total_gestures = hands_data.get("total_gestures", 0)
            pdf.cell(60, 8, "Gestures Detected", ln=False)
            pdf.cell(40, 8, f"{total_gestures}", ln=False)

            if total_gestures > 50:
                assessment = "Excellent variety"
                color = "excellent"
            elif total_gestures > 20:
                assessment = "Good usage"
                color = "good"
            else:
                assessment = "Limited usage"
                color = "needs_improvement"

            pdf.cell(60, 8, assessment, ln=True)

            # Gesture breakdown
            if "gesture_percentages" in hands_data:
                pdf.ln(4)
                pdf.set_font("Arial", "B", 9)
                pdf.set_text_color(59, 130, 246)  # Softer blue color
                pdf.cell(0, 8, "Gesture Breakdown:", ln=True)

                for gesture, percentage in hands_data["gesture_percentages"].items():
                    pdf.set_font("Arial", "", 8)
                    pdf.set_text_color(0, 0, 0)
                    pdf.cell(
                        0,
                        6,
                        f"  - {gesture.replace('_', ' ').title()}: {percentage:.1f}%",
                        ln=True,
                    )

            pdf.ln(8)
            pdf.assessment_box(f"Gesture Assessment: {assessment}", color)
            pdf.ln(10)

        # Pose Analysis Section
        if pose_valid:
            pdf.section_title("Body Posture Analysis")

            # Data table
            pdf.set_font("Arial", "B", 9)
            pdf.set_text_color(59, 130, 246)  # Softer blue color
            pdf.cell(60, 8, "Metric", ln=False)
            pdf.cell(40, 8, "Value", ln=False)
            pdf.cell(60, 8, "Assessment", ln=True)

            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(0, 0, 0)

            # Total frames
            total_frames = pose_data.get("total_frames", 0)
            pdf.cell(60, 8, "Frames Analyzed", ln=False)
            pdf.cell(40, 8, f"{total_frames:,}", ln=False)
            pdf.cell(60, 8, "Comprehensive analysis", ln=True)

            # Posture score
            posture_pct = pose_data.get("average_posture_score", 0)
            pdf.cell(60, 8, "Posture Score", ln=False)
            pdf.cell(40, 8, f"{posture_pct:.1f}%", ln=False)

            if posture_pct >= 80:
                assessment = "Excellent posture"
                color = "excellent"
            elif posture_pct >= 60:
                assessment = "Good posture"
                color = "good"
            else:
                assessment = "Needs improvement"
                color = "needs_improvement"

            pdf.cell(60, 8, assessment, ln=True)

            # Good posture frames
            good_posture = pose_data.get("good_posture_frames", 0)
            pdf.cell(60, 8, "Good Posture Frames", ln=False)
            pdf.cell(40, 8, f"{good_posture}/{total_frames}", ln=False)
            pdf.cell(60, 8, "Consistent performance", ln=True)

            pdf.ln(8)
            pdf.assessment_box(f"Posture Assessment: {assessment}", color)
            pdf.ln(10)

        # ===== VISUAL CHARTS PAGE =====
        if hands_valid or pose_valid:
            pdf.add_page()
            pdf.chapter_title("Visual Analysis Charts")

            # Track vertical position for proper spacing
            current_y = pdf.get_y()

            # Gesture chart
            if hands_valid and os.path.exists("data/gesture_pie_chart.png"):
                try:
                    pdf.section_title("Gesture Analysis Distribution")
                    pdf.ln(5)  # Add some space after title

                    # Center the image horizontally and position vertically with smaller size
                    image_width = 100  # Reduced from 140 to 100
                    x_position = (210 - image_width) / 2  # Center horizontally
                    y_position = pdf.get_y()

                    # Add image with proper positioning
                    pdf.image(
                        "data/gesture_pie_chart.png",
                        x=x_position,
                        y=y_position,
                        w=image_width,
                    )

                    # Move to position after image
                    pdf.set_y(y_position + 70)  # Reduced space for smaller image
                    pdf.ln(10)  # Additional spacing

                except Exception as e:
                    print(f"Warning: Could not add gesture chart: {e}")
                    pdf.ln(20)  # Add space if image fails

            # Movement heatmap
            if pose_valid and os.path.exists("data/pacing_heatmap.png"):
                try:
                    pdf.section_title("Movement Pacing Heatmap")
                    pdf.ln(5)  # Add some space after title

                    # Center the image horizontally and position vertically with smaller size
                    image_width = 100  # Reduced from 140 to 100
                    x_position = (210 - image_width) / 2  # Center horizontally
                    y_position = pdf.get_y()

                    # Add image with proper positioning
                    pdf.image(
                        "data/pacing_heatmap.png",
                        x=x_position,
                        y=y_position,
                        w=image_width,
                    )

                    # Move to position after image
                    pdf.set_y(y_position + 70)  # Reduced space for smaller image
                    pdf.ln(10)  # Additional spacing

                except Exception as e:
                    print(f"Warning: Could not add pacing heatmap: {e}")
                    pdf.ln(20)  # Add space if image fails

        # ===== RECOMMENDATIONS PAGE =====
        pdf.add_page()
        pdf.chapter_title("Recommendations for Improvement")

        # Introduction
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(
            0,
            6,
            "Based on your analysis results, here are specific, actionable recommendations to enhance your presentation skills and improve your overall performance.",
        )
        pdf.ln(8)

        # Professional recommendations
        recommendations = [
            {
                "title": "Eye Contact Enhancement",
                "tips": [
                    "Practice maintaining 3-5 seconds of eye contact with each audience member",
                    "Use the 'triangle technique' - look at three points in the audience",
                    "Avoid looking at screens or notes for extended periods",
                ],
            },
            {
                "title": "Gesture Optimization",
                "tips": [
                    "Use open palms to convey openness and trust",
                    "Point with your entire hand, not just your finger",
                    "Keep gestures above the waist and within your body frame",
                    "Practice gestures that emphasize key points",
                ],
            },
            {
                "title": "Posture Improvement",
                "tips": [
                    "Stand with feet shoulder-width apart for stability",
                    "Keep your shoulders back and chest open",
                    "Maintain a slight forward lean to show engagement",
                    "Practice power poses before presentations",
                ],
            },
            {
                "title": "Movement and Pacing",
                "tips": [
                    "Move purposefully to emphasize transitions",
                    "Use the stage space effectively",
                    "Avoid pacing back and forth nervously",
                    "Pause strategically for emphasis",
                ],
            },
        ]

        for i, rec in enumerate(recommendations, 1):
            # Recommendation title
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(59, 130, 246)  # Softer blue color
            pdf.cell(0, 8, f"{i}. {rec['title']}", ln=True)

            # Tips
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(0, 0, 0)
            for tip in rec["tips"]:
                pdf.cell(0, 6, f"   - {tip}", ln=True)

            pdf.ln(4)

        # ===== ACTION PLAN PAGE =====
        pdf.add_page()
        pdf.chapter_title("30-Day Action Plan")

        # Week 1
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(59, 130, 246)  # Blue color for topics
        pdf.cell(0, 8, "Week 1: Foundation Building", ln=True)
        pdf.ln(2)

        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(0, 0, 0)  # Black color for content details
        week1_tasks = [
            "Record yourself presenting for 5 minutes daily",
            "Practice eye contact exercises in front of a mirror",
            "Work on basic posture and breathing techniques",
            "Review your analysis results and identify top 2 priorities",
        ]

        for task in week1_tasks:
            pdf.cell(0, 6, f"   - {task}", ln=True)

        pdf.ln(8)

        # Week 2
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(59, 130, 246)  # Blue color for topics
        pdf.cell(0, 8, "Week 2: Skill Development", ln=True)
        pdf.ln(2)

        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(0, 0, 0)  # Black color for content details
        week2_tasks = [
            "Practice specific gestures for different types of content",
            "Work on vocal variety and pacing",
            "Implement movement patterns during practice sessions",
            "Seek feedback from a colleague or mentor",
        ]

        for task in week2_tasks:
            pdf.cell(0, 6, f"   - {task}", ln=True)

        pdf.ln(8)

        # Week 3-4
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(59, 130, 246)  # Blue color for topics
        pdf.cell(0, 8, "Week 3-4: Integration & Practice", ln=True)
        pdf.ln(2)

        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(0, 0, 0)  # Black color for content details
        week3_tasks = [
            "Combine all skills in longer practice sessions",
            "Present to small groups for real feedback",
            "Refine techniques based on feedback",
            "Prepare for your next actual presentation",
        ]

        for task in week3_tasks:
            pdf.cell(0, 6, f"   - {task}", ln=True)

        # ===== FINAL PAGE =====
        pdf.add_page()
        pdf.chapter_title("Next Steps")

        # Professional closing
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(
            0,
            6,
            "Congratulations on taking the first step toward improving your presentation skills! Remember that effective public speaking is a skill that develops with practice and feedback.",
        )
        pdf.ln(8)

        pdf.multi_cell(
            0,
            6,
            "Continue using OratoCoach for regular practice sessions and track your progress over time. Each analysis will help you identify new areas for improvement and celebrate your successes.",
        )
        pdf.ln(8)

        # Contact information
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(59, 130, 246)  # Softer blue color
        pdf.cell(0, 8, "Ready to take your presentations to the next level?", ln=True)
        pdf.ln(4)

        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(
            0,
            6,
            "Continue practicing with OratoCoach and watch your confidence grow!",
            ln=True,
        )

        # Save PDF
        os.makedirs("data", exist_ok=True)
        pdf.output("data/presentation_summary.pdf")

        print(
            "✅ Professional PDF report generated using standardized template: data/presentation_summary.pdf"
        )
        return True

    except Exception as e:
        print(f"❌ Error generating PDF report: {e}")
        return False
