"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
#!/usr/bin/env python3
import pathlib

TARGET = pathlib.Path('./jobnexus_public.html')

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JobNexus — Intelligent Job Search Platform</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
/* CORE ENTERPRISE STYLES */
:root {
  --bg0: #06080d; --bg1: #0b0e16; --bg2: #10141e; --bg3: #171c2a;
  --text0: #e2e8f5; --text1: #8694b5; --text2: #445070;
  --accent: #4f8ef7; --accent-hi: #6ba3ff; --accent-dim: rgba(79, 142, 247, 0.1);
  --border: rgba(255, 255, 255, 0.08); --border-hi: rgba(255, 255, 255, 0.15);
  --green: #34d399; --red: #f87171; --amber: #fbbf24;
  --font: 'IBM Plex Sans', sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); background: var(--bg0); color: var(--text0); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }

/* TOPBAR */
.topbar { display: flex; align-items: center; padding: 0 20px; height: 55px; background: var(--bg1); border-bottom: 1px solid var(--border); flex-shrink: 0; }
.logo { font-size: 16px; font-weight: 700; color: var(--text0); display: flex; align-items: center; gap: 10px; }
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
.input-group { display: flex; flex-direction: column; gap: 6px; position: relative; }
label { font-size: 11px; text-transform: uppercase; color: var(--text2); font-weight: 600; letter-spacing: 0.5px; display: flex; justify-content: space-between; }
input, select, textarea { background: var(--bg2); border: 1px solid var(--border-hi); color: var(--text0); padding: 10px; border-radius: 6px; font-family: var(--font); outline: none; transition: 0.2s; width: 100%; }
input:focus, select:focus, textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-dim); }
.btn { background: var(--accent); color: #fff; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; font-weight: 600; transition: 0.2s; width: 100%; }
.btn:hover { background: var(--accent-hi); }
.btn-ghost { background: transparent; border: 1px solid var(--border-hi); color: var(--text0); }
.btn-ghost:hover { background: var(--bg3); border-color: var(--text1); }

/* TOOLTIPS */
.tooltip-icon { background: var(--bg3); color: var(--text1); border-radius: 50%; width: 14px; height: 14px; display: inline-flex; align-items: center; justify-content: center; font-size: 9px; cursor: help; }
.tooltip-icon[title]:hover::after { content: attr(title); position: absolute; right: 0; top: 20px; background: var(--bg1); border: 1px solid var(--border-hi); padding: 8px; border-radius: 4px; z-index: 100; width: 220px; white-space: normal; color: var(--text0); font-size: 11px; text-transform: none; font-weight: 400; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }

/* JOB CARDS */
.job-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 15px; align-content: start; }
.job-card { background: var(--bg1); border: 1px solid var(--border); padding: 15px; border-radius: 8px; transition: 0.2s; display: flex; flex-direction: column; gap: 10px; }
.job-card:hover { border-color: var(--border-hi); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.job-card.applied { opacity: 0.45; filter: grayscale(1); border-style: dashed; }
.jc-title { font-size: 15px; font-weight: 600; color: var(--accent-hi); }
.jc-company { font-size: 13px; color: var(--text1); }
.jc-meta { display: flex; gap: 8px; flex-wrap: wrap; font-size: 11px; }
.pill { background: var(--bg3); padding: 3px 8px; border-radius: 12px; color: var(--text0); }
.jc-actions { display: flex; gap: 8px; margin-top: auto; padding-top: 10px; border-top: 1px solid var(--border); }

/* SETTINGS PANELS */
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
  <div class="logo">JobNexus <span class="logo-badge">PUBLIC RELEASE</span></div>
  <div class="tabs">
    <button class="tab active" onclick="switchTab('search')">Live Search</button>
    <button class="tab" onclick="switchTab('tracker')">Application Tracker</button>
    <button class="tab" onclick="switchTab('settings')">Configuration & APIs</button>
  </div>
</div>

<div class="body-wrap">
  <div class="sidebar" id="sidebar">
    <div class="input-group">
      <label>Keyword / Role</label>
      <input type="text" id="kw" value="Software Engineer" placeholder="e.g. Customer Service">
    </div>
    <div class="input-group">
      <label>Location <span class="tooltip-icon" title="Leave blank or type 'Remote' for nationwide remote jobs. Auto-detects on first boot.">?</span></label>
      <input type="text" id="loc" placeholder="Detecting location...">
    </div>
    <div class="input-group">
      <label>Data Sources</label>
      <label style="display:flex; align-items:center; gap:8px; text-transform:none; color:var(--text0)"><input type="checkbox" id="src-adzuna" checked style="width:auto"> Adzuna API</label>
      <label style="display:flex; align-items:center; gap:8px; text-transform:none; color:var(--text0)"><input type="checkbox" id="src-indeed" style="width:auto"> Indeed (Requires Bridge)</label>
      <label style="display:flex; align-items:center; gap:8px; text-transform:none; color:var(--text0)"><input type="checkbox" id="src-zip" style="width:auto"> ZipRecruiter (Requires Bridge)</label>
    </div>
    <button class="btn" onclick="executeSearch()" id="search-btn">Search Listings</button>
  </div>

  <div class="main-content">

    <div id="view-search" class="page-section active">
      <h2 style="margin-bottom: 20px; font-weight: 500;" id="results-header">Ready to Search</h2>
      <div class="job-grid" id="job-grid">
        <p style="color: var(--text1); max-width: 500px; line-height: 1.6;">Welcome to JobNexus. To begin, ensure you have configured your free API keys in the <strong>Configuration & APIs</strong> tab, then click Search.</p>
      </div>
    </div>

    <div id="view-tracker" class="page-section">
      <h2 style="margin-bottom: 20px;">Application Tracker</h2>
      <div class="job-grid" id="tracker-grid"></div>
    </div>

    <div id="view-settings" class="page-section" style="max-width: 800px; margin: 0 auto;">

      <div class="card-panel">
        <h3>Integration & Setup Guide</h3>
        <p>JobNexus is a decentralized, local-first application. It communicates directly with job board APIs and AI providers from your browser. <strong>Your data and API keys never leave your machine.</strong></p>

        <div style="margin-top: 20px; padding: 15px; background: var(--bg2); border-radius: 6px; border: 1px solid var(--border-hi);">
            <h4 style="color: var(--accent-hi); margin-bottom: 10px;">1. Adzuna Job API (Required for default search)</h4>
            <p style="font-size: 12px; margin-bottom: 10px;">Provides access to millions of global job listings. Free tier allows 250,000 requests per month.</p>
            <ul style="font-size: 12px; color: var(--text1); margin-left: 20px; margin-bottom: 15px;">
                <li>Go to <a href="https://developer.adzuna.com/" target="_blank" style="color: var(--accent);">developer.adzuna.com</a> and sign up.</li>
                <li>Create a new application to generate your App ID and App Key.</li>
                <li>Paste them below and click Save.</li>
            </ul>

            <h4 style="color: var(--accent-hi); margin-bottom: 10px;">2. Groq AI Cover Letter Engine (Optional)</h4>
            <p style="font-size: 12px; margin-bottom: 10px;">Powers the automated, context-aware cover letter generation using Llama 3.</p>
            <ul style="font-size: 12px; color: var(--text1); margin-left: 20px; margin-bottom: 15px;">
                <li>Go to <a href="https://console.groq.com/" target="_blank" style="color: var(--accent);">console.groq.com</a> and create a free account.</li>
                <li>Navigate to API Keys and generate a new key (starts with <code>gsk_</code>).</li>
            </ul>

            <h4 style="color: var(--accent-hi); margin-bottom: 10px;">3. Headless Scraper Bridge (Advanced)</h4>
            <p style="font-size: 12px; margin-bottom: 0;">To search Indeed and ZipRecruiter, you must be running the JobNexus Deno proxy server locally on port 3456 to bypass CORS and CAPTCHAs. If you are not running the backend, leave these sources unchecked in the sidebar.</p>
        </div>
      </div>

      <div class="card-panel">
        <h3>API Configuration</h3>
        <div style="display:flex; gap:15px; margin-bottom: 15px;">
            <div class="input-group" style="flex:1">
                <label>Adzuna App ID <span class="tooltip-icon" title="Found in your Adzuna Developer Dashboard">?</span></label>
                <input type="text" id="adz-id" placeholder="e.g. a1b2c3d4">
            </div>
            <div class="input-group" style="flex:1">
                <label>Adzuna App Key <span class="tooltip-icon" title="Keep this private. Stored in local browser storage only.">?</span></label>
                <input type="password" id="adz-key" placeholder="e.g. 1234567890abcdef...">
            </div>
        </div>
        <div class="input-group" style="margin-bottom: 15px;">
            <label>Groq API Key (AI Features) <span class="tooltip-icon" title="Required for the 'Generate Cover Letter' feature on job cards.">?</span></label>
            <input type="password" id="groq-key" placeholder="gsk_...">
        </div>
        <button class="btn" onclick="saveKeys()" style="width: auto;">Save Configuration</button>
      </div>

    </div>
  </div>
</div>

<div id="toast"></div>

<script>
// --- STATE MANAGEMENT ---
let jobData = [];
let appliedJobs = JSON.parse(localStorage.getItem('jn_pub_applied') || '[]');

// Load Saved Keys
document.getElementById('adz-id').value = localStorage.getItem('jn_pub_adz_id') || '';
document.getElementById('adz-key').value = localStorage.getItem('jn_pub_adz_key') || '';
document.getElementById('groq-key').value = localStorage.getItem('jn_pub_groq_key') || '';

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
    localStorage.setItem('jn_pub_adz_id', document.getElementById('adz-id').value.trim());
    localStorage.setItem('jn_pub_adz_key', document.getElementById('adz-key').value.trim());
    localStorage.setItem('jn_pub_groq_key', document.getElementById('groq-key').value.trim());
    showToast('API Configuration Saved Locally.');
}

// --- AUTO GEOLOCATION ---
window.onload = function() {
    const locInput = document.getElementById('loc');
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            async (pos) => {
                try {
                    const res = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${pos.coords.latitude}&lon=${pos.coords.longitude}&format=json`);
                    const data = await res.json();
                    const city = data.address.city || data.address.town || data.address.county || "Local Area";
                    const state = data.address.state || "";
                    locInput.value = `${city}, ${state}`.trim();
                    showToast('Location auto-detected.');
                } catch(e) {
                    locInput.value = "Remote";
                }
            },
            (err) => { locInput.value = "Remote"; }
        );
    } else {
        locInput.value = "Remote";
    }
};

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
    btn.innerText = "Search Listings"; btn.disabled = false;
}

async function fetchAdzuna(kw, loc) {
    let id = document.getElementById('adz-id').value;
    let key = document.getElementById('adz-key').value;
    if(!id || !key) {
        showToast('Adzuna API keys missing. Check Settings.');
        return;
    }
    try {
        const res = await fetch(`https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=${id}&app_key=${key}&what=${encodeURIComponent(kw)}&where=${encodeURIComponent(loc)}&results_per_page=20`);
        const data = await res.json();
        const mapped = data.results.map(j => ({
            id: `adz-${j.id}`, title: j.title, company: j.company.display_name, location: j.location.display_name,
            salaryRaw: j.salary_min ? `$${Math.floor(j.salary_min/1000)}k/yr` : 'Undisclosed', source: 'Adzuna', link: j.redirect_url
        }));
        jobData.push(...mapped);
    } catch(e) { console.error(e); }
}

async function fetchIndeed(kw, loc) {
    try {
        const res = await fetch(`http://localhost:3456/api/indeed?q=${encodeURIComponent(kw)}&l=${encodeURIComponent(loc)}`);
        if(!res.ok) throw new Error();
        const data = await res.json();
        jobData.push(...data);
    } catch(e) { showToast('Indeed bridge offline. Uncheck Indeed or start the backend server.'); }
}

async function fetchZip(kw, loc) {
    try {
        const res = await fetch(`http://localhost:3456/api/ziprecruiter?q=${encodeURIComponent(kw)}&l=${encodeURIComponent(loc)}`);
        if(!res.ok) throw new Error();
        const data = await res.json();
        jobData.push(...data);
    } catch(e) { }
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
    localStorage.setItem('jn_pub_applied', JSON.stringify(appliedJobs));
    renderJobs();
    renderTracker();
}

function openApplyLink(url, jobId, event) {
    event.stopPropagation();
    if (!appliedJobs.includes(jobId)) {
        appliedJobs.push(jobId);
        localStorage.setItem('jn_pub_applied', JSON.stringify(appliedJobs));
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
                    ${isApplied ? '↺ Undo' : '✓ Mark Applied'}
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
</script>
</body>
</html>"""

TARGET.write_text(HTML_CONTENT, encoding='utf-8')
print(f"JobNexus Public Release compiled to: {TARGET.absolute()}")
