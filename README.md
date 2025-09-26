# 🕵️‍♂️ OSINT Scanner 

![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Last Commit](https://img.shields.io/github/last-commit/daradkeh69/osint-scanner)
[![Connect with me on LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](www.linkedin.com/in/daradkehh)

**Modular Python OSINT framework for person, company, and keyword reconnaissance with HTML reporting and API integrations.**

---

## ✨ Features

### 👤 Person Search
- Username checks via **Sherlock**, **Social Analyzer**, **WhatsMyName**, **Namechk**, **KnowEm**, and more  
- Email & domain reconnaissance (placeholders for **theHarvester**, **HIBP**, **Dehashed**)  
- Pastebin and breach lookups  
- Generates modern, interactive HTML reports  

### 🏢 Company / Organization Scan
- Integrates with **Shodan**, **WHOISXML**, and **Hunter.io** APIs  
- (Planned) **theHarvester** integration  
- Automated HTML reporting  

### 🔎 Passive Keyword Tracking *(Coming Soon)*
- RSS monitoring & alerting  
- Lightweight HTML tracking dashboards  

### ⚙️ Utilities
- **Tor / Proxy support** for anonymity  
- **Colorful CLI output**  
- **Timestamped reports** in neatly organized folders  

---
## Test on myself
![Test running the tool](test.png)

---
## 🚀 Installation

Clone the repository:
```bash
git clone https://github.com/daradkeh69/osint-scanner.git
cd osint-scanner
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Install recommended external tools: <br>
	•	Sherlock <br>
	•	Social Analyzer <br>
	•	WhatsMyName <br>
	•	theHarvester <br>

---

🔑 API Setup

Edit osint_scanner.py and replace placeholders with your API keys:

SHODAN_API_KEY   = "YOUR_SHODAN_API_KEY" <br>
WHOISXML_API_KEY = "YOUR_WHOISXML_API_KEY" <br>
HUNTER_API_KEY   = "YOUR_HUNTER_API_KEY" <br>
HIBP_API_KEY     = "YOUR_HIBP_API_KEY" <br>
DEHASHED_API_KEY = "YOUR_DEHASHED_API_KEY" <br>

---

📖 Usage

Run the tool:

```bash
python osint_scanner.py
```
You’ll see:

Advanced OSINT Intelligence Suite
1. Person Search
2. Company/Organization Scan
3. Passive Keyword Tracker
4. Exit

Examples:
	•	Person Search: enter a username, email, or domain
	•	Company Scan: enter a domain (e.g., example.com)
	•	Keyword Tracker: enter a keyword/subject

Reports are saved automatically in timestamped folders, e.g.:

person_reports/<date>_<id>/person_report.html


---

🧩 Extending & Customizing
	•	Add new modules/API integrations by following the structure in osint_scanner.py.
	•	Extend the save_report function to support new output formats (PDF, Markdown, etc).
	•	Wrap the CLI for batch automation or import functions into your own projects.

---

📦 Requirements
	•	Python 3.7+
	•	See requirements.txt for dependencies
	•	External tools (optional but recommended)

---

⚠️ Disclaimer

This project is for educational and authorized security research only.
Do not use it against systems/accounts you do not own or have explicit permission to test.

---

🤝 Contributing

Pull requests, feature suggestions, and bug reports are welcome!
Open an issue to discuss improvements before submitting a PR.

---

📜 License

MIT License

---

👨‍💻 Author: daradkeh69
[![Connect with me on LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](www.linkedin.com/in/daradkehh)
