import imaplib
import email
from email.header import decode_header
import re

def fetch_latest_otp(gmail_user, app_password):
    """Fungsi untuk menyemak dan mendapatkan kod OTP terkini dari inbox Gmail menggunakan IMAP."""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_user, app_password)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            mail.logout()
            return "Status IMAP gagal."

        email_ids = messages[0].split()
        if not email_ids:
            status, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()
            if not email_ids:
                mail.logout()
                return "Inbox kosong."

        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            try:
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                            except:
                                pass
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                otp_match = re.search(r'\b\d{4,8}\b', body)
                otp_code = otp_match.group(0) if otp_match else "Tiada OTP"

                mail.logout()
                return f"Tajuk: {subject} | OTP: [{otp_code}]"
        
        mail.logout()
        return "Gagal huraikan mesej."
    except Exception as e:
        return f"Ralat Sambungan IMAP: {str(e)}"