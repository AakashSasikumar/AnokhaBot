import subprocess
import time
import sys

time.sleep(10)
if 'linux' in sys.platform.lower():
    subprocess.Popen(['python3', 'Server.py'])
else:
    subprocess.Popen(['python', 'Server.py'])
