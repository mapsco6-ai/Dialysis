#!/bin/sh
# Generates a self-signed TLS certificate for the on-premise LAN deployment.
# Run once per install from the repo root:
#   ./deploy/nginx/generate_self_signed_cert.sh <center-server-hostname-or-ip>
#
# The resulting dialysis.crt must be installed as a trusted certificate on
# every staff device and iPad that will access the system (see
# docs/deployment.md) - this is a one-time step per device.

set -e

HOST="${1:-dialysis.local}"
CERT_DIR="$(dirname "$0")/certs"
mkdir -p "$CERT_DIR"

openssl req -x509 -nodes -days 825 \
  -newkey rsa:2048 \
  -keyout "$CERT_DIR/dialysis.key" \
  -out "$CERT_DIR/dialysis.crt" \
  -subj "/CN=$HOST" \
  -addext "subjectAltName=DNS:$HOST,IP:${2:-127.0.0.1}"

echo "Certificate written to $CERT_DIR/dialysis.crt"
echo "Install this file as a trusted root certificate on staff devices and iPads."
