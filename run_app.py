import subprocess
import time
import os
import signal
import sys
import webview
from pathlib import Path


# Start streamlit in separate thread
def run_stream_lit():
    script_dir = Path(__file__).parent
    process = subprocess.Popen(
        ["streamlit", "run", f"{script_dir}/main.py", "--server.headless=true"],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        bufsize=-1)
    return process


# Graceful shutdown handler
def stop_streamlit(proc):
    if sys.platform == 'win32':
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)])
    else:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)


# Launch the app
if __name__ == '__main__':
    print('Starting streamlit')
    proc = run_stream_lit()

time.sleep(2)

try:
    # open the app in native window
    webview.create_window("My First Python Desktop App", "http://localhost:8501", width=1000, height=700)
    webview.start()
finally:
    print("Shutting down Streamlit server...")
    stop_streamlit(proc)
