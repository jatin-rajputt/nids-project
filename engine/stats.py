import time
from collections import deque


class IDSStats:

    def __init__(self):

        self.total_packets = 0
        self.total_alerts = 0
        self.threat_history =[]
        self.packet_times = deque()

        self.packet_rate_history = []
        
        self.alert_times = deque()
        self.alert_rate_history =[]

    def packet_seen(self):

        now = time.time()

        self.total_packets += 1

        self.packet_times.append(now)

        # keep last second
        while self.packet_times and now - self.packet_times[0] > 1:
            self.packet_times.popleft()

        packets_per_sec = len(self.packet_times)

        self.packet_rate_history.append(packets_per_sec)

        if len(self.packet_rate_history) > 60:
            self.packet_rate_history.pop(0)
            
     
    def get_rates(self):
        now = time.time()
        
        packets = len([t for t in self.packet_times if now -t <=1]) 
        alerts = len([t for t in self.alert_times if now -t <= 1])
        
        return packets, alerts      
    def alert_seen(self):
        now = time.time()
        self.total_alerts += 1
        self.alert_times.append(now)
        
        while self.alert_times and now - self.alert_times[0] > 1:
            self.alert_times.popleft()
            
        alerts_per_sec = len(self.alert_times)
        self.alert_rate_history.append(alerts_per_sec)
        
        if len(self.alert_rate_history) > 60:
            self.alert_rate_history.pop(0)

    def get_packet_history(self):

        return self.packet_rate_history
    
    def get_alert_history(self):
        return self.alert_rate_history


stats = IDSStats()