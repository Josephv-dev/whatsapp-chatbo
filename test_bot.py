import requests
import json
from app import process_message

def test_bot_responses():
    """Test bot responses locally"""
    print("🧪 Testing WhatsApp Bot Responses Locally")
    print("=" * 50)
    
    test_messages = [
        "hello",
        "help", 
        "menu",
        "contact",
        "about",
        "1",
        "support",
        "random message"
    ]
    
    for msg in test_messages:
        print(f"\n📱 User: {msg}")
        response = process_message(msg, "test_user")
        print(f"🤖 Bot: {response}")
        print("-" * 30)

def test_flask_endpoints():
    """Test Flask endpoints"""
    print("\n🌐 Testing Flask Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health Check: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test home endpoint
        response = requests.get(base_url)
        print(f"✅ Home Page: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Flask app is not running. Start it with: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Test bot logic
    test_bot_responses()
    
    # Test Flask endpoints
    test_flask_endpoints()
