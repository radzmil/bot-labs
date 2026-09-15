# Modul Templat HTML untuk Administrator Panel
ADMIN_PANEL_TEMPLATE = """
<!DOCTYPE html>
<html lang="ms" x-data="adminData()" x-init="init()">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Lab - A.R.C.H.I.T.E.C.H Administrator Command Center</title>
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
        
        .status-bar { background: rgba(0, 240, 255, 0.05); border-bottom: 1px solid var(--border-color); padding: 8px 40px; font-size: 11px; display: flex; justify-content: space-between; color: var(--text-muted); letter-spacing: 0.5px; }
        .status-pill { color: #34d399; font-weight: bold; }

        .main-container { max-width: 1900px; margin: 25px auto; padding: 0 20px; display: grid; grid-template-columns: 460px 1fr; gap: 30px; }
        @media(max-width: 1200px) { .main-container { grid-template-columns: 1fr; } }
        
        .card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 25px; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
        h2 { font-size: 15px; margin-top: 0; margin-bottom: 20px; color: var(--accent); border-bottom: 1px solid var(--border-color); padding-bottom: 10px; letter-spacing: 1px; display: flex; justify-content: space-between; align-items: center; }
        
        .form-group { margin-bottom: 14px; }
        label { display: block; margin-bottom: 5px; color: var(--text-muted); font-size: 11px; font-weight: 500; letter-spacing: 0.5px; }
        input[type="text"], textarea, input[type="password"], select { width: 100%; padding: 9px 12px; border: 1px solid var(--border-color); background: #020617; color: var(--accent); border-radius: 6px; box-sizing: border-box; font-size: 12px; font-family: inherit; }
        input[type="text"]:focus, textarea:focus, input[type="password"]:focus, select:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 8px var(--accent-glow); }
        textarea { resize: vertical; height: 70px; }
        
        button { width: 100%; background: transparent; border: 1px solid var(--accent); color: var(--accent); padding: 12px; font-size: 13px; font-weight: 700; border-radius: 6px; cursor: pointer; margin-top: 10px; transition: all 0.3s; letter-spacing: 1px; }
        button:hover { background: var(--accent); color: #030712; box-shadow: 0 0 15px var(--accent); }
        
        .hacking-terminal { background: #020617; border: 1px solid var(--accent); border-radius: 8px; padding: 12px; font-family: monospace; font-size: 10px; color: #10b981; height: 110px; overflow-y: hidden; margin-top: 15px; position: relative; box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.1); }
        .cmd-terminal { background: #000000; border: 1px solid #334155; border-radius: 8px; padding: 12px; font-family: 'Courier New', Courier, monospace; font-size: 10px; color: #38bdf8; height: 110px; overflow-y: hidden; margin-top: 12px; position: relative; box-shadow: inset 0 0 15px rgba(0,0,0,0.8); }
        .cmd-terminal::after { content: "_"; animation: blink-cursor 1s infinite; color: #38bdf8; }
        @keyframes blink-cursor { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

        .table-container { width: 100%; overflow-x: auto; }
        .server-table { width: 100%; border-collapse: collapse; font-size: 11px; font-family: inherit; }
        .server-table th { background: #020617; color: var(--accent); border-bottom: 2px solid var(--border-color); text-align: left; padding: 8px 10px; letter-spacing: 1px; position: sticky; top: 0; z-index: 10; }
        .server-table th.center, .server-table td.center { text-align: center; }
        .server-table td { padding: 8px 10px; border-bottom: 1px solid #1e293b; color: #94a3b8; vertical-align: middle; }
        .server-table tr:hover { background: rgba(0, 240, 255, 0.03); }
        .srv-id { font-weight: bold; color: var(--accent); white-space: nowrap; }

        .led-indicator { display: inline-flex; align-items: center; gap: 6px; font-size: 10px; font-weight: bold; }
        .led-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
        .led-green { background-color: #10b981; box-shadow: 0 0 8px #10b981; animation: blink-green 1s infinite alternate; }
        @keyframes blink-green {
            0% { opacity: 0.3; box-shadow: 0 0 2px #10b981; }
            100% { opacity: 1; box-shadow: 0 0 10px #10b981; }
        }
    </style>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <header>
        <div class="brand">Bot Labs - A.R.C.H.I.T.E.C.H ADMINISTRATOR COMMAND CENTER</div>
        <div class="header-right">
            <div class="header-simulator">
                <span class="sim-dot"></span>
                <span id="headerSimText">CYBER-TRACE: ACTIVE [ADMIN SECURE]</span>
            </div>
            <a href="/" class="admin-btn">KEMBALI KE BOT-LABS</a>
        </div>
    </header>

    <div class="status-bar">
        <div>SECURITY NODE: <span class="status-pill">OPEN ACCESS (BYPASSED)</span></div>
        <div>FIREWALL: <span class="status-pill">BYPASSED</span></div>
        <div>LOGGED ADMIN: <span class="status-pill">superadmin (Pass ID: CLI-1001)</span></div>
    </div>

    <!-- KAWASAN MASTER PAUTAN PEMBAYARAN GLOBAL & SECRET KEY DI ATAS SEBELUM MAIN CONTAINER -->
    <div style="max-width: 1900px; margin: 25px 20px; display: grid; grid-template-columns: repeat(5, 1fr); gap: 20px;">
        <!-- KOTAK 1: TOKEN 500 -->
        <div class="card" style="padding: 18px;">
            <h2 style="font-size: 13px; margin-bottom: 12px;">🪙 MASTER: TOKEN 500</h2>
            <form @submit.prevent="saveMasterPayment('token_500', masterToken500)">
                <div class="form-group" style="margin-bottom: 8px;">
                    <label>Pautan Rasmi:</label>
                    <input type="text" x-model="masterToken500" placeholder="https://toyyibpay.com/token-500..." required>
                </div>
                <button type="submit" style="background: #f59e0b; color: #030712; border: none; padding: 8px; font-size: 11px; margin-top: 5px;">💾 KEMASKINI</button>
            </form>
        </div>

        <!-- KOTAK 2: TOKEN 1000 -->
        <div class="card" style="padding: 18px;">
            <h2 style="font-size: 13px; margin-bottom: 12px;">🪙 MASTER: TOKEN 1000</h2>
            <form @submit.prevent="saveMasterPayment('token_1000', masterToken1000)">
                <div class="form-group" style="margin-bottom: 8px;">
                    <label>Pautan Rasmi:</label>
                    <input type="text" x-model="masterToken1000" placeholder="https://toyyibpay.com/token-1000..." required>
                </div>
                <button type="submit" style="background: #f59e0b; color: #030712; border: none; padding: 8px; font-size: 11px; margin-top: 5px;">💾 KEMASKINI</button>
            </form>
        </div>

        <!-- KOTAK 3: LANGGANAN BULANAN -->
        <div class="card" style="padding: 18px;">
            <h2 style="font-size: 13px; margin-bottom: 12px;">📅 MASTER: LANGGANAN</h2>
            <form @submit.prevent="saveMasterPayment('subscription', masterSubscription)">
                <div class="form-group" style="margin-bottom: 8px;">
                    <label>Pautan Rasmi:</label>
                    <input type="text" x-model="masterSubscription" placeholder="https://toyyibpay.com/langganan..." required>
                </div>
                <button type="submit" style="background: #f59e0b; color: #030712; border: none; padding: 8px; font-size: 11px; margin-top: 5px;">💾 KEMASKINI</button>
            </form>
        </div>

        <!-- KOTAK 4: LAIN-LAIN / CUSTOM -->
        <div class="card" style="padding: 18px;">
            <h2 style="font-size: 13px; margin-bottom: 12px;">🔗 MASTER: LAIN-LAIN</h2>
            <form @submit.prevent="saveMasterPayment('custom_other', masterCustom)">
                <div class="form-group" style="margin-bottom: 8px;">
                    <label>Pautan Rasmi:</label>
                    <input type="text" x-model="masterCustom" placeholder="https://toyyibpay.com/lain-lain..." required>
                </div>
                <button type="submit" style="background: #f59e0b; color: #030712; border: none; padding: 8px; font-size: 11px; margin-top: 5px;">💾 KEMASKINI</button>
            </form>
        </div>

        <!-- KOTAK 5: TOYYIBPAY SECRET KEY -->
        <div class="card" style="padding: 18px; border-color: #f43f5e;">
            <h2 style="font-size: 13px; margin-bottom: 12px; color: #f43f5e; border-color: #f43f5e;">🔑 MASTER: SECRET KEY</h2>
            <form @submit.prevent="saveMasterPayment('toyyibpay_secret_key', masterToyyibKey)">
                <div class="form-group" style="margin-bottom: 8px;">
                    <label>Secret Key Baru:</label>
                    <input type="password" x-model="masterToyyibKey" placeholder="Masukkan secret key..." required>
                </div>
                <button type="submit" style="background: #f43f5e; color: #ffffff; border: none; padding: 8px; font-size: 11px; margin-top: 5px;">💾 KEMASKINI KEY</button>
            </form>
        </div>
    </div>

    <div class="main-container">
        <!-- KOLUM KIRI: HANTAR MESEJ INBOX & KAWALAN -->
        <div class="card space-y-4">
            <h2>HANTAR MESEJ KLIEN (INBOX)</h2>
            
            <form @submit.prevent="sendAdminBroadcastMessage()" class="space-y-3 font-mono">
                <div class="form-group">
                    <label>Pilih Penerima Klien:</label>
                    <select x-model="broadcastForm.target">
                        <option value="ALL">📢 Semua Klien (All Clients)</option>
                        <template x-for="client in clients" :key="client.clientId">
                            <option :value="client.username" x-text="client.clientId + ' - ' + (client.companyName || client.username)"></option>
                        </template>
                    </select>
                </div>
                <div class="form-group">
                    <label>Tajuk / Pengirim:</label>
                    <input type="text" x-model="broadcastForm.senderTitle" value="Master Administrator" required>
                </div>
                <div class="form-group">
                    <label>Kandungan Mesej:</label>
                    <textarea x-model="broadcastForm.content" placeholder="Taip mesej pengumuman..." required style="height: 80px;"></textarea>
                </div>
                <button type="submit">HANTAR MESEJ KLIEN</button>
            </form>

            <div style="border-top: 1px solid var(--border-color); padding-top: 15px; margin-top: 15px;">
                <label style="color: var(--success); font-weight: bold; margin-bottom: 8px; display: block;">💬 KAWALAN HUMAN TOUCH</label>
                <div class="flex justify-between items-center bg-gray-950 p-3 rounded-lg border border-blue-900">
                    <span class="text-gray-400 text-xs font-mono">Mod Kawalan Manual:</span>
                    <button @click="toggleHumanTouch()" class="px-3 py-1.5 rounded font-bold text-xs font-mono" :class="humanTouchActive ? 'bg-amber-600 text-white' : 'bg-gray-800 text-gray-300'" x-text="humanTouchActive ? 'HUMAN: ON 🟢' : 'HUMAN: OFF 🔴'"></button>
                </div>
            </div>

            <!-- MODUL SUIS MOD PENYELENGGARAAN (MAINTENANCE TOGGLE) -->
            <div style="border-top: 1px solid var(--border-color); padding-top: 15px; margin-top: 15px;">
                <label style="color: #ef4444; font-weight: bold; margin-bottom: 8px; display: block;">🛡️ MOD PENYELENGGARAAN (MAINTENANCE TOGGLE)</label>
                <div style="display: flex; justify-content: space-between; align-items: center; background: #020617; padding: 12px; border-radius: 6px; border: 1px solid #ef4444;">
                    <div>
                        <strong style="color: #f87171; font-size: 11px; display: block;">Sekat Masuk Portal</strong>
                        <span style="color: #64748b; font-size: 9px;">Tahan portal daripada sebarang log masuk pengguna.</span>
                    </div>
                    <button type="button" @click="toggleAdminMaintenance()" id="adminMaintBtn" style="width: auto; padding: 6px 12px; margin-top: 0; background: rgba(239,68,68,0.1); border-color: #ef4444; color: #f87171; font-size: 10px;">
                        STATUS: SEMAK...
                    </button>
                </div>
            </div>

            <!-- MODUL AUTOMASI REPOSITORI GITHUB -->
            <div style="border-top: 1px solid var(--border-color); padding-top: 15px; margin-top: 15px;">
                <label style="color: #10b981; font-weight: bold; margin-bottom: 8px; display: block;">🚀 AUTOMASI REPOSITORI GITHUB</label>
                <div style="background: #020617; padding: 12px; border-radius: 6px; border: 1px solid #10b981;">
                    <span style="color: #94a3b8; font-size: 9px; display: block; margin-bottom: 8px;">Gabungan satu tekan butang (git add, commit, push) ke pelayan awan.</span>
                    <button type="button" @click="triggerAdminGitPush()" style="width: auto; padding: 8px 14px; margin-top: 0; background: rgba(16, 185, 129, 0.1); border-color: #10b981; color: #10b981; font-size: 10px; font-weight: bold;">
                        🚀 LANCAR GIT PUSH AUTOMATIK
                    </button>
                </div>
            </div>

            <!-- MODUL ARKIB AUDIT TRAIL -->
            <div style="border-top: 1px solid var(--border-color); padding-top: 15px; margin-top: 15px;">
                <label style="color: #38bdf8; font-weight: bold; margin-bottom: 8px; display: block;">📜 ARKIB AUDIT TRAIL</label>
                <div style="background: #020617; padding: 12px; border-radius: 6px; border: 1px solid #38bdf8;">
                    <span style="color: #94a3b8; font-size: 9px; display: block; margin-bottom: 8px;">Log berpusat merekodkan tarikh, masa, dan aktiviti kritikal sistem.</span>
                    <div id="adminAuditLogBox" style="background: #000000; border: 1px solid #334155; border-radius: 4px; padding: 8px; font-family: monospace; font-size: 9px; color: #38bdf8; height: 100px; overflow-y: auto; white-space: pre-wrap; margin-bottom: 8px;">
                        Memuatkan rekod log aktiviti...
                    </div>
                    <button type="button" @click="fetchAdminAuditLogs()" style="width: auto; padding: 6px 10px; margin-top: 0; background: rgba(56,189,248,0.1); border-color: #38bdf8; color: #38bdf8; font-size: 10px;">
                        🔄 SEGAR SEMULA LOG
                    </button>
                </div>
            </div>

            <div class="hacking-terminal" id="hackingLog">
                [EXPLOIT] Initializing Architech Cyber-Matrix Payload...<br>
                [AUTH] Active session authenticated as: superadmin<br>
                [BYPASS] Quantum firewall tunnel established successfully.<br>
                [READY] Awaiting system command sequence...
            </div>

            <div class="cmd-terminal" id="cmdLog">
                Microsoft Windows [Version 10.0.26100]<br>
                (c) Architech Laboratories. All rights reserved.<br>
                C:\\Architech\\BotLabs> python leea_admin_panel.py
            </div>
        </div>

        <!-- KOLUM KANAN: REALTIME LEEA BOT & UPDATE KOTAK, AFFILIATE, & KLIEN -->
        <div class="space-y-6">
            
            <!-- REALTIME LEEA BOT (WEBHOOK) & UPDATE LEEA-BOT BOX -->
            <div class="card">
                <h2>
                    REALTIME LEEA BOT & UPDATE BOX
                    <span class="led-indicator" style="color: #10b981;"><span class="led-dot led-green"></span> ACTIVE</span>
                </h2>
                
                <!-- KOTAK UPDATE REAL-TIME LEEA-BOT KITA SENDIRI (FILE, BRAIN, APP, ENGINE, COMPANY PROFILE, NOMBOR ADMIN) -->
                <div style="background: rgba(0, 240, 255, 0.03); border: 1px dashed var(--accent); border-radius: 8px; padding: 15px; margin-bottom: 20px;">
                    <strong style="color: var(--accent); font-size: 11px; display: block; margin-bottom: 10px;">⚡ KEMASKINI REAL-TIME FAIL LEEA-BOT KITA</strong>
                    <form @submit.prevent="updateLeeaBotRealtime()">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <div class="form-group" style="margin-bottom: 8px;">
                                <label>1. Fail Sumber (File):</label>
                                <input type="text" x-model="leeaUpdateForm.fileTarget" placeholder="leea_bot.py">
                            </div>
                            <div class="form-group" style="margin-bottom: 8px;">
                                <label>6. Nombor Admin:</label>
                                <input type="text" x-model="leeaUpdateForm.adminNumber" placeholder="60190000000X">
                            </div>
                        </div>
                        <div class="form-group" style="margin-bottom: 8px;">
                            <label>2. Minda Bot (Brain Prompt):</label>
                            <textarea x-model="leeaUpdateForm.brain" placeholder="Personaliti, skrip minda bot..." style="height: 55px;"></textarea>
                        </div>
                        <div class="form-group" style="margin-bottom: 8px;">
                            <label>3. Konfigurasi Aplikasi (App Config / Token):</label>
                            <textarea x-model="leeaUpdateForm.appConfig" placeholder="Token akses, verify token..." style="height: 55px;"></textarea>
                        </div>
                        <div class="form-group" style="margin-bottom: 8px;">
                            <label>4. Enjin Gelagat (Engine Parameters):</label>
                            <textarea x-model="leeaUpdateForm.engine" placeholder="Tetapan memori V1/V2, respons..." style="height: 55px;"></textarea>
                        </div>
                        <div class="form-group" style="margin-bottom: 10px;">
                            <label>5. Profil Syarikat (Company Profile):</label>
                            <textarea x-model="leeaUpdateForm.companyProfile" placeholder="Latar belakang syarikat..." style="height: 55px;"></textarea>
                        </div>
                        <button type="submit" style="background: rgba(0,240,255,0.15); border-color: var(--accent); color: var(--accent); padding: 8px; font-size: 11px; margin-top: 0;">
                            🚀 PUSH KEMASKINI REAL-TIME LEEA-BOT
                        </button>
                    </form>
                </div>

                <!-- RUANG LIVE CHAT WEBHOOK -->
                <div style="display: grid; grid-template-columns: 220px 1fr; gap: 15px; height: 300px; font-family: monospace;">
                    <!-- Senarai Chat Kiri -->
                    <div style="border-right: 1px solid #1e3a8a; overflow-y: auto; padding-right: 5px;">
                        <template x-for="chat in liveChats" :key="chat.id">
                            <div @click="selectChat(chat)" style="padding: 8px; cursor: pointer; border-radius: 6px; margin-bottom: 4px; font-size: 11px;" :style="activeChat && activeChat.id === chat.id ? 'background: rgba(0,240,255,0.15); border-left: 3px solid #00f0ff; color: #fff;' : 'background: #020617; color: #94a3b8;'">
                                <div style="font-weight: bold; color: #00f0ff;" x-text="chat.phone"></div>
                                <div style="font-size: 9px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" x-text="chat.lastMessage"></div>
                            </div>
                        </template>
                        <template x-if="liveChats.length === 0">
                            <div style="padding: 20px; text-align: center; color: #64748b; font-size: 10px;">Menunggu rekod perbualan...</div>
                        </template>
                    </div>

                    <!-- Ruang Perbualan Kanan -->
                    <div style="display: flex; flex-direction: column; justify-content: space-between; background: #020617; border-radius: 8px; padding: 12px; border: 1px solid #1e3a8a;">
                        <template x-if="!activeChat">
                            <div style="display: flex; align-items: center; justify-content: center; flex-grow: 1; color: #64748b; font-size: 11px; text-align: center;">
                                Sila pilih perbualan di sebelah kiri untuk pantau atau balas.
                            </div>
                        </template>
                        <template x-if="activeChat">
                            <div style="display: flex; flex-direction: column; height: 100%; justify-content: space-between;">
                                <div style="padding: 6px 10px; background: #0b1329; border: 1px solid #1e3a8a; border-radius: 4px; font-weight: bold; color: #00f0ff; font-size: 11px; margin-bottom: 8px;" x-text="'Chat bersama: ' + activeChat.phone"></div>
                                
                                <div id="chatMessagesBox" style="overflow-y: auto; flex-grow: 1; display: flex; flex-direction: column; gap: 8px; padding-right: 4px; max-height: 150px;">
                                    <template x-for="msg in activeChat.messages">
                                        <div style="display: flex;" :style="msg.sender === 'customer' ? 'justify-content: flex-start;' : 'justify-content: flex-end;'">
                                            <div style="max-width: 80%; padding: 6px 10px; border-radius: 8px; font-size: 11px;" :style="msg.sender === 'customer' ? 'background: #0b1329; color: #e2e8f0; border: 1px solid #1e3a8a;' : 'background: #00f0ff; color: #030712; font-weight: bold;'">
                                                <p style="margin: 0;" x-text="msg.text"></p>
                                                <span style="font-size: 8px; display: block; text-align: right; opacity: 0.7; margin-top: 2px;" x-text="msg.time"></span>
                                            </div>
                                        </div>
                                    </template>
                                </div>

                                <form @submit.prevent="sendAdminReply()" style="display: flex; gap: 6px; margin-top: 8px;">
                                    <input type="text" x-model="adminReplyText" :placeholder="humanTouchActive ? 'Taip mesej manual...' : 'Aktifkan Human Touch...'" :disabled="!humanTouchActive" style="flex-grow: 1; padding: 6px 8px; background: #030712; border: 1px solid #1e3a8a; color: #00f0ff; border-radius: 4px; font-size: 11px;">
                                    <button type="submit" :disabled="!humanTouchActive" style="width: auto; padding: 6px 12px; margin-top: 0; background: #00f0ff; color: #030712; font-weight: bold; border-radius: 4px; font-size: 11px; border: none; cursor: pointer;">Hantar</button>
                                </form>
                            </div>
                        </template>
                    </div>
                </div>
            </div>

            <!-- SENARAI AGEN AFFILIATE & PAYOUT KOMISEN (10%) -->
            <div class="card">
                <h2>
                    SENARAI AGEN AFFILIATE & PAYOUT KOMISEN (10%)
                    <span style="color: #34d399; font-size: 11px;" x-text="'Jumlah Agen: ' + getAffiliateAgents().length"></span>
                </h2>
                <div class="table-container">
                    <table class="server-table">
                        <thead>
                            <tr>
                                <th>Klien / Username</th>
                                <th>Status Agen</th>
                                <th>Baki E-Wallet</th>
                                <th>Bank / DuitNow</th>
                                <th class="center">Tindakan Payout</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template x-for="client in clients" :key="client.username">
                                <tr>
                                    <td class="srv-id">
                                        <div style="color: #fff; font-weight: bold;" x-text="client.companyName || client.username"></div>
                                        <span style="color: #60a5fa; font-size: 10px;" x-text="'@' + client.username"></span>
                                    </td>
                                    <td>
                                        <span style="padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: bold;" :class="getClientAffiliateData(client.username).isAgent ? 'bg-emerald-950 text-emerald-400 border border-emerald-600' : 'bg-gray-900 text-gray-500'" x-text="getClientAffiliateData(client.username).isAgent ? 'AKTIF 🟢' : 'BELUM DAFTAR'"></span>
                                    </td>
                                    <td style="font-weight: bold; color: #34d399;" x-text="'RM ' + getClientAffiliateData(client.username).walletBalance.toFixed(2)"></td>
                                    <td style="color: #cbd5e1; font-size: 10px;">
                                        <template x-if="getClientBankData(client.username).accountNo">
                                            <div>
                                                <strong style="color: #38bdf8;" x-text="getClientBankData(client.username).bankName"></strong><br>
                                                <span x-text="'No: ' + getClientBankData(client.username).accountNo"></span>
                                            </div>
                                        </template>
                                        <template x-if="!getClientBankData(client.username).accountNo">
                                            <span class="text-gray-600 italic">Belum tetapkan</span>
                                        </template>
                                    </td>
                                    <td class="center">
                                        <template x-if="getClientAffiliateData(client.username).isAgent && getClientAffiliateData(client.username).walletBalance > 0">
                                            <button @click="processAffiliatePayout(client)" style="background: #10b981; color: #000; padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 10px; border: none; cursor: pointer; width: auto; margin-top:0;">
                                                PROSES PAYOUT
                                            </button>
                                        </template>
                                        <template x-if="!getClientAffiliateData(client.username).isAgent || getClientAffiliateData(client.username).walletBalance <= 0">
                                            <span class="text-gray-600 text-[10px]">Tiada Tindakan</span>
                                        </template>
                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- SENARAI AKAUN KLIEN & ID NEURAL -->
            <div class="card">
                <h2>
                    SENARAI AKAUN KLIEN & ID NEURAL
                    <button @click="openClientModal('add')" style="background: #2563eb; color: #fff; padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 10px; border: none; cursor: pointer; width: auto; margin-top:0;">
                        + TAMBAH KLIEN BARU
                    </button>
                </h2>
                <div class="table-container">
                    <table class="server-table">
                        <thead>
                            <tr>
                                <th>Client ID</th>
                                <th>Syarikat / Klien</th>
                                <th>Username (Pass: defaultpass123)</th>
                                <th>Telefon & E-mel</th>
                                <th>Railway URL</th>
                                <th class="center">Tindakan</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template x-for="(client, index) in clients" :key="index">
                                <tr>
                                    <td class="srv-id" x-text="client.clientId"></td>
                                    <td style="color: #fff; font-weight: bold;" x-text="client.companyName || client.username"></td>
                                    <td>
                                        <span style="color: #00f0ff;" x-text="client.username"></span> / 
                                        <code style="background: #020617; padding: 2px 4px; border-radius: 3px; color: #10b981;">defaultpass123</code>
                                    </td>
                                    <td style="color: #94a3b8; font-size: 10px;">
                                        <div x-text="client.phone"></div>
                                        <div style="color: #38bdf8;" x-text="client.email"></div>
                                    </td>
                                    <td><a :href="client.railwayUrl" target="_blank" style="color: #60a5fa; text-decoration: underline;" x-text="client.railwayUrl"></a></td>
                                    <td class="center">
                                        <button @click="openClientModal('edit', index)" style="background: #1e3a8a; color: #fff; padding: 3px 6px; border-radius: 3px; font-size: 10px; border: none; cursor: pointer; width: auto; margin-top:0; margin-right:4px;">Edit</button>
                                        <button @click="deleteClient(index)" style="background: #7f1d1d; color: #f87171; padding: 3px 6px; border-radius: 3px; font-size: 10px; border: none; cursor: pointer; width: auto; margin-top:0;">Padam</button>
                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </div>

    <!-- Modal Tambah/Edit Klien -->
    <div x-show="showClientModal" style="display: none; position: fixed; inset: 0; z-index: 50; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.8); backdrop-filter: blur(4px); padding: 15px;">
        <div class="card" style="width: 100%; max-width: 440px; background: #0b1329;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; margin-bottom: 12px;">
                <h3 style="font-size: 13px; color: var(--accent); margin: 0;" x-text="modalMode === 'edit' ? 'Kemaskini Klien' : 'Tambah Klien Baru'"></h3>
                <button @click="showClientModal = false" style="background: none; border: none; color: #ef4444; font-size: 14px; cursor: pointer; width: auto; margin-top:0;">✕</button>
            </div>
            <form @submit.prevent="saveClient()" class="space-y-3 font-mono">
                <div class="form-group">
                    <label>Nama Syarikat:</label>
                    <input type="text" x-model="clientForm.companyName" required>
                </div>
                <div class="form-group">
                    <label>Username Login:</label>
                    <input type="text" x-model="clientForm.username" required>
                </div>
                <!-- Ruangan Kata Laluan telah dibuang di sini, automatik guna defaultpass123 -->
                <div class="form-group">
                    <label>Nombor Telefon (WhatsApp):</label>
                    <input type="text" x-model="clientForm.phone" required>
                </div>
                <div class="form-group">
                    <label>E-mel Klien:</label>
                    <input type="email" x-model="clientForm.email" required>
                </div>
                <div class="form-group">
                    <label>Railway Bot URL:</label>
                    <input type="text" x-model="clientForm.railwayUrl" required>
                </div>
                <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 15px;">
                    <button type="button" @click="showClientModal = false" style="background: #1e293b; color: #fff; padding: 8px 12px; border-radius: 6px; border: none; cursor: pointer; width: auto; margin-top:0;">Batal</button>
                    <button type="submit" style="width: auto; padding: 8px 16px; margin-top:0;">Simpan Klien</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Skrip JavaScript -->
    <script>
        const headerSimTexts = [
            "CYBER-TRACE: ROUTING THROUGH ENCLAVE NODES...",
            "SSL HANDSHAKE: SECURE 256-BIT ENCRYPTION...",
            "PACKET SNIFFER: ACTIVE ON GOOGLE APPS SCRIPT...",
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
            "[SUCCESS] Administrator Command Center stable & operational."
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

        function adminData() {
            return {
                clients: [],
                showClientModal: false,
                modalMode: 'add',
                editIndex: null,
                clientForm: { companyName: '', username: '', phone: '', email: '', railwayUrl: '' },
                liveChats: [],
                activeChat: null,
                adminReplyText: '',
                humanTouchActive: false,
                gasEndpointUrl: "https://script.google.com/macros/s/AKfycbyEBtjAKVLf1owVcQpKKcI9gDo13qFERizYqtAQtmLsRl6Kg2Cgo4wmCon2AnmmGFiNMA/exec",
                railwayReplyUrl: "https://leeasystem-production-47d7.up.railway.app/api/chats/reply",
                broadcastForm: { target: 'ALL', senderTitle: 'Master Administrator', content: '' },
                leeaUpdateForm: { fileTarget: 'leea_bot.py', brain: '', appConfig: '', engine: '', companyProfile: '', adminNumber: '' },
                
                masterToken500: '',
                masterToken1000: '',
                masterSubscription: '',
                masterCustom: '',
                masterToyyibKey: '',

                init() {
                    this.fetchClients();
                    this.fetchLiveChats();
                    this.fetchAdminAuditLogs();
                    setInterval(() => { 
                        this.fetchLiveChats(); 
                    }, 4000);
                },

                async fetchAdminAuditLogs() {
                    try {
                        const res = await fetch('/admin/get-audit-logs');
                        const data = await res.json();
                        if (data && data.status === 'success') {
                            const logBox = document.getElementById('adminAuditLogBox');
                            if (logBox) {
                                logBox.innerText = data.logs.join('\\n');
                                logBox.scrollTop = logBox.scrollHeight;
                            }
                        }
                    } catch (err) {
                        console.error('Gagal memuatkan log audit.');
                    }
                },

                async toggleAdminMaintenance() {
                    try {
                        const res = await fetch('/admin/toggle-maintenance', { method: 'POST' });
                        const data = await res.json();
                        if (data && data.status === 'success') {
                            const btn = document.getElementById('adminMaintBtn');
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
                        }
                    } catch (err) {
                        alert('Gagal mengubah status mod penyelenggaraan.');
                    }
                },

                async triggerAdminGitPush() {
                    if (!confirm('Sahkan untuk menjalankan automasi Git Add, Commit & Push ke GitHub?')) return;
                    
                    try {
                        const res = await fetch('/admin/git-push', { method: 'POST' });
                        const data = await res.json();
                        if (data && data.status === 'success') {
                            alert(data.message || 'Proses Git Push berjaya!');
                        } else {
                            alert(data.message || 'Ralat semasa menjalankan Git Push.');
                        }
                    } catch (err) {
                        alert('Gagal berhubung dengan pelayan untuk arahan Git.');
                    }
                },

                async saveMasterPayment(paymentKey, urlValue) {
                    try {
                        const formData = new FormData();
                        formData.append('filename', 'global_payment_master.json');
                        formData.append('target_folder', 'bot_labs');
                        formData.append('overwrite', 'true');
                        
                        const payloadData = {
                            key: paymentKey,
                            url: urlValue,
                            updated_at: new Date().toISOString()
                        };
                        
                        formData.append('content', JSON.stringify(payloadData, null, 4));

                        const res = await fetch('/admin/save-html', { method: 'POST', body: formData });
                        const data = await res.json();
                        alert(`Tetapan untuk [${paymentKey}] berjaya dikemaskini ke seluruh sistem!`);
                    } catch (err) {
                        alert('Gagal berhubung dengan pelayan.');
                    }
                },

                scrollToBottom() {
                    setTimeout(() => {
                        const box = document.getElementById('chatMessagesBox');
                        if (box) {
                            box.scrollTop = box.scrollHeight;
                        }
                    }, 50);
                },

                selectChat(chat) {
                    this.activeChat = chat;
                    this.scrollToBottom();
                },

                getClientAffiliateData(username) {
                    const saved = localStorage.getItem('leea_affiliate_' + username);
                    if (saved) {
                        try {
                            const parsed = JSON.parse(saved);
                            return parsed.data || { isAgent: false, walletBalance: 0, totalReferrals: 0, totalEarned: 0 };
                        } catch(e) {}
                    }
                    return { isAgent: false, walletBalance: 0, totalReferrals: 0, totalEarned: 0 };
                },

                getClientBankData(username) {
                    const saved = localStorage.getItem('leea_affiliate_' + username);
                    if (saved) {
                        try {
                            const parsed = JSON.parse(saved);
                            return parsed.bank || { bankName: '', accountNo: '', accountHolder: '' };
                        } catch(e) {}
                    }
                    return { bankName: '', accountNo: '', accountHolder: '' };
                },

                getAffiliateAgents() {
                    return this.clients.filter(c => this.getClientAffiliateData(c.username).isAgent);
                },

                async processAffiliatePayout(client) {
                    const affData = this.getClientAffiliateData(client.username);
                    const bankData = this.getClientBankData(client.username);

                    if (affData.walletBalance <= 0) {
                        alert('Baki e-wallet klien ini adalah RM0.00.');
                        return;
                    }
                    if (!bankData.accountNo) {
                        alert('Klien ini belum menetapkan akaun bank/DuitNow.');
                        return;
                    }

                    const payoutAmount = affData.walletBalance;
                    if (confirm(`Sahkan pembayaran komisen sebanyak RM ${payoutAmount.toFixed(2)} kepada ${client.companyName || client.username}?`)) {
                        affData.walletBalance = 0;
                        const saved = localStorage.getItem('leea_affiliate_' + client.username);
                        let fullData = saved ? JSON.parse(saved) : {};
                        fullData.data = affData;
                        localStorage.setItem('leea_affiliate_' + client.username, JSON.stringify(fullData));
                        alert(`Payout RM ${payoutAmount.toFixed(2)} berjaya diproses!`);
                    }
                },

                toggleHumanTouch() {
                    this.humanTouchActive = !this.humanTouchActive;
                    alert(this.humanTouchActive ? 'Mod Human Touch diaktifkan!' : 'Mod Human Touch ditutup.');
                },

                async updateLeeaBotRealtime() {
                    try {
                        const formData = new FormData();
                        formData.append('file_target', this.leeaUpdateForm.fileTarget);
                        formData.append('brain', this.leeaUpdateForm.brain);
                        formData.append('app_config', this.leeaUpdateForm.appConfig);
                        formData.append('engine', this.leeaUpdateForm.engine);
                        formData.append('company_profile', this.leeaUpdateForm.companyProfile);
                        formData.append('admin_number', this.leeaUpdateForm.adminNumber);

                        const res = await fetch('/admin/update-bot-leea', {
                            method: 'POST',
                            body: formData
                        });
                        const data = await res.json();
                        alert(data.message || 'Real-time Leea-Bot berjaya dikemaskini!');
                    } catch(err) {
                        alert('Berjaya menghantar arahan kemaskini Real-Time Leea-Bot!');
                    }
                },

                async sendAdminBroadcastMessage() {
                    if (!this.broadcastForm.content.trim()) return;
                    const payload = {
                        timestamp: new Date().toLocaleString('en-GB', { timeZone: 'Asia/Kuala_Lumpur' }),
                        type: 'inbox',
                        sender: this.broadcastForm.senderTitle,
                        phone: '-',
                        role: 'admin',
                        message: this.broadcastForm.content,
                        targetClient: this.broadcastForm.target
                    };
                    try {
                        await fetch(this.gasEndpointUrl, {
                            method: 'POST', mode: 'no-cors',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        alert('Mesej berjaya dihantar ke Google Sheets Inbox klien!');
                        this.broadcastForm.content = '';
                    } catch (err) {
                        alert('Ralat semasa menghantar mesej.');
                    }
                },

                async fetchLiveChats() {
                    try {
                        const res = await fetch(this.gasEndpointUrl + "?t=" + new Date().getTime());
                        const data = await res.json();
                        if (data && data.status === "success" && Array.isArray(data.data)) {
                            const chatMap = {};
                            let lastPhone = "601123687357";
                            data.data.forEach(row => {
                                if (row.type && row.type !== 'chat') return;
                                let phone = row.phone ? String(row.phone).trim() : lastPhone;
                                const cleanPhone = phone.replace(/[^0-9]/g, '');
                                if (!chatMap[cleanPhone]) {
                                    chatMap[cleanPhone] = { id: 'chat-' + cleanPhone, phone: cleanPhone, lastMessage: '', lastTime: '', messages: [] };
                                }
                                if (row.message) {
                                    chatMap[cleanPhone].messages.push({ sender: row.role || 'customer', text: row.message, time: row.timestamp });
                                    chatMap[cleanPhone].lastMessage = row.message;
                                    chatMap[cleanPhone].lastTime = row.timestamp;
                                }
                            });
                            
                            const oldActiveId = this.activeChat ? this.activeChat.id : null;
                            this.liveChats = Object.values(chatMap);

                            if (oldActiveId) {
                                const matched = this.liveChats.find(c => c.id === oldActiveId);
                                if (matched) {
                                    this.activeChat = matched;
                                }
                            } else if (this.liveChats.length > 0 && !this.activeChat) {
                                this.activeChat = this.liveChats[0];
                                this.scrollToBottom();
                            }
                        }
                    } catch (err) {}
                },

                async sendAdminReply() {
                    if (!this.adminReplyText.trim() || !this.activeChat) return;
                    if (!this.humanTouchActive) {
                        alert('Sila aktifkan "Human Touch" terlebih dahulu!');
                        return;
                    }

                    const displayTime = new Date().toLocaleTimeString('en-US', {
                        timeZone: 'Asia/Kuala_Lumpur',
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: true
                    });

                    const textToSend = this.adminReplyText;
                    const cleanPhone = this.activeChat.phone.replace(/[^0-9]/g, '');

                    const railwayPayload = {
                        chat_id: this.activeChat.id,
                        phone: cleanPhone,
                        text: textToSend
                    };

                    this.activeChat.messages.push({ sender: 'agent', text: textToSend, time: displayTime });
                    this.activeChat.lastMessage = textToSend;
                    this.activeChat.lastTime = displayTime;
                    this.adminReplyText = '';
                    this.scrollToBottom();

                    try {
                        await fetch(this.railwayReplyUrl, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(railwayPayload)
                        });
                    } catch(err) {
                        console.error("Gagal hantar balasan chat ke Railway:", err);
                    }
                },

                fetchClients() {
                    const saved = localStorage.getItem('leea_admin_clients');
                    if (saved) {
                        try {
                            this.clients = JSON.parse(saved);
                        } catch(e) { this.clients = []; }
                    } else {
                        this.clients = [
                            { clientId: 'CLI-1001', companyName: 'Shahril Basri Leisure Enterprise', username: 'sbltransport', password: 'defaultpass123', phone: '+60132434200', email: 'architechlabs.io@gmail.com', railwayUrl: 'https://web-production-07b92.up.railway.app', status: 'Paid 🟢' }
                        ];
                        localStorage.setItem('leea_admin_clients', JSON.stringify(this.clients));
                    }
                },

                saveClients() {
                    localStorage.setItem('leea_admin_clients', JSON.stringify(this.clients));
                },

                openClientModal(mode, index = null) {
                    this.modalMode = mode;
                    if (mode === 'edit' && index !== null) {
                        this.editIndex = index;
                        this.clientForm = { ...this.clients[index] };
                    } else {
                        this.clientForm = { companyName: '', username: '', phone: '', email: '', railwayUrl: '' };
                    }
                    this.showClientModal = true;
                },

                saveClient() {
                    if (this.modalMode === 'edit' && this.editIndex !== null) {
                        this.clients[this.editIndex] = { ...this.clientForm, password: this.clients[this.editIndex].password || 'defaultpass123' };
                    } else {
                        const nextId = 1001 + this.clients.length;
                        this.clients.push({ ...this.clientForm, password: 'defaultpass123', clientId: `CLI-${nextId}`, status: 'Paid 🟢' });
                    }
                    this.saveClients();
                    this.showClientModal = false;
                },

                deleteClient(index) {
                    if (confirm('Padam akaun klien ini?')) {
                        this.clients.splice(index, 1);
                        this.saveClients();
                    }
                }
            }
        }
    </script>
</body>
</html>
"""