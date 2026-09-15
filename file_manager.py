# file_manager.py
import os

class FileManagerEngine:
    """Modul pengurusan fail untuk menyenaraikan direktori, mencipta folder baru, dan menyimpan fail."""
    
    def __init__(self, root_dir="."):
        self.root_dir = root_dir

    def get_directories_and_files(self):
        """Mendapatkan senarai folder dan fail yang ada dalam direktori utama dan subfolder."""
        folders = ["Bot-Labs (Direktori Utama / Root)"]
        files_map = {}
        
        try:
            for item in os.listdir(self.root_dir):
                item_path = os.path.join(self.root_dir, item)
                if os.path.isdir(item_path) and not item.startswith('.'):
                    folders.append(item)
                    # Senaraikan fail di dalam subfolder ini
                    sub_files = []
                    try:
                        for sub_item in os.listdir(item_path):
                            if os.path.isfile(os.path.join(item_path, sub_item)):
                                sub_files.append(sub_item)
                    except Exception:
                        pass
                    files_map[item] = sub_files
                elif os.path.isfile(item_path):
                    if "Root" not in files_map:
                        files_map["Root"] = []
                    files_map["Root"].append(item)
        except Exception:
            pass
            
        return folders, files_map

    def create_new_folder(self, folder_name):
        """Mencipta folder baharu di dalam direktori utama (Root)."""
        if not folder_name:
            return {"status": "error", "message": "Nama folder tidak boleh kosong."}
            
        new_dir_path = os.path.join(self.root_dir, folder_name.strip())
        if os.path.exists(new_dir_path):
            return {"status": "error", "message": f"Folder {folder_name} sudah wujud."}
            
        try:
            os.makedirs(new_dir_path)
            return {"status": "success", "message": f"Folder {folder_name} berjaya dicipta."}
        except Exception as e:
            return {"status": "error", "message": f"Gagal mencipta folder: {str(e)}"}

    def create_or_update_file(self, target_folder, file_name, content, overwrite=True):
        """Mencipta fail baharu atau mengemas kini fail dalam folder sasaran yang dipilih."""
        if not file_name:
            return {"status": "error", "message": "Nama fail tidak boleh kosong."}
            
        # Tentukan direktori destinasi
        if target_folder and target_folder != "Bot-Labs (Direktori Utama / Root)":
            dest_dir = os.path.join(self.root_dir, target_folder)
        else:
            dest_dir = self.root_dir
            
        # Pastikan direktori wujud, jika belum wujud cipta baru
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except Exception as e:
                return {"status": "error", "message": f"Gagal mencipta direktori: {str(e)}"}
                
        file_path = os.path.join(dest_dir, file_name.strip())
        
        # Semak jika fail sudah wujud dan mod overwrite ditutup
        if os.path.exists(file_path) and not overwrite:
            return {"status": "error", "message": f"Fail {file_name} sudah wujud dan mod Overwrite ditutup."}
            
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {
                "status": "success", 
                "message": f"Fail {file_name} berjaya dicipta dan disimpan di {dest_dir}.",
                "path": file_path
            }
        except Exception as e:
            return {"status": "error", "message": f"Gagal menyimpan fail: {str(e)}"}

if __name__ == "__main__":
    fm = FileManagerEngine()
    print(fm.get_directories_and_files())