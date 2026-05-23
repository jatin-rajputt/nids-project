import requests
from datetime import datetime
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

NOTIFY_ON = ["LOW","MEDIUM", "HIGH"]

def send(severity, attack_type, source_ip, dest_ip):
    """Send a Telegram notification when an attack is detected."""
    
    

    emoji = {"LOW": "🟡", "MEDIUM": "🟠", "HIGH": "🔴"}.get(severity, "⚠️")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"{emoji} *NIDS ALERT*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🕒 *Time:* `{timestamp}`\n"
        f"⚡ *Attack:* `{attack_type}`\n"
        f"🎯 *Severity:* `{severity}`\n"
        f"📡 *Source IP:* `{source_ip}`\n"
        f"🖥️ *Target IP:* `{dest_ip}`\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"_Your NIDS detected a threat!_"
    )


    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(url, json={
            "chat_id": 8236339892,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=5)
        
        if response.status_code == 200:
            print(f"[NOTIFIER] ✅ Telegram alert sent: {attack_type} ({severity})")
        else:
            print(f"[NOTIFIER] ❌ Failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("[NOTIFIER] ❌ No internet - alert not sent")
    except Exception as e:
        print(f"[NOTIFIER] ❌ Error: {e}")
        print(f"[NOTIFIER] Error: {e}")