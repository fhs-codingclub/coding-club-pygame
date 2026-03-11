#!/usr/bin/env bash
set -e

echo "Fixing package signing keys..."
# Fix Yarn GPG key if missing/outdated
sudo gpg --batch --keyserver keyserver.ubuntu.com --recv-keys 62D54FD4003F6525 2>/dev/null || true
sudo gpg --batch --export 62D54FD4003F6525 2>/dev/null | sudo tee /usr/share/keyrings/yarn-archive-keyring.gpg > /dev/null

echo "Installing dependencies..."
sudo apt-get update -y
sudo apt-get install -y xvfb x11vnc fluxbox websockify novnc

echo "Starting virtual display..."
export XDG_RUNTIME_DIR=/tmp/runtime-$(whoami)
mkdir -p "$XDG_RUNTIME_DIR"
Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1
fluxbox &

echo "Starting VNC server..."
x11vnc -display :1 -nopw -forever -shared -rfbport 5900 &

echo "Starting noVNC on port 6080..."
websockify --web=/usr/share/novnc 6080 localhost:5900 &

echo ""
echo "GUI environment is ready!"
echo "Go to your Codespaces Ports tab, set port 6080 to Public, and open the link."
echo ""
echo "Before running your game, set these in your terminal:"
echo "  export DISPLAY=:1"
echo "  export XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"
echo "  export SDL_AUDIODRIVER=dummy"
echo ""
echo "Then run: python main.py"
echo ""
echo "(Audio is disabled in this environment via SDL_AUDIODRIVER=dummy)"