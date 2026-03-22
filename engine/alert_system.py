from core.event_bus import publish
from core.config import LOG_FILE
from engine.stats import stats
import datetime
import os
from collections import defaultdict
class AlertSystem:
    def __init__(self):

        # keep track of last alert times
        self.last_alert = defaultdict(dict)

        # cooldown time in seconds
        self.cooldown = 10

    def generate_alert(self, threat, packet_info):
        # stats.threat_seen()
        stats.alert_seen()
        src_ip = packet_info["source_ip"]

        now = datetime.datetime.now()

          # e.g. "[HIGH] DoS Attack"

        last = self.last_alert[src_ip].get(threat)

        if last:
            delta = (now - last).total_seconds()
            if delta < self.cooldown:
                return

        self.last_alert[src_ip][threat] = now

        message = f"{threat} detected from {src_ip}"

        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"[{timestamp}] {message}"

        # send alert to GUI
        publish("alert_event", log_entry)

        # ensure log directory exists
        os.makedirs("data", exist_ok=True)

        # write to log file
        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")