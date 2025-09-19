#!/usr/bin/env bash
set -euo pipefail

NAMESPACE=${1:-default}
RETENTION=${2:-168h}

tctl --ns "$NAMESPACE" namespace describe || tctl --ns "$NAMESPACE" namespace register --rd "$RETENTION"
