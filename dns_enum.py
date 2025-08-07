import scapy.all as scapy
import socket
import threading
from queue import Queue
import ipaddress
import concurrent.futures
import sys
import requests
import os


def scan(ip, result_queue):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_request
    answer = scapy.srp(packet, timeout=1, verbose=False)[0]

    clients = []
    for client in answer:
        client_info = {'IP': client[1].psrc, 'MAC': client[1].hwsrc}
        try:
            hostname = socket.gethostbyaddr(client_info['IP'])[0]
            client_info['Hostname'] = hostname
        except socket.herror:
            client_info['Hostname'] = 'Unknown'
        clients.append(client_info)
    result_queue.put(clients)

def print_result(result):
    print('IP' + " "*20 + 'MAC' + " "*20 + 'Hostname')
    print('-'*80)
    for client in result:
        print(client['IP'] + '\t\t' + client['MAC'] + '\t\t' + client['Hostname'])

def main(cidr):
    results_queue = Queue()
    threads = []
    try:
        network = ipaddress.ip_network(cidr, strict=False)

        for ip in network.hosts():
            thread = threading.Thread(target=scan, args=(str(ip), results_queue))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        all_clients = []
        while not results_queue.empty():
            all_clients.extend(results_queue.get())
        
        print_result(all_clients)
    except Exception:
        print("Invalid IP or Impossible to scan. Try 192.168.1.0/24 if you are in your local network. . .")

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def format_port_results(results):
    formatted_results = "Port Scan Result:\n"
    formatted_results += "{:<8} {:15} {:<10}\n".format("Port","Service","Status")
    formatted_results += '-'*85 + "\n"
    for port,service,banner,status in results:
        if status:
            formatted_results = f"{RED}{port:<8} {service:<15} {'Open':<10}{RESET}\n"
            if banner:
                banner_lines = banner.split('\n')
                for line in banner_lines:
                    formatted_results += f"{GREEN}{'':<8}{line}{RESET}\n"

    return formatted_results
    

def get_banner(sock):
    try:
        sock.settimeout(1)
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return ""

def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #if the port will not respond in one second then the port is closed
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                service = 'Unknown'
            banner = get_banner(sock)
            return port, service, banner, True
        else:
            return port, "", "", False
    
    except:
         return port, "", "", False
    finally:
        sock.close()

def port_scan(target_host, start_port, end_port):
    target_ip = socket.gethostbyname(target_host)
    print(f"Starting scan on host: {target_ip}")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in range(start_port, end_port+1)}
        total_ports = end_port - start_port + 1
        for i,future in enumerate(concurrent.futures.as_completed(futures), start=1):
            port, service, banner, status = future.result()
            results.append((port, service, banner, status))
            sys.stdout.write(f"\rProgress: {i}/{total_ports} ports scanned")
            sys.stdout.flush()

    sys.stdout.write("\n")
    print(format_port_results(results))

def check_subdomains(subdomain, domain, lock, discovered_subdomains):
    url = f'http://{subdomain}.{domain}'
    try:
        requests.get(url)
    except requests.ConnectionError:
        pass
    else:
        print("[+] last discorvered subdomain: "+url)
        with lock:
            discovered_subdomains.append(url)

if __name__ == "__main__":
   
    while(True):
        try:
            choice = int(input("1) Network Scan \n2) Port Scan\n3) Subdomain Enumeration \n4) Quit\nSelect: "))
            if choice == 1:
                cidr = input("Enter network ip address: ")
                main(cidr)
            elif choice == 2:
                target_host = input("Enter your target ip (default is 127.0.0.1): ")
                if target_host == "":
                    target_host = '127.0.0.1'

                try:
                    start_port = int(input("Enter the start port: "))
                except Exception:
                    start_port = 1

                try:
                    end_port = int(input("Enter end port: "))
                except Exception:
                    end_port = 10000
                
                port_scan(target_host, start_port, end_port)
            
            elif choice ==3:
                domain = input("Enter the name of the website (default youtube.com): ")
                if domain == "":
                    domain = 'youtube.com'

                with open('.\subdomains.txt') as file:
                    subdomains = file.read().splitlines()

                discovered_subdomains = []
                lock = threading.Lock()
                threads = []

                for subdomain in subdomains:
                    thread = threading.Thread(target=check_subdomains, args=(subdomain, domain, lock, discovered_subdomains))
                    thread.start()
                    threads.append(thread)

                for thread in threads:
                    thread.join()

                with open(os.path.join('.','discovered_subdomain.txt'), 'w') as f:
                    for subdomain in discovered_subdomains:
                        print(subdomain, file=f)
            
            elif choice == 4:
                print("Exiting . . .")
                exit(0)
                
            else:
                print("Error, select 1 for Network Scanning or 2 for Port Scanning, 3 for quit.")

        except KeyboardInterrupt:
            print("Keyboard Interrupt, Exiting . . .")
            exit(0)
        except Exception:
            print("Error, try something else.")    
