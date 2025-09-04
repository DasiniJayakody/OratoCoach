# 🎤 OratoCoach - AI Presentation & Public Speaking Coach

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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

### 1. Home Page

- **Welcome**: Learn about OratoCoach's capabilities
- **Features**: Explore different analysis types
- **Get Started**: Click "Start Analysis" to begin

### 2. Analysis Selection

- **Choose Analyses**: Select one, multiple, or all analysis types
- **Interactive Cards**: Click on analysis cards to select/deselect
- **View Previous Reports**: Access previously generated PDF reports
- **Start Analysis**: Click the button to begin your presentation

### 3. Analysis Process

- **Camera Access**: Allow camera access when prompted
- **Present Naturally**: Present your content while AI analyzes
- **Real-time Feedback**: See analysis progress in real-time
- **Complete Analysis**: Press 'q' to stop when finished

### 4. Results & Reports

- **Executive Summary**: Key metrics at a glance
- **Detailed Results**: Comprehensive analysis for each type
- **Generate Report**: Create professional PDF report
- **View/Download**: Access your report in the browser or download

## 🏗️ Project Structure

```
OratoCoach/
├── app.py                 # Main Flask web application
├── face_analysis.py      # Face analysis module
├── hands_analysis.py     # Hands analysis module
├── pose_analysis.py      # Pose analysis module
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Home page
│   ├── about.html       # About page
│   ├── analysis.html    # Analysis selection page
│   └── results.html     # Results display page
├── static/              # Static files
│   └── css/
│       └── custom.css   # Custom styles and animations
└── data/               # Generated data and reports
    ├── *.json          # Analysis statistics
    ├── *.png           # Generated charts
    └── *.pdf           # PDF reports
```

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

## 🎯 Best Practices

### Environment Setup

- **Lighting**: Ensure good, even lighting for best detection
- **Distance**: Position 2-6 feet from camera for optimal analysis
- **Background**: Use a clean, uncluttered background
- **Stability**: Use a stable camera setup to avoid movement artifacts

### Presentation Tips

- **Natural Delivery**: Present as you would to a real audience
- **Gesture Variety**: Use different hand movements and gestures
- **Good Posture**: Maintain confident, upright body language
- **Eye Contact**: Look directly at the camera for best results
- **Practice**: Rehearse your content beforehand for better analysis

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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

_Built with ❤️ for better public speaking_

