#!/usr/bin/env python3
"""
jobnexus_patch_geo.py  —  Enterprise geolocation patcher for jobnexus_enterprise.html
Usage:  python3 jobnexus_patch_geo.py [--target PATH] [--dry-run] [--verbose] [--no-backup]
"""
import sys, shutil, pathlib, datetime, argparse

DEFAULT_TARGET = pathlib.Path(__file__).parent / 'jobnexus_enterprise.html'


def parse_args():
    p = argparse.ArgumentParser(description='Patch jobnexus_enterprise.html with geolocation features.')
    p.add_argument('--target',    type=pathlib.Path, default=DEFAULT_TARGET)
    p.add_argument('--dry-run',   action='store_true', help='Validate without writing')
    p.add_argument('--verbose',   action='store_true', help='Print match previews')
    p.add_argument('--no-backup', action='store_true', help='Skip backup')
    return p.parse_args()


def abort(msg, code=1):
    print(f'\n[FATAL] {msg}', file=sys.stderr)
    sys.exit(code)


def apply_patch(html, old, new, label, errors, verbose=False):
    count = html.count(old)
    if count == 0:
        errors.append(f'{label} — anchor not found')
        print(f'  [FAIL] {label}')
        return html
    if count > 1:
        errors.append(f'{label} — anchor ambiguous ({count} matches); tighten match string')
        print(f'  [FAIL] {label}')
        return html
    if verbose:
        print(f'  [DIFF] - {repr(old[:72])}')
        print(f'         + {repr(new[:72])}')
    print(f'  [OK]   {label}')
    return html.replace(old, new, 1)


def main():
    args = parse_args()
    target = args.target.resolve()

    print(f'\nJobNexus Geolocation Patcher  ({"DRY RUN" if args.dry_run else "LIVE"})')
    print(f'Target: {target}\n')

    if not target.exists():
        abort(f'{target} not found.')
    if target.suffix != '.html':
        abort(f'Expected .html, got {target.suffix}')

    html = target.read_text(encoding='utf-8')
    backup = None

    if not args.dry_run and not args.no_backup:
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup = target.with_suffix(f'.bak_{ts}')
        shutil.copy2(target, backup)
        print(f'Backup: {backup}\n')

    errors = []
    v = args.verbose

    html = apply_patch(html,
        old='<button class="pill-filter" data-f="Local" id="local-pill" onclick="filterType(this)" style="display:none">📍 Local</button>',
        new='<button class="pill-filter" data-f="Local" id="local-pill" onclick="filterType(this)" style="display:none" aria-label="Filter jobs within 50 miles (requires location)">📍 Near me</button>',
        label='PATCH 1 — Local pill: label & aria-label update',
        errors=errors, verbose=v)

    html = apply_patch(html,
        old="const RADIUS_KM = 80;",
        new="const RADIUS_KM = 80;  // ≈ 50 miles — edit to adjust proximity filter",
        label='PATCH 2 — Proximity radius constant annotated',
        errors=errors, verbose=v)

    html = apply_patch(html,
        old='buildSrcChips();\nbuildCatChips();\nupdateSavedCount();\nupdateApiHealth(loadSettings());\nloadSettingsUI();',
        new="""buildSrcChips();
buildCatChips();
updateSavedCount();
updateApiHealth(loadSettings());
loadSettingsUI();
(function verifyGeoSupport() {
  if (!navigator.geolocation) {
    const btn = document.getElementById('geo-btn');
    if (btn) {
      btn.title    = 'Geolocation not supported by this browser';
      btn.style.opacity = '.35';
      btn.disabled = true;
    }
    const sta = document.getElementById('geo-status');
    if (sta) sta.textContent = 'Geolocation unavailable in this browser.';
  }
})();""",
        label='PATCH 3 — Boot-time geo-support guard injected',
        errors=errors, verbose=v)

    print()
    if errors:
        print(f'[ABORT] {len(errors)} patch(es) failed:')
        for e in errors: print(f'  • {e}')
        if backup and backup.exists():
            shutil.copy2(backup, target)
            print(f'Original restored from backup.')
        sys.exit(1)

    if args.dry_run:
        print('Dry run complete — no file written.')
        return

    target.write_text(html, encoding='utf-8')
    print(f'All patches applied → {target}')
    if backup:
        print(f'Backup → {backup}')


if __name__ == '__main__':
    main()
