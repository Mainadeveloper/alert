import time
import binalert

# Run forever, checking every 6 hours
while True:
    print(binalert.run_alert())
    time.sleep(21600)  # 6 hours
