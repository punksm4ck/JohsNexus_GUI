"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
import pathlib

# Targeting your specific directory
p = pathlib.Path('/home/tsann/Scripts/JohsNexus_GUI/jobnexus.html')
h = p.read_text()

# 1. Add CSS for the grayed-out state
GRAY_CSS = """
.job-card.applied { opacity: 0.45; filter: grayscale(1); border-style: dashed; }
.job-card.applied:hover { opacity: 0.6; filter: grayscale(0.5); }
"""
if '.job-card.applied' not in h:
    h = h.replace('</style>', GRAY_CSS + '</style>')

# 2. Update renderJobList to handle the applied class and button
OLD_BTNS = """<button class="btn-sm btn-primary" onclick="event.stopPropagation();confirmApply('${j.id}')">Apply ↗</button>"""
NEW_BTNS = """<button class="btn-sm btn-primary" onclick="event.stopPropagation();confirmApply('${j.id}')">Apply ↗</button>
        <button class="btn-sm ${isApplied ? 'btn-ghost' : 'btn-ghost'}" onclick="event.stopPropagation();toggleApplied('${j.id}')">
          ${isApplied ? '↺ Undo Applied' : '✓ Applied Already'}
        </button>"""

OLD_CARD_START = """<div class="job-card${selected?' selected':''}${isGrid?' grid-view':''}" id="jcard-${j.id}" onclick="selectJob('${j.id}')">"""
NEW_CARD_START = """<div class="job-card${selected?' selected':''}${isGrid?' grid-view':''}${isApplied?' applied':''}" id="jcard-${j.id}" onclick="selectJob('${j.id}')">"""

# Logic to detect applied status inside the map function
h = h.replace('const isSaved   = savedJobs.some(s=>s.id===j.id);',
              'const isSaved   = savedJobs.some(s=>s.id===j.id);\\n    const isApplied = Object.values(trackerApps).flat().some(a => a.id === j.id);')

h = h.replace(OLD_CARD_START, NEW_CARD_START)
h = h.replace(OLD_BTNS, NEW_BTNS)

# 3. Add the toggleApplied JavaScript function
JS_FUNC = """
function toggleApplied(id) {
    const isApplied = Object.values(trackerApps).flat().some(a => a.id === id);
    if (isApplied) {
        // Remove from tracker
        Object.keys(trackerApps).forEach(stage => {
            trackerApps[stage] = (trackerApps[stage] || []).filter(a => a.id !== id);
        });
        showToast('Marked as not applied.');
    } else {
        // Add to tracker under 'applied' stage
        addToTracker(id, 'applied');
    }
    persistTracker();
    updateTrackerCount();
    renderJobList();
}
"""

if 'function toggleApplied' not in h:
    h = h.replace('</script>', JS_LOGIC + '\n</script>')

p.write_text(h)
print("Patch applied successfully.")
