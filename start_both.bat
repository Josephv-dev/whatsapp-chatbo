@echo off
echo 🚀 Starting WhatsApp Chatbot with ngrok...
echo.

echo ⚠️  IMPORTANT: Keep both windows open!
echo   - Flask app will run in this window
echo   - ngrok will open in a new window
echo.

echo 📱 Step 1: Starting Flask app...
start "Flask App" cmd /k "python app.py"

echo 🌐 Step 2: Starting ngrok tunnel...
timeout /t 3 /nobreak > nul
start "ngrok Tunnel" cmd /k "ngrok.exe http 8080"

echo.
echo ✅ Both services are starting!
echo 📋 Next steps:
echo   1. Wait for both windows to load
echo   2. Copy the ngrok HTTPS URL from the ngrok window
echo   3. Configure the webhook in Twilio Console
echo.
pause
