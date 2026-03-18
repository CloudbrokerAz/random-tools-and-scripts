#!/usr/bin/env bash
set -euo pipefail

# --- Usage: TFC_AGENT_TOKEN=<token> bash fix-tfc-agent.sh ---

: "${TFC_AGENT_TOKEN:?Set TFC_AGENT_TOKEN before running this script}"
export TFC_AGENT_TOKEN
TFC_AGENT_NAME="${TFC_AGENT_NAME:-tfc-agent}"
export TFC_AGENT_NAME

# 1. Write /etc/krb5.conf
sudo tee /etc/krb5.conf > /dev/null <<'EOF'
[libdefaults]
  default_realm = HASHICORP.LOCAL

[realms]
  HASHICORP.LOCAL = {
    kdc = dc-0.hashicorp.local
  }

[domain_realm]
  .hashicorp.local = HASHICORP.LOCAL
EOF

# 2. Kill any existing tfc-agent containers (running or stopped)
docker ps -a --filter "ancestor=hashicorp/tfc-agent" --filter "ancestor=hashicorp/tfc-agent:latest" -q \
  | xargs -r docker rm -f 2>/dev/null || true

# 3. Pull latest image
docker pull hashicorp/tfc-agent:latest

# 4. Start fresh agent
docker run -d \
  --name "$TFC_AGENT_NAME" \
  --restart unless-stopped \
  -e TFC_AGENT_TOKEN \
  -e TFC_AGENT_NAME \
  -v /etc/krb5.conf:/etc/krb5.conf:ro \
  hashicorp/tfc-agent:latest

echo "Agent started. Verifying..."
sleep 3
if docker ps --filter "name=$TFC_AGENT_NAME" --format "{{.Status}}" | grep -q "Restarting"; then
  echo "ERROR: Container is crash-looping. Logs:"
  docker logs --tail 30 "$TFC_AGENT_NAME"
else
  docker ps --filter "name=$TFC_AGENT_NAME" --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
  echo "OK"
fi
