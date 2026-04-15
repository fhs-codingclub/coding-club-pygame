#!/usr/bin/env bash
set -e

echo "Fixing package signing keys..."
# Fix Yarn GPG key if missing/outdated
sudo gpg --batch --keyserver keyserver.ubuntu.com --recv-keys 62D54FD4003F6525 2>/dev/null || true
sudo gpg --batch --export 62D54FD4003F6525 2>/dev/null | sudo tee /usr/share/keyrings/yarn-archive-keyring.gpg > /dev/null

echo "Installing dependencies..."
sudo apt-get update -y
sudo apt-get install -y xvfb x11vnc fluxbox websockify novnc