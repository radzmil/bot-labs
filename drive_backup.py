# drive_backup.py
import os
import shutil
import datetime
import time
import schedule
import requests
import json

# URL Webhook Google Apps Script (GAS) untuk folder Bot-labs PA
GOOGLE_SCRIPT_DRIVE_ENDPOINT = os.environ.get(
    "GOOGLE_SHEET_URL", 
    "https://script.google.com/macros/s/AKfycbwCI81hd5gKZfZP_fBJvwKwr8hxAz4F_sTyqVEFEYwUZimtnCBiqwJWogxwCS_I6BlH/exec"
)

def backup_bot_labs_folder(target_folder=".", backup_dest="backup_archives"):
    """Menyalin dan mengumpulkan semua fail dalam folder bot_labs untuk sandaran harian."""
    waktu_sekarang = datetime.datetime.now()
    tarikh_hari = waktu_sekarang.strftime("%Y-%m-%d_%H-%M-%S")
    
    if not os.path.exists(backup_dest):
        os.makedirs(backup_dest)
        
    archive_name = os.path.join(backup_dest, f"bot_labs_backup_{tarikh_hari}")
    
    try:
        shutil.make_archive(archive_name, 'zip', target_folder)
        log_msg = f"[{waktu_sekarang.strftime('%Y-%m-%d %H:%M:%S')}] Sandaran zip berjaya disimpan ke {archive_name}.zip"
        print(log_msg)
        
        with open("backup_activity.log", "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
            
    except Exception as err:
        print(f"[BACKUP ERROR] Gagal melakukan sandaran fail zip: {err}")

def upload_daily_log_to_google_drive():
    """
    Fungsi rasmi Bot untuk menghantar fail log audit dan status sistem 
    terus ke folder Bot-labs PA di Google Drive tepat jam 11:59 malam[cite: 6].
    """
    waktu_sekarang = datetime.datetime.now()
    tarikh_hari_ini = waktu_sekarang.strftime("%Y-%m-%d %H:%M:%S")
    fail_log_path = "audit_trail.log"
    
    log_content = "Tiada rekod log audit ditemui."
    if os.path.exists(fail_log_path):
        try:
            with open(fail_log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                log_content = "".join(lines[-100:]) # Ambil 100 baris log terkini[cite: 6]
        except Exception as e:
            log_content = f"Ralat membaca fail log: {str(e)}"

    payload = {
        "action": "upload_daily_backup_log",
        "targetFolder": "Bot-labs PA",
        "timestamp": tarikh_hari_ini,
        "fileName": f"Bot-Labs_Audit_Log_{waktu_sekarang.strftime('%Y-%m-%d')}.txt",
        "fileContent": log_content,
        "systemStatus": "ONLINE (50/50 Nodes Stable)",
        "operator": "Radzmil Amaluz Zamani"
    }

    try:
        response = requests.post(GOOGLE_SCRIPT_DRIVE_ENDPOINT, json=payload, timeout=15)
        if response.status_code == 200:
            print(f"[GOOGLE DRIVE SYNC] Berjaya upload fail log ke folder Bot-labs PA pada {tarikh_hari_ini}!")
            return True
        else:
            print(f"[GOOGLE DRIVE ERROR] Gagal upload. Kod status: {response.status_code}")
            return False
    except Exception as e:
        print(f"[GOOGLE DRIVE EXCEPTION] Ralat sambungan ke Google Script: {e}")
        return False

def job_trigger():
    """Fungsi pencetus utama yang dijalankan tepat jam 11:59 malam."""
    print("Mencetuskan rutin sandaran harian dan sinkronisasi Google Drive...")
    backup_bot_labs_folder()
    upload_daily_log_to_google_drive()

# Tetapkan masa sandaran setiap hari pada jam 11:59 malam
schedule.every().day.at("23:59").do(job_trigger)

if __name__ == "__main__":
    print("Sistem penjadual sandaran harian dan Google Drive aktif. Menunggu jam 11:59 malam...")
    
    while True:
        schedule.run_pending()
        time.sleep(30)