import subprocess
import sys
import os

def bootstrap_requirements():
    req_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    if not os.path.exists(req_path):
        return

    try:
        with open(req_path) as f:
            packages = [l.strip() for l in f if l.strip() and not l.startswith("#")]

        missing = []
        for pkg in packages:
            name = pkg.split("==")[0].split(">=")[0].split("<=")[0].strip()
            try:
                __import__(name.replace("-", "_"))
            except ImportError:
                missing.append(pkg)

        if not missing:
            return

        print("\n[!] Missing requirements:")
        for m in missing:
            print(f"    - {m}")

        ans = input("\nInstall now? (Press ENTER to install, type 'skip' to exit): ").strip().lower()
        if ans == "skip":
            print("[!] Cannot continue without requirements. Exiting.")
            sys.exit(1)

        print("\n[*] Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
        print("[✓] Done!\n")
        input("Press ENTER to continue...")

    except subprocess.CalledProcessError:
        print("[ERROR] Installation failed. Install manually with: pip install -r requirements.txt")
        sys.exit(1)

bootstrap_requirements()

# ── Third-party imports (safe after bootstrap) ──
import json
import time
import random
import string
import requests
import keyboard
import psutil
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver

# ═══════════════════════════════════════════════════════════════
#                       CONFIGURATION
# ═══════════════════════════════════════════════════════════════
APP_NAME = "ExitlagAccountGenerator"
DEFAULT_PASS = "Access123!@#"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

browser = None
driver_pid = None


# ─────────────────────────────────────────────────────────────
#                       CONFIG FILE MANAGEMENT
# ─────────────────────────────────────────────────────────────
def get_config_path():
    appdata = os.getenv("APPDATA") or os.path.expanduser("~")
    config_dir = os.path.join(appdata, APP_NAME)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return os.path.join(config_dir, "exitlag_config.json")


def load_config():
    path = get_config_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}


def save_config(data):
    path = get_config_path()
    existing = load_config()
    existing.update(data)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f)


# ─────────────────────────────────────────────────────────────
#                       CLEANUP FUNCTIONS
# ─────────────────────────────────────────────────────────────
def cleanup():
    global browser, driver_pid

    if browser:
        try:
            browser.quit()
        except:
            pass

    if driver_pid:
        subprocess.run(
            f'taskkill /F /PID {driver_pid} /T',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True
        )

    subprocess.run(
        'taskkill /F /IM chromedriver.exe /T',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True
    )


def stop_script():
    print("\n\n[!] Emergency stop activated (ESC pressed)")
    cleanup()
    os._exit(0)


# ─────────────────────────────────────────────────────────────
#                       PASSWORD HELPER
# ─────────────────────────────────────────────────────────────
def check_password_complexity(password):
    return (
        len(password) >= 8
        and re.search(r"[a-z]", password)
        and re.search(r"[A-Z]", password)
        and re.search(r"\d", password)
        and re.search(r"[!@#$%^&*(),.?\":{}|<>_]", password)
    )


def handle_password(force_change=False):
    config = load_config()
    saved_pass = config.get("password")

    if not force_change:
        if saved_pass:
            return saved_pass
        else:
            save_config({"password": DEFAULT_PASS})
            return DEFAULT_PASS

    while True:
        print("\n" + "-" * 40)
        print("SET NEW PASSWORD")
        print("-" * 40)
        print("Requirements:")
        print("  - At least 8 characters")
        print("  - Lowercase (a-z)")
        print("  - Uppercase (A-Z)")
        print("  - Numbers (0-9)")
        print("  - Special chars (!@#$%^&*...)")
        print("-" * 40)
        print("(Type 'back' to go back)")

        new_pass = input("new password: ").strip()

        if new_pass.upper() == "BACK":
            return None

        if check_password_complexity(new_pass):
            save_config({"password": new_pass})
            print("[OK] Password updated")
            return new_pass

        print("\n[ERROR] password does not meet requirements")


def generate_email():
    """Generates a random @juno.com email address."""
    length = random.randint(8, 12)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{username}@juno.com"


# ═══════════════════════════════════════════════════════════════
#                       INITIAL SETUP
# ═══════════════════════════════════════════════════════════════
print("\n[*] initializing...")
current_pass = handle_password()


# ═══════════════════════════════════════════════════════════════
#                       MAIN MENU LOOP
# ═══════════════════════════════════════════════════════════════
while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    print("=" * 70)
    print("  exitlag account generator (by ml8w aka wrld)")
    print("=" * 70)

    print(f"\ncurrent password: {current_pass}")

    print("\n[1] change password")
    print("[2] exit")
    print("\n[ENTER] start generation")

    user_choice = input("\nSelection: ").strip()

    if user_choice == "1":
        updated = handle_password(force_change=True)
        if updated:
            current_pass = updated

    elif user_choice == "2":
        print("\n[*] exiting...")
        os._exit(0)

    elif user_choice == "":
        # ─────────────────────────────────────────────────────
        # START AUTOMATION
        # ─────────────────────────────────────────────────────

        keyboard.add_hotkey('esc', stop_script)

        try:
            print("\n" + "-" * 50)
            print("[1/3] generating email address...")

            email = generate_email()

            print(f"\n    Email: {email}")
            print(f"    Password: {current_pass}")

            print("\n" + "-" * 50)
            print("[2/3] launching browser...")
            print("    (Press ESC to emergency stop)")

            browser = Driver(
                uc=True,
                headless=False,
                dark_mode=True,
                page_load_strategy="eager"
            )
            driver_pid = browser.service.process.pid

            print("\n[3/3] navigating to exitlag...")
            browser.get("https://www.exitlag.com/lp/omen")

            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.NAME, "firstname"))
            )

            print("\n[*] filling account form...")

            browser.execute_script(f"""
                document.getElementsByName('firstname')[0].value = 'a';
                document.getElementsByName('lastname')[0].value = 'a';
                document.getElementsByName('email')[0].value = '{email}';
                document.getElementsByName('password')[0].value = '{current_pass}';
                document.getElementsByName('password2')[0].value = '{current_pass}';
                document.querySelector('div.w-checkbox-input').click();
                document.getElementById('registerButton').click();
            """)

            WebDriverWait(browser, 30).until(
                lambda d: "SUCCESS!" in d.page_source
            )

            with open("created_accounts.txt", "a") as f:
                f.write(f"{email}:{current_pass}\n")

            cleanup()

            print("\n" + "*" * 40)
            print("  SUCCESS: ACCOUNT CREATED")
            print("*" * 40)
            print(f"\n  Email: {email}")
            print(f"  Password: {current_pass}")
            print("\n  (Saved to created_accounts.txt)")
            print("\n")
            input("Press ENTER to continue...")

        except Exception as e:
            print(f"\n[ERROR] {e}")
            cleanup()
            input("\nPress ENTER to return to menu...")