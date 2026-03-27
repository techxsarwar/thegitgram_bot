from pyngrok import ngrok
import time
import sys

import os

os.environ["NGROK_CHECK_CRL"] = "false"

try:
    # Start ngrok tunnel on port 8000
    public_url = ngrok.connect(8000).public_url
    print(f"Ngrok Tunnel Public URL: {public_url}")

    # Write to a file for the agent to read
    with open("ngrok_url.txt", "w") as f:
        f.write(public_url)

    # Keep the tunnel open
    print("Tunnel is active. Press Ctrl+C to stop.")
    while True:
        time.sleep(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
except KeyboardInterrupt:
    print("Stopping ngrok...")
    ngrok.kill()
