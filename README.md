````markdown
# SQLMap Automation Tool (Python Wrapper)

Automate SQL Injection vulnerability scanning and data extraction using SQLMap with this Python script.

---

## 🚀 Features

- Supports **GET** and **POST** requests.
- Accepts multiple IPs or domains.
- Optional **cookie** support.
- Automatically dumps databases if vulnerability is found.
- Works on **Windows** (using local `sqlmap.py`) and **Linux** (global `sqlmap`).
- Configurable crawling depth and threading.
- Integrates Tor for anonymity.

---

## 🧰 Requirements

- Python 3.x
- [SQLMap](https://github.com/sqlmapproject/sqlmap)
  - **Windows users**: Download and provide the path to `sqlmap.py`.
  - **Linux users**: Install via package manager or ensure `sqlmap` command is available.

---

## 🏁 Installation

### Clone the repository

```bash
git clone https://github.com/Mrjaiswal108/sqlmap_auto.git
cd sqlmap_auto
````

### (Optional) Create and activate Python virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### Install dependencies

No external Python packages needed beyond standard library, but ensure `sqlmap` is installed:

* **Linux**:

```bash
sudo apt install sqlmap
```

* **Windows**:

Download from [SQLMap GitHub](https://github.com/sqlmapproject/sqlmap) and provide the path to `sqlmap.py` when prompted.

---

## 🚦 Usage

Run the script:

```bash
python sqlmap_auto.py
```

You will be prompted to provide:

* **Target IPs or domains** (comma or space separated)
* **Path to sqlmap.py** (Windows only)
* **HTTP method**: GET or POST
* **POST data** (if applicable)
* **Crawl depth** (default: 5)
* **Number of threads** (default: 2)
* **Cookies** (optional, for authenticated sessions)

The script will:

1. Check if each target is vulnerable to SQL Injection using sqlmap.
2. If vulnerable, automatically dump all database contents.
3. Store output in timestamped directories under `sqlmap_op/`.

---

## 📝 How It Works

* For **Windows**, the script runs `sqlmap.py` directly via Python from the provided path.
* For **Linux**, the script runs `sqlmap` command assuming it is installed system-wide.
* Supports GET and POST injection vectors.
* Uses options like crawling, multi-threading, random user agent, Tor anonymization.
* Parses sqlmap output to detect vulnerability presence.
* Saves detailed output and dumps in organized folders with timestamps.

---

## 📂 Output

Results and database dumps are saved in:

```
sqlmap_op/sqlmap_<target_ip>_<timestamp>/
```

---

## ⚠️ Disclaimer

**Only test targets you own or have explicit permission to test.**

Unauthorized testing is illegal and unethical.

---

## 📚 License

MIT License

---

## 💡 Tips

* Use Tor to anonymize scans.
* Increase crawl depth and threads for thorough scanning.
* Combine with other pentesting tools for best results.

---

*Happy pentesting!* 🔐

```
```
