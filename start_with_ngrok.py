from pyngrok import ngrok
import threading
import time
from app import app

def start_ngrok():
    """Start ngrok tunnel"""
    try:
        # Start ngrok tunnel
        public_url = ngrok.connect(5000)
        print(f"\n🌐 ngrok tunnel created!")
        print(f"📱 Public URL: {public_url}")
        print(f"🔗 Webhook URL: {public_url}/webhook")
        print("\n" + "="*50)
        print("📋 COPY THIS WEBHOOK URL TO TWILIO:")
        print(f"   {public_url}/webhook")
        print("="*50)
        print("\n✅ Your bot is now accessible from the internet!")
        print("💬 Send a WhatsApp message to test it!")
        
        return public_url
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        print("💡 You may need to sign up for ngrok and set authtoken")
        print("   Go to: https://dashboard.ngrok.com/signup")
        return None

def main():
    print("🚀 Starting WhatsApp Chatbot with ngrok...")
    
    # Start ngrok in a separate thread
    ngrok_thread = threading.Thread(target=start_ngrok)
    ngrok_thread.daemon = True
    ngrok_thread.start()
    
    # Wait a moment for ngrok to start
    time.sleep(3)
    
    # Start Flask app
    print("\n🤖 Starting Flask app...")
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
