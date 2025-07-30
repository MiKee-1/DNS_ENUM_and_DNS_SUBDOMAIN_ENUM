# DNS_ENUM_and_DNS_SUBDOMAIN_ENUM


## 🔍 DNS & Subdomain Enumeration Toolkit

This repository contains two lightweight Python scripts designed to perform DNS record enumeration and subdomain discovery for a given domain. These tools are useful for cybersecurity research, penetration testing, and general reconnaissance tasks.

### 📁 Contents

* **`dns_enum.py`**
  Enumerates DNS records (`A`, `AAAA`, `CNAME`, `MX`, `TXT`, `SOA`) for a target domain using the `dnspython` library.

* **`subdomain_enum.py`**
  Performs multithreaded subdomain enumeration by checking a list of potential subdomains against the target domain using HTTP requests.

### 📌 Features

* Retrieves common DNS record types for a domain.
* Checks live subdomains based on a wordlist (`subdomains.txt`).
* Uses threading for faster subdomain discovery.
* Saves discovered subdomains to `discovered_subdomain.txt`.

### ⚙️ Requirements

* Python 3.x
* `dnspython`
* `requests`

Install dependencies with:

```bash
pip install dnspython requests
```

### 🛠 Usage

Run DNS enumeration:

```bash
python dns_enum.py
```

Run subdomain enumeration:

```bash
python subdomain_enum.py
```

> ⚠️ Ensure the `subdomains.txt` file is present in the `DNS_ENUM` directory.


