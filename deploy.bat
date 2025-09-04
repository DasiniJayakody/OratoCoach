@echo off
echo 🚀 OratoCoach Deployment Script
echo ================================

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

echo ✅ Git found

REM Check if we're in a git repository
if not exist ".git" (
    echo ❌ Not in a git repository. Please initialize git first:
    echo    git init
    echo    git add .
    echo    git commit -m "Initial commit"
    pause
    exit /b 1
)

echo ✅ Git repository found

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Heroku CLI is not installed.
    echo Please install it from: https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

echo ✅ Heroku CLI found

REM Check if user is logged in to Heroku
heroku auth:whoami >nul 2>&1
if errorlevel 1 (
    echo ❌ Not logged in to Heroku. Please run: heroku login
    pause
    exit /b 1
)

echo ✅ Logged in to Heroku

REM Get app name from user
set /p app_name="Enter your Heroku app name (or press Enter to create a new one): "

if "%app_name%"=="" (
    echo Creating new Heroku app...
    for /f "tokens=*" %%i in ('heroku create --json') do set app_name=%%i
    echo ✅ Created app: %app_name%
) else (
    echo Using existing app: %app_name%
)

REM Add buildpacks
echo 📦 Adding buildpacks...
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt -a %app_name%
heroku buildpacks:add heroku/python -a %app_name%

REM Set environment variables
echo 🔧 Setting environment variables...
heroku config:set FLASK_DEBUG=False -a %app_name%

REM Deploy
echo 🚀 Deploying to Heroku...
git push heroku main

if errorlevel 1 (
    echo ❌ Deployment failed. Check the logs above for errors.
    pause
    exit /b 1
) else (
    echo ✅ Deployment successful!
    echo 🌐 Your app is available at: https://%app_name%.herokuapp.com
    echo.
    echo To open your app, run: heroku open -a %app_name%
    echo To view logs, run: heroku logs --tail -a %app_name%
)

pause 