from scapy.all import IP
import queue
import threading

from engine.packet_capture import PacketCapture
from engine.traffic_analyzer import TrafficAnalyzer
from engine.detection import DetectionEngine
from engine.alert_system import AlertSystem
from engine.stats import stats
from core.event_bus import publish
from gui.dashboard import start_dashboard


class IntrusionDetectionSystem:

    def __init__(self):

        self.packet_capture = PacketCapture()
        self.traffic_analyzer = TrafficAnalyzer()
        self.detection_engine = DetectionEngine()
        self.alert_system = AlertSystem()

        self.thread = None

    def start(self, interface):

        self.stop()

        self.thread = threading.Thread(
            target=self.run_ids,
            args=(interface,),
            daemon=True
        )

        self.thread.start()

    
    def run_ids(self, interface):

        self.packet_capture.start_capture(interface)

        while True:

            try:

                packet = self.packet_capture.packet_queue.get(timeout=1)
                

                stats.packet_seen()

                if packet.haslayer(IP):

                    publish(
                        "traffic_event",
                        f"{packet[IP].src} -> {packet[IP].dst}"
                    )

                features = self.traffic_analyzer.analyze_packet(packet)

                if features:

                    threats = self.detection_engine.detect_threats(features)
                    

                    for threat in threats:

                        packet_info = {
                            "source_ip": packet[IP].src,
                            "destination_ip": packet[IP].dst
                        }

                        self.alert_system.generate_alert(threat, packet_info)

            except queue.Empty:
                continue

    def stop(self):
        
        if self.packet_capture:
            self.packet_capture.stop()
            
        self.thread = None


ids = IntrusionDetectionSystem()


def start_ids(interface):

    ids.start(interface)


def stop_ids():

    ids.stop()


if __name__ == "__main__":

    start_dashboard(start_ids, stop_ids)