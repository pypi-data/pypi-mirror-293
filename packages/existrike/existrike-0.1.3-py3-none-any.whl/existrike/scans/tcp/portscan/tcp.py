import socket
import sys
import os
import time
import argparse
from datetime import datetime
print("""\033[91m
░░░░░░███████ ]▄▄▄▄▄▄▄▄
▂▄▅█████████▅▄▃▂
I███████████████████].
◥⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙◤...

𝐁𝐲 𝐄𝐱𝐩𝐢𝐫𝐚𝐯𝐢𝐭 𝐏𝐌𝐂\033[0;0m""")

def scan_ip(ip_address, show_closed_ports=0):
    print(f'Scanning IP \033[1;102m{ip_address}\033[0;0m')
    print('\033[46mScanning open ports:\033[0;0m')
    ports = [20, 21, 22, 23, 42, 43, 43, 69, 80, 109, 110, 115, 118, 143,
             156, 220, 389, 443, 465, 513, 514, 530, 547, 587, 636, 873,
             989, 990, 992, 993, 995, 1433, 1521, 2049, 2081, 2083, 2086,
             3306, 3389, 5432, 5500, 5800]
    try:
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((ip_address, port))
            if result == 0:
                print(f' \033[42;1;33m{port}\033[0;0m \033[42mis open\033[0;0m')
            else:
                if show_closed_ports == 0:
                    print(f' \033[42;1;41m{port}\033[0;0m \033[1;41mis closed\033[0;0m')
            sock.close()
    except KeyboardInterrupt:
        print('You exited the script')
        sys.exit()
    except socket.gaierror:
        print('Host not found.')
        sys.exit()
    except socket.error:
        print('Unable to connect to server')
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Port Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL or domain')
    args = parser.parse_args()

    server_ip = socket.gethostbyname(args.url)
    t1 = datetime.now()

    scan_ip(server_ip)
    t2 = datetime.now()
    total = t2 - t1
    print(f'\033[93mScan completed in:\033[0;0m {total} \033[34mseconds\033[0;0m')
