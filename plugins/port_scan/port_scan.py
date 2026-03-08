import time
import socket
from mclium.api.mc_protocol.packet import Packet
from mclium.api import SubCommandModule
from mclium.mclium_types import Flag
from .syn_scan import syn_scan

from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor

console = Console()

def print_summary(target, open_ports, closed_ports, filtered_ports):
    table = Table(title="Scan Summary")

    table.add_column("State", justify="center")
    table.add_column("Count", justify="center")
    table.add_column("Ports")

    table.add_row(
        "[green]OPEN[/green]",
        str(len(open_ports)),
        ", ".join(map(str, open_ports)) if open_ports else "-"
    )

    table.add_row(
        "[red]CLOSED[/red]",
        str(len(closed_ports)),
        ", ".join(map(str, closed_ports)) if closed_ports else "-"
    )

    table.add_row(
        "[yellow]FILTERED[/yellow]",
        str(len(filtered_ports)),
        ", ".join(map(str, filtered_ports)) if filtered_ports else "-"
    )

    console.print(Panel.fit(
        f"[bold cyan]Target:[/bold cyan] {target}",
        title="Port Scan Result"
    ))

    console.print(table)
def chunk_ports(port_list, workers):
    size = len(port_list) // workers
    chunks = []

    for i in range(workers):
        start = i * size
        end = None if i == workers - 1 else (i + 1) * size
        chunks.append(port_list[start:end])

    return chunks
class Main(SubCommandModule):
    def __init__(self):
        flags = [
            Flag(
                "-a",
                "--address",
                type=str,
                required=True,
                help="Server address",
            ),
            Flag(
                short='-pt',
                long='--protocol',
                type=str,
                required=False,
                default="tcp",
            ),
            Flag(
                short='-w',
                long='--worker',
                type=int,
                required=False,
                default=10,
            ),
            Flag(
                short='-s',
                long='--start',
                type=int,
                required=False,
                default=19000,
            ),
            Flag(
                short='-e',
                long='--end',
                type=int,
                required=False,
                default=30000,
            )
        ]
        super().__init__('port_scan',flags)

    def on_command(self, args):
        address = args.address
        workers = args.worker

        ports = list(range(args.start, args.end + 1))

        port_chunks = chunk_ports(ports, workers)

        open_ports = []
        closed_ports = []
        filtered_ports = []

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(syn_scan, address, chunk)
                for chunk in port_chunks
            ]

            for f in futures:
                o, c, fl = f.result()
                open_ports.extend(o)
                closed_ports.extend(c)
                filtered_ports.extend(fl)

        print_summary(address, open_ports, closed_ports, filtered_ports)
