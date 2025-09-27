#!/bin/bash
# scripts/run_frontend.sh
# One-click frontend launcher for macOS/Linux.

# Move to frontend directory relative to this script
cd "$(dirname "$0")/../frontend" || { echo "Frontend folder not found."; exit 1; }

echo "Starting frontend at http://localhost:8080 ..."
python3 -m http.server 8080 2>/dev/null || python -m http.server 8080
