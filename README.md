# 🎤 OratoCoach - AI Presentation & Public Speaking Coach

**OratoCoach** is an AI-powered web application that analyzes your presentation skills in real-time, providing comprehensive feedback on eye contact, gestures, and posture. Perfect for public speakers, presenters, and anyone looking to improve their communication skills.

## ✨ Features

### 🎯 Real-Time Analysis

- **Face Analysis**: Eye contact tracking and facial engagement
- **Hands Analysis**: Gesture detection and classification
- **Pose Analysis**: Posture quality and movement tracking
- **Flexible Selection**: Choose individual or multiple analyses

### 🎨 Modern Web Interface

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Professional UI**: Clean, modern interface with smooth animations
- **Interactive Elements**: Hover effects, loading states, real-time feedback
- **Bootstrap 5**: Latest framework for consistent styling

### 📊 Comprehensive Reporting

- **Real-time Results**: View analysis results immediately
- **Visual Charts**: Pie charts for gestures, heatmaps for movement
- **Professional PDF Reports**: Download detailed reports
- **Detailed Metrics**: Key performance indicators and assessments

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam access
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or download the project**

   ```bash
   # Navigate to the project directory
   cd OratoCoach
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web application**

   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   Navigate to: http://localhost:5000
   ```

## 📱 How to Use

- 1. Home Page

  - **Welcome**: Learn about OratoCoach's capabilities
  - **Features**: Explore different analysis types
  - **Get Started**: Click "Start Analysis" to begin

- 2. Analysis Selection

  - **Choose Analyses**: Select one, multiple, or all analysis types
  - **Interactive Cards**: Click on analysis cards to select/deselect
  - **View Previous Reports**: Access previously generated PDF reports
  - **Start Analysis**: Click the button to begin your presentation

- 3. Analysis Process

  - **Camera Access**: Allow camera access when prompted
  - **Present Naturally**: Present your content while AI analyzes
  - **Real-time Feedback**: See analysis progress in real-time
  - **Complete Analysis**: Press 'q' to stop when finished

  - Switching analyses while the camera is open
    - If you start an analysis and later want to run a different analysis, press `q` during the live camera session to stop the current analysis and return to the analysis selection screen. From there you can choose another analysis (face, hands, or pose) and restart the camera for that analysis.
    - Example flow:
      1. Start Face Analysis (camera opens).
      2. Press `q` to stop Face Analysis and return to selection.
      3. Select Hands Analysis and start camera again.

- 4. Results & Reports
  - **Executive Summary**: Key metrics at a glance
  - **Detailed Results**: Comprehensive analysis for each selected type
  - **Generate Report**: Create professional PDF report (only includes the analyses you selected)
  - **View/Download**: Access your report in the browser or download

## 📊 Analysis Types

### Face Analysis

- **Eye Contact Tracking**: Monitors gaze patterns and direct eye contact
- **Facial Engagement**: Analyzes facial expressions and engagement
- **Head Positioning**: Tracks head movements and positioning
- **Metrics**: Average score, good contact frames, percentage

### Hands Analysis

- **Gesture Detection**: Identifies hand movements and positions
- **Classification**: Categorizes gesture types (pointing, open palms, etc.)
- **Variety Analysis**: Assesses gesture diversity and effectiveness
- **Metrics**: Total gestures, breakdown by type, percentages

### Pose Analysis

- **Posture Quality**: Evaluates body alignment and posture
- **Movement Tracking**: Records position changes and movement patterns
- **Stability Assessment**: Measures presentation stability and confidence
- **Metrics**: Posture score, good posture frames, movement data

## 🔧 Technical Details

### Backend (Flask)

- **Framework**: Flask 3.0.0
- **Sessions**: User session management
- **Background Processing**: Threading for analysis
- **API Endpoints**: RESTful API for frontend communication
- **File Handling**: Secure file uploads and downloads

### Frontend

- **Bootstrap 5**: Responsive grid and components
- **Font Awesome**: Professional icons
- **Custom CSS**: Enhanced styling and animations
- **JavaScript**: Interactive functionality and AJAX

### Analysis Integration

- **MediaPipe**: AI-powered computer vision
- **OpenCV**: Camera handling and image processing
- **Matplotlib**: Chart generation
- **FPDF**: PDF report creation

## 🔒 Security & Privacy

- **Local Processing**: All analysis runs locally on your machine
- **No Data Storage**: Analysis data is not stored permanently
- **Camera Access**: Only used during active analysis sessions
- **Secure Sessions**: Flask sessions for temporary user data

## 🐛 Troubleshooting

### Common Issues

**Camera Not Working**

- Check camera permissions in your browser
- Ensure no other applications are using the camera
- Try refreshing the page or restarting the application

**Analysis Not Starting**

- Make sure you've selected at least one analysis type
- Check that all dependencies are installed correctly
- Verify Python version (3.8+)

**Slow Performance**

- Close other applications using the camera
- Ensure good lighting conditions
- Check system resources and available memory

**PDF Download Issues**

- Ensure the data folder exists and has write permissions
- Check file permissions in your system
- Try refreshing the results page

### Error Messages

**"Camera access denied"**

- Allow camera access in your browser settings
- Check if camera is being used by another application
- Try a different browser

**"Analysis failed"**

- Check console for detailed error messages
- Ensure all required packages are installed
- Verify camera functionality with other applications

**"PDF generation failed"**

- Check if the data directory exists
- Verify write permissions
- Ensure FPDF is installed correctly

### Fix: "Invalid requirement: '<<<<<<< HEAD'" when running pip

- If pip reports a line like "<<<<<<< HEAD" in requirements.txt, your requirements file has merge conflict markers. Replace requirements.txt with a clean file (see requirements.txt in this repo) or remove the conflict markers manually.

### Fix: ModuleNotFoundError: No module named 'flask'

- Make sure your virtual environment is activated, then install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

- Alternatively install Flask directly:

  ```bash
  pip install Flask
  ```

- If you still see errors, confirm you're using the correct Python interpreter tied to your virtual environment.

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production Deployment

For production deployment, consider:

- **WSGI Server**: Use Gunicorn or uWSGI
- **Reverse Proxy**: Nginx for static files and load balancing
- **Environment Variables**: Configure production settings
- **SSL Certificate**: HTTPS for security

## 📈 Future Enhancements

- **User Accounts**: Save analysis history and progress
- **Progress Tracking**: Compare results over time
- **Advanced Analytics**: More detailed insights and recommendations
- **Mobile App**: Native mobile application
- **Video Recording**: Save presentation videos for review
- **Social Features**: Share results with colleagues or mentors
- **Custom Thresholds**: Adjustable sensitivity settings
- **Multi-language Support**: Internationalization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🆘 Support

For support or questions:

- Check the troubleshooting section above
- Review the documentation
- Open an issue on GitHub
- Check the console output for specific error messages

## 🙏 Acknowledgments

- **MediaPipe**: For AI-powered computer vision capabilities
- **OpenCV**: For camera handling and image processing
- **Flask**: For the web framework
- **Bootstrap**: For the responsive UI framework

---

**OratoCoach** - Transform your presentation skills with AI-powered analysis! 🎤✨

