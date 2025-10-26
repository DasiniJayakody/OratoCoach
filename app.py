import os
import json
import sys
import argparse
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import shutil
import threading

# Import analysis modules
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

# Analysis status
analysis_status = {
    'is_running': False,
    'current_step': '',
    'progress': 0
}

def print_run_instructions():
	"""
	Simple instructions for running the Flask app locally.
	"""
	print("")
	print("OratoCoach - Run instructions")
	print("----------------------------")
	print("1) Create and activate a Python virtual environment (recommended):")
	print("   Windows:  python -m venv venv && venv\\Scripts\\activate")
	print("   macOS/Linux:  python3 -m venv venv && source venv/bin/activate")
	print("")
	print("2) Install requirements (example packages used by this project):")
	print("   pip install flask opencv-python mediapipe numpy reportlab matplotlib")
	print("   Or if you have a requirements.txt: pip install -r requirements.txt")
	print("")
	print("3) Ensure 'data' directory exists (app creates it automatically if missing).")
	print("")
	print("4) Run the app (development):")
	print("   python \"d:\\Linkedln Projects\\OratoCoach\\app.py\"")
	print("   or set debug:  set FLASK_DEBUG=true && python app.py")
	print("")
	print("5) Open in browser: http://localhost:5000")
	print("")
	print("CLI options:")
	print("   --instructions   Print these instructions and exit")
	print("")
	print("Notes:")
	print(" - If you use Docker or a different entrypoint, run the script with appropriate environment variables.")
	print(" - If you encounter missing modules, install them via pip as shown above.")
	print("")

def archive_current_pdf():
    current_pdf = "data/presentation_summary.pdf"
    previous_pdf = "data/previous_presentation_summary.pdf"
    if os.path.exists(current_pdf):
        shutil.copy2(current_pdf, previous_pdf)

def run_complete_analysis(selected_analyses):
    global analysis_results, analysis_status
    try:
        # Ensure we have a valid list of analyses; default to all if empty
        if not selected_analyses:
            selected_analyses = ['face', 'hands', 'pose']
        os.makedirs("data", exist_ok=True)
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
    """Main page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/start_analysis', methods=['GET', 'POST'])
def start_analysis():
	"""Start the complete analysis process (accepts JSON, form, or query params)."""
	global analysis_status, analysis_results

	# If analysis already running -> for POST return JSON error, for GET redirect
	if analysis_status['is_running']:
		if request.method == 'POST':
			return jsonify({'status': 'error', 'message': 'Analysis already in progress'}), 409
		return redirect(url_for('analysis'))

	selected_analyses = None

	# 1) JSON body: {"analyses": ["face","hands"]}
	try:
		json_data = request.get_json(silent=True)
	except Exception:
		json_data = None
	if json_data and 'analyses' in json_data:
		selected_analyses = json_data.get('analyses')

	# 2) Form data: support analyses[] or analyses and individual checkbox names
	if selected_analyses is None and request.form:
		# common: multiple inputs named analyses[] or analyses
		form_list = request.form.getlist('analyses') or request.form.getlist('analyses[]')
		if form_list:
			selected_analyses = form_list
		else:
			# check for individual checkbox names 'face','hands','pose'
			picked = []
			for name in ('face', 'hands', 'pose'):
				v = request.form.get(name)
				if v and str(v).lower() in ('on', 'true', '1', 'yes'):
					picked.append(name)
			if picked:
				selected_analyses = picked
			else:
				# fallback: single string in 'analyses' field (comma-separated or JSON string)
				form_val = request.form.get('analyses')
				if form_val:
					try:
						import ast
						parsed = ast.literal_eval(form_val)
						if isinstance(parsed, (list, tuple)):
							selected_analyses = list(parsed)
						else:
							selected_analyses = [str(parsed)]
					except Exception:
						selected_analyses = [s.strip() for s in form_val.split(',') if s.strip()]

	# 3) Query string: /start_analysis?analyses=face,hands  or analyses[]=face
	if selected_analyses is None:
		args_list = request.args.getlist('analyses') or request.args.getlist('analyses[]')
		if args_list:
			selected_analyses = args_list
		else:
			q = request.args.get('analyses')
			if q:
				selected_analyses = [s.strip() for s in q.split(',') if s.strip()]

	# Default to all analyses so the button works even if frontend doesn't send params
	if not selected_analyses:
		selected_analyses = ['face', 'hands', 'pose']

	# Normalize: strings, lowercase, deduplicate while preserving order
	if isinstance(selected_analyses, str):
		selected_analyses = [selected_analyses]
	normalized = []
	for s in selected_analyses:
		try:
			sval = str(s).lower().strip()
		except Exception:
			continue
		if sval and sval not in normalized:
			normalized.append(sval)
	selected_analyses = normalized or ['face', 'hands', 'pose']

	print(f"Start analysis requested. Resolved analyses: {selected_analyses}")

	# Reset results
	analysis_results = {
		'face_data': None,
		'hands_data': None,
		'pose_data': None,
		'analysis_completed': False,
		'pdf_generated': False
	}

	# Start analysis in background thread and pass selected analyses
	thread = threading.Thread(target=run_complete_analysis, args=(selected_analyses,))
	thread.daemon = True
	thread.start()

	# Behavior:
	# - For POST (AJAX/fetch or form POST) return JSON so frontend JS receives predictable response.
	# - For GET (plain navigation) redirect to /analysis so UI continues.
	if request.method == 'GET':
		return redirect(url_for('analysis'))

	return jsonify({'status': 'success', 'message': 'Analysis started successfully', 'analyses': selected_analyses})

@app.route('/analysis_status')
def get_analysis_status():
    """Get current analysis status"""
    global analysis_status, analysis_results
    
    return jsonify({
        'is_running': analysis_status['is_running'],
        'current_step': analysis_status['current_step'],
        'progress': analysis_status['progress'],
        'analysis_completed': analysis_results['analysis_completed'],
        'pdf_generated': analysis_results['pdf_generated']
    })

@app.route('/analysis')
def analysis():
    """Analysis page"""
    return render_template('analysis.html')

@app.route('/results')
def results():
    """Results page"""
    global analysis_results
    
    if not analysis_results['analysis_completed']:
        return render_template('analysis.html', message="Please complete the analysis first.")
    
    # Prepare data for display
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
    """Generate PDF report"""
    global analysis_results
    
    # Check if analysis is completed or if we have data files
    has_data_files = (os.path.exists("data/face_analysis_stats.json") or 
                     os.path.exists("data/hands_analysis_stats.json") or 
                     os.path.exists("data/pose_analysis_stats.json"))
    
    if not analysis_results['analysis_completed'] and not has_data_files:
        return jsonify({'status': 'error', 'message': 'Please complete the analysis first or ensure data files exist'})
    
    try:
        print("🔍 Starting PDF generation in Flask app...")
        
        # Load data from files if not in memory
        face_data = analysis_results['face_data']
        hands_data = analysis_results['hands_data']
        pose_data = analysis_results['pose_data']
        
        # If data is not in memory, try to load from files
        if face_data is None and os.path.exists("data/face_analysis_stats.json"):
            with open("data/face_analysis_stats.json", "r") as f:
                face_data = json.load(f)
        
        if hands_data is None and os.path.exists("data/hands_analysis_stats.json"):
            with open("data/hands_analysis_stats.json", "r") as f:
                hands_data = json.load(f)
        
        if pose_data is None and os.path.exists("data/pose_analysis_stats.json"):
            with open("data/pose_analysis_stats.json", "r") as f:
                pose_data = json.load(f)
        
        print(f"📊 Data loaded - Face: {face_data is not None}, Hands: {hands_data is not None}, Pose: {pose_data is not None}")
        
        # Generate PDF report
        success = generate_pdf_report(
            face_data=face_data,
            hands_data=hands_data,
            pose_data=pose_data
        )
        
        if success:
            analysis_results['pdf_generated'] = True
            
            # Save PDF generation status
            os.makedirs("data", exist_ok=True)
            with open("data/pdf_generated.txt", "w") as f:
                f.write(f"PDF generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            print("✅ PDF generated successfully in Flask app")
            return jsonify({'status': 'success', 'message': 'PDF generated successfully'})
        else:
            print("❌ PDF generation failed in Flask app")
            return jsonify({'status': 'error', 'message': 'Failed to generate PDF'})
            
    except Exception as e:
        print(f"❌ Error generating PDF in Flask app: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': f'Error generating PDF: {str(e)}'})

@app.route('/download_pdf')
def download_pdf():
    """Download the generated PDF"""
    pdf_path = "data/presentation_summary.pdf"
    
    if not os.path.exists(pdf_path):
        return jsonify({'status': 'error', 'message': 'PDF not found. Please generate it first.'})
    
    try:
        return send_file(pdf_path, as_attachment=True, download_name='presentation_summary.pdf')
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error downloading PDF: {str(e)}'})

@app.route('/api/analysis_data')
def get_analysis_data():
    """API endpoint to get analysis data"""
    global analysis_results
    
    if not analysis_results['analysis_completed']:
        return jsonify({'status': 'error', 'message': 'Analysis not completed'})
    
    # Calculate overall score
    scores = []
    if analysis_results['face_data'] and not analysis_results['face_data'].get('error'):
        scores.append(analysis_results['face_data'].get('eye_contact_percentage', 0))
    if analysis_results['pose_data'] and not analysis_results['pose_data'].get('error'):
        scores.append(analysis_results['pose_data'].get('average_posture_score', 0))
    if analysis_results['hands_data'] and not analysis_results['hands_data'].get('error'):
        total_gestures = analysis_results['hands_data'].get('total_gestures', 0)
        gesture_score = min(100, (total_gestures / 50) * 100) if total_gestures > 0 else 0
        scores.append(gesture_score)
    
    overall_score = sum(scores) / len(scores) if scores else 0
    
    return jsonify({
        'status': 'success',
        'data': {
            'face_data': analysis_results['face_data'],
            'hands_data': analysis_results['hands_data'],
            'pose_data': analysis_results['pose_data'],
            'overall_score': overall_score,
            'has_face_data': analysis_results['face_data'] and not analysis_results['face_data'].get('error'),
            'has_hands_data': analysis_results['hands_data'] and not analysis_results['hands_data'].get('error'),
            'has_pose_data': analysis_results['pose_data'] and not analysis_results['pose_data'].get('error')
        }
    })

@app.route('/reset_analysis')
def reset_analysis():
    """Reset analysis results"""
    global analysis_results, analysis_status
    
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
    
    # Remove status files
    for file in ['data/analysis_completed.txt', 'data/pdf_generated.txt']:
        if os.path.exists(file):
            os.remove(file)
    
    return jsonify({'status': 'success', 'message': 'Analysis reset successfully'})

@app.route('/fix_analysis_status')
def fix_analysis_status():
    """Fix analysis status if data files exist but status is incorrect"""
    global analysis_results
    
    # Check if data files exist
    has_face_data = os.path.exists("data/face_analysis_stats.json")
    has_hands_data = os.path.exists("data/hands_analysis_stats.json")
    has_pose_data = os.path.exists("data/pose_analysis_stats.json")
    
    if has_face_data or has_hands_data or has_pose_data:
        # Load data into memory
        if has_face_data:
            with open("data/face_analysis_stats.json", "r") as f:
                analysis_results['face_data'] = json.load(f)
        
        if has_hands_data:
            with open("data/hands_analysis_stats.json", "r") as f:
                analysis_results['hands_data'] = json.load(f)
        
        if has_pose_data:
            with open("data/pose_analysis_stats.json", "r") as f:
                analysis_results['pose_data'] = json.load(f)
        
        # Mark analysis as completed
        analysis_results['analysis_completed'] = True
        
        # Create completion status file
        os.makedirs("data", exist_ok=True)
        with open("data/analysis_completed.txt", "w") as f:
            f.write(f"Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return jsonify({
            'status': 'success',
            'message': 'Analysis status fixed successfully',
            'has_face_data': has_face_data,
            'has_hands_data': has_hands_data,
            'has_pose_data': has_pose_data
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No analysis data files found'
        })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'analysis_running': analysis_status['is_running'],
        'analysis_completed': analysis_results['analysis_completed']
    })

@app.route('/test_pdf')
def test_pdf():
    """Test PDF generation endpoint"""
    try:
        print("🧪 Testing PDF generation from web interface...")
        
        # Load data from files
        face_data = None
        hands_data = None
        pose_data = None
        
        if os.path.exists("data/face_analysis_stats.json"):
            with open("data/face_analysis_stats.json", "r") as f:
                face_data = json.load(f)
        
        if os.path.exists("data/hands_analysis_stats.json"):
            with open("data/hands_analysis_stats.json", "r") as f:
                hands_data = json.load(f)
        
        if os.path.exists("data/pose_analysis_stats.json"):
            with open("data/pose_analysis_stats.json", "r") as f:
                pose_data = json.load(f)
        
        # Generate PDF
        success = generate_pdf_report(
            face_data=face_data,
            hands_data=hands_data,
            pose_data=pose_data
        )
        
        if success and os.path.exists("data/presentation_summary.pdf"):
            file_size = os.path.getsize("data/presentation_summary.pdf")
            return jsonify({
                'status': 'success',
                'message': f'PDF generated successfully! File size: {file_size} bytes',
                'file_exists': True,
                'file_size': file_size
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'PDF generation failed or file not found',
                'file_exists': os.path.exists("data/presentation_summary.pdf")
            })
            
    except Exception as e:
        print(f"❌ Error in test PDF route: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

@app.route('/api/pdf_exists')
def check_pdf_exists():
    """Check if PDF exists and has content"""
    pdf_path = "data/presentation_summary.pdf"
    
    if os.path.exists(pdf_path):
        file_size = os.path.getsize(pdf_path)
        if file_size > 0:
            return jsonify({
                'exists': True,
                'size': file_size,
                'status': 'ready'
            })
        else:
            return jsonify({
                'exists': True,
                'size': 0,
                'status': 'empty'
            })
    else:
        return jsonify({
            'exists': False,
            'size': 0,
            'status': 'not_found'
        })

@app.route('/view_pdf')
def view_pdf():
    """View PDF in browser"""
    pdf_path = "data/presentation_summary.pdf"
    
    if not os.path.exists(pdf_path):
        return jsonify({'status': 'error', 'message': 'PDF not found'})
    
    try:
        return send_file(pdf_path, mimetype='application/pdf')
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error viewing PDF: {str(e)}'})

@app.route('/sitemap.xml')
def sitemap():
    """Serve sitemap for search engines"""
    return send_file('sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """Serve robots.txt for search engines"""
    return send_file('robots.txt', mimetype='text/plain')

@app.route('/force_generate_pdf')
def force_generate_pdf():
    """Force PDF generation regardless of analysis status"""
    try:
        print("🔧 Force generating PDF...")
        
        # Load data from files
        face_data = None
        hands_data = None
        pose_data = None
        
        if os.path.exists("data/face_analysis_stats.json"):
            with open("data/face_analysis_stats.json", "r") as f:
                face_data = json.load(f)
            print("✅ Face data loaded")
        
        if os.path.exists("data/hands_analysis_stats.json"):
            with open("data/hands_analysis_stats.json", "r") as f:
                hands_data = json.load(f)
            print("✅ Hands data loaded")
        
        if os.path.exists("data/pose_analysis_stats.json"):
            with open("data/pose_analysis_stats.json", "r") as f:
                pose_data = json.load(f)
            print("✅ Pose data loaded")
        
        # Generate PDF
        success = generate_pdf_report(
            face_data=face_data,
            hands_data=hands_data,
            pose_data=pose_data
        )
        
        if success and os.path.exists("data/presentation_summary.pdf"):
            file_size = os.path.getsize("data/presentation_summary.pdf")
            return jsonify({
                'status': 'success',
                'message': f'PDF generated successfully! File size: {file_size} bytes',
                'file_size': file_size
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'PDF generation failed'
            })
            
    except Exception as e:
        print(f"❌ Error in force PDF generation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Quick CLI: --instructions prints usage and exits
    if '--instructions' in sys.argv or '-i' in sys.argv:
    	print_run_instructions()
    	sys.exit(0)
    
    print("🚀 Starting OratoCoach Flask Application...")
    print("📊 AI-Powered Presentation Analysis System")
    print("🌐 Web interface available at: http://localhost:5000")
    print("📁 Data directory: ./data/")
    print("📄 PDF reports will be saved to: ./data/presentation_summary.pdf")
    print("\n" + "="*50)
    
    # Production settings
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
