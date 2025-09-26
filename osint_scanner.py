import os
import sys
import time
import requests
import json
import subprocess
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# === CONFIGURATION ===
PROXY = None  # e.g., "socks5h://127.0.0.1:9050" for Tor
USE_TOR = False
SHODAN_API_KEY = "YOUR_SHODAN_API_KEY"
WHOISXML_API_KEY = "YOUR_WHOISXML_API_KEY"
HUNTER_API_KEY = "YOUR_HUNTER_API_KEY"
HIBP_API_KEY = "YOUR_HIBP_API_KEY"
DEHASHED_API_KEY = "YOUR_DEHASHED_API_KEY"
# ...add other API keys as needed...

# === UTILITY FUNCTIONS ===
def color_print(msg, color=Fore.WHITE):
    print(f"{color}{msg}{Style.RESET_ALL}")

def save_report(data, folder, filename, fmt="html"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{filename}.html")
    # Prepare data for pretty HTML rendering
    def render_value(val):
        if isinstance(val, dict):
            # Special handling for Namechk/KnowEm URLs
            if all(isinstance(v, str) and v.startswith("http") for v in val.values()):
                return '<ul>' + ''.join(f'<li><a href="{v}" target="_blank">{k}</a></li>' for k, v in val.items()) + '</ul>'
            return '<ul>' + ''.join(f'<li><b>{k}:</b> {render_value(v)}</li>' for k, v in val.items()) + '</ul>'
        elif isinstance(val, list):
            return '<ul>' + ''.join(f'<li>{render_value(v)}</li>' for v in val) + '</ul>'
        elif isinstance(val, str) and val.startswith("http"):
            return f'<a href="{val}" target="_blank">{val}</a>'
        else:
            return str(val)
    try:
        parsed = json.loads(data) if isinstance(data, str) else data
    except Exception:
        parsed = data
    html = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <title>OSINT Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6fa; color: #222; margin: 0; padding: 0; }}
            .container {{ max-width: 900px; margin: 40px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 12px #0001; padding: 32px; }}
            h1 {{ color: #4B0082; margin-top: 0; }}
            h2 {{ color: #333; border-bottom: 1px solid #eee; padding-bottom: 4px; }}
            ul {{ padding-left: 1.2em; }}
            li {{ margin-bottom: 0.5em; }}
            pre {{ background: #f6f8fa; padding: 1em; border-radius: 5px; overflow-x: auto; font-size: 1em; }}
            .section {{ margin-bottom: 2em; }}
            a {{ color: #1a0dab; text-decoration: underline; word-break: break-all; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>OSINT Report</h1>
            <div class='section'>
                <h2>Data</h2>
                {render_value(parsed)}
            </div>
        </div>
    </body>
    </html>
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    color_print(f"Report saved to {path}", Fore.GREEN)

def get_timestamp_folder(base):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join(base, ts)
    os.makedirs(folder, exist_ok=True)
    return folder

def run_subprocess(cmd, use_tor=False):
    env = os.environ.copy()
    if use_tor:
        env["ALL_PROXY"] = "socks5h://127.0.0.1:9050"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env, timeout=300)
        return result.stdout
    except Exception as e:
        color_print(f"Error running subprocess: {e}", Fore.RED)
        return ""

def requests_session():
    session = requests.Session()
    if USE_TOR:
        session.proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
    elif PROXY:
        session.proxies = {"http": PROXY, "https": PROXY}
    return session

# === PERSON SEARCH MODULE ===
def sherlock_search(username):
    color_print(f"Running Sherlock for {username}...", Fore.CYAN)
    try:
        output = run_subprocess(f"sherlock {username} --print-found")
        if not output.strip():
            return "No results or Sherlock not installed."
        return output
    except Exception as e:
        return f"Sherlock error: {e}"

# --- Social Analyzer integration (placeholder) ---
def social_analyzer_search(query):
    color_print(f"[Social Analyzer] See https://github.com/qeeqbox/social-analyzer", Fore.CYAN)
    # You can run Social Analyzer via CLI or Web UI. Example CLI usage:
    #   social-analyzer -u <username> -p all --json
    # For now, just return a link to the project and a suggested command.
    return f"Run Social Analyzer for '{query}': https://github.com/qeeqbox/social-analyzer"

# --- WhatsMyName integration (placeholder) ---
def whatsmyname_search(username):
    color_print(f"[WhatsMyName] See https://github.com/WebBreacher/WhatsMyName", Fore.CYAN)
    # WhatsMyName is a database and CLI for username checks.
    # Example CLI usage:
    #   python whatsmyname.py -u <username>
    return f"Check WhatsMyName for '{username}': https://github.com/WebBreacher/WhatsMyName"

# --- Namechk/KnowEm (web) integration (placeholder) ---
def namechk_search(username):
    color_print(f"[Namechk/KnowEm] Web search for username availability.", Fore.CYAN)
    # These are web services, so just return the search URLs.
    return {
        'Namechk': f"https://namechk.com/{username}",
        'KnowEm': f"https://knowem.com/checkusername/{username}"
    }

def pastebin_search(query):
    color_print(f"Searching Pastebin for {query}...", Fore.CYAN)
    # Placeholder: Use public Pastebin crawlers or scraping
    return f"https://www.google.com/search?q={query}+site:pastebin.com"

def person_search(query):
    results = {}
    folder = get_timestamp_folder("person_reports")
    # Sherlock
    sherlock_out = sherlock_search(query)
    results['sherlock'] = sherlock_out
    # Social Analyzer
    results['social_analyzer'] = social_analyzer_search(query)
    # WhatsMyName
    results['whatsmyname'] = whatsmyname_search(query)
    # Namechk/KnowEm
    results['namechk'] = namechk_search(query)
    # theHarvester (if email or domain)
    if "@" in query or "." in query:
        harvester_out = theharvester_search(query)
        results['theHarvester'] = harvester_out
    # Breach checks
    if "@" in query:
        hibp_out = hibp_search(query)
        results['hibp'] = hibp_out if hibp_out else "No breaches found or API error."
        dehashed_out = dehashed_search(query)
        results['dehashed'] = dehashed_out if dehashed_out else "No results or Dehashed API error."
    # Pastebin
    results['pastebin'] = pastebin_search(query)
    # Save reports
    try:
        save_report(json.dumps(results, indent=2, default=str), folder, "person_report", "html")
    except Exception as e:
        color_print(f"Error saving report: {e}", Fore.RED)
    return results

# Placeholders for theHarvester, HIBP, and Dehashed integrations
def theharvester_search(query):
    color_print(f"[theHarvester] Not implemented. See https://github.com/laramies/theHarvester", Fore.CYAN)
    return "theHarvester integration not implemented."

def hibp_search(query):
    color_print(f"[HaveIBeenPwned] Not implemented. See https://haveibeenpwned.com/API/v3", Fore.CYAN)
    return "HIBP integration not implemented."

def dehashed_search(query):
    color_print(f"[Dehashed] Not implemented. See https://www.dehashed.com/docs/api", Fore.CYAN)
    return "Dehashed integration not implemented."

# === COMPANY/ORG SCAN MODULE ===
def shodan_scan(domain):
    color_print(f"Querying Shodan for {domain}...", Fore.CYAN)
    url = f"https://api.shodan.io/dns/domain/{domain}?key={SHODAN_API_KEY}"
    session = requests_session()
    resp = session.get(url)
    if resp.status_code == 200:
        return resp.json()
    return {}

def whoisxml_scan(domain):
    color_print(f"Querying WHOISXML for {domain}...", Fore.CYAN)
    url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={WHOISXML_API_KEY}&domainName={domain}&outputFormat=JSON"
    session = requests_session()
    resp = session.get(url)
    if resp.status_code == 200:
        return resp.json()
    return {}

def hunterio_scan(domain):
    color_print(f"Querying Hunter.io for {domain}...", Fore.CYAN)
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
    session = requests_session()
    resp = session.get(url)
    if resp.status_code == 200:
        return resp.json()
    return {}

def company_scan(domain):
    results = {}
    folder = get_timestamp_folder("company_reports")
    results['shodan'] = shodan_scan(domain)
    results['whoisxml'] = whoisxml_scan(domain)
    results['hunterio'] = hunterio_scan(domain)
    # theHarvester for emails/domains
    results['theHarvester'] = theharvester_search(domain)
    # Save reports
    save_report(json.dumps(results, indent=2), folder, "company_report", "html")
    # Optionally generate HTML and screenshots/graphs here
    return results

# === KEYWORD TRACKER MODULE ===
def rss_monitor(keyword, folder):
    color_print(f"Monitoring RSS feeds for {keyword}...", Fore.CYAN)
    # Placeholder: Use feedparser or similar to monitor RSS feeds
    # Optionally integrate Google Alerts, NewsAPI, etc.
    return f"RSS monitoring for {keyword} not yet implemented."

def passive_keyword_tracker(keyword):
    folder = get_timestamp_folder("tracker_reports")
    results = {}
    results['rss'] = rss_monitor(keyword, folder)
    # Optionally add scraping/API-based alert feeds, notifications, etc.
    save_report(json.dumps(results, indent=2), folder, "tracker_report", "html")
    # Optionally generate HTML and screenshots/graphs here
    return results

# === CLI MENU ===
def main_menu():
    color_print("Advanced OSINT Intelligence Suite", Fore.MAGENTA)
    color_print("1. Person Search\n2. Company/Organization Scan\n3. Passive Keyword Tracker\n4. Exit", Fore.CYAN)
    choice = input("Select option (1/2/3/4): ").strip()
    if choice == "1":
        query = input("Enter username, email, or domain: ").strip()
        person_search(query)
    elif choice == "2":
        domain = input("Enter company domain (e.g. example.com): ").strip()
        company_scan(domain)
    elif choice == "3":
        keyword = input("Enter keyword or subject to monitor: ").strip()
        passive_keyword_tracker(keyword)
    elif choice == "4":
        color_print("Exiting.", Fore.YELLOW)
        sys.exit(0)
    else:
        color_print("Invalid option.", Fore.RED)

if __name__ == "__main__":
    main_menu()