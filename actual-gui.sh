echo "Starting VNC server..."
x11vnc -display :1 -nopw -forever -shared -rfbport 5900 &

echo "Starting noVNC on port 6080..."
websockify --web=/usr/share/novnc 6080 localhost:5900 &

echo ""
echo "GUI environment is ready!"
echo "Go to your Codespaces Ports tab, set port 6080 to Public, and open the link."
echo ""
export DISPLAY=:1
export XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR
export SDL_AUDIODRIVER=dummy
echo ""
echo "Then run: python main.py"
echo ""
echo "(Audio is disabled in this environment via SDL_AUDIODRIVER=dummy)"