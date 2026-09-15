import os

# Konfigurasi URL Klien dan Kapasiti Asas
CLIENT_URLS = {
    "CLI-1001": {"url": "web-production-07b92.up.railway.app", "crashed": False, "model": "V1", "memory": "300MB"},
    "CLI-1002": {"url": "web-production-0a123.up.railway.app", "crashed": True, "model": "V2", "memory": "600MB"},
}

# Senarai Emel Pelayan Railway (1 hingga 50)
SERVER_EMAILS = {i: f"railway.acc{i}@gmail.com" for i in range(1, 51)}

def get_existing_bots():
    """Fungsi untuk mengesan direktori bot sedia ada di dalam sistem."""
    ignored_dirs = {'.git', '__pycache__', '.idea', 'venv'}
    subdirs = [d for d in os.listdir('.') if os.path.isdir(d) and d not in ignored_dirs]
    bots = []
    for d in subdirs:
        env_path = os.path.join(d, '.env')
        has_env = os.path.exists(env_path)
        bots.append({"name": d, "has_env": has_env})
    return bots