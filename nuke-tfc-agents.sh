#!/usr/bin/env bash
set -euo pipefail

# Stop and remove ALL tfc-agent containers (running, stopped, or dead)

echo "Finding all tfc-agent containers..."
CONTAINERS=$(docker ps -a --filter "ancestor=hashicorp/tfc-agent" --filter "ancestor=hashicorp/tfc-agent:latest" -q)

if [ -z "$CONTAINERS" ]; then
  echo "No tfc-agent containers found."
  exit 0
fi

echo "Removing $(echo "$CONTAINERS" | wc -l | tr -d ' ') container(s)..."
echo "$CONTAINERS" | xargs docker rm -f

echo "Done. Remaining containers:"
docker ps -a --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}"
