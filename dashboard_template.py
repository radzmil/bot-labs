# Modul Templat HTML untuk Dashboard Bot-Labs
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Lab - A.R.C.H.I.T.E.C.H Command Center</title>
    <style>
        :root {
            --bg-main: #030712;
            --bg-card: #0b1329;
            --border-color: #1e3a8a;
            --accent: #00f0ff;
            --accent-glow: rgba(0, 240, 255, 0.3);
            --text-main: #e0f2fe;
            --text-muted: #60a5fa;
            --success: #10b981;
            --danger: #ef4444;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: var(--bg-main); color: var(--text-main); margin: 0; padding: 0; }
        
        body::before {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.04));
            z-index: 99;
            background-size: 100% 4px, 6px 100%;
            pointer-events: none;
        }

        header { background: var(--bg-card); border-bottom: 1px solid var(--border-color); padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 0 15px rgba(0, 240, 255, 0.1); }
        .brand { font-weight: 700; font-size: 15px; color: var(--accent); letter-spacing: 1.5px; text-shadow: 0 0 8px var(--accent-glow); }
        
        .header-simulator { background: #020617; border: 1px solid var(--border-color); border-radius: 6px; padding: 4px 12px; font-family: monospace; font-size: 10px; color: #10b981; display: flex; align-items: center; gap: 8px; box-shadow: inset 0 0 8px rgba(0,240,255,0.1); }
        .sim-dot { width: 6px; height: 6px; border-radius: 50%; background-color: #10b981; animation: blink-green 0.8s infinite alternate; }

        .header-right { display: flex; align-items: center; gap: 15px; }
        .admin-btn { background: rgba(0, 240, 255, 0.1); border: 1px solid var(--accent); color: var(--accent); padding: 6px 14px; border-radius: 6px; font-size: 11px; text-decoration: none; font-weight: 600; transition: background 0.2s; letter-spacing: 0.5px; }
        .admin-btn:hover { background: rgba(0, 240, 255, 0.3); }
        .logout-btn { background: rgba(239, 68, 68, 0.1); border: 1px solid var(--danger); color: #f87171; padding: 6px 14px; border-radius: 6px; font-size: 11px; text-decoration: none; font-weight: 600; transition: background 0.2s; letter-spacing: 0.5px; }
        .logout-btn:hover { background: rgba(239, 68, 68, 0.3); }
        
        .status-bar { background: rgba(0, 240, 255, 0.05); border-bottom: 1px solid var(--border-color); padding: 8px 40px; font-size: 11px; display: flex; justify-content: space-between; color: var(--text-muted); letter-spacing: 0.5px; }
        .status-pill { color: #34d399; font-weight: bold; }

        .main-container { max-width: 1900px; margin: 25px auto; padding: 0 20px; display: grid; grid-template-columns: 460px 1fr; gap: 30px; }
        @media(max-width: 1200px) { .main-container { grid-template-columns: 1fr; } }
        
        .card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 25px; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
        h2 { font-size: 15px; margin-top: 0; margin-bottom: 20px; color: var(--accent); border-bottom: 1px solid var(--border-color); padding-bottom: 10px; letter-spacing: 1px; display: flex; justify-content: space-between; align-items: center; }
        
        .form-group { margin-bottom: 14px; }
        label { display: block; margin-bottom: 5px; color: var(--text-muted); font-size: 11px; font-weight: 500; letter-spacing: 0.5px; }
        input[type="text"], textarea, input[type="file"], input[type="password"], select { width: 100%; padding: 9px 12px; border: 1px solid var(--border-color); background: #020617; color: var(--accent); border-radius: 6px; box-sizing: border-box; font-size: 12px; font-family: inherit; }
        input[type="text"]:focus, textarea:focus, input[type="password"]:focus, select:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 8px var(--accent-glow); }
        textarea { resize: vertical; height: 75px; }
        
        button { width: 100%; background: transparent; border: 1px solid var(--accent); color: var(--accent); padding: 12px; font-size: 13px; font-weight: 700; border-radius: 6px; cursor: pointer; margin-top: 10px; transition: all 0.3s; letter-spacing: 1px; }
        button:hover { background: var(--accent); color: #030712; box-shadow: 0 0 15px var(--accent); }
        
        .alert { background: rgba(16, 185, 129, 0.15); border: 1px solid var(--success); color: #6ee7b7; padding: 12px; border-radius: 6px; margin-bottom: 20px; font-size: 12px; text-align: center; letter-spacing: 0.5px; }
        .restricted-box { background: rgba(239, 68, 68, 0.1); border: 1px dashed var(--danger); padding: 15px; border-radius: 8px; text-align: center; color: #f87171; font-size: 11px; letter-spacing: 0.5px; margin-bottom: 20px; }

        .hacking-terminal { background: #020617; border: 1px solid var(--accent); border-radius: 8px; padding: 12px; font-family: monospace; font-size: 10px; color: #10b981; height: 110px; overflow-y: hidden; margin-top: 15px; position: relative; box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.1); }
        .cmd-terminal { background: #000000; border: 1px solid var(--accent); border-radius: 8px; padding: 14px; font-family: 'Courier New', Courier, monospace; font-size: 11px; color: #38bdf8; height: 180px; overflow-y: auto; margin-top: 20px; position: relative; box-shadow: inset 0 0 15px rgba(0,0,0,0.8); white-space: pre-wrap; word-break: break-all; }
        
        .table-container { width: 100%; }
        .server-table { width: 100%; border-collapse: collapse; font-size: 11px; font-family: inherit; }
        .server-table th { background: #020617; color: var(--accent); border-bottom: 2px solid var(--border-color); text-align: left; padding: 8px 10px; letter-spacing: 1px; position: sticky; top: 0; z-index: 10; }
        .server-table th.center, .server-table td.center { text-align: center; }
        .server-table td { padding: 6px 10px; border-bottom: 1px solid #1e293b; color: #94a3b8; vertical-align: middle; }
        .server-table tr:hover { background: rgba(0, 240, 255, 0.03); }
        .srv-id { font-weight: bold; color: var(--accent); white-space: nowrap; }
        
        .bell-icon-link { color: #38bdf8; text-decoration: none; font-size: 15px; display: inline-flex; align-items: center; justify-content: center; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 6px; width: 30px; height: 30px; transition: all 0.2s; }
        .bell-icon-link:hover { background: rgba(56, 189, 248, 0.3); color: #fff; box-shadow: 0 0 8px rgba(56, 189, 248, 0.5); }

        .capacity-badge { background: rgba(16, 185, 129, 0.1); border: 1px solid var(--success); color: #34d399; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: bold; white-space: nowrap; display: inline-block; }
        
        .slots-grid { display: inline-flex; gap: 6px; justify-content: center; align-items: center; }
        .client-slot-box { background: #020617; border: 1px solid #1e3a8a; border-radius: 6px; padding: 6px 8px; font-size: 10px; text-align: center; min-width: 85px; display: flex; flex-direction: column; gap: 2px; transition: all 0.3s ease; position: relative; text-decoration: none; color: var(--text-muted); }
        .client-slot-box:hover { border-color: var(--accent); background: rgba(0, 240, 255, 0.1); box-shadow: 0 0 12px var(--accent-glow); }
        
        .client-slot-box.status-active { border-color: #10b981; background: rgba(16, 185, 129, 0.15); box-shadow: 0 0 8px rgba(16, 185, 129, 0.3); }
        .client-slot-box.status-active .slot-led { background-color: #10b981; box-shadow: 0 0 6px #10b981; animation: blink-green 0.8s infinite alternate; }

        .client-slot-box.status-crash { border-color: #ef4444; background: rgba(239, 68, 68, 0.25); box-shadow: 0 0 12px rgba(239, 68, 68, 0.6); }
        .client-slot-box.status-crash .slot-led { background-color: #ef4444; box-shadow: 0 0 8px #ef4444; animation: blink-red 0.3s infinite alternate; }

        .slot-led { width: 6px; height: 6px; border-radius: 50%; position: absolute; top: 6px; right: 6px; background-color: #334155; }
        .slot-title { font-weight: bold; color: var(--accent); font-size: 9px; border-bottom: 1px solid #1e293b; padding-bottom: 2px; margin-bottom: 2px; }
        .client-id-val { font-size: 9px; color: #38bdf8; font-weight: bold; font-family: monospace; }
        .memory-tag { font-size: 8px; padding: 1px 4px; border-radius: 3px; font-weight: bold; margin-top: 2px; display: inline-block; }
        .memory-v1 { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid #38bdf8; }
        .memory-v2 { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }

        .led-indicator { display: inline-flex; align-items: center; gap: 6px; font-size: 10px; font-weight: bold; }
        .led-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
        .led-green { background-color: #10b981; box-shadow: 0 0 8px #10b981; animation: blink-green 1s infinite alternate; }
        .led-red { background-color: #ef4444; box-shadow: 0 0 8px #ef4444; animation: blink-red 0.5s infinite alternate; }

        @keyframes blink-green {
            0% { opacity: 0.3; box-shadow: 0 0 2px #10b981; }
            100% { opacity: 1; box-shadow: 0 0 10px #10b981; }
        }
        @keyframes blink-red {
            0% { opacity: 0.2; box-shadow: 0 0 2px #ef4444; }
            100% { opacity: 1; box-shadow: 0 0 12px #ef4444; }
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">Bot Labs - A.R.C.H.I.T.E.C.H PROTOCOL [SECURE ACCESS]</div>
        <div class="header-right">
            <div class="header-simulator">
                <span class="sim-dot"></span>
                <span id="headerSimText">CYBER-TRACE: ROUTING ENCLAVE...</span>
            </div>
            <div style="font-size: 11px; color: #34d399; background: rgba(16,185,129,0.1); border: 1px solid #10b981; padding: 5px 10px; border-radius: 20px; letter-spacing: 0.5px;">
                ROLE: {{ role_name }}
            </div>
            <a href="/portal/index.html" target="_blank" class="admin-btn" style="background: rgba(56, 189, 248, 0.1); border-color: #38bdf8; color: #38bdf8;">LEEA PORTAL</a>
            <a href="/admin-panel" class="admin-btn">ADMIN PANEL</a>
            <a href="/logout" class="logout-btn">LOG KELUAR</a>
        </div>
    </header>

    <div class="status-bar">
        <div>SECURITY NODE: <span class="status-pill" style="color: #34d399;">SECURE (PASSWORD PROTECTED)</span></div>
        <div>FIREWALL: <span class="status-pill" style="color: #34d399;">ACTIVE</span></div>
        <div>LOGGED USER: <span class="status-pill">{{ current_user }} (Pass ID: {{ current_pass_id }})</span></div>
    </div>

    <div class="main-container">
        <!-- Borang Kiri -->
        <div class="card">
            
            <!-- KOTAK ANALYSIS PA-BOT DI ATAS SEKALI -->
            <div style="background: rgba(0, 240, 255, 0.02); border: 1px solid var(--accent); border-radius: 8px; padding: 18px; margin-bottom: 25px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <label style="color: var(--accent); font-weight: bold; font-size: 13px; margin: 0; letter-spacing: 0.5px;">
                        ANALYSIS PA-BOT (ADVANCED)
                    </label>
                    <button type="button" id="voiceToggleBtn" onclick="toggleVoiceOutput()" title="Tukar status Suara AI (Text-to-Speech)" style="width: auto; margin: 0; padding: 4px 10px; font-size: 10px; background: rgba(16,185,129,0.2); border: 1px solid #10b981; color: #34d399; border-radius: 4px; cursor: pointer; font-weight: bold;">
                        SUARA AI: ON
                    </button>
                </div>
                <span style="color: var(--text-muted); font-size: 11px; display: block; margin-bottom: 12px;">Interaksi analisis & kod bersama PA-Bot. Salin ralat sistem dari kotak bawah untuk dibantu AI.</span>
                
                <div id="geminiChatBox" style="background: #000000; border: 1px solid var(--accent); border-radius: 6px; padding: 12px; font-family: monospace; font-size: 12px; color: #ffffff; height: 280px; overflow-y: auto; margin-bottom: 12px; display: flex; flex-direction: column; gap: 10px; line-height: 1.4;">
                    <div style="color: #00f0ff; font-weight: bold;">[BOT-LABS PA]: Hai Boss Radzmil! Kotak analisis bersedia. Tanyakan sebarang ralat atau isu bug sistem di sini.</div>
                </div>

                <div style="display: flex; gap: 8px; align-items: center; margin-top: 10px; padding: 0 4px 4px 4px;">
                    <input type="text" id="geminiInputText" placeholder="Taip arahan atau paste ralat sistem di sini..." style="flex-grow: 1; padding: 10px; font-size: 12px; background: #020617; border: 1px solid var(--accent); color: #ffffff; border-radius: 4px; margin: 0;" onkeypress="if(event.key === 'Enter') { sendGeminiPromptVanilla(); event.preventDefault(); }">
                    
                    <button type="button" id="micBtn" onclick="toggleSpeechRecognition()" title="Cakap dengan Bot (Voice Input)" style="width: auto; padding: 10px 12px; margin: 0; background: rgba(245,158,11,0.2); border: 1px solid #f59e0b; color: #f59e0b; font-weight: bold; border-radius: 4px; font-size: 13px; cursor: pointer;">
                        🎤
                    </button>

                    <button type="button" onclick="sendGeminiPromptVanilla()" style="width: auto; padding: 10px 14px; margin: 0; background: var(--accent); color: #030712; font-weight: bold; border-radius: 4px; font-size: 12px; border: none; cursor: pointer;">Hantar</button>
                </div>
            </div>

            <h2>BOT FACTORY ENGINE</h2>
            
            {% if success_msg %}
                <div class="alert">{{ success_msg }}</div>
            {% endif %}

            {% if error_msg %}
                <div class="restricted-box" style="color: #f87171; border-color: #ef4444;">{{ error_msg }}</div>
            {% endif %}

            {% if otp_result %}
                <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; padding: 12px; border-radius: 6px; margin-bottom: 15px; font-size: 11px; color: #38bdf8;">
                    <strong>📥 HASIL OTP CHECKER:</strong><br>{{ otp_result }}
                </div>
            {% endif %}

            <!-- Modul Upgrade Bot V1 / V2 -->
            <div style="background: rgba(245, 158, 11, 0.03); border: 1px dashed #f59e0b; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
                <label style="color: #f59e0b; font-weight: bold; margin-bottom: 10px; display: block;">⚡ UPGRADE BOT MODEL (V1 -> V2)</label>
                <form method="POST">
                    <input type="hidden" name="action_type" value="upgrade_bot">
                    <div class="form-group" style="margin-bottom: 8px;">
                        <label>Select Client ID:</label>
                        <select name="upgrade_client_id" style="width: 100%; padding: 9px; border: 1px solid var(--border-color); background: #020617; color: #f59e0b; border-radius: 6px; font-family: monospace;">
                            {% for n in range(1, 201) %}
                                {% set cid = "CLI-%04d" | format(1000 + n) %}
                                <option value="{{ cid }}">{{ cid }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group" style="margin-bottom: 10px;">
                        <label>Target Model:</label>
                        <select name="target_model" style="width: 100%; padding: 9px; border: 1px solid var(--border-color); background: #020617; color: #f59e0b; border-radius: 6px;">
                            <option value="V1">Model Bot V1 (300 MB)</option>
                            <option value="V2" selected>Model Bot V2 (600 MB)</option>
                        </select>
                    </div>
                    <button type="submit" style="margin-top: 0; padding: 8px; font-size: 11px; border-color: #f59e0b; color: #f59e0b;">PROSES UPGRADE BOT</button>
                </form>
            </div>

            <!-- Modul Key-In Server Mail (Email) -->
            <div style="background: rgba(56, 189, 248, 0.03); border: 1px dashed #38bdf8; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
                <label style="color: #38bdf8; font-weight: bold; margin-bottom: 10px; display: block;">🔔 KEY-IN SERVER MAIL (GMAIL & OTP)</label>
                <form method="POST">
                    <input type="hidden" name="action_type" value="update_server_email">
                    <div class="form-group" style="margin-bottom: 8px;">
                        <label>Select Server:</label>
                        <select name="target_server_id" style="width: 100%; padding: 9px; border: 1px solid var(--border-color); background: #020617; color: #38bdf8; border-radius: 6px; font-family: monospace;">
                            {% for s in range(1, 51) %}
                                <option value="{{ s }}">SRV #{{ s }} ({{ server_emails.get(s, "railway.acc" ~ s ~ "@gmail.com") }})</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group" style="margin-bottom: 8px;">
                        <label>Gmail Address:</label>
                        <input type="text" name="server_email" placeholder="radzmil@gmail.com" required>
                    </div>
                    <div class="form-group" style="margin-bottom: 10px;">
                        <label>Gmail App Password (16 chars):</label>
                        <input type="password" name="app_password" placeholder="bsya wjgy urrp ipuq">
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button type="submit" style="margin-top: 0; padding: 8px; font-size: 11px; border-color: #38bdf8; color: #38bdf8;">SIMPAN EMAIL</button>
                        <button type="submit" name="check_otp" value="1" style="margin-top: 0; padding: 8px; font-size: 11px; background: #38bdf8; color: #030712;">SEMAK OTP INBOX</button>
                    </div>
                </form>
            </div>

            <!-- Modul Key-In URL Railway untuk Client ID -->
            <div style="background: rgba(0, 240, 255, 0.03); border: 1px dashed var(--accent); border-radius: 8px; padding: 15px; margin-bottom: 20px;">
                <label style="color: var(--accent); font-weight: bold; margin-bottom: 10px; display: block;">🔗 KEY-IN CLIENT RAILWAY URL</label>
                <form method="POST">
                    <input type="hidden" name="action_type" value="update_client_url">
                    <div class="form-group" style="margin-bottom: 8px;">
                        <label>Select Client ID:</label>
                        <select name="target_client_id" style="width: 100%; padding: 9px; border: 1px solid var(--border-color); background: #020617; color: var(--accent); border-radius: 6px; font-family: monospace;">
                            {% for n in range(1, 201) %}
                                {% set cid = "CLI-%04d" | format(1000 + n) %}
                                <option value="{{ cid }}">{{ cid }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group" style="margin-bottom: 8px;">
                        <label>Railway Domain URL:</label>
                        <input type="text" name="client_url" placeholder="web-production-07b92.up.railway.app" required>
                    </div>
                    <div class="form-group" style="margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                        <input type="checkbox" id="is_crash" name="is_crash" style="width: auto;">
                        <label for="is_crash" style="color: #f87171; margin-bottom: 0; cursor: pointer;">🚨 Simulasi Crash (Lampu Merah Amaran)</label>
                    </div>
                    <button type="submit" style="margin-top: 0; padding: 8px; font-size: 11px;">UPDATE CLIENT URL</button>
                </form>
            </div>

            <!-- Borang Cipta Robot (Bot Factory Engine) -->
            <form method="POST" enctype="multipart/form-data">
                <input type="hidden" name="action_type" value="deploy_bot">
                <div class="form-group">
                    <label>Bot / Project Name:</label>
                    <input type="text" name="bot_name" placeholder="Example: SalesBot_Alpha" required>
                </div>
                <div class="form-group">
                    <label>Pilihan Model Bot (Memory Allocation):</label>
                    <select name="bot_model" style="width: 100%; padding: 9px; border: 1px solid var(--border-color); background: #020617; color: var(--accent); border-radius: 6px;">
                        <option value="V1">Model Bot V1 (Default - 300MB Memory)</option>
                        <option value="V2">Model Bot V2 (Upgrade - 600MB Memory)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Company / Entity Name:</label>
                    <input type="text" name="company_name" value="Architech Laboratory" required>
                </div>
                <div class="form-group">
                    <label>Payment Info / Bank SOP:</label>
                    <input type="text" name="bank_info" value="Maybank - 5621XXXX - Architech Lab" required>
                </div>
                <div class="form-group">
                    <label>Payment Gateway Link:</label>
                    <input type="text" name="payment_gateway_link" placeholder="https://toyyibpay.com/...">
                </div>
                <div class="form-group">
                    <label>Upload QR Code Image (Auto-Generate Code):</label>
                    <input type="file" name="qr_code_image" accept="image/*">
                </div>
                <div class="form-group">
                    <label>Admin WhatsApp Number (group_admin_number):</label>
                    <input type="text" name="group_admin_number" placeholder="6019XXXXXXXX">
                </div>
                <div class="form-group">
                    <label>WhatsApp Access Token:</label>
                    <input type="text" name="whatsapp_token" placeholder="EAAP..." required>
                </div>
                <div class="form-group">
                    <label>WhatsApp Phone ID:</label>
                    <input type="text" name="phone_id" placeholder="1000..." required>
                </div>
                <div class="form-group">
                    <label>Verify Token (Webhook):</label>
                    <input type="text" name="verify_token" value="verifysini123" required>
                </div>
                <div class="form-group">
                    <label>Gemini API Key:</label>
                    <input type="text" name="gemini_api_key" placeholder="AIza..." required>
                </div>
                <div class="form-group">
                    <label>Railway API Token (Auto-Deploy):</label>
                    <input type="text" name="railway_token" placeholder="Leave blank for local storage only">
                </div>
                
                <div class="form-group">
                    <label>Bot Brain Prompt / Data:</label>
                    <textarea name="bot_brain_prompt" placeholder="Sifat, personaliti, dan skrip minda bot..."></textarea>
                </div>
                <div class="form-group">
                    <label>Bot Engine Config:</label>
                    <textarea name="bot_engine_config" placeholder="Tetapan asas gelagat enjin bot..."></textarea>
                </div>
                <div class="form-group">
                    <label>Company Profile Prompt:</label>
                    <textarea name="company_profile_prompt" placeholder="Latar belakang syarikat untuk rujukan bot..."></textarea>
                </div>
                <div class="form-group">
                    <label>SOP Payment Details / Rules:</label>
                    <textarea name="sop_payment_prompt" placeholder="Tatacara sahkan bayaran, resit, dan arahan transfer..."></textarea>
                </div>

                <button type="submit">EXECUTE & DEPLOY BOT</button>
            </form>

            <!-- MODUL PENGURUSAN FAIL HTML & FOLDER DINAMIK -->
            <div class="card" style="margin-top: 20px; background: rgba(56, 189, 248, 0.02);">
                <h2>
                    PENGURUSAN FAIL HTML (EDITOR)
                    <span class="led-indicator" style="color: #38bdf8;"><span class="led-dot" style="background: #38bdf8; box-shadow: 0 0 8px #38bdf8;"></span> ACTIVE</span>
                </h2>
                <p style="color: var(--text-muted); font-size: 11px; margin-bottom: 10px;">
                    Cipta fail baru atau kemaskini kod sumber HTML dengan pilihan direktori fizikal sebenar.
                </p>
                
                <div class="form-group">
                    <label>Destinasi Simpanan (Target Folder):</label>
                    <select id="htmlTargetFolder" style="width: 100%; padding: 9px; border: 1px solid var(--border-color); background: #020617; color: #38bdf8; border-radius: 6px;">
                        <option value="Bot-Labs (Direktori Utama / Root)">Bot-Labs (Direktori Utama / Root)</option>
                        <option value="pa_bot">pa_bot</option>
                        <option value="testbot">testbot</option>
                        <option value="bot_labs_backups">bot_labs_backups</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Nama Fail / Nama Folder Baru (Contoh: custom_page.html atau folder_baru):</label>
                    <input type="text" id="htmlFilename" placeholder="nama_fail.html">
                </div>

                <div style="display: flex; gap: 8px; margin-bottom: 10px;">
                    <button type="button" onclick="createNewFolderAction()" style="background: rgba(16,185,129,0.1); border-color: #10b981; color: #10b981; flex: 1; padding: 8px; font-size: 11px;">
                        CIPTA FOLDER BARU
                    </button>
                </div>

                <div class="form-group">
                    <label>Kandungan Kod Sumber HTML:</label>
                    <textarea id="htmlContent" placeholder="Masukkan kod HTML di sini..." style="height: 110px; font-family: monospace; font-size: 10px; width: 100%;"></textarea>
                </div>

                <div class="form-group" style="display: flex; align-items: center; gap: 8px;">
                    <input type="checkbox" id="htmlOverwrite" style="width: auto;" checked>
                    <label for="htmlOverwrite" style="color: #38bdf8; margin-bottom: 0; cursor: pointer;">Overwrite Mode (Tulis ganti jika fail wujud)</label>
                </div>
                
                <button type="button" onclick="saveHtmlFileAction()" style="background: rgba(56,189,248,0.1); border-color: #38bdf8; color: #38bdf8; width: 100%; padding: 10px; font-weight: bold; cursor: pointer; border-radius: 6px;">
                    SIMPAN / CIPTA FAIL HTML
                </button>

                <div style="margin-top: 15px;">
                    <button type="button" onclick="triggerGitAutomation()" style="background: rgba(16, 185, 129, 0.1); border-color: #10b981; color: #10b981; width: 100%; padding: 10px; font-weight: bold; cursor: pointer; border-radius: 6px;">
                        LANCAR AUTOMASI GIT PUSH
                    </button>
                </div>

                <div id="htmlSaveResultBox" style="display: none; background: #020617; border: 1px solid #38bdf8; border-radius: 6px; padding: 12px; margin-top: 12px; font-family: monospace; font-size: 11px; color: #38bdf8;">
                    <strong style="color: #10b981; display: block; margin-bottom: 6px;">STATUS OPERASI FAIL:</strong>
                    <p id="htmlSaveText" style="margin: 0; white-space: pre-wrap;"></p>
                </div>
            </div>

            <!-- KAD KAWALAN SISTEM & AUDIT TRAIL -->
            <div class="card" style="margin-top: 20px; background: rgba(239, 68, 68, 0.02); border-color: #ef4444;">
                <h2 style="color: #ef4444; border-color: #ef4444;">
                    KAWALAN SISTEM & AUDIT TRAIL
                </h2>
                <p style="color: var(--text-muted); font-size: 11px; margin-bottom: 12px;">
                    Urus mod penyelenggaraan keselamatan sistem dan pantau log aktiviti pentadbir secara langsung.
                </p>

                <div style="display: flex; justify-content: space-between; align-items: center; background: #020617; padding: 12px; border-radius: 6px; border: 1px solid #1e3a8a; margin-bottom: 15px;">
                    <div>
                        <strong style="color: #f87171; font-size: 12px; display: block;">Mod Penyelenggaraan (Maintenance Mode)</strong>
                        <span style="color: #64748b; font-size: 10px;">Sekat akses pengguna luar semasa kemaskini sistem.</span>
                    </div>
                    <button type="button" onclick="toggleMaintenanceMode()" id="maintBtn" style="width: auto; padding: 8px 14px; margin-top: 0; background: rgba(239,68,68,0.1); border-color: #ef4444; color: #f87171; font-size: 11px;">
                        STATUS: SEMAK...
                    </button>
                </div>

                <div class="form-group">
                    <label>Log Aktiviti Terkini (Audit Trail Log):</label>
                    <div id="auditLogBox" style="background: #000000; border: 1px solid #334155; border-radius: 6px; padding: 10px; font-family: monospace; font-size: 10px; color: #38bdf8; height: 120px; overflow-y: auto; white-space: pre-wrap;">
                        Memuatkan rekod log aktiviti...
                    </div>
                </div>
                
                <button type="button" onclick="fetchAuditLogs()" style="background: rgba(56,189,248,0.1); border-color: #38bdf8; color: #38bdf8; font-size: 11px; padding: 8px;">
                    SEGAR SEMULA LOG AKTIVITI
                </button>
            </div>

            <!-- MODUL LANJUTAN -->
            <div class="card" style="margin-top: 20px; background: rgba(0, 240, 255, 0.02); border-color: var(--accent);">
                <h2>
                    MODUL LANJUTAN: PANEL BOT & KEMPEN PEMASARAN
                    <span class="led-indicator" style="color: var(--accent);"><span class="led-dot" style="background: var(--accent); box-shadow: 0 0 8px var(--accent);"></span> ONLINE</span>
                </h2>
                <p style="color: var(--text-muted); font-size: 11px; margin-bottom: 15px;">
                    Pusat kawalan operasi lanjutan untuk pengurusan bot, automasi media sosial, kempen Ads Army, dan AI Call.
                </p>

                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px;">
                    <div style="background: #020617; border: 1px solid var(--border-color); padding: 12px; border-radius: 6px;">
                        <strong style="color: var(--accent); font-size: 11px; display: block; margin-bottom: 4px;">Panel Bot Management</strong>
                        <span style="color: #64748b; font-size: 9px; display: block; margin-bottom: 8px;">Pantau aktiviti skrip dan status sambungan bot secara langsung.</span>
                        <button type="button" onclick="alert('Panel Bot sedia aktif.')" style="margin-top: 0; padding: 6px; font-size: 10px; background: rgba(0,240,255,0.1); border-color: var(--accent); color: var(--accent);">BUKA PANEL BOT</button>
                    </div>

                    <div style="background: #020617; border: 1px solid var(--border-color); padding: 12px; border-radius: 6px;">
                        <strong style="color: #38bdf8; font-size: 11px; display: block; margin-bottom: 4px;">Automasi Post (Social)</strong>
                        <span style="color: #64748b; font-size: 9px; display: block; margin-bottom: 8px;">Jadualkan penerbitan kandungan pemasaran secara automatik.</span>
                        <a href="/admin/auto-post-setup" style="text-decoration: none; display: block;">
                            <button type="button" style="margin-top: 0; padding: 6px; font-size: 10px; background: rgba(56,189,248,0.1); border-color: #38bdf8; color: #38bdf8; width: 100%;">TETAP JADUAL POST</button>
                        </a>
                    </div>

                    <div style="background: #020617; border: 1px solid var(--border-color); padding: 12px; border-radius: 6px;">
                        <strong style="color: #f59e0b; font-size: 11px; display: block; margin-bottom: 4px;">Ads Army Campaign</strong>
                        <span style="color: #64748b; font-size: 9px; display: block; margin-bottom: 8px;">Selaras trafik iklan berbayar dan agihan prospek ke slot bot.</span>
                        <a href="/admin/fb-army-setup" style="text-decoration: none; display: block;">
                            <button type="button" style="margin-top: 0; padding: 6px; font-size: 10px; background: rgba(245,158,11,0.1); border-color: #f59e0b; color: #f59e0b; width: 100%;">BUKA SETUP FB ARMY</button>
                        </a>
                    </div>

                    <div style="background: #020617; border: 1px solid var(--border-color); padding: 12px; border-radius: 6px;">
                        <strong style="color: #10b981; font-size: 11px; display: block; margin-bottom: 4px;">AI Voice Call System</strong>
                        <span style="color: #64748b; font-size: 9px; display: block; margin-bottom: 8px;">Sistem panggilan suara pintar berasaskan sintesis AI neural.</span>
                        <a href="/admin/ai-call-setup" style="text-decoration: none; display: block;">
                            <button type="button" style="margin-top: 0; padding: 6px; font-size: 10px; background: rgba(16,185,129,0.1); border-color: #10b981; color: #10b981; width: 100%;">UJI AI VOICE CALL</button>
                        </a>
                    </div>
                </div>

                <div class="hacking-terminal" id="hackingLog">
                    [EXPLOIT] Initializing Architech Cyber-Matrix Payload...<br>
                    [AUTH] Active user session authenticated as: {{ current_user }}<br>
                    [BYPASS] Quantum firewall tunnel established successfully.<br>
                    [READY] Awaiting system command sequence...
                </div>
            </div>
        </div>

        <!-- Jadual Kanan -->
        <div class="card">
            <h2>
                RAILWAY SERVER MONITOR (50 NODES)
                <div style="display: flex; gap: 10px;">
                    <span class="led-indicator" style="color: #10b981;"><span class="led-dot led-green"></span> ACTIVE</span>
                    <span class="led-indicator" style="color: #ef4444;"><span class="led-dot led-red"></span> ERROR</span>
                </div>
            </h2>
            <div class="table-container">
                <table class="server-table">
                    <thead>
                        <tr>
                            <th>SERVER</th>
                            <th>STATUS</th>
                            <th>KAPASITI</th>
                            <th class="center">BOT ID SLOT & MEMORY MONITOR</th>
                            <th>INBOX</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for i in range(1, 51) %}
                        <tr>
                            <td class="srv-id">SRV #{{ i }}</td>
                            <td>
                                {% if i == 6 %}
                                <span class="led-indicator" style="color: #ef4444;"><span class="led-dot led-red"></span> ERROR</span>
                                {% else %}
                                <span class="led-indicator" style="color: #10b981;"><span class="led-dot led-green"></span> ACTIVE</span>
                                {% endif %}
                            </td>
                            <td>
                                <span class="capacity-badge">0/4 (0%)</span>
                            </td>
                            <td class="center">
                                <div class="slots-grid" data-server-slots="{{ i }}">
                                    {% for s in range(1, 5) %}
                                        {% set client_id = "CLI-%04d" | format(1000 + (i-1)*4 + s) %}
                                        {% set client_data = client_urls.get(client_id, {"url": "web-production-07b92.up.railway.app", "crashed": false, "model": "V1", "memory": "300MB"}) %}
                                        <a href="https://{{ client_data.url }}" target="_blank" class="client-slot-box {% if client_data.crashed %}status-crash{% else %}status-active{% endif %}" data-slot="{{ s }}" title="URL: {{ client_data.url }} | Model: {{ client_data.model }} ({{ client_data.memory }}) {% if client_data.crashed %}[CRASHED]{% endif %}">
                                            <div class="slot-title">Slot {{ s }}</div>
                                            <div class="client-id-val">{{ client_id }}</div>
                                            <span class="memory-tag {% if client_data.model == 'V2' %}memory-v2{% else %}memory-v1{% endif %}">
                                                {{ client_data.model }} • {{ client_data.memory }}
                                            </span>
                                            <span class="slot-led"></span>
                                        </a>
                                    {% endfor %}
                                </div>
                            </td>
                            <td>
                                <a href="mailto:{{ server_emails.get(i, 'railway.acc' ~ i ~ '@gmail.com') }}" class="bell-icon-link" title="Buka e-mel pendaftaran untuk SRV #{{ i }}">
                                    🔔
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            <!-- KOTAK TERMINAL SEBENAR (REAL-TIME LIVE LOGS) DI SEbelAH KANAN YANG LUAS -->
            <div style="margin-top: 25px;">
                <label style="color: var(--accent); font-weight: bold; margin-bottom: 8px; display: block; font-size: 12px; letter-spacing: 0.5px;">
                    🖥️ LIVE SYSTEM CONSOLE STREAM (REAL-TIME)
                </label>
                <div class="cmd-terminal" id="liveCmdLog">
                    Microsoft Windows [Version 10.0.26100]
                    (c) Architech Laboratories. All rights reserved.
                    C:\\Architech\\BotLabs> Memuatkan live stream log pelayan...
                </div>
            </div>
        </div>
    </div>

    <!-- Skrip JavaScript -->
    <script>
        const headerSimTexts = [
            "CYBER-TRACE: ROUTING THROUGH ENCLAVE NODES...",
            "SSL HANDSHAKE: SECURE 256-BIT ENCRYPTION...",
            "PACKET SNIFFER: ACTIVE ON 50 RAILWAY SERVERS...",
            "SUB-ROUTINE: ZERO-TRUST PROTOCOL ENFORCED."
        ];
        let hsIndex = 0;
        setInterval(() => {
            const hSim = document.getElementById("headerSimText");
            if(hSim) {
                hSim.innerText = headerSimTexts[hsIndex];
                hsIndex = (hsIndex + 1) % headerSimTexts.length;
            }
        }, 4000);

        const hackLogs = [
            "[INJECT] Injecting Meta Graph API webhook listener...",
            "[BYPASS] Overriding SSL certificate handshake on port 443...",
            "[CIPHER] Generating RSA-4096 encryption keys for bot core...",
            "[SYNC] Establishing secure tunnel with Google Sheets DB...",
            "[INFO] Intercepting packet streams across 50 Railway nodes...",
            "[SUCCESS] Memory allocation stable. Zero-trace protocol active."
        ];

        let hIndex = 0;
        setInterval(() => {
            const hackBox = document.getElementById("hackingLog");
            if(hackBox && hackLogs[hIndex]) {
                hackBox.innerHTML += "<br>" + hackLogs[hIndex];
                hackBox.scrollTop = hackBox.scrollHeight;
                hIndex = (hIndex + 1) % hackLogs.length;
            }
        }, 2500);

        async function fetchLiveServerLogs() {
            try {
                const res = await fetch('/admin/get-live-logs');
                const data = await res.json();
                if (data && data.status === 'success') {
                    const logContainer = document.getElementById('liveCmdLog');
                    if (logContainer) {
                        const latestLogs = data.logs.slice(-8);
                        logContainer.innerText = latestLogs.join('\\n');
                        logContainer.scrollTop = logContainer.scrollHeight;
                    }
                }
            } catch (err) {
                console.error('Gagal mendapatkan live log pelayan.');
            }
        }
        setInterval(fetchLiveServerLogs, 3000);

        let isVoiceEnabled = true;
        let recognition = null;

        function toggleVoiceOutput() {
            isVoiceEnabled = !isVoiceEnabled;
            const btn = document.getElementById('voiceToggleBtn');
            if (btn) {
                if (isVoiceEnabled) {
                    btn.style.background = 'rgba(16,185,129,0.2)';
                    btn.style.borderColor = '#10b981';
                    btn.style.color = '#34d399';
                    btn.innerText = 'SUARA AI: ON';
                } else {
                    btn.style.background = 'rgba(239,68,68,0.2)';
                    btn.style.borderColor = '#ef4444';
                    btn.style.color = '#f87171';
                    btn.innerText = 'SUARA AI: OFF';
                }
            }
        }

        function formatAiMessageWithCode(rawText) {
            let formatted = rawText.replace(/\\n/g, '<br>');
            return formatted;
        }

        function speakText(text) {
            if (!isVoiceEnabled || !('speechSynthesis' in window)) return;
            window.speechSynthesis.cancel();
            const cleanText = text.replace(/```[\s\S]*?```/g, "Berikut adalah kod pengaturcaraan yang diminta.").replace(/[*#_`]/g, "");
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang = 'ms-MY';
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            window.speechSynthesis.speak(utterance);
        }

        function toggleSpeechRecognition() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert('Pelayar web anda tidak menyokong pengecaman suara.');
                return;
            }
            const micBtn = document.getElementById('micBtn');
            const inputField = document.getElementById('geminiInputText');

            if (recognition) {
                recognition.stop();
                recognition = null;
                if(micBtn) micBtn.style.background = 'rgba(245,158,11,0.2)';
                return;
            }

            recognition = new SpeechRecognition();
            recognition.lang = 'ms-MY';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.onstart = function() {
                if(micBtn) micBtn.style.background = '#ef4444';
                if(inputField) inputField.placeholder = "Mendengar suara...";
            };
            recognition.onresult = function(event) {
                if(inputField) inputField.value = event.results[0][0].transcript;
                if(micBtn) micBtn.style.background = 'rgba(245,158,11,0.2)';
                if(inputField) inputField.placeholder = "Taip arahan atau minta bot buat kod...";
                sendGeminiPromptVanilla();
            };
            recognition.onerror = function() {
                if(micBtn) micBtn.style.background = 'rgba(245,158,11,0.2)';
                if(inputField) inputField.placeholder = "Taip arahan atau minta bot buat kod...";
            };
            recognition.onend = function() {
                if(micBtn) micBtn.style.background = 'rgba(245,158,11,0.2)';
                if(inputField) inputField.placeholder = "Taip arahan atau minta bot buat kod...";
            };
            recognition.start();
        }

        async function sendGeminiPromptVanilla() {
            const inputField = document.getElementById('geminiInputText');
            const chatBox = document.getElementById('geminiChatBox');
            if (!inputField || !inputField.value.trim()) return;
            
            const userMsg = inputField.value.trim();
            inputField.value = '';

            const userDiv = document.createElement('div');
            userDiv.style.color = '#38bdf8';
            userDiv.style.fontWeight = 'bold';
            userDiv.innerText = '[RADZMIL]: ' + userMsg;
            chatBox.appendChild(userDiv);

            let aiReply = "Eh Boss, sekejap ya, talian Gemini agak sibuk.";
            try {
                const response = await fetch('/admin/gemini-command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: userMsg })
                });
                const result = await response.json();
                if (result && result.status === 'success') {
                    aiReply = result.response;
                }
            } catch(err) {
                aiReply = '[BOT-LABS PA]: Ralat sambungan pelayan.';
            }

            const aiDiv = document.createElement('div');
            aiDiv.style.color = '#ffffff';
            aiDiv.style.background = 'rgba(0, 240, 255, 0.08)';
            aiDiv.style.padding = '6px 8px';
            aiDiv.style.borderRadius = '4px';
            aiDiv.innerHTML = formatAiMessageWithCode(aiReply);
            chatBox.appendChild(aiDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            speakText(aiReply);
            try {
                localStorage.setItem('radzmil_gemini_chat_history_html', chatBox.innerHTML);
            } catch(e) {}
        }

        async function saveHtmlFileAction() {
            const filename = document.getElementById('htmlFilename').value;
            const content = document.getElementById('htmlContent').value;
            const targetFolder = document.getElementById('htmlTargetFolder').value;
            const overwrite = document.getElementById('htmlOverwrite').checked;
            const resultBox = document.getElementById('htmlSaveResultBox');
            const resultText = document.getElementById('htmlSaveText');

            if (!filename.trim()) {
                alert('Sila masukkan nama fail HTML terlebih dahulu.');
                return;
            }

            resultBox.style.display = 'block';
            resultText.innerText = "Sedang memproses fail HTML ke pelayan...";

            try {
                const formData = new FormData();
                formData.append('filename', filename);
                formData.append('content', content);
                formData.append('target_folder', targetFolder);
                formData.append('overwrite', overwrite ? 'true' : 'false');

                const res = await fetch('/admin/save-html', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (data && data.status === 'success') {
                    resultText.innerText = data.message;
                } else {
                    resultText.innerText = data ? data.message : "Ralat semasa menyimpan fail.";
                }
            } catch (err) {
                resultText.innerText = "Gagal berhubung dengan API penyimpanan fail backend.";
            }
        }

        async function createNewFolderAction() {
            const folderName = document.getElementById('htmlFilename').value;
            const resultBox = document.getElementById('htmlSaveResultBox');
            const resultText = document.getElementById('htmlSaveText');

            if (!folderName.trim()) {
                alert('Sila masukkan nama folder baru pada ruangan Nama Fail.');
                return;
            }

            resultBox.style.display = 'block';
            resultText.innerText = "Sedang mencipta folder baru...";

            try {
                const formData = new FormData();
                formData.append('folder_name', folderName);

                const res = await fetch('/admin/create-folder', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (data && data.status === 'success') {
                    resultText.innerText = data.message;
                } else {
                    resultText.innerText = data ? data.message : "Ralat mencipta folder.";
                }
            } catch (err) {
                resultText.innerText = "Gagal berhubung dengan pelayan untuk mencipta folder.";
            }
        }

        async function triggerGitAutomation() {
            if (!confirm('Sahkan untuk menjalankan automasi Git Add, Commit & Push ke GitHub?')) return;
            try {
                const res = await fetch('/admin/git-push', { method: 'POST' });
                const data = await res.json();
                alert(data.message || 'Proses Git Push selesai.');
            } catch (err) {
                alert('Gagal berhubung dengan pelayan untuk arahan Git.');
            }
        }

        async function toggleMaintenanceMode() {
            try {
                const res = await fetch('/admin/toggle-maintenance', { method: 'POST' });
                const data = await res.json();
                if (data && data.status === 'success') {
                    const btn = document.getElementById('maintBtn');
                    if (data.maintenance_mode) {
                        btn.style.background = '#ef4444';
                        btn.style.color = '#fff';
                        btn.innerText = 'STATUS: ON (AKTIF)';
                    } else {
                        btn.style.background = 'rgba(239,68,68,0.1)';
                        btn.style.color = '#ef4444';
                        btn.innerText = 'STATUS: OFF (TUTUP)';
                    }
                    alert(data.message);
                    fetchAuditLogs();
                }
            } catch (err) {
                alert('Gagal mengubah status mod penyelenggaraan.');
            }
        }

        async function fetchAuditLogs() {
            try {
                const res = await fetch('/admin/get-audit-logs');
                const data = await res.json();
                if (data && data.status === 'success') {
                    const logBox = document.getElementById('auditLogBox');
                    logBox.innerText = data.logs.join('\\n');
                    logBox.scrollTop = logBox.scrollHeight;
                }
            } catch (err) {
                console.error('Gagal memuatkan log audit.');
            }
        }

        document.addEventListener("DOMContentLoaded", function() {
            fetchAuditLogs();
            fetchLiveServerLogs();
            try {
                const savedChatHistory = localStorage.getItem('radzmil_gemini_chat_history_html');
                const chatBox = document.getElementById('geminiChatBox');
                if (savedChatHistory && chatBox) {
                    chatBox.innerHTML = savedChatHistory;
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            } catch(e) {}
        });
    </script>
</body>
</html>
"""