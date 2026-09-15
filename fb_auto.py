# fb_auto.py
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class FacebookAutomationHandler:
    """Kelas untuk mengendalikan automasi Facebook Graph API (Auto-reply & Campaign Sync)"""
    
    def __init__(self, page_access_token="", page_id=""):
        self.access_token = page_access_token or os.environ.get("FB_ACCESS_TOKEN", "")
        self.page_id = page_id or os.environ.get("FB_PAGE_ID", "")
        self.graph_api_version = "v17.0"
        
    def send_page_message(self, recipient_id, message_text):
        """Menghantar mesej auto-balas kepada pengguna melalui Facebook Messenger Page API"""
        if not self.access_token or not self.page_id:
            print("[FB AUTO ERROR] Access Token atau Page ID tidak dijumpai.")
            return False
            
        url = f"https://graph.facebook.com/{self.graph_api_version}/me/messages"
        params = {"access_token": self.access_token}
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }
        
        try:
            response = requests.post(url, params=params, json=payload, timeout=10)
            result = response.json()
            if response.status_code == 200:
                print(f"[FB AUTO] Mesej berjaya dihantar kepada penerima: {recipient_id}")
                return True
            else:
                print(f"[FB AUTO ERROR] Gagal hantar mesej: {result}")
                return False
        except Exception as e:
            print(f"[FB AUTO ERROR] Ralat sambungan API: {e}")
            return False

    def setup_webhook_subscription(self, callback_url, verify_token):
        """Mendaftarkan webhook untuk mengesan mesej masuk atau komen automatik dari FB Page"""
        url = f"https://graph.facebook.com/{self.graph_api_version}/{self.page_id}/subscribed_apps"
        payload = {
            "access_token": self.access_token,
            "subscribed_fields": ["feed", "messages", "messaging_postbacks"]
        }
        
        try:
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code == 200:
                print("[FB AUTO] Langganan webhook Page berjaya diaktifkan!")
                return True
            else:
                print(f"[FB AUTO ERROR] Gagal melanggan webhook: {response.text}")
                return False
        except Exception as e:
            print(f"[FB AUTO ERROR] Ralat webhook setup: {e}")
            return False

if __name__ == "__main__":
    # Contoh ujian tempatan
    fb_bot = FacebookAutomationHandler()
    print("[FB AUTO] Modul Facebook Automation sedia untuk dihubungkan, Tuan.")