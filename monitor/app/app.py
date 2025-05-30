from flask import Flask, jsonify
import os
import shutil
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)


@app.route("/api/stats")
def stats():
    try:
        total, used, free = shutil.disk_usage("/host/docker")
        free_gb = free / (1024**3)
        disk_info = {"free_space_gb": round(free_gb, 2)}
    except Exception as e:
        disk_info = {"error": str(e)}

    temperature = "N/A (Requires host integration)"
    wlan_ip = os.getenv("WLAN_IP", "dynamic")  # Fallback to client-side detection

    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[503])
    session.mount("http://", HTTPAdapter(max_retries=retries))

    try:
        jellyfin_response = session.get("http://jellyfin:8096/System/Info", timeout=10)
        jellyfin_response.raise_for_status()
        jellyfin_version = jellyfin_response.json().get("Version", "Unknown")
    except Exception as e:
        jellyfin_version = f"Error: {str(e)}"

    try:
        login_data = {
            "username": os.getenv("QBITTORRENT_USERNAME", "admin"),
            "password": os.getenv("QBITTORRENT_PASSWORD", "adminadmin"),
        }
        login_response = session.post(
            "http://qbittorrent:8080/api/v2/auth/login", data=login_data, timeout=10
        )
        login_response.raise_for_status()
        if "SID" not in session.cookies:
            raise Exception("Login failed")
        qbittorrent_response = session.get(
            "http://qbittorrent:8080/api/v2/app/version", timeout=10
        )
        qbittorrent_response.raise_for_status()
        qbittorrent_version = qbittorrent_response.text.strip() or "Unknown"
    except Exception as e:
        qbittorrent_version = f"Error: {str(e)}"

    return jsonify(
        {
            "disk": disk_info,
            "temperature": temperature,
            "wlan_ip": wlan_ip,
            "jellyfin_version": jellyfin_version,
            "qbittorrent_version": qbittorrent_version,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
