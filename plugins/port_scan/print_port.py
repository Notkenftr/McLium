from rich.console import Console

console = Console()
def print_ports(port, state):
    if state == "Open":
        console.print(f"[green]OPEN[/green]      : {port}")

    elif state == "Closed":
        console.print(f"[red]CLOSED[/red]    : {port}")

    elif state == "Filtered":
        console.print(f"[yellow]FILTERED[/yellow]  : {port}")

    elif state == "Unanswered":
        console.print(f"[magenta]NO RESP[/magenta]  : {port}")

    else:
        console.print(f"[white]{state}[/white] : {port}")
