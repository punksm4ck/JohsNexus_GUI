"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
import pathlib
html_path = pathlib.Path('./jobnexus.html')
html = html_path.read_text()

# 1. Update the Window Icon (Favicon)
ICON_TAG = '<link rel="icon" type="image/png" href="file:///home/tsann/.local/share/icons/jobnexus/icon.png">'
if '</title>' in html:
    html = html.replace('</title>', f'</title>\n{ICON_TAG}')

# 2. Add the dynamic button to Settings
SETTINGS_TARGET = '<div class="settings-card-title">Data Management</div>'
LAUNCHER_UI = '''
      <div class="settings-card">
        <div class="settings-card-title">System Integration</div>
        <div class="settings-card-sub">Manage desktop and application menu shortcuts.</div>
        <button id="launcher-btn" class="btn-sm btn-ghost" onclick="toggleLauncher()" style="padding:7px 16px">Checking status...</button>
      </div>
'''
html = html.replace(SETTINGS_TARGET, LAUNCHER_UI + SETTINGS_TARGET)

# 3. Add the logic to the script section
LOGIC = '''
async def runSystemIntegrator(cmd) {
    // This requires a local bridge to execute system commands,
    // we'll use the Deno bridge we already have running.
    try {
        const res = await fetch(`http://localhost:3456/api/system?cmd=${cmd}`);
        return await res.text();
    } catch(e) { return "ERROR"; }
}

async def checkLauncherStatus() {
    const status = await runSystemIntegrator("check");
    const btn = document.getElementById('launcher-btn');
    if (status.includes("EXISTS")) {
        btn.textContent = "Remove Desktop Launcher";
        btn.className = "btn-sm btn-ghost-red";
    } else {
        btn.textContent = "Create Desktop Launcher";
        btn.className = "btn-sm btn-primary";
    }
}

async def toggleLauncher() {
    const btn = document.getElementById('launcher-btn');
    const cmd = btn.textContent.includes("Create") ? "create" : "remove";
    await runSystemIntegrator(cmd);
    setTimeout(checkLauncherStatus, 500);
}

// Add to init()
setTimeout(checkLauncherStatus, 1000);
'''
html = html.replace('loadSkillsUI();', 'loadSkillsUI();\n  checkLauncherStatus();')
html_path.write_text(html)
