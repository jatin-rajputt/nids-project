from scapy.all import sniff

def pkt(p):
    print(p.summary())

sniff(prn=pkt, store=0)