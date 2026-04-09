"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
set -euo pipefail

RED='\033[0;31m'; GRN='\033[0;32m'; YLW='\033[1;33m'
BLU='\033[1;34m'; CYN='\033[0;36m'; RST='\033[0m'
BOLD='\033[1m'

ENVFILE="$HOME/.jobnexus_keys.env"

ADZUNA_APP_ID="a2a7eba2"
ADZUNA_APP_KEY="75f72695ce72d384c0049190ec788084"
INDEED_PUBLISHER_ID="0000000000000000"
ZIPRECRUITER_API_KEY=""

echo -e "${BLU}╔══════════════════════════════════════════════════════╗${RST}"
echo -e "${BLU}║     JobNexus Setup — RESUME (Recovered Session)      ║${RST}"
echo -e "${BLU}╚══════════════════════════════════════════════════════╝${RST}\n"

echo -e "${GRN}✔ Recovered Adzuna App ID: ${ADZUNA_APP_ID}${RST}"
echo -e "${GRN}✔ Recovered Adzuna App Key: ${ADZUNA_APP_KEY}${RST}"
echo -e "${GRN}✔ Recovered Indeed ID (Bypass): ${INDEED_PUBLISHER_ID}${RST}"
echo -e "${GRN}✔ Recovered ZipRecruiter (Skipped)${RST}\n"

echo -e "${YLW}▶  STEP 4/4 — USAJobs — developer.usajobs.gov${RST}\n"

while [[ -z "${USAJOBS_API_KEY:-}" ]]; do
  echo -en "${BOLD}Paste your USAJobs API key:${RST} "
  read -r USAJOBS_API_KEY
done

while [[ -z "${USAJOBS_EMAIL:-}" ]]; do
  echo -en "${BOLD}Enter the email address you registered with USAJobs:${RST} "
  read -r USAJOBS_EMAIL
done

echo -e "\n${GRN}✔ USAJobs credentials saved.${RST}\n"

echo -e "${BLU}══════════════════════════════════════════════════════${RST}"
echo -e "${BOLD}Writing keys to ${CYN}${ENVFILE}${RST}"

cat > "$ENVFILE" <<EOF
ADZUNA_APP_ID="${ADZUNA_APP_ID}"
ADZUNA_APP_KEY="${ADZUNA_APP_KEY}"
INDEED_PUBLISHER_ID="${INDEED_PUBLISHER_ID}"
ZIPRECRUITER_API_KEY="${ZIPRECRUITER_API_KEY}"
USAJOBS_API_KEY="${USAJOBS_API_KEY}"
USAJOBS_EMAIL="${USAJOBS_EMAIL}"
EOF

chmod 600 "$ENVFILE"
echo -e "${GRN}✔ Keys saved to ${ENVFILE} (chmod 600 — readable only by you)${RST}\n"

echo -e "${BLU}══════════════════════════════════════════════════════${RST}"
echo -e "${BOLD}Paste these values into JobNexus Settings tab:${RST}"
echo -e "${BLU}══════════════════════════════════════════════════════${RST}\n"
echo -e "  ${CYN}Adzuna App ID  :${RST}  ${ADZUNA_APP_ID}"
echo -e "  ${CYN}Adzuna App Key :${RST}  ${ADZUNA_APP_KEY}"
echo -e "  ${CYN}Indeed ID      :${RST}  ${INDEED_PUBLISHER_ID}"
echo -e "  ${CYN}ZipRecruiter   :${RST}  (skipped)"
echo -e "  ${CYN}USAJobs Key    :${RST}  ${USAJOBS_API_KEY}"
echo -e "  ${CYN}USAJobs Email  :${RST}  ${USAJOBS_EMAIL}\n"

echo -e "${GRN}Setup complete! Open jobnexus.html in Chrome and paste${RST}"
echo -e "${GRN}the keys above into the Settings tab.${RST}\n"
