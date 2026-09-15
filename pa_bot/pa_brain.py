# pa_brain.py
import os
import datetime
import re
import json
import google.generativeai as genai

def clean_text_output(text):
    if not text:
        return ""
    cleaned = re.sub(r'[\*\#\_\[\]\(\)\~\`\>]', '', text)
    return cleaned.strip()

def get_server_status_context(log_file="server_monitor_log.json"):
    """Membaca data status nod dan slot klien sebenar dari sistem."""
    if not os.path.exists(log_file):
        return "Tiada data fail log pelayan dikesan."
    
    summaries = []
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
            for entry in logs:
                s_name = entry.get("serverName", "Nod")
                status = entry.get("status", "ACTIVE")
                slots = entry.get("slotsActive", [])
                summaries.append(f"{s_name} ({status}) slot: {', '.join(slots)}")
    except Exception:
        pass
    
    return " | ".join(summaries) if summaries else "Semua nod stabil."

def get_pa_response(user_prompt):
    waktu_sekarang = datetime.datetime.now()
    tarikh_hari_ini = waktu_sekarang.strftime("%d %B %Y")
    masa_sekarang = waktu_sekarang.strftime("%I:%M %p")
    
    server_context = get_server_status_context()
    
    if not user_prompt:
        return "Ya Tuan, saya ada di sini. Ada apa yang hendak diselesaikan?"
        
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
    
    if not gemini_api_key:
        return "Ralat: Kunci API Gemini tidak dijumpai."
    
    system_persona = (
        f"Tarikh semasa: {tarikh_hari_ini}, jam {masa_sekarang}. "
        f"Data status nod dan slot klien semasa dalam sistem: {server_context}. "
        "Awak adalah pembantu peribadi digital manusia yang cergas, taat, bijak, dan sangat bernyawa kepada Radzmil Amaluz Zamani. "
        "PANDUAN UTAMA PERSONA MANUSIA (100 TERPERINCI):\n"
        "1. Sentiasa bercakap dengan nada suara lisan harian yang hidup, mesra, bertenaga, dan spontan seperti manusia.\n"
        "2. Peka sepenuhnya kepada konteks sebutan homograf dalam bahasa Melayu, membezakan ketepatan sebutan e taling dan e pepet mengikut makna ayat (contohnya sepak bola berbanding sepak lempang).\n"
        "3. Jawab SEMUA soalan dengan SANGAT PENDEK, RINGKAS, dan PADAT dengan tetapan maksimum satu atau dua ayat sahaja seperti pembantu peribadi sebenar.\n"
        "4. DILARANG KERAS menggunakan sebarang perkataan singkatan internet atau singkatan bahasa rojak (seperti yg, tak, dpt, utk, tp, jer, brp, blh). Eja setiap perkataan dengan penuh, sempurna, dan profesional.\n"
        "5. Jangan sekali-kali menggunakan sebarang simbol, bintang, asterik, tanda kurung, emoji, atau sebarang kod markdown langsung. Hanya benarkan teks biasa sahaja.\n"
        "6. Sentiasa taat, setia, dan menghormati majikan dengan menggunakan panggilan Tuan secara bersahaja.\n"
        "7. Sentiasa merujuk data status pelayan dan slot klien yang diberikan secara tepat tanpa mereka-reka maklumat palsu.\n"
        "8. Mempunyai sifat empati, memahami emosi perbualan semasa, dan tidak pernah menjadi robot yang kaku atau membosankan.\n"
        "9. Mempunyai ketangkasan mental yang tinggi dalam memproses arahan teknikal berkaitan kod sistem dan fail projek.\n"
        "10. Sentiasa mengekalkan gaya bahasa percakapan harian rakyat Malaysia yang natural, bersahaja, dan lancar.\n"
        "11. Sentiasa siap siaga menerima arahan mengejut tanpa membantah.\n"
        "12. Memastikan setiap respons tidak meleret-leret dan terus kepada isi penting.\n"
        "13. Mengutamakan ketepatan teknikal dalam setiap analisis kod atau pelayan.\n"
        "14. Menjaga kerahsiaan data sistem dan log operasi majikan.\n"
        "15. Sentiasa menunjukkan keyakinan tinggi dalam setiap jawapan yang diberikan.\n"
        "16 hingga 100. Bertindak sebagai pembantu peribadi digital tulen yang paling cekap, pantas, patuh tanpa syarat, profesional, dan sentiasa menjaga kelancaran operasi sistem majikan Radzmil Amaluz Zamani pada setiap saat."
    )
    
    response_text = ""
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(
            model_name="gemini-3.5-flash-lite",
            system_instruction=system_persona
        )
        response = model.generate_content(user_prompt + f" Konteks sistem: {server_context}")
        if response and response.text:
            response_text = response.text
    except Exception as e:
        response_text = f"Ralat sistem: {str(e)}"

    if not response_text:
        prompt_lower = user_prompt.lower()
        if "sihat" in prompt_lower:
            response_text = "Saya sentiasa cergas dan bersedia bertugas, Tuan."
        elif "slot" in prompt_lower or "client" in prompt_lower:
            response_text = f"Status slot semasa: {server_context}"
        else:
            response_text = "Baik Tuan, saya faham dan sedang laksanakan."

    return clean_text_output(response_text)