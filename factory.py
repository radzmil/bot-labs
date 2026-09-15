import os
import subprocess
import requests
from datetime import datetime
from sheets_db import save_bot_to_sheet

def deploy_to_railway(folder_name, bot_name, railway_token):
    if not railway_token:
        print("Railway Token tidak dijumpai. Proses deploy ke Railway dilangkau.")
        return

    print(f"Menghantar projek '{bot_name}' ke Railway melalui API...")
    url = "https://backboard.railway.app/graphql/v2"
    headers = {
        "Authorization": f"Bearer {railway_token}",
        "Content-Type": "application/json"
    }
    create_project_query = """
    mutation createProject($name: String) {
        projectCreate(input: { name: $name }) {
            id
            name
        }
    }
    """
    payload = {
        "query": create_project_query,
        "variables": {"name": bot_name}
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        if "errors" in result:
            print(f"Ralat Railway API: {result['errors'][0]['message']}")
        else:
            project_data = result.get("data", {}).get("projectCreate", {})
            project_id = project_data.get("id")
            print(f"Projek Railway berjaya dicipta! Project ID: {project_id}")
    except Exception as e:
        print(f"Ralat sambungan ke Railway: {e}")

def create_bot_factory(bot_name, whatsapp_token, phone_id, verify_token, gemini_api_key, company_name="Architech Laboratory", bank_info="Maybank / DuitNow", railway_token=""):
    folder_name = bot_name.lower().replace(" ", "_")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Direktori '{folder_name}' berjaya dicipta.")
    else:
        print(f"Direktori '{folder_name}' sudah wujud.")

    # 1. Fail .env
    env_content = f"""WHATSAPP_TOKEN={whatsapp_token}
WHATSAPP_PHONE_ID={phone_id}
VERIFY_TOKEN={verify_token}
GEMINI_API_KEY={gemini_api_key}
"""
    with open(os.path.join(folder_name, ".env"), "w") as f:
        f.write(env_content)

    # 2. Fail Procfile
    with open(os.path.join(folder_name, "Procfile"), "w") as f:
        f.write("web: python bot_engine.py\n")

    # 3. Fail requirements.txt (Termasuk gspread & google-auth untuk Google Sheets)
    requirements_content = """flask
requests
google-genai
python-dotenv
gspread
google-auth
"""
    with open(os.path.join(folder_name, "requirements.txt"), "w") as f:
        f.write(requirements_content)

    # 4. Fail .gitignore
    with open(os.path.join(folder_name, ".gitignore"), "w") as f:
        f.write(".env\n__pycache__/\nvenv/\n")

    # 5. Modul: company_profile.py
    company_profile_content = f"""# Company Profile Setup
COMPANY_NAME = "{company_name}"
TAGLINE = "Automasi Pintar & Perkhidmatan Pelanggan Digital"
SERVICES = "Sistem Bot WhatsApp AI dan Pengurusan Operasi Perniagaan."
"""
    with open(os.path.join(folder_name, "company_profile.py"), "w") as f:
        f.write(company_profile_content)

    # 6. Modul: sop_payment.py
    sop_payment_content = f"""# SOP Payment Setup
BANK_INFO = "{bank_info}"
PAYMENT_INSTRUCTION = "Sila hantar resit transaksi ke saluran ini untuk pengesahan."
"""
    with open(os.path.join(folder_name, "sop_payment.py"), "w") as f:
        f.write(sop_payment_content)

    # 7. Modul: bot_brain.py
    bot_brain_content = '''from google import genai
from company_profile import COMPANY_NAME, SERVICES
from sop_payment import BANK_INFO, PAYMENT_INSTRUCTION

def get_ai_response(client, user_message):
    persona = f"Anda adalah pembantu digital rasmi untuk {COMPANY_NAME}. Fokus anda ialah membantu pelanggan mengenai {SERVICES}."
    payment_context = f"Maklumat Bayaran: {BANK_INFO}. {PAYMENT_INSTRUCTION}"
    
    prompt = f"{persona}\\n{payment_context}\\n\\nPeraturan: Jawab dengan mesra, profesional, dan ringkas dalam Bahasa Melayu.\\nMesej Pelanggan: {user_message}"
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
'''
    with open(os.path.join(folder_name, "bot_brain.py"), "w") as f:
        f.write(bot_brain_content)

    # 8. Modul: bot_engine.py
    bot_engine_content = """import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google import genai
from bot_brain import get_ai_response

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "Bot Engine is Online and Active!"

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
        try:
            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages")
            
            if messages:
                message = messages[0]
                from_number = message.get("from")
                msg_body = message.get("text", {}).get("body")
                
                if msg_body:
                    ai_reply = get_ai_response(client, msg_body)
                    send_whatsapp_message(from_number, ai_reply)
                    
        except Exception as e:
            print(f"Ralat memproses webhook: {e}")
            
        return jsonify({"status": "success"}), 200

def send_whatsapp_message(to_number, message_text):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
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
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
"""
    with open(os.path.join(folder_name, "bot_engine.py"), "w") as f:
        f.write(bot_engine_content)

    # 9. Simpan Rekod Bot ke Google Sheets Akaun Radzmil
    webhook_url = f"https://{folder_name}-production.up.railway.app/webhook"
    bot_data = {
        "company_name": company_name,
        "bot_name": bot_name,
        "phone_id": phone_id,
        "access_token": whatsapp_token,
        "gemini_api_key": gemini_api_key,
        "webhook_url": webhook_url,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")
    if sheet_id:
        try:
            save_bot_to_sheet(sheet_id, bot_data)
            print(f"Data bot {bot_name} berjaya direkodkan ke Google Sheets!")
        except Exception as e:
            print(f"Ralat menyimpan ke Google Sheets: {e}")
    else:
        print("GOOGLE_SHEET_ID tidak disetkan. Rekod Google Sheets dilangkau.")

    # 10. Automasi Git & Push ke GitHub
    try:
        subprocess.run(["git", "init"], cwd=folder_name, check=True, capture_output=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=folder_name, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=folder_name, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Initial modular commit for {bot_name}"], cwd=folder_name, check=True, capture_output=True)
        
        # Sambungkan ke GitHub remote repository di bawah organisasi architechlabsserver1
        repo_url = f"https://github.com/architechlabsserver1/{folder_name}.git"
        subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=folder_name, check=True, capture_output=True)
        
        # Push ke GitHub
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=folder_name, check=True, capture_output=True)
        print(f"Kod berjaya di-push ke GitHub untuk bot {bot_name}!")
    except Exception as e:
        print(f"Ralat semasa automasi Git & Push: {e}")

    # 11. Deploy ke Railway
    if railway_token:
        deploy_to_railway(folder_name, bot_name, railway_token)