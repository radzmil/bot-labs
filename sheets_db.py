import os
import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheets_client():
    """Mengesahkan sambungan ke Google Sheets menggunakan Service Account JSON"""
    credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    
    if credentials_json:
        creds_dict = json.loads(credentials_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        # Fallback jika guna fail json tempatan
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
        
    return gspread.authorize(creds)

def save_bot_to_sheet(sheet_id, bot_data):
    """Menyimpan data bot baru ke Google Sheet akaun Radzmil"""
    client = get_sheets_client()
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)
    
    row_values = [
        bot_data.get("company_name", ""),
        bot_data.get("bot_name", ""),
        bot_data.get("phone_id", ""),
        bot_data.get("access_token", ""),
        bot_data.get("gemini_api_key", ""),
        bot_data.get("webhook_url", ""),
        bot_data.get("created_at", "")
    ]
    
    worksheet.append_row(row_values)
    return True