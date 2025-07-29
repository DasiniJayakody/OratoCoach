#!/bin/bash

echo "🚀 OratoCoach Deployment Script"
echo "================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

echo "✅ Git repository found"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed."
    echo "Please install it from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✅ Heroku CLI found"

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "❌ Not logged in to Heroku. Please run: heroku login"
    exit 1
fi

echo "✅ Logged in to Heroku"

# Get app name from user
read -p "Enter your Heroku app name (or press Enter to create a new one): " app_name

if [ -z "$app_name" ]; then
    echo "Creating new Heroku app..."
    app_name=$(heroku create --json | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Created app: $app_name"
else
    echo "Using existing app: $app_name"
fi

# Add buildpacks
echo "📦 Adding buildpacks..."
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt -a $app_name
heroku buildpacks:add heroku/python -a $app_name

# Set environment variables
echo "🔧 Setting environment variables..."
heroku config:set FLASK_DEBUG=False -a $app_name

# Deploy
echo "🚀 Deploying to Heroku..."
git push heroku main

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Your app is available at: https://$app_name.herokuapp.com"
    echo ""
    echo "To open your app, run: heroku open -a $app_name"
    echo "To view logs, run: heroku logs --tail -a $app_name"
else
    echo "❌ Deployment failed. Check the logs above for errors."
    exit 1
fi 