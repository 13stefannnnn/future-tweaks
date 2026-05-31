import subprocess
import sys
import time
import os
import importlib.util

# --- Clear screen ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Restart script ---
def restart_script():
    print("[FUTURE-SCRIPT] >> Restarting script to apply changes...\n")
    time.sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)

# --- Ensure modules ---
def ensure_modules(modules):
    missing = []
    for pip_name, import_name in modules:
        if importlib.util.find_spec(import_name) is None:
            missing.append(pip_name)

    if missing:
        print(f"[FUTURE-PLUGINS] >> Installing missing modules: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("[FUTURE-PLUGINS] >> Installation complete.")
            restart_script()  # Restart after install
        except subprocess.CalledProcessError:
            print("[FUTURE-PLUGINS] >> Failed to install modules. Exiting.")
            sys.exit(1)

# List of required modules: (pip_name, import_name)
required_modules = [
    ("colorama", "colorama"),
    ("psutil", "psutil"),
    ("py-cpuinfo", "cpuinfo"),
    ("gputil", "GPUtil"),
    ("wmi", "wmi"),
    ("setuptools", "setuptools") # Replaced distutils with setuptools
]

ensure_modules(required_modules)

# --- Import modules safely ---
from colorama import init, Fore
import psutil
import cpuinfo
import GPUtil
import wmi 
import setuptools # Safe to import now

init(autoreset=True)

# --- Color helpers ---
def prRed(text):
    print(Fore.RED + text)

def prCyan(text):
    print(Fore.CYAN + text)

# --- Test print ---
prCyan("[FUTURE-SCRIPT] >> All required modules are installed and working.")