@echo off
chcp 65001 > nul
REM Get the actual IP addresses
echo.
echo ========================================
echo   MedLens Server Connection Setup
echo ========================================
echo.
echo Your PC IP Addresses:
echo.
ipconfig | findstr /R "IPv4.*[0-9]"
echo.
echo ========================================
echo.
echo INSTRUCTIONS FOR ANDROID APP:
echo 1. Find your PC IP from the list above
echo    (Usually starts with 192.168 or 172.16-31 or 10.x)
echo.
echo 2. In the Android App, enter:
echo    Base URL: http://YOUR_PC_IP:8000
echo    (Example: http://192.168.1.100:8000)
echo.
echo 3. Endpoint Path: /api/chat/
echo.
echo 4. Then start the server below...
echo.
pause
echo.
echo Starting diagnostic server...
echo.
python diagnostic_server.py
pause
