import requests
import json

def test_webhook_manually():
    """Simulate Twilio webhook calls manually"""
    
    print("🧪 Manual Webhook Testing")
    print("=" * 50)
    print("This simulates what Twilio would send to your webhook")
    
    # Sample Twilio webhook data
    webhook_data = {
        'From': 'whatsapp:+1234567890',
        'To': 'whatsapp:+14155238886',
        'Body': 'hello',
        'MessageSid': 'SM1234567890',
        'AccountSid': 'AC1234567890'
    }
    
    test_messages = ['hello', 'help', 'menu', '1', 'contact']
    
    base_url = "http://localhost:8080"
    
    for message in test_messages:
        print(f"\n📱 Testing message: '{message}'")
        
        # Update the message body
        webhook_data['Body'] = message
        
        try:
            response = requests.post(f"{base_url}/webhook", data=webhook_data)
            print(f"✅ Status: {response.status_code}")
            print(f"🤖 Response: {response.text}")
            
        except requests.exceptions.ConnectionError:
            print("❌ Flask app not running. Start with: python app.py")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_webhook_manually()
