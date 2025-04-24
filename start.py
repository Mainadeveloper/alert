import time
import binalert

# Run forever, checking every 5 minutes
while True:
    print(binalert.run_alert())
    time.sleep(300)  # 5 minutes
