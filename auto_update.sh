#!/bin/bash
# Script de mise à jour automatique tous les 2 jours

# Chemins
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/arxiv_collector.py"
LOG_FILE="$SCRIPT_DIR/update.log"

# Date
echo "==================================================" >> "$LOG_FILE"
echo "Mise à jour: $(date)" >> "$LOG_FILE"
echo "==================================================" >> "$LOG_FILE"

# Exécution
python3 "$PYTHON_SCRIPT" update 2 >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
