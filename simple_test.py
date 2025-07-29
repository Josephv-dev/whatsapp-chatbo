from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask is working!"

@app.route('/test')
def test():
    return "🧪 Test endpoint working!"

if __name__ == '__main__':
    print("🚀 Starting simple Flask test...")
    try:
        app.run(debug=True, host='127.0.0.1', port=8080)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Trying port 3000...")
        app.run(debug=True, host='127.0.0.1', port=3000)
