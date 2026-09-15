# ai_call.py
from flask import render_template_string, redirect, url_for, session

def get_ai_call_page():
    """Mengembalikan paparan halaman konfigurasi AI Voice Call"""
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    AI_CALL_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AI Voice Call Setup - Bot Labs</title>
        <style>
            body { font-family: monospace; background: #030712; color: #e0f2fe; padding: 40px; }
            .card { background: #0b1329; border: 1px solid #10b981; padding: 30px; border-radius: 12px; max-width: 800px; margin: auto; box-shadow: 0 0 20px rgba(16,185,129,0.2); }
            h1 { color: #10b981; font-size: 18px; border-bottom: 1px solid #1e3a8a; padding-bottom: 10px; }
            label { display: block; margin-top: 15px; color: #60a5fa; font-size: 12px; }
            input, textarea, select { width: 100%; padding: 10px; margin-top: 5px; background: #020617; border: 1px solid #1e3a8a; color: #10b981; border-radius: 6px; box-sizing: border-box; }
            button { background: #10b981; color: #030712; border: none; padding: 12px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 20px; }
            .back-btn { background: transparent; border: 1px solid #60a5fa; color: #60a5fa; margin-left: 10px; text-decoration: none; display: inline-block; padding: 11px 20px; border-radius: 6px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>📞 AI VOICE CALL SYSTEM CONFIGURATION</h1>
            <p style="font-size: 11px; color: #94a3b8;">Tetapkan parameter sintesis suara AI neural untuk panggilan keluar dan hantar notifikasi kepada klien.</p>
            
            <form id="aiCallForm" onsubmit="submitModuleDeploy(event, 'AI Call')">
                <label>Pilih Client ID / Pelanggan Sasaran:</label>
                <select name="target_client_id" required>
                    {% for n in range(1, 201) %}
                        {% set cid = "CLI-%04d" | format(1000 + n) %}
                        <option value="{{ cid }}">{{ cid }}</option>
                    {% endfor %}
                </select>

                <label>Model Suara AI (Neural Voice Engine):</label>
                <select name="ai_voice_model">
                    <option value="gemini-audio-v1">Gemini Neural Voice - Bahasa Melayu (Standard)</option>
                    <option value="gemini-audio-v2">Gemini Neural Voice - Profesional / Korporat</option>
                </select>

                <label>Skrip Perbualan Pembantu Suara (Voice Prompt):</label>
                <textarea name="ai_call_script" rows="4" placeholder="Arahan gelagat dan skrip percakapan bot semasa membuat panggilan..."></textarea>

                <label>Nombor Telefon Sasaran (Test Target):</label>
                <input type="text" name="test_phone" placeholder="6019XXXXXXXX">

                <button type="submit">📩 HANTAR & E-MEL NOTIFIKASI KLIEN</button>
                <a href="/" class="back-btn">KEMBALI KE DASHBOARD</a>
            </form>
        </div>
        <script>
            async function submitModuleDeploy(e, modName) {
                e.preventDefault();
                const form = e.target;
                const formData = new FormData(form);
                formData.append('module_type', modName);
                
                try {
                    const res = await fetch('/admin/deploy-client-module', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await res.json();
                    alert(data.message || 'Modul berjaya dihantar!');
                } catch (err) {
                    alert('Gagal berhubung dengan pelayan.');
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(AI_CALL_TEMPLATE)