# bot_project.py
import os
import json
import datetime

class BotFactoryEngine:
    """Modul pengurusan Bot Factory Engine untuk menaik taraf model bot klien (V1 ke V2)"""
    
    def __init__(self, storage_file="bot_factory_state.json"):
        self.storage_file = storage_file
        self.load_state()

    def load_state(self):
        """Memuatkan status state bot factory dari storan tempatan"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.state = json.load(f)
            except Exception:
                self.state = {"upgraded_clients": {}}
        else:
            self.state = {"upgraded_clients": {}}

    def save_state(self):
        """Menyimpan status state bot factory"""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=4, ensure_ascii=False)
        except Exception as err:
            print(f"[BOT FACTORY ERROR] Gagal menyimpan state: {err}")

    def upgrade_bot_model(self, client_id, target_model="Model Bot V2 (600 MB)"):
        """Proses menaik taraf model bot klien dari V1 ke V2 dengan peruntukan memori"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        memory_allocation = "600 MB" if "V2" in target_model else "300 MB"
        
        upgrade_record = {
            "client_id": client_id,
            "target_model": target_model,
            "memory": memory_allocation,
            "upgraded_at": timestamp,
            "status": "SUCCESS"
        }
        
        self.state["upgraded_clients"][client_id] = upgrade_record
        self.save_state()
        
        log_message = f"[{timestamp}] [BOT FACTORY] Klien {client_id} berjaya dinaik taraf ke {target_model} dengan peruntukan memori {memory_allocation}."
        print(log_message)
        
        try:
            with open("bot_factory_upgrade.log", "a", encoding="utf-8") as log_file:
                log_file.write(log_message + "\n")
        except Exception:
            pass
            
        return {
            "status": "success",
            "message": f"Klien {client_id} berjaya dinaik taraf kepada {target_model}.",
            "details": upgrade_record
        }

    def get_client_status(self, client_id):
        """Mendapatkan maklumat taraf model bot bagi klien tertentu"""
        return self.state["upgraded_clients"].get(client_id, {"target_model": "Model Bot V1 (Default - 300MB Memory)", "memory": "300 MB"})

if __name__ == "__main__":
    factory = BotFactoryEngine()
    result = factory.upgrade_bot_model("CLI-1001", "Model Bot V2 (600 MB)")
    print(result)