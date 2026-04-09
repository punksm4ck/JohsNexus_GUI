#!/usr/bin/env python3
import sys, shutil, pathlib, datetime

TARGET = pathlib.Path('./jobnexus.html')
if not TARGET.exists(): sys.exit(f'ERROR: {TARGET} not found.')

backup = TARGET.with_suffix(f'.bak_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}')
shutil.copy2(TARGET, backup)
print(f'Backup created: {backup}')

html = TARGET.read_text(encoding='utf-8')
errors = []

P1_OLD = '''    if (enabledSrcs.find(s=>s.id==='remoteok')) fetches.push(fetchRemoteOK(kw));

    const results = await Promise.all(fetches);'''

P1_NEW = '''    if (enabledSrcs.find(s=>s.id==='remoteok')) fetches.push(fetchRemoteOK(kw));
    if (enabledSrcs.find(s=>s.id==='indeed')) fetches.push(fetchIndeedScrape(kw, loc));
    if (enabledSrcs.find(s=>s.id==='ziprecruiter')) fetches.push(fetchZipScrape(kw, loc));

    const results = await Promise.all(fetches);'''

if P1_OLD in html:
    html = html.replace(P1_OLD, P1_NEW, 1)
    print('PATCH 1 OK — Wired scrape endpoints into async fetch array')
else:
    errors.append('PATCH 1 FAILED')

P2_OLD = '''    const mockSrcs = enabledSrcs.filter(s => !['adzuna','usajobs','remoteok'].includes(s.id));'''
P2_NEW = '''    const mockSrcs = enabledSrcs.filter(s => !['adzuna','usajobs','remoteok','indeed','ziprecruiter'].includes(s.id));'''

if P2_OLD in html:
    html = html.replace(P2_OLD, P2_NEW, 1)
    print('PATCH 2 OK — Excluded scraped sources from mock fallback')
else:
    errors.append('PATCH 2 FAILED')

P3_OLD = '''async function fetchRemoteOK(kw) {'''
P3_NEW = '''async function fetchIndeedScrape(kw, loc) {
  try {
    const res = await fetch(`http://localhost:3456/api/indeed?q=${encodeURIComponent(kw)}&l=${encodeURIComponent(loc)}`);
    if (!res.ok) throw new Error('Deno scraper offline');
    const data = await res.json();
    return data.map(j => {
      j.salaryLoK = 0; j.salaryHiK = 0; j.salary = j.salaryRaw || 'Undisclosed';
      j.arrangement = (j.location.toLowerCase().includes('remote') || loc.toLowerCase().includes('remote')) ? 'Remote' : 'On-site';
      j.jobType = 'Full-time'; j.expLevel = 'Mid level';
      j._matchScore = getMatchScore(j, userSkills);
      return j;
    });
  } catch(e) { console.error('Indeed scrape fail:', e); showToast('Deno scraper offline.', 4000, 'error'); return []; }
}

async function fetchZipScrape(kw, loc) {
  try {
    const res = await fetch(`http://localhost:3456/api/ziprecruiter?q=${encodeURIComponent(kw)}&l=${encodeURIComponent(loc)}`);
    if (!res.ok) throw new Error('Deno scraper offline');
    const data = await res.json();
    return data.map(j => {
      j.salaryLoK = 0; j.salaryHiK = 0; j.salary = j.salaryRaw || 'Undisclosed';
      j.arrangement = (j.location.toLowerCase().includes('remote') || loc.toLowerCase().includes('remote')) ? 'Remote' : 'On-site';
      j.jobType = 'Full-time'; j.expLevel = 'Mid level';
      j._matchScore = getMatchScore(j, userSkills);
      return j;
    });
  } catch(e) { console.error('Zip scrape fail:', e); return []; }
}

async function fetchRemoteOK(kw) {'''

if P3_OLD in html:
    html = html.replace(P3_OLD, P3_NEW, 1)
    print('PATCH 3 OK — Injected Deno fetch bridge functions')
else:
    errors.append('PATCH 3 FAILED')

if errors:
    for e in errors: print(e); sys.exit(1)

TARGET.write_text(html, encoding='utf-8')
print(f'All patches applied to {TARGET}')
