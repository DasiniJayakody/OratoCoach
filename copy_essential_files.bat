@echo off
echo Creating clean OratoCoach repository for GitHub...

:: Create clean directory
mkdir OratoCoach-GitHub
cd OratoCoach-GitHub

:: Copy core Python files
copy ..\app.py .
copy ..\requirements.txt .
copy ..\face_analysis.py .
copy ..\hands_analysis.py .
copy ..\pose_analysis.py .
copy ..\report_functions.py .
copy ..\main.py .
copy ..\wsgi.py .

:: Copy templates
mkdir templates
copy ..\templates\*.html templates\

:: Copy static files
mkdir static
mkdir static\css
copy ..\static\css\*.css static\css\

:: Copy deployment files
copy ..\Procfile .
copy ..\runtime.txt .
copy ..\Dockerfile .
copy ..\docker-compose.yml .
copy ..\Aptfile .
copy ..\deploy.sh .
copy ..\deploy.bat .

:: Copy SEO files
copy ..\sitemap.xml .
copy ..\robots.txt .
copy ..\.gitignore .

:: Copy documentation
copy ..\SEO_GUIDE.md .
copy ..\DEPLOYMENT_GUIDE.md .
copy ..\DEPLOYMENT_CHECKLIST.md .
copy ..\FINAL_DEPLOYMENT_STEPS.md .
copy ..\QUICK_START.md .

:: Create empty data directory
mkdir data

echo Essential files copied successfully!
echo Now you can initialize Git and push to GitHub.
pause 