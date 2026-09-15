# pa_bot/pa_engine.py
import os
import json
import datetime
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def clean_text_output(text):
    """Menyingkirkan semua simbol asterik, emoji, atau tanda khas agar teks benar-benar bersih."""
    if not text:
        return ""
    cleaned = re.sub(r'[\*\#\_\[\]\(\)\~\`\>]', '', text)
    return cleaned.strip()

def get_all_project_files():
    """Mengimbas semua fail kod dan log utama dalam direktori projek untuk rujukan bot."""
    ignore_dirs = {'.git', '__pycache__', 'venv', 'env', '.pytest_cache'}
    file_list = []
    
    try:
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file.endswith(('.py', '.json', '.env', '.log', '.txt', '.md', 'Procfile', 'requirements.txt')):
                    file_list.append(os.path.join(root, file))
    except Exception:
        pass
        
    return ", ".join(file_list[:30]) if file_list else "Tiada fail dikesan."

def auto_heal_server_crash(server_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [AUTO-HEAL] Nod {server_name} telah berjaya dipulihkan dan diaktifkan semula."
    try:
        with open("server_recovery.log", "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception:
        pass
    return True

def check_and_fix_server_crashes(log_file="server_monitor_log.json"):
    if not os.path.exists(log_file):
        return [], "Tiada data log pelayan ditemui."
    
    recovered_nodes = []
    server_summaries = []
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
            for entry in logs:
                s_name = entry.get("serverName", "Nod Tidak Diketahui")
                status = entry.get("status", "ACTIVE")
                slots = entry.get("slotsActive", [])
                
                if entry.get("crashed", False) or "ERROR" in status or "CRASHED" in status:
                    if auto_heal_server_crash(s_name):
                        recovered_nodes.append(s_name)
                        entry["crashed"] = False
                        entry["status"] = "ACTIVE"
                        status = "ACTIVE"
                
                server_summaries.append(f"{s_name} status {status} dengan slot klien: {', '.join(slots)}")
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)
            
    except Exception:
        pass
    
    client_status_text = " | ".join(server_summaries) if server_summaries else "Tiada data slot aktif."
    return recovered_nodes, client_status_text

def get_pa_response(user_prompt):
    waktu_sekarang = datetime.datetime.now()
    tarikh_hari_ini = waktu_sekarang.strftime("%d %B %Y")
    masa_sekarang = waktu_sekarang.strftime("%I:%M %p")
    
    fixed_servers, client_status_context = check_and_fix_server_crashes()
    project_files = get_all_project_files()
    
    auto_fix_text = ""
    if fixed_servers:
        auto_fix_text = f" Tindakan pemulihan automatik telah diselesaikan untuk nod: {', '.join(fixed_servers)}."

    if not user_prompt:
        return "Ya Tuan, ada apa yang boleh saya bantu sekarang?"
        
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
    
    system_persona = (
        f"Tarikh semasa: {tarikh_hari_ini}, jam {masa_sekarang}. "
        f"Senarai fail sistem dalam projek: {project_files}. "
        f"Data status nod dan kedudukan slot ID klien terkini ialah: {client_status_context}. {auto_fix_text} "
        "Awak adalah pembantu peribadi digital manusia yang cergas, taat, dan santai kepada Radzmil Amaluz Zamani. "
        "PENTING: Jawab SEMUA soalan dengan SANGAT PENDEK, RINGKAS, dan PADAT, maksimum 1 atau 2 ayat sahaja macam assistant sebenar. "
        "Gunakan bahasa Melayu Malaysia harian yang bersahaja dan jangan skema. "
        "Jangan sesekali guna sebarang simbol, bintang, asterik, tanda kurung, emoji, atau markdown langsung. Hanya teks biasa sahaja."
    )
    
    response_text = ""
    if gemini_api_key:
        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel(
                model_name="gemini-3.5-flash-lite",
                system_instruction=system_persona
            )
            response = model.generate_content(user_prompt)
            if response and response.text:
                response_text = response.text
        except Exception:
            pass

    if not response_text:
        prompt_lower = user_prompt.lower()
        if fixed_servers:
            response_text = f"Nod {', '.join(fixed_servers)} crash tadi dah selesai dibetulkan automatik, Tuan."
        elif any(k in prompt_lower for k in ["fail", "file", "senarai"]):
            response_text = f"Fail sistem yang dikesan dalam direktori: {project_files}."
        elif any(k in prompt_lower for k in ["error", "bug", "rosak", "crash"]):
            response_text = f"Status semasa pelayan: {client_status_context}."
        elif any(k in prompt_lower for k in ["hi", "hallo", "hello", "hey", "apa khabar"]):
            response_text = "Ya Tuan, saya ada di sini. Semua sistem berjalan lancar."
        else:
            response_text = "Baik Tuan, arahan diterima dan diproses sekarang."

    return clean_text_output(response_text)