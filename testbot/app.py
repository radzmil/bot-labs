import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inisialisasi klien Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "Bot AI Backend is Online and Active!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return "Verification failed", 403
        return "Hello World", 200

    elif request.method == "POST":
        data = request.json
        print("Webhook received:", data)
        
        try:
            # Semak sama ada mesej WhatsApp masuk
            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages")
            
            if messages:
                message = messages[0]
                from_number = message.get("from") # Nombor telefon pengirim
                msg_body = message.get("text", {}).get("body") # Teks mesej
                
                if msg_body:
                    print(f"Mesej diterima daripada {from_number}: {msg_body}")
                    
                    # 1. Jana jawapan pintar menggunakan Gemini
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"Anda adalah pembantu perkhidmatan pelanggan digital yang mesra dan membantu. Jawab mesej pelanggan ini dengan ringkas: {msg_body}"
                    )
                    ai_reply = response.text
                    print(f"Jawapan AI: {ai_reply}")
                    
                    # 2. Hantar semula jawapan ke WhatsApp API
                    send_whatsapp_message(from_number, ai_reply)
                    
        except Exception as e:
            print(f"Ralat memproses webhook: {e}")
            
        return jsonify({"status": "success"}), 200

def send_whatsapp_message(to_number, message_text):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        print("Kredensial WhatsApp tidak lengkap. Mesej tidak dapat dihantar.")
        return
        
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print("WhatsApp Send Status:", response.status_code, response.text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)