import socket

import psutil


def norm(ip):
    return ip.replace("::ffff:", "").strip()


def find_process(server_address, server_port):
    try:
        addr_info = socket.getaddrinfo(server_address, server_port)
        target_ips = {norm(info[4][0]) for info in addr_info}
    except Exception as e:
        print(f"[Error] DNS Lookup failed: {e}")
        return None, None, None

    try:
        connections = psutil.net_connections(kind='inet')
    except psutil.AccessDenied:
        connections = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                connections.extend(proc.connections(kind='inet'))
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue

    for conn in connections:
        if not conn.raddr:
            continue

        current_r_ip = norm(conn.raddr.ip)

        if current_r_ip in target_ips and conn.raddr.port == server_port:
            pid = conn.pid
            return pid, conn.raddr, conn.laddr

    return None, None, None
