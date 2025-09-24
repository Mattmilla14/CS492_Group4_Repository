#!/usr/bin/env bash
(set -m; bash scripts/run_backend.sh &)
sleep 3
bash scripts/run_frontend.sh
