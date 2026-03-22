import time
from collections import defaultdict

from core.config import PORT_SCAN_THRESHOLD, DOS_THRESHOLD,TIME_WINDOW,BRUTE_FORCE_PORTS,BRUTE_FORCE_THRESHOLD
from scapy.layers.inet import TCP
class DetectionEngine:
    def __init__(self):
        self.port_tracker= defaultdict(list)
        self.traffic_tracker = defaultdict(list)
        self.bruteforce_tracker = defaultdict(list)
        self.last_alert_time = {}
        self.ALERT_COOLDOWN = 10
        
    def detect_threats(self, features):
        threats = []
        
        src = features["src_ip"]
        port = features["dst_port"]
        
        now= time.time()
        
        # ------------------
# Port Scan Detection
# ------------------

        if features["syn"] and port is not None:

            key = (src, features["dst_ip"])

            self.port_tracker[key].append((port, now))

            # remove old entries
            self.port_tracker[key] = [
                (p, t) for p, t in self.port_tracker[key]
                if now - t < TIME_WINDOW
            ]

            unique_ports = set(p for p, t in self.port_tracker[key])

            if len(unique_ports) >= PORT_SCAN_THRESHOLD:

                last = self.last_alert_time.get(src, 0)

                if now - last > self.ALERT_COOLDOWN:

                    threats.append("[LOW] Port Scan")

                    self.last_alert_time[src] = now
                
        self.traffic_tracker[src].append(now)
        
        self.traffic_tracker[src] = [
            t for t in self.traffic_tracker[src]
            if now - t < TIME_WINDOW
        ]
        
        if len(self.traffic_tracker[src]) > DOS_THRESHOLD :
            last = self.last_alert_time.get(src, 0)
            if now - last > self.ALERT_COOLDOWN:

                threats.append("[HIGH] DoS Attack")

                self.last_alert_time[src] = now
            
        self.traffic_tracker[src].append(now)
        
        self.traffic_tracker[src] = [
            t for t in self.traffic_tracker[src]
            if now - t < TIME_WINDOW
        ]
            
        
        if port in BRUTE_FORCE_PORTS:

            self.bruteforce_tracker[src].append(now)

            self.bruteforce_tracker[src] = [
                t for t in self.bruteforce_tracker[src]
                if now - t < TIME_WINDOW
            ]

            if len(self.bruteforce_tracker[src]) > BRUTE_FORCE_THRESHOLD:
                threats.append("[MEDIUM] Brute Force Attack")
            
        return threats