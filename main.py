import os
import json
import ctypes
import sys
from tools import prRed, prCyan, clear_screen
from functions import future_restorePoint, future_diskcleanup, future_clearTempFiles, future_cleardownloads, future_systemInfo, enable_ultimate_performance_plan, run_christitus_powershell, future_pingcustomhost, clear_fivem_cache

# --- Require Admin ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("Requesting administrator access...")
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

# --- Event Handlers ---
event_handlers = {
    "future:restorePoint": future_restorePoint,
    "future:diskcleanup": future_diskcleanup,
    "future:clearTempFiles": future_clearTempFiles,
    "future:clearDownloads": future_cleardownloads,
    "future:systemInfo": future_systemInfo,
    "future:ultperf": enable_ultimate_performance_plan,
    "future:christitus": run_christitus_powershell,
    "future:customDNS": future_pingcustomhost,
    #"future:disableHPET": disable_hpet,
    "future:fivemCache": clear_fivem_cache

}

# --- Load Config ---
def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    with open(config_path, "r") as f:
        return json.load(f)

# --- Start App ---
def startApp():
    config = load_config()
    categories = config.get("categories", {})

    while True:
        clear_screen()

        prRed("by 13.stefannnnn (github.com/13stefannnnn)\n")
        prRed("  ______     _                    _______          _ ")
        prRed(" |  ____|   | |                  |__   __|        | |")
        prRed(" | |__ _   _| |_ _   _ _ __ ___     | | ___   ___ | |")
        prRed(" |  __| | | | __| | | | '__/ _ \    | |/ _ \ / _ \| |")
        prRed(" | |  | |_| | |_| |_| | | |  __/    | | (_) | (_) | |")
        prRed(" |_|   \__,_|\__|\__,_|_|  \___|    |_|\___/ \___/|_|\n\n")
        prCyan("[0] >> Exit")
        for cat_id, cat_data in categories.items():
            prCyan(f"[{cat_id}] >> {cat_data['name']}")

        cat_choice = input("\nChoose a category: ").strip()
        if cat_choice == "0":
            prRed("Exiting Future App...")
            break
        elif cat_choice in categories:
            show_category_menu(categories[cat_choice])
        else:
            prRed("Invalid category. Try again.")

def show_category_menu(category):
    while True:
      #  prCyan(f"\n-- {category['name']} --")
        prCyan("\n[0] >> Back to main menu")
        options = category.get("options", {})
        for opt_id, opt in options.items():
            prCyan(f"[{opt_id}] >> {opt['name']}")

        choice = input("\nSelect an option: ").strip()
        if choice == "0":
            break
        elif choice in options:
            event = options[choice]["event"]
            handler = event_handlers.get(event)
            if handler:
                try:
                    handler()
                except Exception as e:
                    prRed(f"Error running handler: {e}")
            else:
                prRed(f"No function found for event '{event}'")
        else:
            prRed("Invalid option. Try again.")

startApp()

       