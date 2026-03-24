import os.path
import time

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
            )
        ]
        super().__init__(name='packet_capture',flags=flags)

    def on_command(self, args):
        address = args.address
        port = args.port
        output_file = os.path.expanduser(args.output)
        print("[PacketCapture] waiting for packet")
        print(f"[PacketCapture] Save at {output_file}")

        while True:
            pid, raddr, laddr = find_process(address, port)

            if raddr is not None:
                print(f"[PacketCapture] {laddr} -> {raddr} ({pid})")
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
            if IP in pkt and TCP in pkt:
                dst_ip = pkt[IP].dst
                src_ip = pkt[IP].src

                dst_port = pkt[TCP].dport
                src_port = pkt[TCP].sport

                print(f"From {src_ip}:{src_port} -> To {dst_ip}:{dst_port}")

                raw = bytes(pkt)
                print(raw)

                if output_file:
                    with open(output_file, 'ab') as f:
                        f.write(raw + b'\n')


        sniff(filter="tcp",prn=handle,lfilter=match)
