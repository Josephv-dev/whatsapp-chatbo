from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv
from dictionary import get_word_definition, is_dictionary_request, extract_word_from_message

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Twilio configuration
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

client = Client(account_sid, auth_token)

def process_message(incoming_msg, sender_number):
    """
    Process incoming message and generate response
    """
    original_msg = incoming_msg.strip()  # Keep original case for dictionary
    incoming_msg = incoming_msg.lower().strip()
    
    # Check for dictionary requests first
    if is_dictionary_request(original_msg):
        word = extract_word_from_message(original_msg)
        if word:
            return get_word_definition(word)
        else:
            return "📖 Please specify a word to define. Try: 'define python' or 'what is artificial'"
    
    # Simple bot responses
    if 'hello' in incoming_msg or 'hi' in incoming_msg:
        return "Hello! 👋 Welcome to our WhatsApp chatbot. How can I help you today?"
    
    elif 'help' in incoming_msg:
        return """Here's what I can help you with:
        
📍 Type 'menu' - See our services
💬 Type 'contact' - Get our contact info
📞 Type 'support' - Talk to a human
🤖 Type 'about' - Learn about this bot
📖 Dictionary - Type 'define [word]' or 'what is [word]'

📝 Examples:
• define python
• what is artificial
• meaning of hello"""
    
    elif 'menu' in incoming_msg:
        return """🍽️ Our Services:
        
1. 🍕 Food Delivery
2. 📦 Package Tracking
3. 💳 Bill Payment
4. 📱 Tech Support
5. 🛒 Online Shopping

Reply with the number (1-5) to get started!"""
    
    elif 'contact' in incoming_msg:
        return """📞 Contact Information:
        
📧 Email: support@company.com
📱 Phone: +1-555-0123
🌐 Website: www.company.com
📍 Address: 123 Main St, City, State"""
    
    elif 'about' in incoming_msg:
        return """🤖 About This Bot:
        
I'm an AI-powered WhatsApp chatbot built with Python and Twilio. I can help you with various tasks and answer your questions 24/7!
        
Type 'help' to see what I can do."""
    
    elif incoming_msg in ['1', '2', '3', '4', '5']:
        services = {
            '1': '🍕 Food Delivery: Visit our app or call +1-555-FOOD',
            '2': '📦 Package Tracking: Send us your tracking number',
            '3': '💳 Bill Payment: Visit our secure portal at pay.company.com',
            '4': '📱 Tech Support: Connecting you to our tech team...',
            '5': '🛒 Online Shopping: Check out our store at shop.company.com'
        }
        return services.get(incoming_msg, "Invalid option. Please try again.")
    
    elif 'support' in incoming_msg:
        return "🆘 Connecting you to our support team. Please wait while we find an available agent..."
    
    else:
        return """I'm sorry, I didn't understand that. 🤔

Type 'help' to see what I can assist you with, or try:
• hello
• menu  
• contact
• about
• define [word] - for dictionary lookup"""

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive WhatsApp messages
    """
    try:
        # Get the incoming message
        incoming_msg = request.values.get('Body', '').strip()
        sender_number = request.values.get('From', '')
        
        print(f"Received message from {sender_number}: {incoming_msg}")
        
        # Process the message and get response
        response_text = process_message(incoming_msg, sender_number)
        
        # Create Twilio response
        response = MessagingResponse()
        msg = response.message()
        msg.body(response_text)
        
        print(f"Sending response: {response_text}")
        
        return str(response)
    
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        response = MessagingResponse()
        msg = response.message()
        msg.body("Sorry, I encountered an error. Please try again later.")
        return str(response)

@app.route('/send-message', methods=['POST'])
def send_message():
    """
    Endpoint to send messages programmatically (for testing)
    """
    try:
        data = request.json
        to_number = data.get('to')
        message_body = data.get('message')
        
        if not to_number or not message_body:
            return jsonify({'error': 'Missing required fields: to, message'}), 400
        
        # Send message via Twilio
        message = client.messages.create(
            body=message_body,
            from_=twilio_whatsapp_number,
            to=f'whatsapp:{to_number}'
        )
        
        return jsonify({
            'success': True,
            'message_sid': message.sid,
            'status': message.status
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'WhatsApp Chatbot',
        'twilio_configured': bool(account_sid and auth_token)
    })

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with basic info
    """
    return """
    <h1>WhatsApp Chatbot Server</h1>
    <p>Your WhatsApp chatbot is running!</p>
    <ul>
        <li><strong>Webhook URL:</strong> /webhook</li>
        <li><strong>Health Check:</strong> /health</li>
        <li><strong>Send Message:</strong> /send-message (POST)</li>
    </ul>
    <p>Configure your Twilio webhook to point to: <code>your-domain.com/webhook</code></p>
    """

# For Vercel serverless deployment, we export the app
# No need to run app.run() in serverless environment
if __name__ == '__main__':
    # This will only run in local development
    print("🧪 Running locally for testing...")
    app.run(debug=True, host='127.0.0.1', port=8080)
