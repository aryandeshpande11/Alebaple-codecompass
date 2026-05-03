"""Wait for server reload and test"""
import time
print("Waiting 3 seconds for server to reload...")
time.sleep(3)
print("Running test...")

import subprocess
subprocess.run(["python", "test_final_api.py"])

# Made with Bob
