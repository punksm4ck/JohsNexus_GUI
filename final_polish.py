import pathlib
html_path = pathlib.Path('./jobnexus.html')
html = html_path.read_text()

# 1. Add Favicon Link
ICON_LINK = '<link rel="icon" type="image/png" href="file:///home/tsann/.local/share/icons/jobnexus/icon.png">'
if '</title>' in html and ICON_LINK not in html:
    html = html.replace('</title>', f'</title>\n{ICON_LINK}')

# 2. Add System Integration Card to Settings
if 'System Integration' not in html:
    SETTINGS_TARGET = '<div class="settings-card-title">Data Management</div>'
    LAUNCHER_UI = '''
      <div class="settings-card">
        <div class="settings-card-title">System Integration</div>
        <div class="settings-card-sub">Manage desktop and application menu shortcuts.</div>
        <button id="launcher-btn" class="btn-sm btn-ghost" onclick="toggleLauncher()" style="padding:7px 16px">Checking status...</button>
      </div>
'''
    html = html.replace(SETTINGS_TARGET, LAUNCHER_UI + SETTINGS_TARGET)

# 3. Inject JavaScript Logic
JS_LOGIC = '''
async function runSystemIntegrator(cmd) {
    try {
        const res = await fetch(`http://localhost:3456/api/system?cmd=${cmd}`);
        return await res.text();
    } catch(e) { return "ERROR"; }
}

async function checkLauncherStatus() {
    const status = await runSystemIntegrator("check");
    const btn = document.getElementById('launcher-btn');
    if (!btn) return;
    if (status.includes("EXISTS")) {
        btn.textContent = "Remove Desktop Launcher";
        btn.className = "btn-sm btn-ghost-danger";
    } else {
        btn.textContent = "Create Desktop Launcher";
        btn.className = "btn-sm btn-primary";
    }
}

async function toggleLauncher() {
    const btn = document.getElementById('launcher-btn');
    const isCreate = btn.textContent.includes("Create");
    btn.textContent = isCreate ? "Creating..." : "Removing...";
    const cmd = isCreate ? "create" : "remove";
    await runSystemIntegrator(cmd);
    setTimeout(checkLauncherStatus, 1000);
}
'''
if 'runSystemIntegrator' not in html:
    html = html.replace('</script>', JS_LOGIC + '\n</script>')

# 4. Trigger check on init
if 'checkLauncherStatus();' not in html:
    html = html.replace('loadSkillsUI();', 'loadSkillsUI();\n  checkLauncherStatus();')

html_path.write_text(html)
print("GUI Polish Complete.")
