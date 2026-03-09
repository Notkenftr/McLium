from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP, UDP

from .print_port import print_ports

# The port scanning methods implemented below are based on the open-source project https://github.com/cptpugwash/Scapy-port-scanner
# , with additional modifications and optimizations applied.

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

def udp_scan(target, ports):
    open_port = []
    close_port = []
    filtered = []

    for port in ports:
        pkt = sr1(IP(dst=target)/UDP(dport=port), timeout=0.5, verbose=0)

        if pkt is None:
            open_port.append(port)
            print_ports(port, "Open / Filtered")

        else:
            if pkt.haslayer(ICMP):

                icmp_type = pkt[ICMP].type
                icmp_code = pkt[ICMP].code

                if icmp_type == 3 and icmp_code == 3:
                    close_port.append(port)
                    print_ports(port, "Closed")

                else:
                    filtered.append(port)
                    print_ports(port, "Filtered")

            elif pkt.haslayer(UDP):
                open_port.append(port)
                print_ports(port, "Open")

            else:
                print_ports(port, "Unknown resp")

    return open_port, close_port, filtered


def xmas_scan(target, ports):
    open_port = []
    close_port = []
    filtered = []

    sport = RandShort()

    for port in ports:
        pkt = sr1(
            IP(dst=target) /
            TCP(sport=sport, dport=port, flags="FPU"),
            timeout=0.3,
            verbose=0
        )

        if pkt is None:
            open_port.append(port)
            print_ports(port, "Open / Filtered")

        else:
            if pkt.haslayer(TCP):

                if pkt[TCP].flags == 20:
                    close_port.append(port)
                    print_ports(port, "Closed")

                else:
                    filtered.append(port)
                    print_ports(port, "Filtered")

            elif pkt.haslayer(ICMP):
                filtered.append(port)
                print_ports(port, "ICMP resp / Filtered")

            else:
                print_ports(port, "Unknown resp")

    return open_port, close_port, filtered
