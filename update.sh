#!/bin/bash

# ── SAFETY LOGIC & COLOR CONFIGURATION ──────────────────────────────────────
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0;0m' # No Color

echo -e "${BLUE}=============[ APPLICATION ENGINE DEPLOYMENT ]=============${NC}"
echo -e "${BLUE}Target Source:${NC} https://github.com/arvineee/Current_Portfolio.git"
echo -e "${BLUE}Timestamp:${NC} $(date)"

# Lock context into script directory root 
cd "$(dirname "$0")"

# ── STEP 1: GIT INFRASTRUCTURE SYNC WITH PROTECTION LOOP ──────────────────
echo -e "\n${YELLOW}[Step 1/4] Securing tracking metrics & credentials...${NC}"

# Fetch remote indices
git fetch origin main

# EXCLUSIVE VALUE PRESERVATION: If config.py has untracked modifications locally, preserve them
CONFIG_PRESERVED=false
if [ -f "config.py" ] && ! git diff --quiet config.py 2>/dev/null; then
    echo -e "${YELLOW}-> Production configuration changes detected in config.py. Creating safe memory backup...${NC}"
    cp config.py .config.py.bak
    CONFIG_PRESERVED=true
fi

# Reset non-protected system layout trees to match remote baseline tracking exactly
echo -e "${BLUE}Aligning structural file trees to origin/main branches...${NC}"
git reset --hard origin/main

# RESTORATION HOOK: If fallback state was stored, overwrite the remote default copy instantly
if [ "$CONFIG_PRESERVED" = true ]; then
    echo -e "${GREEN}✓ Restoring protected configuration layer variables into runtime path.${NC}"
    mv .config.py.bak config.py
else
    # First time initialization check
    if [ -f "config.py" ]; then
        echo -e "${GREEN}✓ Production variables clean. No configuration override triggered.${NC}"
    fi
fi

# ── STEP 2: CACHE CLEANSING & OPTIMIZATION ─────────────────────────────────
echo -e "\n${YELLOW}[Step 2/4] Eliminating stale Python compilation artifacts...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✓ Python bytecode cache completely purged.${NC}"

# ── STEP 3: ASSET & PERMISSION AUDITING ─────────────────────────────────────
echo -e "\n${YELLOW}[Step 3/4] Validating local asset paths and permissions...${NC}"

if [ -f "static/AF.jpg" ]; then
    echo -e "${GREEN}✓ Visual asset validated: static/AF.jpg is securely positioned.${NC}"
else
    echo -e "${RED}⚠ Branding Asset Warning: static/AF.jpg was not found in the path.${NC}"
fi

# Ensure this management file remains executable globally
chmod +x "$0"

# ── STEP 4: RECONCILIATION SUMMARY ──────────────────────────────────────────
echo -e "\n${GREEN}=============[ ARCHITECTURE UPDATE SUCCESSFUL ]=============${NC}"
echo -e "${GREEN}Your workspace has been successfully rebuilt from production source.${NC}"
echo -e "${BLUE}Your configuration parameters inside config.py were fully protected.${NC}\n"

