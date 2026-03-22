from scapy.all import AsyncSniffer
import queue


class PacketCapture:

    def __init__(self):

        self.packet_queue = queue.Queue()
        self.sniffer = None
        self.interface = None

    def packet_handler(self, packet):

        self.packet_queue.put(packet)

    def start_capture(self, interface):

        # stop old sniffer if running
        if self.sniffer and self.sniffer.running:
            self.sniffer.stop()
            
        self.packet_queue = queue.Queue()

        print("Starting capture on:", interface)

        self.interface = interface

        self.sniffer = AsyncSniffer(
            iface=self.interface,
            prn=self.packet_handler,
            store=False
        )

        self.sniffer.start()

    def stop(self):

        if self.sniffer and self.sniffer.running:

            print("Stopping capture")

            self.sniffer.stop()
            
        self.sniffer = None