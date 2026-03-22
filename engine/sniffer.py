from scapy.all import sniff, IP, TCP, UDP

from engine.detection import detect_port_scan, detect_dos
from  engine.stats import stats
from core.event_bus import publish

running = False

def process_packet(packet):
    if packet.haslayer(IP):
        
        src = packet[IP].src
        dst = packet[IP].dst
        
        
        stats.packet_seen()
        
        publish("traffic_event", f"{src} -> {dst}")
        
        detect_dos(src)
        
        if packet.haslayer(TCP):
            dst_port = packet[TCP].dport
            
            detect_port_scan(src, dst_port)
        elif packet.haslayer(UDP):
            dst_port = packet[UDP].dport
            
def start_sniffer(interface):
    
    global running
    
    running = True
    print("Sniffer started on interface:", interface)

    sniff(
        iface= interface,
        prn=process_packet,
        store=False,
        filter="ip",
        stop_filter= lambda x: not running
        
    )

def stop_sniffer():
    global running
    running = False
    print("Sniffer stopped")