# Modul Templat HTML untuk Skrin Log Masuk (Secure Password & WhatsApp OTP Gateway + API Sebenar)
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ms" x-data="loginData()">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Labs - Secure WhatsApp OTP Gateway</title>
    <style>
        :root {
            --bg-main: #030712;
            --bg-card: #0b1329;
            --border-color: #1e3a8a;
            --accent: #00f0ff;
            --accent-glow: rgba(0, 240, 255, 0.4);
            --text-main: #e0f2fe;
            --text-muted: #60a5fa;
            --success: #10b981;
            --danger: #ef4444;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: var(--bg-main); color: var(--text-main); margin: 0; padding: 0; display: flex; flex-direction: column; min-height: 100vh; justify-content: space-between; }
        header { background: var(--bg-card); border-bottom: 1px solid var(--border-color); padding: 16px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 0 15px rgba(0, 240, 255, 0.1); }
        .brand { font-weight: 700; font-size: 15px; color: var(--accent); letter-spacing: 1.5px; }
        .center-wrapper { display: flex; justify-content: center; align-items: center; flex: 1; padding: 20px; }
        .security-card { background: var(--bg-card); border: 1px solid var(--success); border-radius: 16px; padding: 35px; width: 100%; max-width: 440px; box-shadow: 0 0 30px rgba(16, 185, 129, 0.2); transition: all 0.3s ease; }
        .security-card.alert-mode { border-color: var(--danger); box-shadow: 0 0 50px rgba(239, 68, 68, 0.8); animation: shake 0.25s infinite alternate; background: linear-gradient(135deg, #0b1329 0%, #1f1215 100%); }
        @keyframes shake { 0% { transform: translateX(-4px) translateY(0); } 100% { transform: translateX(4px) translateY(-2px); } }
        
        h2 { font-size: 16px; margin: 0 0 5px 0; color: var(--success); letter-spacing: 2px; text-align: center; }
        h2.alert-text { color: var(--danger); text-shadow: 0 0 10px rgba(239, 68, 68, 0.5); }
        p { color: var(--text-muted); font-size: 11px; margin-bottom: 25px; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; color: var(--text-muted); font-size: 11px; font-weight: 500; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px 12px; border: 1px solid var(--border-color); background: #020617; color: var(--accent); border-radius: 6px; box-sizing: border-box; font-size: 13px; font-family: monospace; }
        input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 8px var(--accent-glow); }
        button { width: 100%; background: var(--success); border: 1px solid var(--success); color: #030712; padding: 12px; font-size: 13px; font-weight: 700; border-radius: 8px; cursor: pointer; transition: all 0.3s; letter-spacing: 1px; margin-top: 10px; }
        button:hover { background: transparent; color: var(--success); box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }
        .btn-secondary { background: rgba(0, 240, 255, 0.1); border-color: var(--accent); color: var(--accent); }
        .btn-secondary:hover { background: var(--accent); color: #030712; }
        .btn-danger { background: var(--danger); border-color: var(--danger); color: #fff; }
        .btn-danger:hover { background: transparent; color: var(--danger); box-shadow: 0 0 20px rgba(239, 68, 68, 0.6); }
        footer { text-align: center; padding: 15px; color: var(--text-muted); font-size: 10px; border-top: 1px solid var(--border-color); background: var(--bg-card); }
    </style>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body>
    <header>
        <div class="brand">Bot Labs - SECURE GATEWAY</div>
    </header>
    
    <div class="center-wrapper">
        <div class="security-card" :class="isAlarmActive ? 'alert-mode' : ''">
            <h2 :class="isAlarmActive ? 'alert-text' : ''" x-text="isAlarmActive ? '🚨 AMARAN PENETRASI SISTEM!' : 'PENGESAHAN KESELAMATAN'"></h2>
            <p x-text="isAlarmActive ? 'AMARAN: Percubaan akses tidak sah dikesan! Siren kecemasan aktif.' : (step === 1 ? 'Masukkan Secure Code untuk menghantar OTP WhatsApp sebenar.' : 'Kod OTP telah dihantar ke nombor WhatsApp anda. Sila masukkan untuk akses masuk.')"></p>

            <!-- Langkah 1: Masukkan Secure Code -->
            <template x-if="step === 1">
                <form @submit.prevent="sendOtpRequest()">
                    <div class="form-group">
                        <label>Secure Login Password:</label>
                        <input type="password" x-model="secureCode" placeholder="Masukkan Secure Code..." required>
                    </div>
                    <button type="submit" class="btn-secondary" x-show="!isAlarmActive">HANTAR KOD OTP WHATSAPP</button>
                    <button type="button" class="btn-danger" x-show="isAlarmActive" @click="stopAlarm()">SEKAT & MATIKAN SIREN AMARAN</button>
                </form>
            </template>

            <!-- Langkah 2: Masukkan Kod OTP -->
            <template x-if="step === 2">
                <form @submit.prevent="verifyOtpAndLogin()">
                    <div class="form-group">
                        <label>Kod OTP WhatsApp (6 Digit):</label>
                        <input type="text" x-model="otpCode" placeholder="Contoh: 123456" maxlength="6" required autofocus>
                    </div>
                    <button type="submit" x-show="!isAlarmActive">SAHKAN & MASUK</button>
                    <button type="button" class="btn-danger" x-show="isAlarmActive" @click="stopAlarm()">SEKAT & MATIKAN SIREN AMARAN</button>
                    <button type="button" @click="step = 1; otpCode = ''" style="background: transparent; border: 1px solid #60a5fa; color: #60a5fa; margin-top: 8px;" x-show="!isAlarmActive">KEMBALI</button>
                </form>
            </template>
        </div>
    </div>

    <footer>ARCHITECH LABS // SECURE WHATSAPP GATEWAY ACTIVE</footer>

    <script>
        function loginData() {
            return {
                step: 1,
                secureCode: '',
                otpCode: '',
                isAlarmActive: false,
                alarmInterval: null,
                audioCtx: null,
                
                startContinuousAlarm() {
                    if (this.alarmInterval) return;
                    try {
                        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        const playSirenBurst = () => {
                            if (!this.isAlarmActive || !this.audioCtx) return;
                            const osc = this.audioCtx.createOscillator();
                            const gain = this.audioCtx.createGain();
                            osc.type = 'sawtooth';
                            osc.frequency.setValueAtTime(600, this.audioCtx.currentTime);
                            osc.frequency.linearRampToValueAtTime(1200, this.audioCtx.currentTime + 0.25);
                            osc.frequency.linearRampToValueAtTime(600, this.audioCtx.currentTime + 0.5);
                            
                            gain.gain.setValueAtTime(0.25, this.audioCtx.currentTime);
                            gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + 0.5);
                            
                            osc.connect(gain);
                            gain.connect(this.audioCtx.destination);
                            osc.start();
                            osc.stop(this.audioCtx.currentTime + 0.5);
                        };
                        playSirenBurst();
                        this.alarmInterval = setInterval(playSirenBurst, 550);
                    } catch(e) {}
                },

                stopAlarm() {
                    this.isAlarmActive = false;
                    if (this.alarmInterval) {
                        clearInterval(this.alarmInterval);
                        this.alarmInterval = null;
                    }
                    if (this.audioCtx) {
                        try { this.audioCtx.close(); } catch(e) {}
                        this.audioCtx = null;
                    }
                },

                async sendOtpRequest() {
                    try {
                        const response = await fetch('/api/request-otp', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ secureCode: this.secureCode })
                        });
                        const data = await response.json();
                        
                        if (response.ok && data.status === 'success') {
                            this.stopAlarm();
                            this.step = 2;
                            alert('Kod OTP WhatsApp telah berjaya dihantar ke nombor anda melalui Cloud API!');
                        } else {
                            this.isAlarmActive = true;
                            this.startContinuousAlarm();
                        }
                    } catch (e) {
                        this.isAlarmActive = true;
                        this.startContinuousAlarm();
                    }
                },

                async verifyOtpAndLogin() {
                    try {
                        const response = await fetch('/api/verify-otp', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ otpCode: this.otpCode })
                        });
                        const data = await response.json();
                        
                        if (response.ok && data.status === 'success') {
                            this.stopAlarm();
                            alert('Akses Disahkan! Memasuki papan pemuka...');
                            window.location.href = "/";
                        } else {
                            this.isAlarmActive = true;
                            this.startContinuousAlarm();
                        }
                    } catch (e) {
                        this.isAlarmActive = true;
                        this.startContinuousAlarm();
                    }
                }
            }
        }
    </script>
</body>
</html>
"""