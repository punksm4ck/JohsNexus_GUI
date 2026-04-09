"© 2026 Punksm4ck. All rights reserved."
#!/bin/bash
set -euo pipefail

cd /home/tsann/Scripts/JohsNexus_GUI

if pgrep -f "jobnexus_deno_bridge.ts" > /dev/null; then
    pkill -f "jobnexus_deno_bridge.ts"
fi

if pgrep -f "aegis_shadow_agent.py" > /dev/null; then
    pkill -f "aegis_shadow_agent.py"
fi

export PUPPETEER_EXECUTABLE_PATH="/usr/bin/google-chrome"

deno run --allow-net --allow-read --allow-env --allow-run --allow-write jobnexus_deno_bridge.ts &

python3 aegis_shadow_agent.py &

sleep 2

xdg-open jobnexus.html
