# extra_templates.py

FB_ARMY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FB Army Campaign Setup - Bot Labs</title>
    <style>
        body { font-family: monospace; background: #030712; color: #e0f2fe; padding: 40px; }
        .card { background: #0b1329; border: 1px solid #f59e0b; padding: 30px; border-radius: 12px; max-width: 800px; margin: auto; box-shadow: 0 0 20px rgba(245,158,11,0.2); }
        h1 { color: #f59e0b; font-size: 18px; border-bottom: 1px solid #1e3a8a; padding-bottom: 10px; }
        label { display: block; margin-top: 15px; color: #60a5fa; font-size: 12px; }
        input, textarea, select { width: 100%; padding: 10px; margin-top: 5px; background: #020617; border: 1px solid #1e3a8a; color: #f59e0b; border-radius: 6px; box-sizing: border-box; }
        button { background: #f59e0b; color: #030712; border: none; padding: 12px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 20px; }
        .back-btn { background: transparent; border: 1px solid #60a5fa; color: #60a5fa; margin-left: 10px; text-decoration: none; display: inline-block; padding: 11px 20px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 FB ARMY CAMPAIGN SETUP & CONFIGURATION</h1>
        <p style="font-size: 11px; color: #94a3b8;">Selaras dan uruskan kempen trafik iklan berbayar serta hantar pengesahan langganan kepada klien.</p>
        
        <form id="fbArmyForm" onsubmit="submitModuleDeploy(event, 'Ads Army')">
            <label>Pilih Client ID / Pelanggan Sasaran:</label>
            <select name="target_client_id" required>
                {% for n in range(1, 201) %}
                    {% set cid = "CLI-%04d" | format(1000 + n) %}
                    <option value="{{ cid }}">{{ cid }}</option>
                {% endfor %}
            </select>

            <label>Campaign Name / Target Produk:</label>
            <input type="text" name="fb_campaign_name" placeholder="Contoh: Kempen Leads WhatsApp V2">

            <label>Facebook Page ID / Ad Account:</label>
            <input type="text" name="fb_page_id" placeholder="1029384859102">

            <label>Meta Access Token (Graph API):</label>
            <input type="password" name="fb_access_token" placeholder="EAAB...">

            <label>Auto-Reply Script / Ad Copy Template:</label>
            <textarea name="fb_ad_script" rows="4" placeholder="Skrip sambutan automatik untuk prospek masuk dari iklan FB..."></textarea>

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

AUTO_POST_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Automasi Post Setup - Bot Labs</title>
    <style>
        body { font-family: monospace; background: #030712; color: #e0f2fe; padding: 40px; }
        .card { background: #0b1329; border: 1px solid #38bdf8; padding: 30px; border-radius: 12px; max-width: 800px; margin: auto; box-shadow: 0 0 20px rgba(56,189,248,0.2); }
        h1 { color: #38bdf8; font-size: 18px; border-bottom: 1px solid #1e3a8a; padding-bottom: 10px; }
        label { display: block; margin-top: 15px; color: #60a5fa; font-size: 12px; }
        input, textarea, select { width: 100%; padding: 10px; margin-top: 5px; background: #020617; border: 1px solid #1e3a8a; color: #38bdf8; border-radius: 6px; box-sizing: border-box; }
        button { background: #38bdf8; color: #030712; border: none; padding: 12px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 20px; }
        .back-btn { background: transparent; border: 1px solid #60a5fa; color: #60a5fa; margin-left: 10px; text-decoration: none; display: inline-block; padding: 11px 20px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📡 AUTOMATION POST (SOCIAL MEDIA SCHEDULER)</h1>
        <p style="font-size: 11px; color: #94a3b8;">Jadualkan penerbitan kandungan pemasaran secara automatik dan hantar pengesahan kepada klien.</p>
        
        <form id="autoPostForm" onsubmit="submitModuleDeploy(event, 'Automasi Post')">
            <label>Pilih Client ID / Pelanggan Sasaran:</label>
            <select name="target_client_id" required>
                {% for n in range(1, 201) %}
                    {% set cid = "CLI-%04d" | format(1000 + n) %}
                    <option value="{{ cid }}">{{ cid }}</option>
                {% endfor %}
            </select>

            <label>Pilih Platform Sasaran:</label>
            <select name="post_platform">
                <option value="facebook">Facebook Page / Group</option>
                <option value="telegram">Telegram Channel</option>
                <option value="whatsapp">WhatsApp Broadcast</option>
            </select>

            <label>Masa & Jadual Terbit (Schedule Time):</label>
            <input type="text" name="post_time" placeholder="Contoh: Setiap hari jam 09:00 AM">

            <label>Kandungan Hantaran (Post Copy / Caption):</label>
            <textarea name="post_content" rows="4" placeholder="Tulis ayat promosi atau info produk di sini..."></textarea>

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