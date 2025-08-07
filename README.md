# Network Security Scanner

A comprehensive Python-based network security scanner that provides multiple scanning capabilities for network reconnaissance and security assessment.

## Features

### 🌐 Network Discovery
- **ARP Scanning**: Discover active devices on your local network
- **Host Information**: Retrieve IP addresses, MAC addresses, and hostnames
- **CIDR Support**: Scan entire network ranges using CIDR notation

### 🔍 Port Scanning
- **TCP Port Scanning**: Scan specified port ranges on target hosts
- **Service Detection**: Identify services running on open ports
- **Banner Grabbing**: Capture service banners for additional information
- **Multi-threaded**: Fast scanning with concurrent thread execution
- **Progress Tracking**: Real-time scan progress display

### 🌍 Subdomain Enumeration
- **Subdomain Discovery**: Find active subdomains for target domains
- **Wordlist-based**: Uses customizable wordlist for comprehensive scanning
- **Result Export**: Saves discovered subdomains to file for further analysis

## Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Required Dependencies
Install the required packages using pip:

```bash
pip install scapy requests
```

### Additional Requirements
- **Linux/macOS**: May require sudo privileges for ARP scanning
- **Windows**: Install Npcap or WinPcap for Scapy functionality

## Usage

Run the scanner with:
```bash
python scanner.py
```

### Interactive Menu
The scanner provides an interactive menu with the following options:

```
1) Network Scan
2) Port Scan
3) Subdomain Enumeration
4) Quit
```

### 1. Network Scanning
- Enter a network range in CIDR notation (e.g., `192.168.1.0/24`)
- Discovers all active devices on the specified network
- Displays IP addresses, MAC addresses, and hostnames

**Example:**
```
Enter network ip address: 192.168.1.0/24
```

### 2. Port Scanning
- Enter target IP address (defaults to `127.0.0.1`)
- Specify start and end port range
- Scans for open TCP ports and identifies services

**Example:**
```
Enter your target ip: 192.168.1.100
Enter the start port: 1
Enter end port: 1000
```

### 3. Subdomain Enumeration
- Enter target domain (defaults to `youtube.com`)
- Requires a `subdomains.txt` wordlist file in the same directory
- Saves discovered subdomains to `discovered_subdomain.txt`

**Example:**
```
Enter the name of the website: example.com
```

## File Structure

```
network-scanner/
├── scanner.py              # Main scanner script
├── subdomains.txt         # Subdomain wordlist (required for option 3)
├── discovered_subdomain.txt # Output file for discovered subdomains
└── README.md              # This file
```

## Output Examples

### Network Scan Results
```
IP                    MAC                    Hostname
--------------------------------------------------------------------------------
192.168.1.1          aa:bb:cc:dd:ee:ff      router.local
192.168.1.100        11:22:33:44:55:66      desktop-pc
```

### Port Scan Results
```
Port     Service         Status
---------------------------------------------------------------------------------
22       ssh             Open
        SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
80       http            Open
        Apache/2.4.41 (Ubuntu)
```

## Configuration

### Subdomain Wordlist
Create/Download a `subdomains.txt` file with common subdomain names:
```
www
mail
ftp
admin
test
dev
api
```

### Threading Configuration
- **Network Scan**: One thread per IP address
- **Port Scan**: Up to 1000 concurrent threads
- **Subdomain Enum**: One thread per subdomain

## Legal Disclaimer

⚠️ **IMPORTANT**: This tool is intended for educational purposes and authorized security testing only.

- Only use this scanner on networks and systems you own or have explicit permission to test
- Unauthorized network scanning may violate local laws and regulations
- Users are solely responsible for complying with applicable laws
- The authors are not responsible for any misuse of this tool

## Limitations

- **Network Scanning**: Limited to local network segments (ARP-based)
- **Port Scanning**: TCP ports only (no UDP support)
- **Banner Grabbing**: 1-second timeout may miss some services
- **Subdomain Enumeration**: HTTP-only checking (no HTTPS validation)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Potential Improvements
- Add UDP port scanning support
- Implement HTTPS support for subdomain enumeration
- Add XML/JSON export options
- Include vulnerability scanning capabilities
- Add stealth scanning modes

---

**Remember**: Always obtain proper authorization before scanning networks or systems you do not own.
