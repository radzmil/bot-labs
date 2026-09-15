import os
import subprocess
import datetime
import time
import threading
import shutil
from functools import wraps
from flask import request, abort, jsonify
from google import genai

# Senarai IP yang dibenarkan (Whitelist) & Token YubiKey Master
ALLOWED_IPS = ['127.0.0.1', '192.168.1.100']
YUBIKEY_MASTER_TOKEN = "architech-yubikey-secure-token-2026"
MAINTENANCE_MODE = False

# 1. Lapisan Keselamatan: Sekatan IP (Whitelisting) & akses warisan kecemasan YubiKey
def security_guard(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        yubikey_token = request.headers.get('X-YubiKey-Token')
        
        if client_ip not in ALLOWED_IPS and yubikey_token != YUBIKEY_MASTER_TOKEN:
            audit_logger(f"AMARAN: Akses ditolak untuk IP {client_ip}")
            abort(403, description="Akses ditolak: IP tidak disenarai putih atau token YubiKey tidak sah.")
        return f(*args, **kwargs)
    return decorated_function

# 2. Kotak Pembantu AI: Alat analisis log (AI Log Analyzer) sebenar menggunakan Gemini API
def analyze_error_log(log_content):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Ralat: Kunci API Gemini (GEMINI_API_KEY) tidak disetkan di dalam persekitaran (environment) pelayan."
    
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        Anda ialah Pembantu Pakar Sistem Backend dan Pembaikan Pepijat (Bug Fixer). 
        Sila analisis mesej ralat log pelayan berikut, kenal pasti punca kerosakan, dan berikan cadangan kod pembaikan yang tepat dalam Bahasa Melayu:
        
        {log_content}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        audit_logger("Kotak Pembantu AI berjaya menganalisis log ralat menggunakan Gemini API.")
        return response.text
    except Exception as e:
        audit_logger(f"Ralat sambungan AI Gemini: {str(e)}")
        return f"Gagal berhubung dengan pelayan AI Gemini: {str(e)}"

# 3. Pengurusan Fail HTML: Fungsi muat naik (Overwrite Mode) & penciptaan fail baru
def manage_html_file(filename, content, overwrite=True):
    target_dir = os.path.join(os.getcwd(), 'templates')
    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, filename)
    
    if os.path.exists(file_path) and not overwrite:
        return False, f"Fail {filename} sudah wujud dan mod overwrite ditutup."
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    audit_logger(f"Fail HTML '{filename}' berjaya dikemaskini/dicipta.")
    return True, f"Fail {filename} berjaya disimpan."

# 4. Automasi Git: Pelaksanaan push, commit, dan add automatik ke GitHub
def execute_git_automation(commit_message="Auto-update by Bot-Labs Admin Panel"):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        audit_logger("Automasi Git: Push ke GitHub berjaya.")
        return True, "Git push berjaya dilaksanakan."
    except subprocess.CalledProcessError as e:
        audit_logger(f"Ralat Git automation: {str(e)}")
        return False, f"Ralat Git automation: {str(e)}"

# 5. Kawalan Sistem: Suis Mod Penyelenggaraan & Log Aktiviti (Audit Trail)
def toggle_maintenance_mode(status: bool):
    global MAINTENANCE_MODE
    MAINTENANCE_MODE = status
    audit_logger(f"Mod Penyelenggaraan ditukar kepada: {MAINTENANCE_MODE}")
    return MAINTENANCE_MODE

def audit_logger(action_description):
    log_path = os.path.join(os.getcwd(), 'audit_trail.log')
    with open(log_path, 'a', encoding='utf-8') as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {action_description}\n")

# 6. Modul Scheduler Backup (Daemon Thread) - Berjalan automatik setiap jam 11:59 malam
def perform_daily_backup():
    try:
        backup_dir = os.path.join(os.getcwd(), 'bot_labs_backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        target_archive = os.path.join(backup_dir, f"backup_{date_str}")
        
        # Salin direktori projek semasa ke dalam folder arkib harian
        if os.path.exists(target_archive):
            shutil.rmtree(target_archive)
        
        # Mengabaikan folder persekitaran maya atau arkib itu sendiri
        shutil.copytree(os.getcwd(), target_archive, ignore=shutil.ignore_patterns('bot_labs_backups', '__pycache__', '.git', 'venv'))
        audit_logger(f"SANDARAN HARIAN: Berjaya menyalin fail sistem ke arkib [{date_str}].")
    except Exception as e:
        audit_logger(f"RALAT SANDARAN HARIAN: {str(e)}")

def background_backup_scheduler():
    """Daemon thread untuk mengimbas masa dan mencetuskan backup pada pukul 11:59 malam."""
    while True:
        now = datetime.datetime.now()
        # Semak jika jam 23:59 (11:59 malam)
        if now.hour == 23 and now.minute == 59:
            perform_daily_backup()
            # Tunggu selama 70 saat supaya ia tidak berulang berkali-kali dalam minit yang sama
            time.sleep(70)
        else:
            # Semak setiap 30 saat
            time.sleep(30)

# Mulakan daemon thread di latar belakang secara automatik apabila backend diimport/dijalankan
backup_thread = threading.Thread(target=background_backup_scheduler, daemon=True)
backup_thread.start()
audit_logger("Sistem Daemon Thread Scheduler Backup harian telah diaktifkan di latar belakang.")