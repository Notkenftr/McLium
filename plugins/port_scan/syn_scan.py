from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP

from .print_port import print_ports

def syn_scan(target, ports):
    open_port = []
    close_port = []
    filtered = []
    sport = RandShort()

    for port in ports:
        pkt = sr1(IP(dst=target)/TCP(sport=sport, dport=port, flags="S"), timeout=0.3, verbose=0)

        if pkt is not None:
            if pkt.haslayer(TCP):
                if pkt[TCP].flags == 20:
                    close_port.append(port)
                    print_ports(port, "Closed")

                elif pkt[TCP].flags == 18:
                    open_port.append(port)
                    print_ports(port, "Open")

                else:
                    filtered.append(port)
                    print_ports(port, "TCP packet resp / filtered")

            elif pkt.haslayer(ICMP):
                print_ports(port, "ICMP resp / filtered")

            else:
                print_ports(port, "Unknown resp")

        else:
            print_ports(port, "Unanswered")
    return open_port, close_port, filtered
