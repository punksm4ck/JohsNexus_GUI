"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_VERSION="2.0.0"
ENVFILE="${JOBNEXUS_ENVFILE:-${HOME}/.jobnexus_keys.env}"
LOG_DIR="${HOME}/.jobnexus"
LOG_FILE="${LOG_DIR}/setup_$(date +%Y%m%d_%H%M%S).log"
TIMEOUT_SECONDS=300

RED='\033[0;31m'; GRN='\033[0;32m'; YLW='\033[1;33m'
BLU='\033[1;34m'; CYN='\033[0;36m'; RST='\033[0m'; BOLD='\033[1m'

ADZUNA_APP_ID=''
ADZUNA_APP_KEY=''
INDEED_PUBLISHER_ID=''
ZIPRECRUITER_API_KEY=''
USAJOBS_API_KEY=''
USAJOBS_EMAIL=''

banner() {
  echo ""
  echo -e "${BLU}╔══════════════════════════════════════════════════════════╗${RST}"
  echo -e "${BLU}║      JobNexus Enterprise  —  API Key Setup  v${SCRIPT_VERSION}       ║${RST}"
  echo -e "${BLU}╚══════════════════════════════════════════════════════════╝${RST}"
  echo ""
}

log()  { echo "[$(date '+%H:%M:%S')] $*" >> "${LOG_FILE}"; }
step() { echo -e "\n${YLW}▶  STEP $1/4 — $2${RST}\n"; log "STEP $1: $2"; }
ok()   { echo -e "${GRN}✔  $1${RST}";   log "OK: $1"; }
info() { echo -e "${CYN}ℹ  $1${RST}";   log "INFO: $1"; }
warn() { echo -e "${RED}⚠  $1${RST}";   log "WARN: $1"; }
die()  { echo -e "${RED}[FATAL] $1${RST}" >&2; log "FATAL: $1"; exit 1; }

open_url() {
  local url="$1"
  local opened=false
  for cmd in google-chrome google-chrome-stable chromium-browser chromium xdg-open open; do
    if command -v "${cmd}" &>/dev/null; then
      "${cmd}" "${url}" &>/dev/null & disown
      opened=true
      break
    fi
  done
  if [[ "${opened}" == false ]]; then
    warn "No browser found. Open manually: ${url}"
  fi
  log "Opened URL: ${url}"
}

validate_nonempty() {
  local val="$1" label="$2"
  if [[ -z "${val}" ]]; then
    die "${label} cannot be empty."
  fi
}

validate_email() {
  local val="$1"
  if [[ ! "${val}" =~ ^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$ ]]; then
    warn "Value '${val}' does not look like a valid email address."
    echo -en "${BOLD}Continue anyway? [y/N]: ${RST}"
    read -r yn
    [[ "${yn,,}" == 'y' ]] || die "Aborted by user."
  fi
}

prompt_required() {
  local -n _outvar="$1"
  local label="$2"
  local value=''
  local attempts=0
  while [[ -z "${value}" ]]; do
    (( attempts++ )) || true
    if (( attempts > 5 )); then
      die "Too many empty attempts for: ${label}"
    fi
    echo -en "${BOLD}${label}: ${RST}"
    read -r value
    if [[ -z "${value}" ]]; then
      warn "Value required — press Ctrl-C to abort."
    fi
  done
  _outvar="${value}"
  log "Received value for: ${label} (${#value} chars)"
}

prompt_optional() {
  local -n _outvar="$1"
  local label="$2"
  echo -en "${BOLD}${label} (Enter to skip): ${RST}"
  local value=''
  read -r value
  _outvar="${value}"
  log "Optional field '${label}': ${value:+(set)}"
}

write_envfile() {
  mkdir -p "$(dirname "${ENVFILE}")"
  cat > "${ENVFILE}" <<EOF
ADZUNA_APP_ID="${ADZUNA_APP_ID}"
ADZUNA_APP_KEY="${ADZUNA_APP_KEY}"
INDEED_PUBLISHER_ID="${INDEED_PUBLISHER_ID}"
ZIPRECRUITER_API_KEY="${ZIPRECRUITER_API_KEY}"
USAJOBS_API_KEY="${USAJOBS_API_KEY}"
USAJOBS_EMAIL="${USAJOBS_EMAIL}"
EOF
  chmod 600 "${ENVFILE}"
}

print_summary() {
  local masked_adz="${ADZUNA_APP_KEY:0:4}****${ADZUNA_APP_KEY: -4}"
  local masked_zip="${ZIPRECRUITER_API_KEY:0:8}****"
  local masked_usa="${USAJOBS_API_KEY:0:4}****"

  echo ""
  echo -e "${BLU}══════════════════════════════════════════════════════════${RST}"
  echo -e "${BOLD}Paste into JobNexus Settings tab:${RST}"
  echo -e "${BLU}══════════════════════════════════════════════════════════${RST}"
  printf "  %-26s %s\n" "Adzuna App ID:"        "${ADZUNA_APP_ID}"
  printf "  %-26s %s\n" "Adzuna App Key:"       "${masked_adz:-  (skipped)}"
  printf "  %-26s %s\n" "Indeed Publisher ID:"  "${INDEED_PUBLISHER_ID}"
  printf "  %-26s %s\n" "ZipRecruiter Key:"     "${masked_zip:-  (skipped)}"
  printf "  %-26s %s\n" "USAJobs API Key:"      "${masked_usa:-  (skipped)}"
  printf "  %-26s %s\n" "USAJobs Email:"        "${USAJOBS_EMAIL}"
  echo ""
  echo -e "  Keys stored at: ${CYN}${ENVFILE}${RST} (chmod 600)"
  echo -e "  Log:            ${CYN}${LOG_FILE}${RST}"
  echo ""
  echo -e "  Load any time:  ${CYN}source ${ENVFILE}${RST}"
  echo ""
}

print_api_reference() {
  echo -e "${BLU}══════════════════════════════════════════════════════════${RST}"
  echo -e "${BOLD}API reference for jobnexus_enterprise.html:${RST}"
  echo -e "${BLU}══════════════════════════════════════════════════════════${RST}"
  echo ""
  echo "  ADZUNA"
  echo "  GET https://api.adzuna.com/v1/api/jobs/us/search/1"
  echo "      ?app_id=\$ADZUNA_APP_ID&app_key=\$ADZUNA_APP_KEY"
  echo "      &what=<query>&where=<location>&results_per_page=50&content-type=application/json"
  echo ""
  echo "  INDEED  (Publisher XML/JSON feed)"
  echo "  GET https://api.indeed.com/ads/apisearch"
  echo "      ?publisher=\$INDEED_PUBLISHER_ID&q=<query>&l=<location>"
  echo "      &format=json&v=2&limit=25&radius=50"
  echo ""
  echo "  ZIPRECRUITER"
  echo "  GET https://api.ziprecruiter.com/jobs/v1?search=<query>&location=<location>&jobs_per_page=50"
  echo "  Header: Authorization: Bearer \$ZIPRECRUITER_API_KEY"
  echo ""
  echo "  USAJOBS"
  echo "  GET https://data.usajobs.gov/api/search?Keyword=<query>&LocationName=<location>&ResultsPerPage=50"
  echo "  Headers: Authorization-Key: \$USAJOBS_API_KEY"
  echo "           User-Agent: \$USAJOBS_EMAIL"
  echo ""
}

check_deps() {
  local missing=()
  for cmd in curl bash; do
    command -v "${cmd}" &>/dev/null || missing+=("${cmd}")
  done
  if (( ${#missing[@]} > 0 )); then
    die "Missing required tools: ${missing[*]}"
  fi
}

main() {
  mkdir -p "${LOG_DIR}"
  log "=== JobNexus API Setup v${SCRIPT_VERSION} started ==="

  banner
  check_deps

  echo -e "This wizard will:"
  echo    "  1. Open each job board's free API registration page"
  echo    "  2. Walk you through each signup step"
  echo    "  3. Collect and validate your keys"
  echo -e "  4. Save them to ${CYN}${ENVFILE}${RST} (chmod 600)\n"
  echo -en "Press ${BOLD}Enter${RST} to begin, or Ctrl-C to abort: "
  read -r

  step 1 "Adzuna — developer.adzuna.com"
  echo "  Free tier: 250 calls/day, no credit card required."
  echo ""
  echo -e "  ${CYN}Opening: https://developer.adzuna.com/signup${RST}"
  open_url "https://developer.adzuna.com/signup"
  sleep 1
  echo ""
  echo "  Steps:"
  echo "    1. Create account (email + password) and verify email"
  echo "    2. Log in → Dashboard → 'Create application'"
  echo "    3. Name it 'JobNexus' — you receive an App ID and App Key"
  echo ""
  prompt_required ADZUNA_APP_ID  "Adzuna App ID"
  prompt_required ADZUNA_APP_KEY "Adzuna App Key"
  ok "Adzuna credentials stored."

  step 2 "Indeed Publisher — ads.indeed.com/jobroll"
  echo "  Free, requires an Indeed account. Approval is usually instant."
  echo ""
  echo -e "  ${CYN}Opening: https://ads.indeed.com/jobroll/xmlfeed${RST}"
  open_url "https://ads.indeed.com/jobroll/xmlfeed"
  sleep 1
  echo ""
  echo "  Steps:"
  echo "    1. Sign in with your Indeed account (or create one free)"
  echo "    2. Click 'Join the Indeed Publisher Programme'"
  echo "    3. Site name: 'JobNexus', category: 'Job Search Tool'"
  echo "    4. Your numeric Publisher ID appears on approval"
  echo ""
  prompt_required INDEED_PUBLISHER_ID "Indeed Publisher ID"
  ok "Indeed Publisher ID stored."

  step 3 "ZipRecruiter ZipSearch — ziprecruiter.com/zipsearch"
  echo "  Free tier available. Key delivered by email within minutes."
  echo ""
  echo -e "  ${CYN}Opening: https://www.ziprecruiter.com/zipsearch${RST}"
  open_url "https://www.ziprecruiter.com/zipsearch"
  sleep 1
  echo ""
  echo "  Steps:"
  echo "    1. Click 'Get API Access' and sign in or register"
  echo "    2. Submit the developer form — key format: zr_live_XXXXX..."
  echo "    3. Key arrives by email (may take a few minutes)"
  echo ""
  warn "ZipRecruiter key may not have arrived yet. Leave blank to skip."
  prompt_optional ZIPRECRUITER_API_KEY "ZipRecruiter API key"
  ok "ZipRecruiter key noted."

  step 4 "USAJobs — developer.usajobs.gov"
  echo "  Official US federal job board. Free, no rate limits for personal use."
  echo ""
  echo -e "  ${CYN}Opening: https://developer.usajobs.gov/APIRequest/Index${RST}"
  open_url "https://developer.usajobs.gov/APIRequest/Index"
  sleep 1
  echo ""
  echo "  Steps:"
  echo "    1. Fill in name, email, Agency/Org: 'Personal Use'"
  echo "    2. Purpose: 'Personal job search aggregation'"
  echo "    3. Key arrives by email — also supply your registered email as User-Agent"
  echo ""
  prompt_required USAJOBS_API_KEY "USAJobs API key"
  prompt_required USAJOBS_EMAIL   "USAJobs registered email"
  validate_email  "${USAJOBS_EMAIL}"
  ok "USAJobs credentials stored."

  write_envfile
  log "Keys written to ${ENVFILE}"

  print_summary
  print_api_reference

  echo -e "${GRN}Setup complete. Open jobnexus_enterprise.html and paste the keys into the Settings tab.${RST}"
  echo ""
  log "=== Setup complete ==="
}

main "$@"
