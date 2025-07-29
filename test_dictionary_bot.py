from app import process_message

def test_dictionary_bot():
    """Test the enhanced bot with dictionary functionality"""
    
    print("🧪 Testing Enhanced WhatsApp Bot with Dictionary")
    print("=" * 60)
    
    test_messages = [
        # Regular bot functions
        "hello",
        "help",
        "menu",
        
        # Dictionary requests
        "define python",
        "what is artificial",
        "meaning of hello",
        "define beautiful",
        "what does amazing mean",
        "dictionary love",
        
        # Invalid dictionary requests
        "define",
        "define xyz123invalid",
        
        # Regular unknown message
        "random message"
    ]
    
    for msg in test_messages:
        print(f"\n📱 User: {msg}")
        response = process_message(msg, "test_user")
        print(f"🤖 Bot: {response[:200]}...")  # Limit output for readability
        print("-" * 50)

if __name__ == "__main__":
    test_dictionary_bot()
