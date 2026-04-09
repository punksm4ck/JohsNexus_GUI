import os
import subprocess
import time
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
html_file = os.path.join(base_dir, "jobnexus.html")
shadow_agent = os.path.join(base_dir, "aegis_shadow_agent.py")

try:
    if os.path.exists(shadow_agent):
        subprocess.Popen(["python3", "-m", "uvicorn", "aegis_shadow_agent:app", "--port", "3457"], cwd=base_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1) 
    
    if os.path.exists(html_file):
        subprocess.Popen(["google-chrome", html_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print(f"ERROR: {html_file} not found.")
except Exception as e:
    print(f"Ignition failed: {e}")
