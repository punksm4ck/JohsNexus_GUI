"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
#!/usr/bin/env python3
"""
Surgical API Patch for JobNexus Enterprise
Grafts live async fetch functions into the existing 2293-line jobnexus.html
"""
import sys, shutil, pathlib, datetime

TARGET = pathlib.Path('/home/tsann/Scripts/jobnexus.html')

if not TARGET.exists():
    sys.exit(f'ERROR: {TARGET} not found.')

backup = TARGET.with_suffix(f'.bak_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}')
shutil.copy2(TARGET, backup)
print(f'Backup created: {backup}')

html = TARGET.read_text(encoding='utf-8')
errors = []

P1_OLD = '''function doSearch() {
  const kw  = (document.getElementById('kw').value.trim()||'Software Engineer').substring(0,120);
  const loc = (document.getElementById('loc').value.trim()||'Remote USA').substring(0,120);
  const btn = document.getElementById('search-btn');
  btn.disabled = true;
  btn.textContent = 'Searching…';
  setStatus(`Searching "${kw}" in ${loc}…`, 'loading');
  const enabledSrcs = SOURCES.filter(s => document.getElementById('chk-'+s.id)?.checked);
  if (!enabledSrcs.length) {
    showToast('Select at least one job board source.', 3000, 'error');
    btn.disabled=false; btn.textContent='Search jobs';
    setStatus('No sources selected — enable at least one job board.', 'error');
    return;
  }
  document.getElementById('job-list').innerHTML =
    `<div class="empty-state"><div class="spinner spinner-lg"></div><div style="margin-top:14px;font-size:12px;color:var(--text1)">Fetching listings from <strong>${enabledSrcs.length}</strong> source${enabledSrcs.length!==1?'s':''}…</div><div style="font-size:10px;color:var(--text2);margin-top:5px">Matching skills · sorting by relevance · applying filters</div></div>`;
  document.getElementById('detail-panel').style.display = 'none';
  selectedJob = null;

  setTimeout(() => {
    try {
      const cfg = loadSettings();
      userSkills = cfg.skills || [];
      allJobs = generateJobs(kw, loc, enabledSrcs);
      filteredJobs = [...allJobs];
      activeFilter = 'all';
      document.querySelectorAll('.pill-filter').forEach(p => p.classList.toggle('active', p.dataset.f==='all'));
      applyClientFilters();
      renderJobList();
      updateMetricCards();
      const srcs = [...new Set(allJobs.map(j=>j.source))].length;
      setStatus(`Found ${allJobs.length} listings across ${srcs} source${srcs!==1?'s':''} · ${filteredJobs.length} matching filters`);
    } catch(err) {
      setStatus('Search error — see console.', 'error');
      console.error('Search error:', err);
      showToast('Search error. Check the browser console.', 4000, 'error');
    } finally {
      btn.disabled=false;
      btn.textContent='Search jobs';
    }
  }, 1200);
}'''

P1_NEW = '''async function doSearch() {
  const kw  = (document.getElementById('kw').value.trim()||'Software Engineer').substring(0,120);
  const loc = (document.getElementById('loc').value.trim()||'Remote USA').substring(0,120);
  const btn = document.getElementById('search-btn');
  btn.disabled = true;
  btn.textContent = 'Searching APIs…';
  setStatus(`Searching "${kw}" in ${loc}…`, 'loading');
  const enabledSrcs = SOURCES.filter(s => document.getElementById('chk-'+s.id)?.checked);
  if (!enabledSrcs.length) {
    showToast('Select at least one job board source.', 3000, 'error');
    btn.disabled=false; btn.textContent='Search jobs';
    setStatus('No sources selected — enable at least one job board.', 'error');
    return;
  }
  document.getElementById('job-list').innerHTML =
    `<div class="empty-state"><div class="spinner spinner-lg"></div><div style="margin-top:14px;font-size:12px;color:var(--text1)">Fetching live listings…</div><div style="font-size:10px;color:var(--text2);margin-top:5px">Querying REST APIs and applying AI matches</div></div>`;
  document.getElementById('detail-panel').style.display = 'none';
  selectedJob = null;

  try {
    const cfg = loadSettings();
    userSkills = cfg.skills || [];
    allJobs = [];
    const fetches = [];

    if (enabledSrcs.find(s=>s.id==='adzuna')) fetches.push(fetchAdzuna(kw, loc, cfg));
    if (enabledSrcs.find(s=>s.id==='usajobs')) fetches.push(fetchUSAJobs(kw, loc, cfg));
    if (enabledSrcs.find(s=>s.id==='remoteok')) fetches.push(fetchRemoteOK(kw));

    const results = await Promise.all(fetches);
    results.forEach(res => { if (res) allJobs = allJobs.concat(res); });

    const mockSrcs = enabledSrcs.filter(s => !['adzuna','usajobs','remoteok'].includes(s.id));
    if (mockSrcs.length) {
      allJobs = allJobs.concat(generateJobs(kw, loc, mockSrcs));
    }

    filteredJobs = [...allJobs];
    activeFilter = 'all';
    document.querySelectorAll('.pill-filter').forEach(p => p.classList.toggle('active', p.dataset.f==='all'));
    applyClientFilters();
    renderJobList();
    updateMetricCards();
    const srcs = [...new Set(allJobs.map(j=>j.source))].length;
    setStatus(`Found ${allJobs.length} listings across ${srcs} source${srcs!==1?'s':''} · ${filteredJobs.length} matching filters`);
  } catch(err) {
    setStatus('Search error — see console.', 'error');
    console.error('Search error:', err);
    showToast('Search error. Check the browser console.', 4000, 'error');
  } finally {
    btn.disabled=false;
    btn.textContent='Search jobs';
  }
}'''

if P1_OLD in html:
    html = html.replace(P1_OLD, P1_NEW, 1)
    print('PATCH 1 OK — Updated doSearch with async API fetching')
else:
    errors.append('PATCH 1 FAILED — target doSearch block not found')

P2_OLD = '''function applyClientFilters() {'''

P2_NEW = '''async function fetchAdzuna(kw, loc, cfg) {
  if (!cfg.adzunaId || !cfg.adzunaKey) return [];
  try {
    const res = await fetch(`https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=${cfg.adzunaId}&app_key=${cfg.adzunaKey}&what=${encodeURIComponent(kw)}&where=${encodeURIComponent(loc)}&results_per_page=25`);
    const data = await res.json();
    return (data.results||[]).map(j => {
      const salMin = j.salary_min ? Math.floor(j.salary_min/1000) : 0;
      const salMax = j.salary_max ? Math.floor(j.salary_max/1000) : salMin;
      const isRemote = (j.location?.display_name||'').toLowerCase().includes('remote') || loc.toLowerCase().includes('remote');
      const job = {
        id: `adz-${j.id}`, title: j.title, company: j.company?.display_name||'Unknown',
        location: j.location?.display_name||loc, arrangement: isRemote?'Remote':'On-site',
        salaryLoK: salMin, salaryHiK: salMax, salary: salMin?`$${salMin}K–$${salMax}K/yr`:'Undisclosed',
        source: 'Adzuna', srcAbbr: 'AZ', srcColor: '#f87171',
        posted: j.created ? new Date(j.created).toLocaleDateString() : 'Recent',
        postedDays: j.created ? Math.floor((Date.now()-new Date(j.created))/(1000*60*60*24)) : 0,
        description: j.description, link: j.redirect_url,
        jobType: j.contract_time==='contract'?'Contract':'Full-time', expLevel: 'Mid level',
        _rawCoords: [j.latitude, j.longitude], verified: true
      };
      job._matchScore = getMatchScore(job, userSkills);
      return job;
    });
  } catch(e) { console.error('Adzuna fail:',e); return []; }
}

async function fetchUSAJobs(kw, loc, cfg) {
  if (!cfg.usajobsKey || !cfg.usajobsEmail) return [];
  try {
    const res = await fetch(`https://data.usajobs.gov/api/search?Keyword=${encodeURIComponent(kw)}&LocationName=${encodeURIComponent(loc)}`, {headers:{'Authorization-Key':cfg.usajobsKey, 'User-Agent':cfg.usajobsEmail}});
    const data = await res.json();
    return (data.SearchResult?.SearchResultItems||[]).map((j,i) => {
      const it = j.MatchedObjectDescriptor;
      const salMin = it.PositionRemuneration?.[0]?Math.floor(it.PositionRemuneration[0].MinimumRange/1000):0;
      const salMax = it.PositionRemuneration?.[0]?Math.floor(it.PositionRemuneration[0].MaximumRange/1000):salMin;
      const isRemote = (it.PositionLocationDisplay||'').toLowerCase().includes('anywhere') || loc.toLowerCase().includes('remote');
      const job = {
        id: `usa-${it.PositionID||i}`, title: it.PositionTitle, company: it.OrganizationName,
        location: it.PositionLocationDisplay||loc, arrangement: isRemote?'Remote':'On-site',
        salaryLoK: salMin, salaryHiK: salMax, salary: salMin?`$${salMin}K–$${salMax}K/yr`:'Federal Scale',
        source: 'USAJobs', srcAbbr: 'US', srcColor: '#22d3ee',
        posted: it.PublicationStartDate ? new Date(it.PublicationStartDate).toLocaleDateString() : 'Recent',
        postedDays: it.PublicationStartDate ? Math.floor((Date.now()-new Date(it.PublicationStartDate))/(1000*60*60*24)) : 0,
        description: (it.UserArea?.Details?.JobSummary||'Federal listing.') + ' ' + (it.QualificationSummary||''),
        link: it.PositionURI, jobType: 'Full-time', expLevel: 'Mid level',
        _rawCoords: [it.PositionLocation?.[0]?.Latitude, it.PositionLocation?.[0]?.Longitude], verified: true
      };
      job._matchScore = getMatchScore(job, userSkills);
      return job;
    });
  } catch(e) { console.error('USAJobs fail:',e); return []; }
}

async function fetchRemoteOK(kw) {
  try {
    const res = await fetch(`https://corsproxy.io/?https://remoteok.com/api?tags=${encodeURIComponent(kw)}`);
    const data = await res.json();
    return data.filter(d=>d.legal!=='API').map((j,i) => {
      const salMin = j.salary_min ? Math.floor(j.salary_min/1000) : 0;
      const salMax = j.salary_max ? Math.floor(j.salary_max/1000) : salMin;
      const job = {
        id: `rok-${j.id||i}`, title: j.position, company: j.company,
        location: j.location||'Remote', arrangement: 'Remote',
        salaryLoK: salMin, salaryHiK: salMax, salary: salMin?`$${salMin}K–$${salMax}K/yr`:'Undisclosed',
        source: 'RemoteOK', srcAbbr: 'RO', srcColor: '#fb923c',
        posted: j.date ? new Date(j.date).toLocaleDateString() : 'Recent',
        postedDays: j.date ? Math.floor((Date.now()-new Date(j.date))/(1000*60*60*24)) : 0,
        description: String(j.description).replace(/<[^>]*>?/gm, ''),
        link: j.url, jobType: 'Full-time', expLevel: 'Mid level', _rawCoords: null, verified: true
      };
      job._matchScore = getMatchScore(job, userSkills);
      return job;
    });
  } catch(e) { console.error('RemoteOK fail:',e); return []; }
}

function applyClientFilters() {'''

if P2_OLD in html:
    html = html.replace(P2_OLD, P2_NEW, 1)
    print('PATCH 2 OK — Injected async API fetch functions')
else:
    errors.append('PATCH 2 FAILED — target applyClientFilters block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    print(f'\nRestoring original from backup…')
    shutil.copy2(backup, TARGET)
    sys.exit(1)

TARGET.write_text(html, encoding='utf-8')
print(f'\nAll patches applied successfully to {TARGET}')
print(f'Original 2293-line file backed up to {backup}')
