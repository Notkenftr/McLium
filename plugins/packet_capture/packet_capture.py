import os.path
from datetime import datetime
from scapy.packet import Raw

from mclium.api import SubCommandModule
from mclium.mclium_types import Flag
from plugins.packet_capture.find_process import find_process

from scapy.layers.inet import TCP,IP
from scapy.all import sniff

class Main(SubCommandModule):
    def __init__(self):
        flags = [
            Flag(
                "-a",
                "--address",
                type=str,
                default=None,
            ),
            Flag(
                "-p",
                "--port",
                type=int,
                default=None,
            ),
            Flag(
                '-o',
                '--output',
                type=str,
                default=None,
            ),
            Flag(
                '-sd',
                '--show_direction',
                type=bool,
                default=True,
            )
        ]
        super().__init__(name='packet_capture',flags=flags)

    def on_command(self, args):
        address = args.address
        port = args.port
        output_file = os.path.expanduser(args.output)
        print("[PacketCapture] waiting for packet")
        print(f"[PacketCapture] Save at {output_file}")

        with open(output_file,'a') as f:
            f.write("McLium Packet Capture\n"
                    f"Capture at: {datetime.now()}\n\n")

        while True:
            pid, raddr, laddr = find_process(address, port)

            if raddr is not None:
                break

        def match(pkt):
            if IP in pkt and TCP in pkt:
                src_ip = pkt[IP].src
                dst_ip = pkt[IP].dst
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport

                def norm(ip):
                    return ip.replace("::ffff:", "") if ip.startswith("::ffff:") else ip

                src_ip = norm(src_ip)
                dst_ip = norm(dst_ip)

                local_ip = norm(laddr.ip)
                remote_ip = norm(raddr.ip)

                if (src_ip == local_ip and dst_ip == remote_ip) or (src_ip == remote_ip and dst_ip == local_ip):
                    return True

                if (
                    src_ip == remote_ip and
                    dst_ip == local_ip and
                    sport == raddr.port and
                    dport == laddr.port
                ):
                    return True

            return False

        def handle(pkt):
            if pkt.haslayer(Raw):

                src_ip = pkt[IP].src
                src_port = pkt[TCP].sport

                if src_ip == address and src_port == port:
                    direction = "S2C"
                else:
                    direction = "C2S"

                raw_payload = pkt[Raw].load
                print(f"[PacketCapture] {repr(raw_payload)}")
                if output_file:
                    with open(output_file, 'a') as f:
                        if args.show_direction:
                            f.write(f"{direction} > {repr(raw_payload)}\n")
                        else:
                            f.write(f"{repr(raw_payload)}\n")


        sniff(filter="tcp",prn=handle,lfilter=match)
