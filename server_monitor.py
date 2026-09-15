# server_monitor.py
import os
import requests
import datetime
import json
from dotenv import load_dotenv

load_dotenv()

class RailwayServerMonitor:
    """Kelas untuk memantau kesihatan nod server Railway dan slot ID klien secara aktif"""
    
    def __init__(self, target_nodes=None):
        # Pemetaan nod pelayan dan slot ID klien yang diuruskan dalam sistem
        self.target_nodes = target_nodes or {
            "SRV #1": {"url": "https://web-production-07b92.up.railway.app", "slots": ["CLI-1001", "CLI-1002", "CLI-1003", "CLI-1004"]},
            "SRV #2": {"url": "https://web-production-07b92.up.railway.app", "slots": ["CLI-1005", "CLI-1006", "CLI-1007", "CLI-1008"]}
        }
        
    def check_node_health(self, server_name, node_data):
        """Menyemak status sambungan URL Railway dan mengemas kini status slot klien"""
        url = node_data["url"]
        slots = node_data["slots"]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            response = requests.get(url, timeout=10)
            is_active = response.status_code < 400
            status_desc = "ACTIVE 🟢" if is_active else f"WARNING (Code: {response.status_code}) 🟡"
            crashed = False
        except requests.exceptions.RequestException as e:
            status_desc = "ERROR 🔴"
            crashed = True
            
        result = {
            "timestamp": timestamp,
            "serverName": server_name,
            "url": url,
            "status": status_desc,
            "crashed": crashed,
            "slotsActive": slots
        }
        print(f"[{timestamp}] {server_name} -> Status: {status_desc} | Slots: {slots}")
        return result

    def run_active_monitor(self, log_output_file="server_monitor_log.json"):
        """Menjalankan imbasan aktif untuk semua nod pelayan dan merekodkan status slot"""
        report_results = []
        for name, data in self.target_nodes.items():
            status_data = self.check_node_health(name, data)
            report_results.append(status_data)
            
        try:
            with open(log_output_file, "w", encoding="utf-8") as f:
                json.dump(report_results, f, indent=4, ensure_ascii=False)
        except Exception as err:
            print(f"[MONITOR ERROR] Gagal menyimpan log semakan: {err}")
            
        return report_results

if __name__ == "__main__":
    print("Memulakan pemantauan aktif nod pelayan dan slot klien...")
    monitor = RailwayServerMonitor()
    monitor.run_active_monitor()