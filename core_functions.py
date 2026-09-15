# core_functions.py
import os
import datetime
import smtplib
import shutil
import schedule
import time
import threading
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request
from dotenv import load_dotenv
from drive_backup import upload_daily_log_to_google_drive

load_dotenv()

def log_audit_action(username, action_desc):
    """Merekodkan setiap aktiviti penting ke dalam audit_trail.log"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        client_ip = request.remote_addr if request else "127.0.0.1"
    except RuntimeError:
        client_ip = "127.0.0.1"
        
    log_entry = f"[{timestamp}] USER: {username} | ACTION: {action_desc} | IP: {client_ip}\n"
    try:
        with open("audit_trail.log", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print("Gagal menulis log audit:", e)

def send_whatsapp_otp_real(phone_number, otp_code):
    """Menghantar kod OTP sebenar melalui WhatsApp Business Cloud API menggunakan kredensial .env"""
    whatsapp_token = os.environ.get("WHATSAPP_TOKEN", "")
    phone_id = os.environ.get("WHATSAPP_PHONE_ID", "")
    
    url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": f"🔐 [BOT-LABS SECURITY] Kod pengesahan OTP WhatsApp anda ialah: *{otp_code}*. Sahkan segera untuk log masuk ke sistem."
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Ralat hantaran WhatsApp API: {e}")
        return False

def perform_daily_backup():
    """Fungsi untuk menyalin dan membuat sandaran semua fail di Bot-Labs ke folder backup & auto-upload ke Google Drive tepat 11:59 PM"""
    source_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dest_dir = os.path.join(source_dir, "bot_labs_backups", f"backup_{timestamp}")
    
    try:
        shutil.copytree(
            source_dir, 
            backup_dest_dir, 
            ignore=shutil.ignore_patterns('bot_labs_backups', '.git', '__pycache__', '*.log')
        )
        print(f"[AUTO BACKUP] Berjaya menyandarkan semua fail Bot-Labs pada {timestamp} ke: {backup_dest_dir}")
        
        log_path = os.path.join(source_dir, 'audit_trail.log')
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{log_timestamp}] USER: system_scheduler | ACTION: Auto backup harian berjaya disimpan ke {backup_dest_dir} | IP: 127.0.0.1\n")
            
        upload_daily_log_to_google_drive()
        print(f"[AUTO BACKUP] Google Drive sync ke folder Bot-labs PA berjaya dijalankan!")
            
    except Exception as e:
        print(f"[AUTO BACKUP ERROR] Gagal melakukan sandaran harian: {e}")

def run_scheduler():
    """Menjalankan gelung penjadual masa di latar belakang"""
    schedule.every().day.at("23:59").do(perform_daily_backup)
    
    while True:
        schedule.run_pending()
        time.sleep(30)

def start_background_scheduler():
    """Memulakan thread penjadual masa di latar belakang"""
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

def send_subscription_email(client_id, module_type):
    """Menghantar e-mel notifikasi pengesahan langganan produk kepada klien menggunakan akaun rasmi"""
    sender_email = "architechlaboratory@gmail.com"
    app_password = "H@$$ayang8683"
    
    client_email = f"{client_id.lower()}@client.architechlaboratory.my"
    
    subject = f"[A.R.C.H.I.T.E.C.H] Pengesahan Langganan Modul: {module_type}"
    body = f"""
    Tahniah!
    
    Akaun / Slot Klien anda ({client_id}) telah berjaya melanggan dan mengaktifkan modul eksklusif: {module_type}.
    
    Sistem automasi dan pautan kawalan anda kini sudah bersedia beroperasi di bawah ekosistem Bot-Labs Architech Laboratory (www.architechlaboratory.my).
    
    Sekian,
    Pentadbir Sistem Bot-Labs
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, client_email, msg.as_string())
        server.quit()
        print(f"E-mel pengesahan berjaya dihantar kepada {client_email}")
    except Exception as e:
        print(f"Ralat hantaran e-mel SMTP: {e}")