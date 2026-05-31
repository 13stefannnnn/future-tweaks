import subprocess
import os
import shutil
import tempfile
from tools import prRed
from tools import clear_screen


def future_restorePoint():
    prRed("[FUTURE-TOOLS] >> Simulating restore point creation...")

def future_diskcleanup():
    prRed("[FUTURE-TOOLS] >> Opening Disk Cleanup...")
    subprocess.Popen("cleanmgr.exe")

def future_clearTempFiles():
    folders_to_clear = [
        tempfile.gettempdir(),       # User Temp
        r"C:\Windows\Temp",          # System Temp
        r"C:\Windows\Prefetch"       # Prefetch
    ]

    for folder in folders_to_clear:
        prRed(f"[FUTURE-TOOLS] >> Clearing: {folder}")
        if not os.path.exists(folder):
            prRed(f"Folder not found: {folder}")
            continue

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                prRed(f"Failed to delete {file_path}. Reason: {e}")
    prRed("[FUTURE-TOOLS] >> Temporary files cleared.")

def future_cleardownloads():
    choice = input(
        "This tool will delete all files in your Downloads folder.\n"
        "Make sure you've saved anything important!\n\n"
        "Are you sure you want to continue? (y/n): "
    ).strip().lower()

    if choice == "y":
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

        if not os.path.exists(downloads_path):
            prRed(f"[ERROR] Downloads folder not found at: {downloads_path}")
            return

        deleted = 0
        failed = 0

        for filename in os.listdir(downloads_path):
            file_path = os.path.join(downloads_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    deleted += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted += 1
            except Exception as e:
                prRed(f"[FAILED] {file_path} — Reason: {e}")
                failed += 1

        prRed(f"[CLEANUP] ✅ Deleted: {deleted} item(s), ❌ Failed: {failed} item(s)\n")
    else:
        prRed("\n[ABORTED] Downloads cleanup canceled.")
        clear_screen()
        
import psutil
import cpuinfo
import GPUtil

def future_systemInfo():
    prRed("\n[FUTURE-INFO] >> System Hardware Overview")

    # CPU Info
    cpu = cpuinfo.get_cpu_info()
    prRed("\n[CPU]")
    prRed(f"Name         : {cpu.get('brand_raw', 'Unknown')}")
    prRed(f"Cores        : {psutil.cpu_count(logical=False)} physical / {psutil.cpu_count(logical=True)} logical")
    freq = psutil.cpu_freq()
    if freq:
        prRed(f"Max Frequency: {round(freq.max, 2)} MHz")

    # RAM Info
    prRed("\n[RAM]")
    virtual_mem = psutil.virtual_memory()
    total_gb = round(virtual_mem.total / (1024 ** 3), 2)
    prRed(f"Total RAM    : {total_gb} GB")
    try:
        import wmi
        c = wmi.WMI()
        for mem in c.Win32_PhysicalMemory():
            prRed(f"RAM Speed    : {mem.Speed} MHz")
            break
    except ImportError:
        prRed("RAM Speed    : wmi not installed (optional)")

    # GPU Info
    prRed("\n[GPU]")
    try:
        gpus = GPUtil.getGPUs()
        gpu_found = False
        for gpu in gpus:
            if gpu.memoryTotal > 0:
                prRed(f"Name         : {gpu.name}")
              #  prRed(f"VRAM         : {round(gpu.memoryTotal)} MB")
                gpu_found = True
                break
        
        if not gpu_found:
            try:
                import wmi
                c = wmi.WMI()
                wmi_gpus = c.Win32_VideoController()
                if wmi_gpus:
                    for gpu in wmi_gpus:
                        prRed(f"Name         : {gpu.Name}")
                        vram_mb = int(gpu.AdapterRAM) // (1024**2) if gpu.AdapterRAM else "Unknown"
                      #  prRed(f"VRAM         : {vram_mb} MB")
                        gpu_found = True
                        break
                if not gpu_found:
                    prRed("No GPU detected.")
            except Exception:
                prRed("No GPU detected.")
    except Exception:
        prRed("No GPU detected.")

    # Storage Info
    prRed("\n[STORAGE]")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total_gb = round(usage.total / (1024 ** 3), 2)
            prRed(f"{partition.device} - {total_gb} GB total")
        except PermissionError:
            continue

    prRed("\n[FUTURE-INFO] >> Done\n")


def enable_ultimate_performance_plan():
    """
    Enables the Ultimate Performance power plan (if available) and sets it as active.
    Requires admin privileges.
    """
    try:
        ultimate_perf_guid = "e9a42b02-d5df-448d-aa00-03f14749eb61"

        result = subprocess.run(
            ["powercfg", "-l"], capture_output=True, text=True, check=True
        )
        plans = result.stdout.lower()

        if ultimate_perf_guid not in plans:
            print("[INFO] Ultimate Performance plan not found, trying to create it...")
            subprocess.run(
                ["powercfg", "-duplicatescheme", ultimate_perf_guid],
                check=True,
            )
            print("[INFO] Ultimate Performance plan created.")

        subprocess.run(
            ["powercfg", "-setactive", ultimate_perf_guid], check=True
        )
        print("[SUCCESS] Ultimate Performance power plan enabled and activated.")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to enable Ultimate Performance plan: {e}")
    except Exception as ex:
        print(f"[ERROR] Unexpected error: {ex}")

def run_christitus_powershell():
    command = "iwr -useb https://christitus.com/win | iex"

    subprocess.Popen([
        "powershell.exe",
        "-NoExit",
        "-Command",
        command
    ], creationflags=subprocess.CREATE_NEW_CONSOLE)

import platform

def future_pingcustomhost():
    host = input("Enter IP address or domain to ping: ").strip()
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Ping to {host} successful!")
            print(result.stdout)
        else:
            print(f"Ping to {host} failed.")
            print(result.stdout)
    except Exception as e:
        print(f"Error pinging {host}: {e}")

def clear_fivem_cache():
    username = os.getlogin()
    base_path = fr"C:\Users\{username}\AppData\Local\FiveM\FiveM.app\data"
    cache_folders = ["cache", "server-cache", "server-cache-priv"]

    for folder in cache_folders:
        folder_path = os.path.join(base_path, folder)

        if os.path.exists(folder_path):
            prRed(f"Deleting contents of {folder_path}...")
            try:
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
            except Exception as e:
                prRed(f"[ERROR] Failed to clear {folder_path}: {e}")
        else:
            prRed(f"Folder {folder_path} not found!")

    prRed("Cache folders emptied successfully.")

