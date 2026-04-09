#!/usr/bin/env python3
import os, sys

APP_NAME = "JobNexus"
EXEC_PATH = "/home/tsann/Scripts/JohsNexus_GUI/launch_jobnexus.sh"
ICON_PATH = "/home/tsann/.local/share/icons/jobnexus/icon.png"
DESKTOP_FILE = f"""[Desktop Entry]
Name={APP_NAME}
Comment=Enterprise Job Search Aggregator
Exec={EXEC_PATH}
Icon={ICON_PATH}
Terminal=false
Type=Application
Categories=Office;Network;
"""

paths = [
    os.path.expanduser("~/Desktop/JobNexus.desktop"),
    os.path.expanduser("~/.local/share/applications/JobNexus.desktop")
]

def check():
    exists = all(os.path.exists(p) for p in paths)
    print("EXISTS" if exists else "NOT_FOUND")

def create():
    for p in paths:
        with open(p, "w") as f: f.write(DESKTOP_FILE)
        os.chmod(p, 0o755)
    print("CREATED")

def remove():
    for p in paths:
        if os.path.exists(p): os.remove(p)
    print("REMOVED")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "check": check()
        elif cmd == "create": create()
        elif cmd == "remove": remove()
