from mclium.api import SubCommandModule
from mclium.mclium_types import Flag
from .scan import syn_scan,udp_scan,xmas_scan

from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor

console = Console()

def format_ports(ports):
    return ", ".join(map(str, ports)) if ports else "-"

def print_summary(target, open_ports, closed_ports, filtered_ports, unknown_ports=None):
    if unknown_ports is None:
        unknown_ports = []

    console.print(
        Panel.fit(
            f"[bold cyan]Target:[/bold cyan] {target}",
            title="Port Scan Result"
        )
    )

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("State", width=12)
    table.add_column("Ports")

    table.add_row("[green]OPEN[/green]", format_ports(open_ports))
    table.add_row("[red]CLOSED[/red]", format_ports(closed_ports))
    table.add_row("[yellow]FILTERED[/yellow]", format_ports(filtered_ports))
    table.add_row("[magenta]UNKNOWN[/magenta]", format_ports(unknown_ports))

    console.print(table)

def print_single_port_summary(target, mode, ports):
    if ports is None:
        ports = []
    console.print(
        Panel.fit(
            f"[bold cyan]Target:[/bold cyan] {target}",
            title="Port Scan Result"
        )
    )
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("State", width=12)
    table.add_column("Ports")
    if mode == "open":
        table.add_row("[green]OPEN[/green]", format_ports(ports))
    if mode == "closed":
        table.add_row("[red]CLOSED[/red]", format_ports(ports))
    if mode == "filtered":
        table.add_row("[yellow]FILTERED[/yellow]", format_ports(ports))
    if mode == "unknown":
        table.add_row("[magenta]UNKNOWN[/magenta]", format_ports(ports))
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
        self.filtered_ports = None
        self.open_ports = None
        self.closed_ports = None
        self.type = None
        self.address = None

        flags = [
            Flag(
                "-a",
                "--address",
                type=str,
                required=True,
                help="Target address or IP",
            ),
            Flag(
                "-t",
                "--type",
                type=str,
                required=False,
                default="syn",
                help="Scan type (syn, udp, xmas)",
            ),
            Flag(
                "-w",
                "--workers",
                type=int,
                required=False,
                default=10,
                help="Number of worker threads",
            ),
            Flag(
                "-sp",
                "--start-port",
                type=int,
                required=False,
                default=19000,
                help="Start port",
            ),
            Flag(
                "-ep",
                "--end-port",
                type=int,
                required=False,
                default=30000,
                help="End port",
            )
        ]

        super().__init__("port_scan", flags)

    def on_command(self, args):
        self.address = args.address
        workers = args.workers
        self.type = args.type.lower()

        ports = list(range(args.start_port, args.end_port + 1))
        port_chunks = chunk_ports(ports, workers)

        self.open_ports = []
        self.closed_ports = []
        self.filtered_ports = []

        if self.type in ["tcp", "syn", "s"]:
            scan_func = syn_scan

        elif self.type in ["udp", "u"]:
            scan_func = udp_scan

        elif self.type in ["xmas", "x"]:
            scan_func = xmas_scan

        else:
            console.print(f"[red]Unsupported scan type: {self.type}[/red]")
            return

        with ThreadPoolExecutor(max_workers=workers) as executor:

            futures = [
                executor.submit(scan_func, self.address, chunk)
                for chunk in port_chunks
            ]

            for f in futures:
                o, c, fl = f.result()

                self.open_ports.extend(o)
                self.closed_ports.extend(c)
                self.filtered_ports.extend(fl)

        print_summary(
            self.address,
            self.open_ports,
            self.closed_ports,
            self.filtered_ports
        )
    def interactive(self,command):
        cmd = command.strip().lower()

        match cmd:
            case "-o" | "--open":
                print_single_port_summary(self.address, "open", self.open_ports)

            case "-c" | "--closed":
                print_single_port_summary(self.address, "closed", self.closed_ports)

            case "-f" | "--filtered":
                print_single_port_summary(self.address, "filtered", self.filtered_ports)

            case "-u" | "--unknown":
                print_single_port_summary(self.address, "unknown", [])

            case "-a" | "--all":
                print_summary(
                    self.address,
                    self.open_ports,
                    self.closed_ports,
                    self.filtered_ports
                )

            case "help":
                self.console.print("""
    [bold cyan]Available commands[/bold cyan]

    -o  --open       Show open ports
    -c  --closed     Show closed ports
    -f  --filtered   Show filtered ports
    -u  --unknown    Show unknown ports
    -a  --all        Show full summary
    exit             Exit module
    """)

            case _:
                self.console.print("[red]Unknown command[/red]")

