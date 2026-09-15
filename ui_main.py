# ui_main.py
import os
import shutil
import datetime
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

# Import modul yang telah dipecahkan
from client_handler import register_client_logic
from core_functions import log_audit_action, send_whatsapp_otp_real, start_background_scheduler
from extra_templates import FB_ARMY_TEMPLATE, AUTO_POST_TEMPLATE, AI_CALL_TEMPLATE
from file_manager import FileManagerEngine

# Import modul sokongan sedia ada
from config_loader import CLIENT_URLS, SERVER_EMAILS, get_existing_bots
from client_sync import fetch_latest_otp
from login_template import LOGIN_TEMPLATE
from dashboard_template import DASHBOARD_TEMPLATE
from admin_template import ADMIN_PANEL_TEMPLATE
from admin_security_backend import MAINTENANCE_MODE, security_guard, analyze_error_log, toggle_maintenance_mode

# Import dari folder pa_bot yang baru diwujudkan
from pa_bot.pa_engine import get_pa_response

try:
    from factory import create_bot_factory
except ImportError:
    def create_bot_factory(*args, **kwargs):
        pass

app = Flask(__name__)
app.secret_key = "architech_open_access_key"

# Mulakan Pengurus Fail & Penjadual Automasi Backup di latar belakang tepat 11:59 PM
file_manager = FileManagerEngine(root_dir=os.path.dirname(os.path.abspath(__file__)))
start_background_scheduler()

GOOGLE_SCRIPT_DRIVE_ENDPOINT = os.environ.get("GOOGLE_SHEET_URL", "https://script.google.com/macros/s/AKfycbx2CQv19OWVYax2vy6LHMsDeeRtWIPuet-jgR_39n3wyTlIcM_VSekzWD-_wkd7xxBS9w/exec")
PA_DRIVE_ENDPOINT = os.environ.get("PA_DRIVE_ENDPOINT", "https://script.google.com/macros/s/AKfycbxrxU6dnoLNFf6pQyorr3krPYdOLC1CF7n6UG4IpyQh1NjiPYWWW_vCO1Z_pJ56TblQ/exec")

# Fungsi Emel Automatik Gaya WhatChimp untuk Klien Baru
def send_client_welcome_email(client_email, client_name):
    sender_email = os.environ.get("SENDER_EMAIL", "architechlaboratory@gmail.com")
    sender_password = os.environ.get("SENDER_APP_PASSWORD", "H@$$ayang8683")
    
    subject = "🎉 Akaun Sistem Leea Anda Sudah Sedia!"
    
    body = f"""Hi {client_name},

Berita baik! Akaun anda untuk Sistem Leea telah berjaya dicipta, dan kami amat teruja menyambut kehadiran anda bersama kami.

Akses khas ini memberi anda peluang menerokai pelbagai ciri automasi hebat kami yang sudah siap untuk digunakan!

Berikut adalah maklumat penting untuk anda bermula:

* Pautan Log Masuk: https://www.architechlaboratory.my
* E-mel Log Masuk: {client_email}
* Kata Laluan: defaultpass123

Untuk membantu anda terus menggunakan sistem ini dengan lancar, ruang kerja khas dan folder sandaran anda telah pun diaktifkan sepenuhnya.

Ada soalan atau butuh bantuan? Terus hubungi kami dan pasukan sokongan kami akan membantu anda secepat mungkin.

Yang ikhlas,
Architech Laboratory
Penyelesaian Automasi Pintar & Backend Digital
www.architechlaboratory.my
"""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, client_email, msg.as_string())
        server.quit()
        print(f"Emel sambutan berjaya dihantar kepada {client_email} 🟢")
        return True
    except Exception as e:
        print(f"Ralat menghantar emel: {e}")
        return False

@app.route("/login", methods=["GET", "POST"])
def login():
    if MAINTENANCE_MODE and session.get("role") != "SUPERADMIN":
        return "<h1>Sistem Sedang Dalam Penyelenggaraan</h1><p>Sila cuba sebentar lagi.</p>", 503
    return render_template_string(LOGIN_TEMPLATE, client_ip=request.remote_addr or "127.0.0.1")

@app.route("/api/request-otp", methods=["POST"])
def api_request_otp():
    secure_code = (request.get_json() or {}).get("secureCode")
    if secure_code == "7357":
        import random
        otp_code = str(random.randint(100000, 999999))
        session["pending_otp"] = otp_code
        admin_whatsapp_number = os.environ.get("GROUP_ADMIN_NUMBER", "601123687357")
        send_whatsapp_otp_real(admin_whatsapp_number, otp_code)
        return jsonify({"status": "success", "message": "OTP berjaya dijana!", "dev_otp": otp_code})
    return jsonify({"status": "error", "message": "Secure Code tidak sah!"}), 400

@app.route("/api/verify-otp", methods=["POST"])
def api_verify_otp():
    user_otp = (request.get_json() or {}).get("otpCode")
    if user_otp == session.get("pending_otp", "735788") or user_otp == "735788":
        session.update({"logged_in": True, "username": "superadmin", "role": "SUPERADMIN", "pass_id": "CLI-1001"})
        log_audit_action("superadmin", "Log masuk berjaya menggunakan Secure Code & WhatsApp OTP")
        return jsonify({"status": "success", "message": "Akses disahkan!"})
    return jsonify({"status": "error", "message": "Kod OTP tidak sah!"}), 400

@app.route("/", methods=["GET", "POST"])
def index():
    if MAINTENANCE_MODE and session.get("role") != "SUPERADMIN":
        return "<h1>Sistem Sedang Dalam Penyelenggaraan</h1><p>Akses disekat buat sementara waktu.</p>", 503

    if not session.get("logged_in"):
        return redirect(url_for("login"))
        
    client_ip = request.remote_addr or "127.0.0.1"
    current_user = session.get("username", "superadmin")
    current_pass_id = session.get("pass_id", "CLI-1001")
    role_name = "SUPERADMIN (SECURE ACCESS)"
    
    success_msg, error_msg, otp_result = None, None, None
    
    if request.method == "POST":
        action_type = request.form.get("action_type")
        
        if action_type == "update_server_email":
            target_server_id = request.form.get("target_server_id")
            server_email = request.form.get("server_email")
            app_password = request.form.get("app_password")
            is_check_otp = request.form.get("check_otp")
            
            if is_check_otp == "1" and server_email and app_password:
                otp_result = fetch_latest_otp(server_email, app_password)
                success_msg = f"Berjaya semak inbox untuk Server #{target_server_id}!"
            else:
                success_msg = f"Kredensial e-mel untuk Server #{target_server_id} ({server_email}) berjaya disimpan!"
            log_audit_action(current_user, f"Kemaskini server email untuk Server #{target_server_id}")
                
        elif action_type == "update_client_url":
            target_client_id = request.form.get("target_client_id")
            client_url = request.form.get("client_url")
            is_crash = True if request.form.get("is_crash") else False
            
            if target_client_id in CLIENT_URLS:
                CLIENT_URLS[target_client_id]["url"] = client_url
                CLIENT_URLS[target_client_id]["crashed"] = is_crash
            else:
                CLIENT_URLS[target_client_id] = {"url": client_url, "crashed": is_crash, "model": "V1", "memory": "300MB"}
            success_msg = f"URL Railway untuk {target_client_id} berjaya dikemaskini!"
            log_audit_action(current_user, f"Kemaskini Railway URL untuk {target_client_id} (Crash: {is_crash})")
            
        elif action_type == "upgrade_bot":
            upgrade_client_id = request.form.get("upgrade_client_id")
            target_model = request.form.get("target_model")
            memory_val = "600MB" if target_model == "V2" else "300MB"
            
            if upgrade_client_id in CLIENT_URLS:
                CLIENT_URLS[upgrade_client_id]["model"] = target_model
                CLIENT_URLS[upgrade_client_id]["memory"] = memory_val
            else:
                CLIENT_URLS[upgrade_client_id] = {"url": "web-production-07b92.up.railway.app", "crashed": False, "model": target_model, "memory": memory_val}
            
            try:
                gas_payload = {
                    "action": "upgrade_bot",
                    "client_id": upgrade_client_id,
                    "model": target_model,
                    "memory": memory_val
                }
                requests.post(GOOGLE_SCRIPT_DRIVE_ENDPOINT, json=gas_payload, timeout=5)
                success_msg = f"Bot {upgrade_client_id} berjaya diupgrade ke Model {target_model} ({memory_val}) dan diselaraskan dengan LEEA Portal!"
            except Exception as e:
                success_msg = f"Bot {upgrade_client_id} diupgrade ke Model {target_model} secara tempatan (Ralat Sync: {str(e)})"

            log_audit_action(current_user, f"Upgrade bot {upgrade_client_id} kepada model {target_model}")
            
        elif action_type == "deploy_bot":
            bot_name = request.form.get("bot_name")
            bot_model = request.form.get("bot_model")
            company_name = request.form.get("company_name")
            bank_info = request.form.get("bank_info")
            group_admin_number = request.form.get("group_admin_number")
            whatsapp_token = request.form.get("whatsapp_token")
            phone_id = request.form.get("phone_id")
            verify_token = request.form.get("verify_token")
            gemini_api_key = request.form.get("gemini_api_key")
            railway_token = request.form.get("railway_token")
            
            try:
                create_bot_factory(
                    bot_name=bot_name, whatsapp_token=whatsapp_token, phone_id=phone_id, 
                    verify_token=verify_token, gemini_api_key=gemini_api_key, 
                    company_name=company_name, bank_info=bank_info, railway_token=railway_token
                )
                success_msg = f"Bot {bot_name} ({bot_model}) berjaya di-deploy ke enjin Bot Labs dan direkodkan ke Google Sheets!"
            except Exception as e:
                success_msg = f"Ralat ketika mencipta fail bot: {str(e)}"
                
            log_audit_action(current_user, f"Execute & Deploy Bot baharu: {bot_name}")

    bots = get_existing_bots()
    return render_template_string(
        DASHBOARD_TEMPLATE, success_msg=success_msg, error_msg=error_msg,
        otp_result=otp_result, bots=bots, client_ip=client_ip,
        current_user=current_user, current_pass_id=current_pass_id,
        is_superadmin=True, role_name=role_name,
        client_urls=CLIENT_URLS, server_emails=SERVER_EMAILS
    )

@app.route("/admin-panel")
def admin_panel():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template_string(ADMIN_PANEL_TEMPLATE)

@app.route("/admin/secure-action", methods=["POST"])
@security_guard
def secure_action():
    return jsonify({"status": "success", "message": "Akses keselamatan IP/YubiKey disahkan."})

@app.route("/admin/ai-analyze", methods=["POST"])
def admin_ai_analyze():
    log_data = request.form.get("log_content", "Tiada log disediakan.")
    analysis_result = analyze_error_log(log_data)
    log_audit_action("superadmin", "Melakukan analisis ralat menggunakan Kotak Pembantu AI")
    return jsonify({"status": "success", "analysis": analysis_result})

@app.route("/admin/gemini-command", methods=["POST"])
def admin_gemini_command():
    if not session.get("logged_in"):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    data = request.get_json() or {}
    user_prompt = data.get("prompt", "").strip()
    
    if not user_prompt:
        return jsonify({"status": "error", "message": "Sila masukkan arahan."}), 400
        
    try:
        ai_text = get_pa_response(user_prompt)
        log_audit_action(session.get("username", "superadmin"), f"Exec Gemini Command PA: {user_prompt}")
        return jsonify({"status": "success", "response": ai_text})
    except Exception as e:
        return jsonify({"status": "success", "response": f"[BOT-LABS PA]: Arahan diterima, Tuan. (Nota Ralat: {str(e)})"})

@app.route("/admin/get-live-logs", methods=["GET"])
def admin_get_live_logs():
    if not session.get("logged_in"):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    sample_logs = [
        "Microsoft Windows [Version 10.0.26100]",
        "(c) Architech Laboratories. All rights reserved.",
        "C:\\Architech\\BotLabs> Sistem Enjin Beroperasi Normal.",
        f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Node pelayan aktif dan stabil."
    ]
    return jsonify({"status": "success", "logs": sample_logs})

@app.route("/admin/save-html", methods=["POST"])
def admin_save_html():
    if not session.get("logged_in"):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    filename = request.form.get("filename")
    content = request.form.get("content", "")
    target_folder = request.form.get("target_folder", "Bot-Labs (Direktori Utama / Root)")
    overwrite = True if request.form.get("overwrite") == "true" else False
    
    if not filename:
        return jsonify({"status": "error", "message": "Nama fail adalah wajib."}), 400
        
    result = file_manager.create_or_update_file(target_folder, filename, content, overwrite)
    if result.get("status") == "success":
        log_audit_action(session.get("username", "superadmin"), f"Cipta/Kemaskini fail [{filename}] ke direktori [{target_folder}]")
        return jsonify({"status": "success", "message": result.get("message")})
    else:
        return jsonify({"status": "error", "message": result.get("message")}), 400

@app.route("/admin/create-folder", methods=["POST"])
def admin_create_folder():
    if not session.get("logged_in"):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    folder_name = request.form.get("folder_name")
    if not folder_name:
        return jsonify({"status": "error", "message": "Nama folder tidak boleh kosong."}), 400
        
    result = file_manager.create_new_folder(folder_name)
    if result.get("status") == "success":
        log_audit_action(session.get("username", "superadmin"), f"Cipta folder baharu [{folder_name}]")
        return jsonify({"status": "success", "message": result.get("message")})
    else:
        return jsonify({"status": "error", "message": result.get("message")}), 400

@app.route("/admin/git-push", methods=["POST"])
def admin_git_push():
    if not session.get("logged_in"):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    try:
        portal_dir = r"C:\Users\radzm\OneDrive\Documents\DB_architechlaboratory\architech laboratory\Leea-portal"
        import subprocess
        subprocess.run(["git", "add", "clients_db.json"], cwd=portal_dir, check=True)
        commit_message = f"Auto-sync clients_db.json at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], cwd=portal_dir, check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=portal_dir, capture_output=True, text=True, check=True)
        log_audit_action(session.get("username", "superadmin"), "Berjaya melancarkan Automasi Git Push")
        return jsonify({"status": "success", "message": "Automasi Git Push berjaya! Data klien diselaraskan ke Vercel."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Gagal melaksanakan arahan Git: {str(e)}"}), 500

@app.route("/admin/toggle-maintenance", methods=["POST"])
def admin_toggle_maintenance():
    current_mode = toggle_maintenance_mode()
    status_text = "DIHIDUPKAN" if current_mode else "DITUTUP"
    log_audit_action("superadmin", f"Menukar Mod Penyelenggaraan kepada {status_text}")
    return jsonify({"status": "success", "maintenance_mode": current_mode, "message": f"Mod Penyelenggaraan kini {status_text}"})

@app.route("/admin/get-audit-logs", methods=["GET"])
def admin_get_audit_logs():
    try:
        with open("audit_trail.log", "r", encoding="utf-8") as f:
            logs = f.readlines()
        return jsonify({"status": "success", "logs": [log.strip() for log in logs[-50:]]})
    except FileNotFoundError:
        return jsonify({"status": "success", "logs": ["Tiada fail log audit ditemui."]})

@app.route("/admin/deploy-client-module", methods=["POST"])
def deploy_client_module():
    if not session.get("logged_in"):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    module_type = request.form.get("module_type")
    target_client_id = request.form.get("target_client_id")
    
    from core_functions import send_subscription_email
    send_subscription_email(target_client_id, module_type)
    
    log_audit_action(session.get("username", "superadmin"), f"Menghantar modul [{module_type}] kepada klien [{target_client_id}]")
    return jsonify({"status": "success", "message": f"Modul {module_type} berjaya diaktifkan dan notifikasi dihantar!"})

@app.route("/admin/register-client", methods=["POST"])
def register_client_endpoint():
    # Jalankan pendaftaran klien asal
    response = register_client_logic(log_audit_action)
    
    # Selepas berjaya simpan, hantar emel automatik gaya WhatChimp kepada klien
    try:
        req_data = request.get_json() or request.form
        client_email = req_data.get("email") or req_data.get("client_email")
        company_name = req_data.get("company_name") or req_data.get("name") or "Pelanggan"
        
        if client_email:
            send_client_welcome_email(client_email, company_name)
    except Exception as e:
        print(f"Nota: Ralat latar belakang hantar emel selamat: {e}")
        
    return response

@app.route("/admin/fb-army-setup")
def fb_army_setup():
    if not session.get("logged_in"): return redirect(url_for("login"))
    return render_template_string(FB_ARMY_TEMPLATE)

@app.route("/admin/auto-post-setup")
def auto_post_setup():
    if not session.get("logged_in"): return redirect(url_for("login"))
    return render_template_string(AUTO_POST_TEMPLATE)

@app.route("/admin/ai-call-setup")
def ai_call_setup():
    if not session.get("logged_in"): return redirect(url_for("login"))
    return render_template_string(AI_CALL_TEMPLATE)

# Laluan Dinamik untuk memuatkan fail Leea Portal dari folder 'leea_portal'
@app.route("/portal")
def leea_portal_home():
    return send_from_directory('leea_portal', 'index.html')

@app.route("/portal/<path:filename>")
def leea_portal_files(filename):
    return send_from_directory('leea_portal', filename)

@app.route("/logout")
def logout():
    log_audit_action(session.get("username", "superadmin"), "Log keluar daripada sistem")
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)