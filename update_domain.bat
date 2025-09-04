@echo off
echo ========================================
echo    OratoCoach Domain Update Script
echo ========================================
echo.
echo This script will update your sitemap.xml and robots.txt
echo with your actual deployed domain.
echo.
set /p DOMAIN="Enter your deployed domain (e.g., https://oratocoach-production.up.railway.app): "
echo.
echo Updating sitemap.xml...
powershell -Command "(Get-Content 'sitemap.xml') -replace 'YOUR-ACTUAL-DOMAIN\.com', '%DOMAIN%' | Set-Content 'sitemap.xml'"
echo.
echo Updating robots.txt...
powershell -Command "(Get-Content 'robots.txt') -replace 'YOUR-ACTUAL-DOMAIN\.com', '%DOMAIN%' | Set-Content 'robots.txt'"
echo.
echo ========================================
echo Domain updated successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Commit and push these changes to GitHub
echo 2. Go to Google Search Console
echo 3. Add your website and submit sitemap
echo.
pause 