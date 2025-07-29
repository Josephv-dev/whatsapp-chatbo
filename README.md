# WhatsApp Chatbot with Python & Twilio

A simple WhatsApp chatbot built using Python, Flask, and Twilio's WhatsApp Business API.

## Features

- 🤖 Automated responses to common queries
- 📱 WhatsApp integration via Twilio
- 🍽️ Service menu system
- 📞 Contact information sharing
- 🆘 Support routing
- 🏥 Health check endpoint

## Setup Instructions

### 1. Prerequisites
- Python 3.7+
- Twilio account
- ngrok (for local testing)

### 2. Installation

```bash
# Clone or download this project
cd whatsapp-chatbot

# Install dependencies
pip install -r requirements.txt
```

### 3. Twilio Configuration

1. **Create Twilio Account**: Go to [twilio.com](https://twilio.com) and sign up
2. **Get Credentials**: From your Twilio Console, copy:
   - Account SID (starts with AC...)
   - Auth Token
3. **Update .env file**:
   ```
   TWILIO_ACCOUNT_SID=your_actual_account_sid
   TWILIO_AUTH_TOKEN=your_actual_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```

### 4. Twilio WhatsApp Sandbox Setup

1. Go to Twilio Console → Messaging → Try it out → Send a WhatsApp message
2. Send "join [your-sandbox-keyword]" to +1 415 523 8886 from your WhatsApp
3. You'll receive a confirmation message

### 5. Running the Bot

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 6. Webhook Configuration

For production, you need to expose your webhook to the internet:

1. **Install ngrok**: Download from [ngrok.com](https://ngrok.com)
2. **Expose local server**:
   ```bash
   ngrok http 5000
   ```
3. **Configure Twilio Webhook**:
   - Go to Twilio Console → Messaging → Settings → WhatsApp sandbox settings
   - Set webhook URL to: `https://your-ngrok-url.ngrok.io/webhook`

## Bot Commands

Send these messages to your bot:

- `hello` or `hi` - Welcome message
- `help` - Show available commands
- `menu` - Display service menu
- `contact` - Get contact information
- `about` - Learn about the bot
- `support` - Connect to support
- `1-5` - Select from service menu

## API Endpoints

- `GET /` - Home page with bot info
- `POST /webhook` - WhatsApp webhook endpoint
- `GET /health` - Health check
- `POST /send-message` - Send message programmatically

## Testing

Test the health endpoint:
```bash
curl http://localhost:5000/health
```

## Project Structure

```
whatsapp-chatbot/
├── app.py              # Main Flask application
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Customization

Edit the `process_message()` function in `app.py` to add your own bot responses and logic.

## Troubleshooting

1. **Twilio credentials not found**: Update your `.env` file with correct credentials
2. **Webhook not receiving messages**: Check ngrok URL and Twilio webhook configuration
3. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## Production Deployment

For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Deploying to cloud platforms (Heroku, AWS, Google Cloud)
- Using environment variables instead of .env file
- Adding database for conversation storage
- Implementing proper logging and monitoring
