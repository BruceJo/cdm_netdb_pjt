import subprocess
import time
import sys

for i in range(1, 4):
    subprocess.Popen([sys.executable or 'python', 'test2.py', str(i)])