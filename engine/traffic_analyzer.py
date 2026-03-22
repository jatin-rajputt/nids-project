from scapy.all import IP, TCP
class TrafficAnalyzer:
    
    def analyze_packet(self, packet):
    
        if not packet.haslayer(IP):
            return None
    
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
    
        port = None
        syn_flag = False
        if packet.haslayer(TCP):
            port = packet[TCP].dport
            
            if packet[TCP].flags == "S":
                syn_flag = True
        return {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "dst_port": port,
            "syn": syn_flag
        }