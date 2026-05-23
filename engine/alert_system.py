from core.event_bus import publish
from core.config import LOG_FILE
from engine.notifier import send
from engine.stats import stats
import datetime
import os
from collections import defaultdict

class AlertSystem:
    def __init__(self):
        self.last_alert = defaultdict(dict)
        self.cooldown = 10

    def generate_alert(self, threat, packet_info):
        stats.alert_seen()
        src_ip = packet_info["source_ip"]
        dest_ip = packet_info.get("destination_ip", "unknown")

        now = datetime.datetime.now()

        last = self.last_alert[src_ip].get(threat)
        if last:
            delta = (now - last).total_seconds()
            if delta < self.cooldown:
                return

        self.last_alert[src_ip][threat] = now

        message = f"{threat} detected from {src_ip}"
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"

        # ✅ send alert to GUI
        publish("alert_event", log_entry)

        # ✅ fix log path - always resolves correctly
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_path = os.path.join(BASE_DIR, "data", "alerts.log")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # ✅ write to log file with flush
        with open(log_path, "a") as f:
            f.write(log_entry + "\n")
            f.flush()

        # ✅ send Telegram notification (NEW)
        # parse severity and attack type from threat string
        # threat format is like: "[HIGH] DoS Attack"
        try:
            severity = threat.split("]")[0].replace("[", "").strip()
            attack_type = threat.split("]")[1].strip()
        except:
            severity = "UNKNOWN"
            attack_type = threat

        send(severity, attack_type, src_ip, dest_ip)