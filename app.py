import os
import json
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
import shutil

from face_analysis import analyze_face
from hands_analysis import analyze_hands
from pose_analysis import analyze_pose
from report_functions import generate_pdf_report, generate_gesture_chart, generate_pacing_heatmap

app = Flask(__name__)

# Global variables to store analysis results
analysis_results = {
    'face_data': None,
    'hands_data': None,
    'pose_data': None,
    'analysis_completed': False,
    'pdf_generated': False
}

analysis_status = {
    'is_running': False,
    'current_step': '',
    'progress': 0
}

def archive_current_pdf():
    current_pdf = "data/presentation_summary.pdf"
    previous_pdf = "data/previous_presentation_summary.pdf"
    if os.path.exists(current_pdf):
        shutil.copy2(current_pdf, previous_pdf)

def run_complete_analysis(selected_analyses):
    global analysis_results, analysis_status
    try:
        analysis_status['is_running'] = True
        analysis_status['progress'] = 0
        total_steps = len(selected_analyses)
        current_step = 0
        # Face Analysis
        if 'face' in selected_analyses:
            current_step += 1
            analysis_status['current_step'] = 'Analyzing eye contact and facial expressions...'
            analysis_status['progress'] = int((current_step/total_steps)*100)
            face_data = analyze_face()
            analysis_results['face_data'] = face_data
        else:
            analysis_results['face_data'] = None
        # Hands Analysis
        if 'hands' in selected_analyses:
            current_step += 1
            analysis_status['current_step'] = 'Analyzing hand gestures and movements...'
            analysis_status['progress'] = int((current_step/total_steps)*100)
            hands_data = analyze_hands()
            analysis_results['hands_data'] = hands_data
        else:
            analysis_results['hands_data'] = None
        # Pose Analysis
        if 'pose' in selected_analyses:
            current_step += 1
            analysis_status['current_step'] = 'Analyzing body posture and movement...'
            analysis_status['progress'] = int((current_step/total_steps)*100)
            pose_data = analyze_pose()
            analysis_results['pose_data'] = pose_data
        else:
            analysis_results['pose_data'] = None
        # Generate charts
        if analysis_results['hands_data'] and not analysis_results['hands_data'].get('error'):
            generate_gesture_chart(analysis_results['hands_data'])
        if analysis_results['pose_data'] and not analysis_results['pose_data'].get('error'):
            generate_pacing_heatmap(analysis_results['pose_data'])
        analysis_results['analysis_completed'] = True
        analysis_status['progress'] = 100
        analysis_status['current_step'] = 'Analysis completed!'
        with open("data/analysis_completed.txt", "w") as f:
            f.write(f"Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        analysis_status['current_step'] = f'Error: {str(e)}'
    finally:
        analysis_status['is_running'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/start_analysis', methods=['POST'])
def start_analysis():
    global analysis_results
    if analysis_status['is_running']:
        return jsonify({'status': 'error', 'message': 'Analysis already in progress'})
    data = request.get_json()
    selected_analyses = data.get('analyses', [])
    if not selected_analyses:
        return jsonify({'status': 'error', 'message': 'No analyses selected'})
    # Reset results
    analysis_results.update({
        'face_data': None,
        'hands_data': None,
        'pose_data': None,
        'analysis_completed': False,
        'pdf_generated': False
    })
    # Clear previous files
    for file in [
        'data/analysis_completed.txt',
        'data/pdf_generated.txt',
        'data/presentation_summary.pdf',
        'data/previous_presentation_summary.pdf',
        'data/gesture_pie_chart.png',
        'data/pacing_heatmap.png',
        'data/face_analysis_stats.json',
        'data/hands_analysis_stats.json',
        'data/pose_analysis_stats.json']:
        if os.path.exists(file):
            os.remove(file)
    # Start analysis in background
    thread = threading.Thread(target=run_complete_analysis, args=(selected_analyses,))
    thread.daemon = True
    thread.start()
    return jsonify({'status': 'success', 'message': 'Analysis started'})

@app.route('/analysis_status')
def get_analysis_status():
    return jsonify({
        'is_running': analysis_status['is_running'],
        'current_step': analysis_status['current_step'],
        'progress': analysis_status['progress'],
        'analysis_completed': analysis_results['analysis_completed'],
        'pdf_generated': analysis_results['pdf_generated']
    })

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/results')
def results():
    results_data = {
        'face_data': analysis_results['face_data'],
        'hands_data': analysis_results['hands_data'],
        'pose_data': analysis_results['pose_data'],
        'has_face_data': analysis_results['face_data'] and not analysis_results['face_data'].get('error'),
        'has_hands_data': analysis_results['hands_data'] and not analysis_results['hands_data'].get('error'),
        'has_pose_data': analysis_results['pose_data'] and not analysis_results['pose_data'].get('error')
    }
    return render_template('results.html', results=results_data)

@app.route('/generate_pdf')
def generate_pdf():
    global analysis_results
    if not analysis_results['analysis_completed']:
        return jsonify({'status': 'error', 'message': 'Please complete the analysis first'})
    try:
        archive_current_pdf()
        face_data = analysis_results['face_data']
        hands_data = analysis_results['hands_data']
        pose_data = analysis_results['pose_data']
        success = generate_pdf_report(face_data, hands_data, pose_data)
        if success:
            analysis_results['pdf_generated'] = True
            with open("data/pdf_generated.txt", "w") as f:
                f.write(f"PDF generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return jsonify({'status': 'success', 'message': 'PDF generated successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to generate PDF'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error generating PDF: {str(e)}'})

@app.route('/download_pdf')
def download_pdf():
    pdf_path = "data/presentation_summary.pdf"
    if not os.path.exists(pdf_path):
        return jsonify({'status': 'error', 'message': 'PDF not found. Please generate it first.'})
    return send_file(pdf_path, as_attachment=True, download_name='presentation_summary.pdf')

@app.route('/view_pdf')
def view_pdf():
    pdf_path = "data/presentation_summary.pdf"
    if not os.path.exists(pdf_path):
        return jsonify({'status': 'error', 'message': 'PDF not found'})
    return send_file(pdf_path, mimetype='application/pdf')

@app.route('/download_previous_pdf')
def download_previous_pdf():
    previous_pdf = "data/previous_presentation_summary.pdf"
    if not os.path.exists(previous_pdf):
        return jsonify({'status': 'error', 'message': 'Previous PDF not found'})
    return send_file(previous_pdf, as_attachment=True, download_name='previous_presentation_summary.pdf')

@app.route('/view_previous_pdf')
def view_previous_pdf():
    previous_pdf = "data/previous_presentation_summary.pdf"
    if not os.path.exists(previous_pdf):
        return jsonify({'status': 'error', 'message': 'Previous PDF not found'})
    return send_file(previous_pdf, mimetype='application/pdf')

@app.route('/api/pdf_exists')
def check_pdf_exists():
    pdf_path = "data/presentation_summary.pdf"
    if os.path.exists(pdf_path):
        file_size = os.path.getsize(pdf_path)
        return jsonify({'exists': True, 'file_size': file_size, 'status': 'ready'})
    else:
        return jsonify({'exists': False, 'file_size': 0, 'status': 'not_found'})

@app.route('/reset_analysis')
def reset_analysis():
    global analysis_results
    analysis_results.update({
        'face_data': None,
        'hands_data': None,
        'pose_data': None,
        'analysis_completed': False,
        'pdf_generated': False
    })
    for file in [
        'data/analysis_completed.txt',
        'data/pdf_generated.txt',
        'data/presentation_summary.pdf',
        'data/previous_presentation_summary.pdf',
        'data/gesture_pie_chart.png',
        'data/pacing_heatmap.png',
        'data/face_analysis_stats.json',
        'data/hands_analysis_stats.json',
        'data/pose_analysis_stats.json']:
        if os.path.exists(file):
            os.remove(file)
    return jsonify({'status': 'success', 'message': 'Analysis reset successfully'})

@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    os.makedirs("data", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000) 