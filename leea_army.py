# leea_army.py
import os
import json
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

class LeeaArmyCampaignManager:
    """Kelas untuk menguruskan kempen automasi pemasaran dan pengedaran iklan sistem Leea Army"""
    
    def __init__(self, client_id="CLI-1001"):
        self.client_id = client_id
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def generate_campaign_payload(self, campaign_name, ad_copy, target_platform="facebook"):
        """Menjana struktur data fail konfigurasi kempen Ads Army"""
        campaign_data = {
            "clientId": self.client_id,
            "campaignName": campaign_name,
            "targetPlatform": target_platform,
            "adCopyTemplate": ad_copy,
            "status": "Active 🟢",
            "createdDate": self.timestamp,
            "metrics": {
                "totalLeads": 0,
                "engagementRate": "0.0%"
            }
        }
        return campaign_data

    def save_campaign_config(self, campaign_name, ad_copy, output_dir="leea_army_logs"):
        """Menyimpan fail log konfigurasi kempen ke direktori tempatan"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            file_name = f"{self.client_id}_campaign_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path = os.path.join(output_dir, file_name)
            
            payload = self.generate_campaign_payload(campaign_name, ad_copy)
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
                
            print(f"[LEEA ARMY] Kempen '{campaign_name}' untuk klien {self.client_id} berjaya disimpan di: {file_path}")
            return {"status": "success", "path": file_path}
            
        except Exception as e:
            print(f"[LEEA ARMY ERROR] Gagal menyimpan fail kempen: {e}")
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Contoh ujian tempatan
    manager = LeeaArmyCampaignManager(client_id="CLI-1002")
    manager.save_campaign_config(
        campaign_name="Kempen Leads WhatsApp V2",
        ad_copy="Dapatkan sistem automasi WhatsApp perniagaan anda sekarang!"
    )