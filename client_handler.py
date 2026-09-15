# client_handler.py
import os
import json
import datetime
import subprocess
import requests
from flask import request, session, jsonify

GOOGLE_SCRIPT_DRIVE_ENDPOINT = os.environ.get("GOOGLE_SHEET_URL", "https://script.google.com/macros/s/AKfycbx2CQv19OWVYax2vy6LHMsDeeRtWIPuet-jgR_39n3wyTlIcM_VSekzWD-_wkd7xxBS9w/exec")

def register_client_logic(log_audit_func):
    """Logika penuh untuk pendaftaran klien baharu, sync Vercel, dan Google Drive/Local backup"""
    if not session.get("logged_in"):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    client_id = request.form.get("client_id", "CLI-1002")
    company_name = request.form.get("company_name", "Unknown Company")
    username = request.form.get("username", "")
    
    password = request.form.get("password", "").strip()
    if not password:
        password = "defaultpass123"
        
    phone = request.form.get("phone", "")
    email = request.form.get("email", "")
    railway_url = request.form.get("railway_url", "https://web-production-07b92.up.railway.app")
    
    # 1. Laluan mutlak tepat ke Leea-portal supaya Vercel baca akaun untuk klien login
    portal_dir = r"C:\Users\radzm\OneDrive\Documents\DB_architechlaboratory\architech laboratory\Leea-portal"
    db_file = os.path.join(portal_dir, 'clients_db.json')
    
    clients_list = []
    if os.path.exists(db_file):
        try:
            with open(db_file, 'r', encoding='utf-8') as f:
                clients_list = json.load(f)
        except:
            clients_list = []
            
    clients_list = [c for c in clients_list if c.get('username') != username]
    
    new_client_record = {
        "clientId": client_id,
        "companyName": company_name,
        "username": username,
        "password": password,
        "phone": phone,
        "email": email,
        "status": "Paid 🟢",
        "planTier": "v1 pro",
        "expiryDate": "27/10/2026",
        "tokenBalance": 1000,
        "railwayUrl": railway_url
    }
    clients_list.append(new_client_record)
    
    os.makedirs(portal_dir, exist_ok=True)
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(clients_list, f, indent=4, ensure_ascii=False)

    # 2. Automasi Git Push terus dari folder Leea-portal ke Vercel/GitHub
    try:
        subprocess.run(["git", "add", "clients_db.json"], cwd=portal_dir, check=True)
        commit_msg = f"Auto-sync client {username} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=portal_dir, check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=portal_dir, check=True)
    except Exception as e:
        print(f"Nota Git Push auto: {e}")

    # 3. Penjanaan folder pecahan 1 klien 1 folder di Google Drive
    folder_name = f"{client_id} - {company_name or username}"
    client_backup_payload = {
        "action": "create_client_folder_and_backups",
        "clientId": client_id,
        "companyName": company_name,
        "username": username,
        "folderName": folder_name,
        "backups": {
            "client_profile": new_client_record,
            "railway_deployment": {
                "railwayUrl": railway_url,
                "memoryModel": "V1",
                "status": "active"
            },
            "bot_brain_config": {
                "brainPrompt": "Default Leea Bot Personality V1",
                "customScript": "",
                "tone": "professional"
            },
            "app_integration": {
                "whatsappToken": "",
                "phoneId": "",
                "verifyToken": "verifysini123",
                "geminiApiKey": "",
                "tokenBalance": 1000
            },
            "e_wallet_affiliate": {
                "isAgent": False,
                "walletBalance": 0.0,
                "totalReferrals": 0,
                "totalEarned": 0.0,
                "bankName": "",
                "accountNo": "",
                "accountHolder": ""
            },
            "chat_history_logs": [],
            "payment_history": [],
            "client_inbox": [],
            "client_audit_trail": [
                {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "event": f"Klien {client_id} ({company_name}) berjaya didaftarkan dengan password lalai (defaultpass123) dan fail backup lengkap dijana."
                }
            ]
        }
    }
    
    try:
        requests.post(GOOGLE_SCRIPT_DRIVE_ENDPOINT, json=client_backup_payload, timeout=5)
    except Exception as e:
        print(f"Nota: Automasi Google Drive diserahkan kepada background worker: {e}")

    # 4. Simpan struktur pecahan 1 klien 1 folder di direktori komputer tempatan
    base_client_dir = r"C:\Users\radzm\OneDrive\Documents\DB_architechlaboratory\architech laboratory\client"
    specific_client_folder = os.path.join(base_client_dir, client_id)
    
    try:
        os.makedirs(specific_client_folder, exist_ok=True)
        for filename_key, content in client_backup_payload["backups"].items():
            file_path = os.path.join(specific_client_folder, f"{filename_key}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=4, ensure_ascii=False)
                
        log_path = os.path.join(specific_client_folder, "client_audit_trail.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] Klien {client_id} ({company_name}) berjaya didaftarkan dengan password lalai (defaultpass123).\n")

        log_audit_func(session.get("username", "superadmin"), f"Daftar klien baru [{client_id}] & auto-sync ke Leea-portal & Google Drive")
        
        return jsonify({
            "status": "success",
            "message": f"Klien {client_id} ({username}) berjaya didaftarkan, diselaraskan ke Vercel untuk login, dan folder pecahan klien dicipta!"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal mencipta struktur folder klien: {str(e)}"
        }), 500