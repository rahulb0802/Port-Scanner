import socket
import threading
import ipaddress
from tqdm import tqdm

def scan_port(ip, port, op, protocol):
    # Checking whether it's IPv4 or IPv6
    if ':' in ip:
        type = socket.AF_INET6
    else:
        type = socket.AF_INET
    if protocol == 'udp':
        scanner = socket.socket(type, socket.SOCK_DGRAM)
    else:
        scanner = socket.socket(type, socket.SOCK_STREAM)
    
    scanner.settimeout(1)

    # Displaying different results based on user input
    global result
    result = scanner.connect_ex((ip, port))
    if op == 'o':
        find_open_ports(ip, port)
    elif op == 'c':
        find_closed_ports(ip, port)
    else:
        find_open_ports(ip, port)
        find_closed_ports(ip, port)
    scanner.close()

def find_open_ports(ip, port):
    if result == 0:
        try:
            service = socket.getservbyport(port) # Getting service
            scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scanner.settimeout(2)
            scanner.connect((ip, port))
            banner = scanner.recv(1024).decode().strip() # Fetching banner
        except:
            service = 'Unknown'
            banner = 'No banner'
        print(f"Port {port} is open on {ip} (Service: {service}, Banner: {banner})")

def find_closed_ports(ip, port):
    if result != 0:
        print(f"Port {port} is closed on {ip}")

    

def scan_multiple_ports(ip, start, end):
    threads = []
    option = input('Enter option (o for open, c for closed, a for all):')
    protocol = input('Enter protocol (tcp/udp):').lower()

    # Threading to scan ports much faster (multiple ongoing processes)
    for port in tqdm(range(start, end + 1)):
        thread = threading.Thread(target=scan_port, args=(ip, port, option, protocol))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip) # Checking for valid IP
        return True
    except:
        print("Invalid IP address")
        return False

def main():
    target = input('Enter IP:')

    while not validate_ip(target):
        target = input('Enter IP:')

    num = input('Range or single port? (r/s)')
    
    
    if num == 'r':
        start = int(input('Enter start port:'))
        end = int(input('Enter end port:'))
        scan_multiple_ports(target, start, end)
    if num == 's':
        protocol = input('Enter protocol (tcp/udp):').lower()
        port = int(input('Enter port:'))
        scan_port(target, port, 'a', protocol)

main()