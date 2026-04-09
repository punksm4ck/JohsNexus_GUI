"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
#!/usr/bin/env python3
import pathlib

TARGET = pathlib.Path('/home/tsann/Scripts/JohsNexus_GUI/jobnexus.html')

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JobNexus Enterprise</title>
<link rel="icon" type="image/png" href="file:///home/tsann/.local/share/icons/jobnexus/icon.png">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* CORE ENTERPRISE STYLES */
:root {
  --bg0: #06080d; --bg1: #0b0e16; --bg2: #10141e; --bg3: #171c2a;
  --text0: #e2e8f5; --text1: #8694b5; --text2: #445070;
  --accent: #4f8ef7; --accent-hi: #6ba3ff; --accent-dim: rgba(79, 142, 247, 0.1);
  --border: rgba(255, 255, 255, 0.08); --border-hi: rgba(255, 255, 255, 0.15);
  --green: #34d399; --red: #f87171; --amber: #fbbf24;
  --font: 'IBM Plex Sans', sans-serif; --mono: 'IBM Plex Mono', monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); background: var(--bg0); color: var(--text0); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }

/* TOPBAR */
.topbar { display: flex; align-items: center; padding: 0 20px; height: 55px; background: var(--bg1); border-bottom: 1px solid var(--border); flex-shrink: 0; }
.logo { font-size: 16px; font-weight: 700; color: var(--text0); text-decoration: none; display: flex; align-items: center; gap: 10px; }
.logo-badge { font-size: 10px; background: var(--accent-dim); color: var(--accent); padding: 3px 8px; border-radius: 4px; border: 1px solid var(--accent); }
.tabs { display: flex; gap: 5px; margin-left: 30px; }
.tab { background: transparent; border: none; color: var(--text1); padding: 8px 16px; cursor: pointer; border-radius: 6px; font-weight: 500; transition: 0.2s; }
.tab.active, .tab:hover { background: var(--bg3); color: var(--text0); }

/* LAYOUT */
.body-wrap { display: flex; flex: 1; overflow: hidden; }
.sidebar { width: 280px; background: var(--bg1); border-right: 1px solid var(--border); padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
.main-content { flex: 1; overflow-y: auto; padding: 20px; position: relative; }
.page-section { display: none; flex-direction: column; height: 100%; }
.page-section.active { display: flex; }

/* FORMS & BUTTONS */
.input-group { display: flex; flex-direction: column; gap: 6px; }
label { font-size: 11px; text-transform: uppercase; color: var(--text2); font-weight: 600; letter-spacing: 0.5px; }
input, select, textarea { background: var(--bg2); border: 1px solid var(--border-hi); color: var(--text0); padding: 10px; border-radius: 6px; font-family: var(--font); outline: none; transition: 0.2s; width: 100%; }
input:focus, select:focus, textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-dim); }
.btn { background: var(--accent); color: #fff; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; font-weight: 600; transition: 0.2s; width: 100%; }
.btn:hover { background: var(--accent-hi); }
.btn-ghost { background: transparent; border: 1px solid var(--border-hi); color: var(--text0); }
.btn-ghost:hover { background: var(--bg3); border-color: var(--text1); }

/* JOB CARDS (WITH APPLIED LOGIC) */
.job-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 15px; align-content: start; }
.job-card { background: var(--bg1); border: 1px solid var(--border); padding: 15px; border-radius: 8px; transition: 0.2s; display: flex; flex-direction: column; gap: 10px; }
.job-card:hover { border-color: var(--border-hi); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.job-card.applied { opacity: 0.45; filter: grayscale(1); border-style: dashed; }
.job-card.applied:hover { opacity: 0.65; filter: grayscale(0.5); }
.jc-title { font-size: 15px; font-weight: 600; color: var(--accent-hi); }
.jc-company { font-size: 13px; color: var(--text1); }
.jc-meta { display: flex; gap: 8px; flex-wrap: wrap; font-size: 11px; }
.pill { background: var(--bg3); padding: 3px 8px; border-radius: 12px; color: var(--text0); }
.jc-actions { display: flex; gap: 8px; margin-top: auto; padding-top: 10px; border-top: 1px solid var(--border); }

/* SETTINGS & METRICS */
.card-panel { background: var(--bg1); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 20px; }
.card-panel h3 { margin-bottom: 5px; color: var(--text0); }
.card-panel p { color: var(--text1); font-size: 13px; margin-bottom: 15px; line-height: 1.5; }

/* TOAST */
#toast { position: fixed; bottom: 20px; right: 20px; background: var(--bg3); border: 1px solid var(--accent); color: #fff; padding: 12px 20px; border-radius: 6px; transform: translateY(100px); opacity: 0; transition: 0.3s; z-index: 9999; }
#toast.show { transform: translateY(0); opacity: 1; }
</style>
</head>
<body>

<div class="topbar">
  <div class="logo">JobNexus <span class="logo-badge">ENTERPRISE v4</span></div>
  <div class="tabs">
    <button class="tab active" onclick="switchTab('search')">Live Search</button>
    <button class="tab" onclick="switchTab('tracker')">Application Tracker</button>
    <button class="tab" onclick="switchTab('settings')">System Settings</button>
  </div>
</div>

<div class="body-wrap">
  <div class="sidebar" id="sidebar">
    <div class="input-group">
      <label>Keyword / Role</label>
      <input type="text" id="kw" value="Customer Service" placeholder="e.g. Software Engineer">
    </div>
    <div class="input-group">
      <label>Location</label>
      <input type="text" id="loc" value="Simi Valley, CA" placeholder="City, State, or Remote">
    </div>
    <div class="input-group">
      <label>Data Sources</label>
      <label style="display:flex; align-items:center; gap:8px; text-transform:none; color:var(--text0)"><input type="checkbox" id="src-indeed" checked style="width:auto"> Indeed (Headless Bridge)</label>
      <label style="display:flex; align-items:center; gap:8px; text-transform:none; color:var(--text0)"><input type="checkbox" id="src-zip" checked style="width:auto"> ZipRecruiter (Headless Bridge)</label>
      <label style="display:flex; align-items:center; gap:8px; text-transform:none; color:var(--text0)"><input type="checkbox" id="src-adzuna" checked style="width:auto"> Adzuna API</label>
    </div>
    <button class="btn" onclick="executeSearch()" id="search-btn">Execute Global Search</button>
  </div>

  <div class="main-content">

    <div id="view-search" class="page-section active">
      <h2 style="margin-bottom: 20px; font-weight: 500;" id="results-header">Awaiting Search Execution...</h2>
      <div class="job-grid" id="job-grid"></div>
    </div>

    <div id="view-tracker" class="page-section">
      <h2 style="margin-bottom: 20px;">Application Tracker Pipeline</h2>
      <div class="job-grid" id="tracker-grid"></div>
    </div>

    <div id="view-settings" class="page-section" style="max-width: 800px; margin: 0 auto;">

      <div class="card-panel">
        <h3>System Integration</h3>
        <p>Manage desktop and application menu shortcuts for Kubuntu. The desktop launcher will automatically boot the Deno stealth backend before opening the GUI.</p>
        <button id="launcher-btn" class="btn btn-ghost" onclick="toggleLauncher()" style="width: auto;">Checking status...</button>
      </div>

      <div class="card-panel">
        <h3>Job Board API Keys</h3>
        <p>Ensure your headless bridge is active. Indeed and ZipRecruiter operate via local Deno proxy on port 3456.</p>
        <div style="display:flex; gap:15px;">
            <div class="input-group" style="flex:1"><label>Adzuna App ID</label><input type="text" id="adz-id" placeholder="App ID"></div>
            <div class="input-group" style="flex:1"><label>Adzuna App Key</label><input type="text" id="adz-key" placeholder="App Key"></div>
        </div>
        <button class="btn" onclick="saveKeys()" style="width: auto; margin-top: 15px;">Save API Configuration</button>
      </div>

    </div>
  </div>
</div>

<div id="toast"></div>

<script>
// --- STATE MANAGEMENT ---
let jobData = [];
let appliedJobs = JSON.parse(localStorage.getItem('jn_applied') || '[]');
let adzunaId = localStorage.getItem('jn_adz_id') || '';
let adzunaKey = localStorage.getItem('jn_adz_key') || '';

document.getElementById('adz-id').value = adzunaId;
document.getElementById('adz-key').value = adzunaKey;

function showToast(msg) {
    const t = document.getElementById('toast');
    t.innerText = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
}

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    document.querySelectorAll('.page-section').forEach(p => p.classList.remove('active'));
    document.getElementById('view-' + tab).classList.add('active');
    if(tab === 'tracker') renderTracker();
    if(tab === 'search') document.getElementById('sidebar').style.display = 'flex';
    else document.getElementById('sidebar').style.display = 'none';
}

function saveKeys() {
    localStorage.setItem('jn_adz_id', document.getElementById('adz-id').value);
    localStorage.setItem('jn_adz_key', document.getElementById('adz-key').value);
    showToast('API Configuration Saved.');
}

// --- DENO SYSTEM INTEGRATOR (DESKTOP LAUNCHER) ---
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
        btn.style.borderColor = "var(--red)"; btn.style.color = "var(--red)";
    } else {
        btn.textContent = "Create Desktop Launcher";
        btn.style.borderColor = "var(--accent)"; btn.style.color = "var(--accent)";
    }
}

async function toggleLauncher() {
    const btn = document.getElementById('launcher-btn');
    const isCreate = btn.textContent.includes("Create");
    btn.textContent = isCreate ? "Processing..." : "Removing...";
    await runSystemIntegrator(isCreate ? "create" : "remove");
    setTimeout(checkLauncherStatus, 1000);
    showToast(isCreate ? "Desktop Launcher Created!" : "Launcher Removed.");
}

// --- SCRAPING & RENDERING ---
async function executeSearch() {
    const kw = document.getElementById('kw').value;
    const loc = document.getElementById('loc').value;
    const btn = document.getElementById('search-btn');
    btn.innerText = "Executing..."; btn.disabled = true;

    document.getElementById('results-header').innerText = `Fetching results for "${kw}"...`;
    jobData = [];
    const fetches = [];

    if(document.getElementById('src-indeed').checked) fetches.push(fetchIndeed(kw, loc));
    if(document.getElementById('src-zip').checked) fetches.push(fetchZip(kw, loc));
    if(document.getElementById('src-adzuna').checked) fetches.push(fetchAdzuna(kw, loc));

    await Promise.all(fetches);

    document.getElementById('results-header').innerText = `Found ${jobData.length} Live Listings`;
    renderJobs();
    btn.innerText = "Execute Global Search"; btn.disabled = false;
}

async function fetchIndeed(kw, loc) {
    try {
        const res = await fetch(`http://localhost:3456/api/indeed?q=${encodeURIComponent(kw)}&l=${encodeURIComponent(loc)}`);
        const data = await res.json();
        jobData.push(...data);
    } catch(e) { console.error('Indeed block:', e); showToast('Indeed bridge offline.'); }
}

async function fetchZip(kw, loc) {
    try {
        const res = await fetch(`http://localhost:3456/api/ziprecruiter?q=${encodeURIComponent(kw)}&l=${encodeURIComponent(loc)}`);
        const data = await res.json();
        jobData.push(...data);
    } catch(e) { console.error('Zip block:', e); }
}

async function fetchAdzuna(kw, loc) {
    let id = document.getElementById('adz-id').value;
    let key = document.getElementById('adz-key').value;
    if(!id || !key) return;
    try {
        const res = await fetch(`https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=${id}&app_key=${key}&what=${encodeURIComponent(kw)}&where=${encodeURIComponent(loc)}&results_per_page=20`);
        const data = await res.json();
        const mapped = data.results.map(j => ({
            id: `adz-${j.id}`, title: j.title, company: j.company.display_name, location: j.location.display_name,
            salaryRaw: j.salary_min ? `$${Math.floor(j.salary_min/1000)}k/yr` : 'Undisclosed', source: 'Adzuna', link: j.redirect_url
        }));
        jobData.push(...mapped);
    } catch(e) {}
}

// --- APPLIED LOGIC ---
function toggleApplied(jobId, event) {
    if(event) event.stopPropagation();
    const idx = appliedJobs.indexOf(jobId);
    if (idx > -1) {
        appliedJobs.splice(idx, 1);
        showToast('Application marked as undone.');
    } else {
        appliedJobs.push(jobId);
        showToast('Job marked as applied.');
    }
    localStorage.setItem('jn_applied', JSON.stringify(appliedJobs));
    renderJobs();
    renderTracker();
}

function openApplyLink(url, jobId, event) {
    event.stopPropagation();
    if (!appliedJobs.includes(jobId)) {
        appliedJobs.push(jobId);
        localStorage.setItem('jn_applied', JSON.stringify(appliedJobs));
    }
    window.open(url, '_blank');
    renderJobs();
}

function renderJobs() {
    const grid = document.getElementById('job-grid');
    grid.innerHTML = jobData.map(j => {
        const isApplied = appliedJobs.includes(j.id);
        return `
        <div class="job-card ${isApplied ? 'applied' : ''}">
            <div>
                <div class="jc-title">${j.title}</div>
                <div class="jc-company">${j.company}</div>
            </div>
            <div class="jc-meta">
                <span class="pill">${j.location}</span>
                <span class="pill">${j.salaryRaw || 'Undisclosed'}</span>
                <span class="pill">${j.source}</span>
            </div>
            <div class="jc-actions">
                <button class="btn" style="flex:1" onclick="openApplyLink('${j.link}', '${j.id}', event)">Apply ↗</button>
                <button class="btn btn-ghost" style="flex:1" onclick="toggleApplied('${j.id}', event)">
                    ${isApplied ? '↺ Undo Applied' : '✓ Mark Applied'}
                </button>
            </div>
        </div>`;
    }).join('');
}

function renderTracker() {
    const grid = document.getElementById('tracker-grid');
    const trackedJobs = jobData.filter(j => appliedJobs.includes(j.id));

    if(trackedJobs.length === 0) {
        grid.innerHTML = "<p style='color:var(--text1)'>No applications tracked yet in this session.</p>";
        return;
    }

    grid.innerHTML = trackedJobs.map(j => `
        <div class="job-card applied" style="border-color: var(--accent);">
            <div>
                <div class="jc-title">${j.title}</div>
                <div class="jc-company">${j.company}</div>
            </div>
            <div class="jc-meta">
                <span class="pill" style="background: var(--green); color: #000; font-weight:bold;">APPLIED</span>
                <span class="pill">${j.source}</span>
            </div>
            <div class="jc-actions">
                <button class="btn btn-ghost" style="flex:1; border-color: var(--red); color: var(--red);" onclick="toggleApplied('${j.id}', event)">Remove from Pipeline</button>
            </div>
        </div>`).join('');
}

// Init system check
setTimeout(checkLauncherStatus, 1500);
</script>
</body>
</html>"""

TARGET.write_text(HTML_CONTENT, encoding='utf-8')
print(f"Enterprise GUI successfully compiled and written to: {TARGET}")
