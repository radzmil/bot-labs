# fb_post.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class FacebookPostAutomation:
    """Kelas untuk mengendalikan automasi hantaran pos ke Facebook Page secara programatik"""
    
    def __init__(self, page_access_token="", page_id=""):
        self.access_token = page_access_token or os.environ.get("FB_ACCESS_TOKEN", "")
        self.page_id = page_id or os.environ.get("FB_PAGE_ID", "")
        self.graph_api_version = "v17.0"
        
    def publish_text_post(self, message_content):
        """Menerbitkan hantaran teks biasa ke Facebook Page"""
        if not self.access_token or not self.page_id:
            print("[FB POST ERROR] Access Token atau Page ID tidak dijumpai.")
            return {"status": "error", "message": "Kredensial Facebook tidak lengkap."}
            
        url = f"https://graph.facebook.com/{self.graph_api_version}/{self.page_id}/feed"
        payload = {
            "message": message_content,
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(url, data=payload, timeout=15)
            result = response.json()
            
            if response.status_code == 200 and "id" in result:
                post_id = result["id"]
                print(f"[FB POST] Hantaran berjaya diterbitkan! Post ID: {post_id}")
                return {"status": "success", "postId": post_id, "message": "Pos berjaya diterbitkan ke Facebook Page."}
            else:
                print(f"[FB POST ERROR] Gagal terbit pos: {result}")
                return {"status": "error", "message": result.get("error", {}).get("message", "Ralat tidak diketahui")}
                
        except Exception as e:
            print(f"[FB POST ERROR] Ralat sambungan API: {e}")
            return {"status": "error", "message": str(e)}

    def publish_photo_post(self, image_url, caption_text=""):
        """Menerbitkan hantaran gambar beserta kapsyen ke Facebook Page"""
        if not self.access_token or not self.page_id:
            return {"status": "error", "message": "Kredensial Facebook tidak lengkap."}
            
        url = f"https://graph.facebook.com/{self.graph_api_version}/{self.page_id}/photos"
        payload = {
            "url": image_url,
            "caption": caption_text,
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(url, data=payload, timeout=20)
            result = response.json()
            
            if response.status_code == 200 and "id" in result:
                photo_id = result["id"]
                print(f"[FB POST] Gambar berjaya diterbitkan! Photo ID: {photo_id}")
                return {"status": "success", "photoId": photo_id, "message": "Gambar berjaya dimuat naik ke Facebook Page."}
            else:
                return {"status": "error", "message": result.get("error", {}).get("message", "Gagal muat naik gambar")}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Contoh ujian tempatan
    print("[FB POST] Modul Facebook Post Automation sedia beroperasi, Tuan.")